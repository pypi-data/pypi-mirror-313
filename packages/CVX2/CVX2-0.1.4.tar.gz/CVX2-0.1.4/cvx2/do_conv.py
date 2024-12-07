# 使用 utf-8 编码
# 导入必要的库
import math  # 导入数学库
import torch  # 导入 PyTorch 库
import numpy as np  # 导入 NumPy 库
from torch.nn import init  # 导入 PyTorch 中的初始化函数
from itertools import repeat  # 导入 itertools 库中的 repeat 函数
from torch.nn import functional as F  # 导入 PyTorch 中的函数式接口
from torch._jit_internal import Optional  # 导入 PyTorch 中的可选模块
from torch.nn.parameter import Parameter  # 导入 PyTorch 中的参数类
from torch.nn.modules.module import Module  # 导入 PyTorch 中的模块类
import collections  # 导入 collections 库

# 定义自定义模块 DOConv2d
class DOConv2d(Module):
	"""
    DOConv2d 可以作为 torch.nn.Conv2d 的替代。
    接口与 Conv2d 类似，但有一个例外：
		1. D_mul：超参数的深度乘法器。
    请注意，groups 参数在 DO-Conv（groups=1）、DO-DConv（groups=in_channels）、DO-GConv（其他情况）之间切换。
	"""
	# 常量声明
	__constants__ = ['stride', 'padding', 'dilation', 'groups',
	                 'padding_mode', 'output_padding', 'in_channels',
	                 'out_channels', 'kernel_size', 'D_mul']
	# 注解声明
	__annotations__ = {'bias': Optional[torch.Tensor]}
	
	# 初始化函数
	def __init__(self, in_channels, out_channels, kernel_size, D_mul=None, stride=1,
	             padding=0, dilation=1, groups=1, bias=True, padding_mode='zeros'):
		super(DOConv2d, self).__init__()
		
		# 将 kernel_size、stride、padding、dilation 转化为二元元组
		kernel_size = _pair(kernel_size)
		stride = _pair(stride)
		padding = _pair(padding)
		dilation = _pair(dilation)
		
		# 检查 groups 是否合法
		if in_channels % groups != 0:
			raise ValueError('in_channels 必须能被 groups 整除')
		if out_channels % groups != 0:
			raise ValueError('out_channels 必须能被 groups 整除')
		# 检查 padding_mode 是否合法
		valid_padding_modes = {'zeros', 'reflect', 'replicate', 'circular'}
		if padding_mode not in valid_padding_modes:
			raise ValueError("padding_mode 必须为 {} 中的一种，但得到 padding_mode='{}'".format(
				valid_padding_modes, padding_mode))
		
		# 初始化模块参数
		self.in_channels = in_channels
		self.out_channels = out_channels
		self.kernel_size = kernel_size
		self.stride = stride
		self.padding = padding
		self.dilation = dilation
		self.groups = groups
		self.padding_mode = padding_mode
		self._padding_repeated_twice = tuple(x for x in self.padding for _ in range(2))
		
		#################################### 初始化 D & W ###################################
		M = self.kernel_size[0]
		N = self.kernel_size[1]
		self.D_mul = M * N if D_mul is None or M * N <= 1 else D_mul
		self.W = Parameter(torch.Tensor(out_channels, in_channels // groups, self.D_mul))
		init.kaiming_uniform_(self.W, a=math.sqrt(5))
		
		if M * N > 1:
			self.D = Parameter(torch.Tensor(in_channels, M * N, self.D_mul))
			init_zero = np.zeros([in_channels, M * N, self.D_mul], dtype=np.float32)
			self.D.data = torch.from_numpy(init_zero)
			
			eye = torch.reshape(torch.eye(M * N, dtype=torch.float32), (1, M * N, M * N))
			d_diag = eye.repeat((in_channels, 1, self.D_mul // (M * N)))
			if self.D_mul % (M * N) != 0:  # 当 D_mul > M * N 时
				zeros = torch.zeros([in_channels, M * N, self.D_mul % (M * N)])
				self.d_diag = Parameter(torch.cat([d_diag, zeros], dim=2), requires_grad=False)
			else:  # 当 D_mul = M * N 时
				self.d_diag = Parameter(d_diag, requires_grad=False)
		##################################################################################################
		
		# 初始化偏置参数
		if bias:
			self.bias = Parameter(torch.Tensor(out_channels))
			fan_in, _ = init._calculate_fan_in_and_fan_out(self.W)
			bound = 1 / math.sqrt(fan_in)
			init.uniform_(self.bias, -bound, bound)
		else:
			self.register_parameter('bias', None)
	
	# 返回模块配置的字符串表示形式
	def extra_repr(self):
		s = ('{in_channels}, {out_channels}, kernel_size={kernel_size}'
		     ', stride={stride}')
		if self.padding != (0,) * len(self.padding):
			s += ', padding={padding}'
		if self.dilation != (1,) * len(self.dilation):
			s += ', dilation={dilation}'
		if self.groups != 1:
			s += ', groups={groups}'
		if self.bias is None:
			s += ', bias=False'
		if self.padding_mode != 'zeros':
			s += ', padding_mode={padding_mode}'
		return s.format(**self.__dict__)
	
	# 重新设置状态
	def __setstate__(self, state):
		super(DOConv2d, self).__setstate__(state)
		if not hasattr(self, 'padding_mode'):
			self.padding_mode = 'zeros'
	
	# 辅助函数，执行卷积操作
	def _conv_forward(self, input, weight):
		if self.padding_mode != 'zeros':
			return F.conv2d(F.pad(input, self._padding_repeated_twice, mode=self.padding_mode),
			                weight, self.bias, self.stride,
			                _pair(0), self.dilation, self.groups)
		return F.conv2d(input, weight, self.bias, self.stride,
		                self.padding, self.dilation, self.groups)
	
	# 前向传播函数
	def forward(self, input):
		M = self.kernel_size[0]
		N = self.kernel_size[1]
		DoW_shape = (self.out_channels, self.in_channels // self.groups, M, N)
		if M * N > 1:
			######################### 计算 DoW #################
			# (input_channels, D_mul, M * N)
			D = self.D + self.d_diag
			W = torch.reshape(self.W, (self.out_channels // self.groups, self.in_channels, self.D_mul))
			
			# einsum 输出 (out_channels // groups, in_channels, M * N),
			# 重塑为
			# (out_channels, in_channels // groups, M, N)
			DoW = torch.reshape(torch.einsum('ims,ois->oim', D, W), DoW_shape)
		#######################################################
		else:
			# 在这种情况下 D_mul == M * N
			# 从 (out_channels, in_channels // groups, D_mul) 重塑为 (out_channels, in_channels // groups, M, N)
			DoW = torch.reshape(self.W, DoW_shape)
		return self._conv_forward(input, DoW)


# 定义辅助函数
def _ntuple(n):
	def parse(x):
		if isinstance(x, collections.abc.Iterable):
			return x
		return tuple(repeat(x, n))
	
	return parse


# 定义辅助函数，将输入转化为二元元组
_pair = _ntuple(2)

if __name__ == '__main__':
	input = torch.rand(1, 64, 64, 64)
	conv = DOConv2d(64, 64, kernel_size=3, padding=1)
	output = conv(input)
	print(output.shape, output)
