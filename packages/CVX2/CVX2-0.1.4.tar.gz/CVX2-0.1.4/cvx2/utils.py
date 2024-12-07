import random
import math
from typing import Union
import numpy as np
import cv2
import PIL
from torchvision import transforms
from model_wrapper.utils import get_device

# PIL图像转tensor
def pil_to_tensor(img: PIL.Image.Image, img_size: Union[int, tuple[int, int]]):
	if isinstance(img_size, int):
		img_size = (img_size, img_size)
	return transforms.Compose([
		transforms.Resize(img_size),  # PIL图像尺寸统一
		transforms.ToTensor()  # PIL图像转tensor, (H,W,C) ->（C,H,W）,像素值[0,1]
	])(img)

# tensor转PIL图像
tensor_to_pil = transforms.Compose([
	transforms.Lambda(lambda t: t * 255),  # 像素还原
	transforms.Lambda(lambda t: t.type(torch.uint8)),  # 像素值取整
	transforms.ToPILImage(),  # tensor转回PIL图像, (C,H,W) -> (H,W,C)
])

def auto_pad(k, p=None, d=1):  # kernel, padding, dilation
	"""Pad to 'same' shape outputs."""
	if d > 1:
		k = d * (k - 1) + 1 if isinstance(k, int) else [d * (x - 1) + 1 for x in k]  # actual kernel-size
	if p is None:
		p = k // 2 if isinstance(k, int) else [x // 2 for x in k]  # auto-pad
	return p


def random_perspective(im, degrees=10, translate=0.1, scale=0.1, shear=10, perspective=0.0, border=(0, 0)):
	# torchvision.transforms.RandomAffine(degrees=(-10, 10), translate=(0.1, 0.1), scale=(0.9, 1.1), shear=(-10, 10))
	# https://blog.csdn.net/weixin_46334272/article/details/135420634
	"""Applies random perspective transformation to an image, modifying the image and corresponding labels."""
	height = im.shape[0] + border[0] * 2  # shape(h,w,c)
	width = im.shape[1] + border[1] * 2
	
	# Center
	C = np.eye(3)
	C[0, 2] = -im.shape[1] / 2  # x translation (pixels)
	C[1, 2] = -im.shape[0] / 2  # y translation (pixels)
	
	# Perspective
	P = np.eye(3)
	P[2, 0] = random.uniform(-perspective, perspective)  # x perspective (about y)
	P[2, 1] = random.uniform(-perspective, perspective)  # y perspective (about x)
	
	# Rotation and Scale
	R = np.eye(3)
	a = random.uniform(-degrees, degrees)
	# a += random.choice([-180, -90, 0, 90])  # add 90deg rotations to small rotations
	s = random.uniform(1 - scale, 1 + scale)
	# s = 2 ** random.uniform(-scale, scale)
	R[:2] = cv2.getRotationMatrix2D(angle=a, center=(0, 0), scale=s)
	
	# Shear
	S = np.eye(3)
	S[0, 1] = math.tan(random.uniform(-shear, shear) * math.pi / 180)  # x shear (deg)
	S[1, 0] = math.tan(random.uniform(-shear, shear) * math.pi / 180)  # y shear (deg)
	
	# Translation
	T = np.eye(3)
	T[0, 2] = random.uniform(0.5 - translate, 0.5 + translate) * width  # x translation (pixels)
	T[1, 2] = random.uniform(0.5 - translate, 0.5 + translate) * height  # y translation (pixels)
	
	# Combined rotation matrix
	M = T @ S @ R @ P @ C  # order of operations (right to left) is IMPORTANT
	if (border[0] != 0) or (border[1] != 0) or (M != np.eye(3)).any():  # image changed
		if perspective:
			im = cv2.warpPerspective(im, M, dsize=(width, height), borderValue=(114, 114, 114))
		else:  # affine
			im = cv2.warpAffine(im, M[:2], dsize=(width, height), borderValue=(114, 114, 114))
	
	return im
