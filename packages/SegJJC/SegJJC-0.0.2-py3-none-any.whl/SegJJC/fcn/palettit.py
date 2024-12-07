import os
import cv2
import numpy as np
from PIL import Image


def palette():
    # 获取当前目录
    root = os.getcwd()
    # 灰度图的位置
    imgFile = root + '\\SegmentationClass'
    # 将所有的灰度图添加调色板
    for i, img in enumerate(os.listdir(imgFile)):
        filename, _ = os.path.splitext(img)
        # 这个地方需要将图片路径添加完整，不然后面读取图片文件不存在
        img = 'SegmentationClass/' + img
        img = cv2.imread(img, cv2.IMREAD_GRAYSCALE)
        save_path = root + '\\imgPalette\\' + filename + '.png'
        img = Image.fromarray(img)  # 将图像从numpy的数据格式转为PIL中的图像格式
        palette = []
        for i in range(256):
            palette.extend((i, i, i))
        # 这里设置21个颜色，其中背景为黑色，总共21个类别（包括背景）
        palette[:3 * 21] = np.array([[0, 0, 0], [0, 255, 255], [0, 128, 0], [128, 128, 0], [0, 0, 128],
                                     [128, 0, 128], [0, 128, 128], [128, 128, 128], [64, 0, 0], [192, 0, 0],
                                     [64, 128, 0], [192, 128, 0], [64, 0, 128], [192, 0, 128], [64, 128, 128],
                                     [192, 128, 128], [0, 64, 0], [128, 64, 0], [0, 192, 0], [128, 192, 0], [0, 64, 128]
                                     ], dtype='uint8').flatten()

        img.putpalette(palette)
        # print(np.shape(palette)) 输出（768,)
        img.save(save_path)


if __name__ == '__main__':
    print('Pycharm')
    palette()