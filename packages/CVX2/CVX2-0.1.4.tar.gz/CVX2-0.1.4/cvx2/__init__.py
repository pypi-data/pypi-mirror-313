import torch
from torch import nn
from .utils import auto_pad
from ._cbam import ChannelAttention, SpatialAttention, CBAM
from .do_conv import DOConv2d

__all__ = [
    'Conv',
    'WidthBlock',
    'DOConv',
    'DOConv2d',
    'DOWidthBlock',
    'ChannelAttention',
    'SpatialAttention',
    'CBAM',
]


class Conv(nn.Module):
    """Standard convolution with args(ch_in, ch_out, kernel, stride, padding, groups, dilation, activation)."""
    
    default_act = nn.SiLU()  # 默认激活函数
    
    def __init__(self, c1, c2, k=1, s=1, p=None, g=1, d=1, act=True):
        """
        初始化 Conv 层。
        
        参数:
            c1 (int): 输入通道数
            c2 (int): 输出通道数
            k (int): 卷积核大小，默认为 1
            s (int): 步长，默认为 1
            p (int or None): 填充大小，默认为 None，自动计算
            g (int): 分组数，默认为 1
            d (int): 空洞率，默认为 1
            act (bool or nn.Module): 是否使用激活函数，默认为 True 使用默认激活函数
        """
        super().__init__()
        self.conv = nn.Conv2d(c1, c2, k, s, auto_pad(k, p, d), groups=g, dilation=d, bias=False)
        self.bn = nn.BatchNorm2d(c2)
        self.act = self.default_act if act is True else act if isinstance(act, nn.Module) else nn.Identity()
    
    def forward(self, x):
        """
        前向传播。
        
        参数:
            x (torch.Tensor): 输入张量
        
        返回:
            torch.Tensor: 经过卷积、批归一化和激活后的输出张量
        """
        return self.act(self.bn(self.conv(x)))
    
    def forward_fuse(self, x):
        """
        融合前向传播。
        
        参数:
            x (torch.Tensor): 输入张量
        
        返回:
            torch.Tensor: 经过卷积和激活后的输出张量
        """
        return self.act(self.conv(x))


class DOConv(nn.Module):
    """Standard convolution with args(ch_in, ch_out, kernel, stride, padding, groups, dilation, activation)."""
    
    default_act = nn.SiLU()  # 默认激活函数
    
    def __init__(self, c1, c2, k=1, s=1, p=None, g=1, d=1, act=True):
        """
        初始化 DOConv 层。
        
        参数:
            c1 (int): 输入通道数
            c2 (int): 输出通道数
            k (int): 卷积核大小，默认为 1
            s (int): 步长，默认为 1
            p (int or None): 填充大小，默认为 None，自动计算
            g (int): 分组数，默认为 1
            d (int): 空洞率，默认为 1
            act (bool or nn.Module): 是否使用激活函数，默认为 True 使用默认激活函数
        """
        super().__init__()
        self.conv = DOConv2d(c1, c2, k, None, s, auto_pad(k, p, d), groups=g, dilation=d, bias=False)
        self.bn = nn.BatchNorm2d(c2)
        self.act = self.default_act if act is True else act if isinstance(act, nn.Module) else nn.Identity()
    
    def forward(self, x):
        """
        前向传播。
        
        参数:
            x (torch.Tensor): 输入张量
        
        返回:
            torch.Tensor: 经过卷积、批归一化和激活后的输出张量
        """
        return self.act(self.bn(self.conv(x)))
    
    def forward_fuse(self, x):
        """
        融合前向传播。
        
        参数:
            x (torch.Tensor): 输入张量
        
        返回:
            torch.Tensor: 经过卷积和激活后的输出张量
        """
        return self.act(self.conv(x))


class WidthBlock(nn.Module):
    
    def __init__(self, c1, c2, kernel_sizes=(3, 5, 7), shortcut=True):
        """
        初始化 WidthBlock 层。
        
        参数:
            c1 (int): 输入通道数
            c2 (int): 输出通道数
            kernel_sizes (tuple): 卷积核大小列表，默认为 (3, 5, 7)
            shortcut (bool): 是否使用残差连接，默认为 True
        """
        super().__init__()
        self.convs = nn.ModuleList(
            [Conv(c1, c2, k) for k in kernel_sizes]
        )
        self.final_conv = nn.Conv2d(len(kernel_sizes) * c2, c2, kernel_size=1)
        self.add = shortcut and c1 == c2
    
    def forward(self, x: torch.Tensor):
        """
        前向传播。
        
        参数:
            x (torch.Tensor): 输入张量
        
        返回:
            torch.Tensor: 经过多个卷积层和最终卷积层后的输出张量，如果有残差连接则加上输入张量
        """
        y = torch.cat([conv(x) for conv in self.convs], dim=1)
        return x + self.final_conv(y) if self.add else self.final_conv(y)


class DOWidthBlock(WidthBlock):
    
    def __init__(self, c1, c2, kernel_sizes=(3, 5, 7), shortcut=True):
        """
        初始化 DOWidthBlock 层。
        
        参数:
            c1 (int): 输入通道数
            c2 (int): 输出通道数
            kernel_sizes (tuple): 卷积核大小列表，默认为 (3, 5, 7)
            shortcut (bool): 是否使用残差连接，默认为 True
        """
        super().__init__(c1, c2, kernel_sizes, shortcut)
        self.convs = nn.ModuleList(
            [DOConv(c1, c2, k) for k in kernel_sizes]
        )
        