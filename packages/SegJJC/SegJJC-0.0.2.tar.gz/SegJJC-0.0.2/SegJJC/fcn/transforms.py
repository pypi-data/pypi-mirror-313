import numpy as np
import random
from typing import Tuple

import torch
from torchvision import transforms as T
from torchvision.transforms import functional as F
from PIL import Image


def letterbox_pil(image: Image.Image, new_shape: Tuple[int, int] = (640, 640), auto=True, scaleFill=False, scaleup=True,
                  stride=32):
    """
    Resize and pad PIL Image while meeting stride-multiple constraints.

    Args:
        image (Image.Image): The input PIL Image to be resized and padded.
        new_shape (Tuple[int, int]): The desired output shape of the image.
        auto (bool): Whether to keep the original ratio and pad the image.
        scaleFill (bool): Whether to stretch the image to fit the new shape.
        scaleup (bool): Whether to scale up the image.
        stride (int): Stride used for padding.

    Returns:
        Image.Image: Resized and padded PIL Image.
    """
    # Compute scale ratio and new shape
    shape = image.size  # current shape [width, height]
    if isinstance(new_shape, int):
        new_shape = (new_shape, new_shape)

    # Scale ratio (new / old)
    r = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
    if not scaleup:  # only scale down, do not scale up (for better val mAP)
        r = min(r, 1.0)

    # Compute padding
    ratio = r, r  # width, height ratios
    new_unpad = int(round(shape[0] * r)), int(round(shape[1] * r))
    dw, dh = new_shape[0] - new_unpad[0], new_shape[1] - new_unpad[1]  # wh padding
    if auto:  # minimum rectangle
        dw, dh = np.mod(dw, stride), np.mod(dh, stride)  # wh padding
    elif scaleFill:  # stretch
        dw, dh = 0.0, 0.0
        new_unpad = (new_shape[0], new_shape[1])
        ratio = new_shape[0] / shape[1], new_shape[1] / shape[0]  # width, height ratios

    dw /= 2  # divide padding into 2 sides
    dh /= 2

    # Resize the image
    mode = 'L' if image.mode == 'L' else 'RGB'
    resized_image = image.resize(new_unpad, Image.BILINEAR).convert(mode)

    # Create a new image with the desired background color
    if mode == 'L':
        new_image = Image.new('L', new_shape, 0)  # 单通道图像填充为 114
    else:
        new_image = Image.new('RGB', new_shape, (114, 114, 114))  # 三通道图像填充为 (114, 114, 114)

    # Calculate the position to paste the resized image
    paste_left = int(round(dw))
    paste_top = int(round(dh))
    paste_right = int(round(paste_left + new_unpad[0]))
    paste_bottom = int(round(paste_top + new_unpad[1]))

    # Paste the resized image onto the new image
    new_image.paste(resized_image, (paste_left, paste_top, paste_right, paste_bottom))

    return new_image

def pad_if_smaller(img, size, fill=0):
    # 如果图像最小边长小于给定size，则用数值fill进行padding
    min_size = min(img.size)
    if min_size < size:
        ow, oh = img.size
        padh = size - oh if oh < size else 0
        padw = size - ow if ow < size else 0
        img = F.pad(img, (0, 0, padw, padh), fill=fill)
    return img


class Compose(object):
    def __init__(self, transforms):
        self.transforms = transforms

    def __call__(self, image, target):
        for t in self.transforms:
            image, target = t(image, target)
        return image, target


class RandomResize(object):
    def __init__(self, min_size, max_size=None):
        self.min_size = min_size
        if max_size is None:
            max_size = min_size
        self.max_size = max_size

    def __call__(self, image, target):
        size = random.randint(self.min_size, self.max_size)
        # 这里size传入的是int类型，所以是将图像的最小边长缩放到size大小
        image = F.resize(image, size)
        # 这里的interpolation注意下，在torchvision(0.9.0)以后才有InterpolationMode.NEAREST
        # 如果是之前的版本需要使用PIL.Image.NEAREST
        target = F.resize(target, size, interpolation=T.InterpolationMode.NEAREST)
        return image, target

class imgResize(object):
    def __init__(self,size:Tuple[int, int]):
        self.max_size = (max(size),max(size))

    def __call__(self, image, target):
        image=letterbox_pil(image,self.max_size)
        target = letterbox_pil(target, self.max_size)
        return image, target

class RandomHorizontalFlip(object):
    def __init__(self, flip_prob):
        self.flip_prob = flip_prob

    def __call__(self, image, target):
        if random.random() < self.flip_prob:
            image = F.hflip(image)
            target = F.hflip(target)
        return image, target


class RandomCrop(object):
    def __init__(self, size):
        self.size = size

    def __call__(self, image, target):
        image = pad_if_smaller(image, self.size)
        target = pad_if_smaller(target, self.size, fill=255)
        crop_params = T.RandomCrop.get_params(image, (self.size, self.size))
        image = F.crop(image, *crop_params)
        target = F.crop(target, *crop_params)
        return image, target


class CenterCrop(object):
    def __init__(self, size):
        self.size = size

    def __call__(self, image, target):
        image = F.center_crop(image, self.size)
        target = F.center_crop(target, self.size)
        return image, target


class ToTensor(object):
    def __call__(self, image, target):
        image = F.to_tensor(image)
        target = torch.as_tensor(np.array(target), dtype=torch.int64)
        return image, target


class Normalize(object):
    def __init__(self, mean, std):
        self.mean = mean
        self.std = std

    def __call__(self, image, target):
        image = F.normalize(image, mean=self.mean, std=self.std)
        return image, target


# # 加载图像
# image_path = 'E:/ALLvision/pycharmproject/yoloseg/githubtry/diyFCN/try2_yaml/fcn/Data_seg/images/train/44.jpg'
# target_path = 'E:/ALLvision/pycharmproject/yoloseg/githubtry/diyFCN/try2_yaml/fcn/tryimgsave/1.png'
#
# img = Image.open(image_path)
# target = Image.open(target_path)
#
# # 创建 imgResize 实例
# img_resizer = imgResize(size=(640, 640))
#
# # 调用 imgResize 实例来调整图像大小
# resized_img, resized_target = img_resizer(img, target)
#
# # 显示调整大小后的图像
# resized_img.show()
# resized_target.show()