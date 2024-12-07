"""
export PYTHONPATH=../
"""
import os
import sys
import torch
from torch import nn

# curPath = os.path.abspath(os.path.dirname(__file__))
# rootPath = os.path.split(curPath)[0]
# sys.path.append(rootPath)

from cvx2 import WidthBlock

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
	
	print(model(img).shape)
	# torch.Size([2, 2])
	
	# import os
	# from pathlib import Path
	# source = Path(os.path.join(data_dir, 'val', 'zebra crossing'))
	# source = (img for img in source.rglob('*') if img.suffix in ('.png', '.jpg', 'jpeg') and img.is_file())
	# print(list(source))
