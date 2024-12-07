import torch
from torch import nn

from cvx2 import WidthBlock, DOConv, DOConv2d, DOWidthBlock

data_dir = '/Users/summy/data/zebra-yolo'

if __name__ == '__main__':
	img = torch.randn(2, 3, 28, 28)
	block = WidthBlock(c1=3, c2=32)
	# print(block(img).shape)
	# torch.Size([2, 32, 28, 28])
	
	model = nn.Sequential(
		WidthBlock(c1=3, c2=32),
		nn.MaxPool2d(kernel_size=2, stride=2),
		WidthBlock(c1=32, c2=32),
		nn.MaxPool2d(kernel_size=2, stride=2),
		nn.Flatten(),
		nn.Linear(in_features=32 * 49, out_features=1024),
		nn.Dropout(0.2),
		nn.SiLU(inplace=True),
		nn.Linear(in_features=1024, out_features=2),
	)
	
	# print(model(img).shape)
	# torch.Size([2, 2])
	
	# import os
	# from pathlib import Path
	# source = Path(os.path.join(data_dir, 'val', 'zebra crossing'))
	# source = (img for img in source.rglob('*') if img.suffix in ('.png', '.jpg', 'jpeg') and img.is_file())
	# print(list(source))

	input = torch.rand(1, 64, 64, 64)
	# conv = DOConv(64, 64, k=5)
	# conv = DOConv2d(64, 64, kernel_size=3)
	# conv = WidthBlock(64, 64)
	conv = DOWidthBlock(64, 64)
	output = conv(input)
	print(output.shape)
