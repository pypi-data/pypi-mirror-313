import os

import torch.utils.data as data
from PIL import Image,ImageDraw


import torch
# from torch.utils.data import DataLoader,Dataset,random_split
from torchvision import transforms
import cv2

class myDataset(data.Dataset):
    def __init__(self,dat_root,transforms=None):
        self.transforms = transforms
        self.imgsdir=dat_root+'/images'
        self.labelsdir = dat_root + '/labels'
        images_names=os.listdir(self.imgsdir)
        #到时可以实际情况修改是否加“_gt”
        self.masks = [os.path.join(self.labelsdir, x.split('.')[0] + '.png').replace('\\', '/') for x in images_names]
        self.images = [os.path.join(self.imgsdir, xi).replace('\\', '/') for xi in images_names]
    def __len__(self):
        return len(self.images)

    def __getitem__(self, index):
        img = Image.open(self.images[index]).convert('RGB')
        target = Image.open(self.masks[index])

        if self.transforms is not None:
            img, target = self.transforms(img, target)

        return img, target

    @staticmethod
    def collate_fn(batch):
        images, targets = list(zip(*batch))
        batched_imgs = cat_list(images, fill_value=0)
        batched_targets = cat_list(targets, fill_value=255)
        return batched_imgs, batched_targets

class myDataset_yaml(data.Dataset):
    def __init__(self,dat_root,transforms=None):
        self.transforms = transforms
        self.imgsdir=dat_root
        self.labelsdir = dat_root.split('/images')[0] + '/labels'+dat_root.split('/images')[1]
        images_names=os.listdir(self.imgsdir)
        #到时可以实际情况修改是否加“_gt”
        self.masks_txt = [os.path.join(self.labelsdir, x.split('.')[0] +'.txt').replace('\\', '/') for x in images_names]
        self.images = [os.path.join(self.imgsdir, xi).replace('\\', '/') for xi in images_names]
    def __len__(self):
        return len(self.images)

    def __getitem__(self, index):
        img = Image.open(self.images[index]).convert('RGB')
        target = txt2mask(img,self.masks_txt[index])

        if self.transforms is not None:
            img, target = self.transforms(img, target)

        return img, target

    @staticmethod
    def collate_fn(batch):
        images, targets = list(zip(*batch))
        batched_imgs = cat_list(images, fill_value=0)
        batched_targets = cat_list(targets, fill_value=255)
        return batched_imgs, batched_targets
def txt2mask(img,mask_txt):
    # 获取原始图像的尺寸
    width, height = img.size

    # 创建一个与图像相同尺寸的空白单通道（灰度）掩码图像
    mask = Image.new('L', (width, height), 0)
    draw = ImageDraw.Draw(mask)

    # 读取 .txt 文件
    with open(mask_txt, 'r') as file:
        lines = file.readlines()

    # 解析每一行
    for line in lines:
        parts = line.strip().split()
        label_index = int(parts[0])
        points = [float(p) for p in parts[1:]]

        # 将归一化的点坐标转换为图像坐标
        points = [(p * width, q * height) for p, q in zip(points[0::2], points[1::2])]

        # 绘制多边形并填充
        color = label_index + 1  # 使用标签索引+1作为灰度值
        draw.polygon(points, fill=color)
    # t=mask_txt.split("/")[-1].split(".txt")[0]
    # # 定义掩码图像的保存路径
    # mask_file_name = f"E:\\ALLvision\\pycharmproject\\yoloseg\\try\\826\\mask\\{t}.png"
    # # 保存掩码图像
    # mask.save(mask_file_name) # 保存掩码图像到文件
    return mask

class VOCSegmentation(data.Dataset):
    def __init__(self, voc_root, year="mydata", transforms=None, txt_name: str = "train.txt"):
        super(VOCSegmentation, self).__init__()
        assert year in ["2007", "2012","mydata"], "year must be in ['2007', '2012','mydata']"
        root = os.path.join(voc_root, "VOCdevkitMyself", f"VOC{year}")
        assert os.path.exists(root), "path '{}' does not exist.".format(root)
        image_dir = os.path.join(root, 'ImageDog')
        mask_dir = os.path.join(root, 'SegmentationClass')

        txt_path = os.path.join(root, "ImageSets", "Segmentation", txt_name)
        assert os.path.exists(txt_path), "file '{}' does not exist.".format(txt_path)
        with open(os.path.join(txt_path), "r") as f:
            file_names = [x.strip() for x in f.readlines() if len(x.strip()) > 0]

        self.images = [os.path.join(image_dir, x + ".jpg") for x in file_names]
        self.masks = [os.path.join(mask_dir, x + ".png") for x in file_names]
        assert (len(self.images) == len(self.masks))
        self.transforms = transforms

    def __getitem__(self, index):
        """
        Args:
            index (int): Index

        Returns:
            tuple: (image, target) where target is the image segmentation.
        """
        img = Image.open(self.images[index]).convert('RGB')
        target = Image.open(self.masks[index])

        if self.transforms is not None:
            img, target = self.transforms(img, target)

        return img, target

    def __len__(self):
        return len(self.images)

    @staticmethod
    def collate_fn(batch):
        images, targets = list(zip(*batch))
        batched_imgs = cat_list(images, fill_value=0)
        batched_targets = cat_list(targets, fill_value=255)
        return batched_imgs, batched_targets

def cat_list(images, fill_value=0):
    # 计算该batch数据中，channel, h, w的最大值
    max_size = tuple(max(s) for s in zip(*[img.shape for img in images]))
    batch_shape = (len(images),) + max_size
    batched_imgs = images[0].new(*batch_shape).fill_(fill_value)
    for img, pad_img in zip(images, batched_imgs):
        pad_img[..., :img.shape[-2], :img.shape[-1]].copy_(img)
    return batched_imgs

# dat_root="E:/ALLvision/pycharmproject/yoloseg/githubtry/diyFCN/try2_yaml/fcn/Data_seg/images/train"
# imgsdir = dat_root
# labelsdir = dat_root.split('/images')[0] + '/labels' + dat_root.split('/images')[1]
# images_names = os.listdir(imgsdir)
# masks_txt = [os.path.join(labelsdir, x.split('.')[0] + '.txt').replace('\\', '/') for x in images_names]
# images = [os.path.join(imgsdir, xi).replace('\\', '/') for xi in images_names]
# index=1
# img = Image.open(images[index]).convert('RGB')
# target = txt2mask(img, masks_txt[index])
# # 构造完整的文件路径
# target_path = "E:/ALLvision/pycharmproject/yoloseg/githubtry/diyFCN/try2_yaml/fcn/tryimgsave/1.png"
# # 保存 target 图像
# target.save(target_path)
# ss=Image.open(target_path)
# t=ss
