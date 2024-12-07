import os
import yaml
from PIL import Image
import numpy as np

class ROIT_det:
    def __init__(self, yaml_path=None,roi_datadir=None,roi=None):
        self.yaml_path=yaml_path
        self.output_yaml_path=None
        self.Data_roi_dir=roi_datadir
        self.roi=roi

###获取切图区域内的标注框####
    def bbox_in_roi(self, bbox, roi_region):
        roi_x, roi_y, roi_w, roi_h = roi_region
        bbox_x1, bbox_y1, bbox_x2, bbox_y2 = bbox

        new_bbox_x1 = max(bbox_x1 - roi_x, 0)
        new_bbox_y1 = max(bbox_y1 - roi_y, 0)
        new_bbox_x2 = min(bbox_x2 - roi_x, roi_w)
        new_bbox_y2 = min(bbox_y2 - roi_y, roi_h)

        if new_bbox_x1 < new_bbox_x2 and new_bbox_y1 < new_bbox_y2:
            return new_bbox_x1, new_bbox_y1, new_bbox_x2, new_bbox_y2
        else:
            return None

    def convert_to_original(self, size, box):
        width, height = size
        x = box[0] * width
        y = box[1] * height
        w = box[2] * width
        h = box[3] * height

        x1 = x - w / 2
        y1 = y - h / 2
        x2 = x + w / 2
        y2 = y + h / 2

        return x1, y1, x2, y2
    def process_imgs(self, image_paths, output_dir):
        output_folder = os.path.join(output_dir, 'images')
        txt_outdir=os.path.join(output_dir,'labels')
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        if not os.path.exists(txt_outdir):
            os.makedirs(txt_outdir)
        new_image_paths = []  # 用于存储新的图片路径

        for image_path in image_paths:
            ##获取图片格式
            imgtype = os.path.basename(image_path).split('.')[-1]
            txt_path = image_path.replace(f".{imgtype}", ".txt").replace("images", "labels")
            with open(txt_path, "r") as f:
                annotations = f.readlines()

            with Image.open(image_path) as img:
                img.load()
                width, height = img.size

                roi_x1, roi_y1, roi_x2, roi_y2 = self.roi
                roi_w=roi_x2-roi_x1
                roi_h=roi_y2 - roi_y1
                roi_region=[roi_x1, roi_y1, roi_w, roi_h]
                roi_img = img.crop((roi_x1, roi_y1, roi_x2 , roi_y2))

                roi_img_filename = os.path.join(output_folder, f"{os.path.basename(image_path).replace(f'.{imgtype}', '')}_roi.{imgtype}")
                roi_img.save(roi_img_filename)

                roi_txt_filename = os.path.join(txt_outdir, f"{os.path.basename(image_path).replace(f'.{imgtype}', '')}_roi.txt")
                with open(roi_txt_filename, "w") as roi_f:
                    has_bbox = False
                    for annotation in annotations:
                        elements = annotation.strip().split()
                        bbox_id = int(elements[0])
                        normalized_bbox = list(map(float, elements[1:]))

                        bbox = self.convert_to_original((width, height), normalized_bbox)

                        new_bbox = self.bbox_in_roi(bbox, roi_region)
                        ###归一化标注框
                        if new_bbox:
                            has_bbox = True
                            x_center = (new_bbox[0] + new_bbox[2]) / 2 / roi_w
                            y_center = (new_bbox[1] + new_bbox[3]) / 2 / roi_h
                            bbox_w = (new_bbox[2] - new_bbox[0]) / roi_w
                            bbox_h = (new_bbox[3] - new_bbox[1]) / roi_h

                            roi_f.write(f"{bbox_id} {x_center} {y_center} {bbox_w} {bbox_h}\n")

                    if not has_bbox:
                        roi_f.write("")

                new_image_paths.append(roi_img_filename)  # 添加新的图片路径

        return new_image_paths
    def update_yaml(self, train_paths, val_paths,test_paths):
        with open(self.yaml_path, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)
        train_paths = train_paths.replace("\\", "/")
        val_paths = val_paths.replace("\\", "/")
        test_paths = test_paths.replace("\\", "/")
        data['train'] = train_paths
        data['val'] = val_paths
        data['test'] = test_paths
        with open(self.output_yaml_path, 'w', encoding='utf-8') as file:
            yaml.dump(data, file, allow_unicode=True)

    def save_image_paths(self, image_paths, output_txt_path):
        with open(output_txt_path, 'w') as f:
            for path in image_paths:
                f.write(f"{path}\n")
    def read_yaml(self):
        with open(self.yaml_path, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)

        train_txt_path = config['train']
        val_txt_path = config['val']
        test_txt_path=train_txt_path.replace("train.txt",'test.txt')
        # 3. 读取 train 和 val 的文件路径
        train_image_paths = [line.strip() for line in open(train_txt_path, 'r')]
        val_image_paths = [line.strip() for line in open(val_txt_path, 'r')]
        # 检查 test.txt 文件是否存在
        if os.path.exists(test_txt_path):
            test_image_paths = [line.strip() for line in open(test_txt_path, 'r')]
        else:
            # 如果 test.txt 文件不存在，则返回空列表
            test_image_paths = []
            print(f"Warning: {test_txt_path} does not exist. Returning empty test image paths.")
        return train_image_paths, val_image_paths, test_image_paths


    def process_data(self):
        # 5. 处理 train 和 val 图片
        train_image_paths, val_image_paths, test_image_paths=self.read_yaml()
        if self.Data_roi_dir:
            Data_roi_dir=self.Data_roi_dir
        else:
        # 获取上层路径
            parent_dir = os.path.dirname(self.yaml_path)
            Data_roi_dir=os.path.join(parent_dir,'Data_det_roi')
        if not os.path.exists(Data_roi_dir):
            os.makedirs(Data_roi_dir)
        trainval_outdir=os.path.join(Data_roi_dir,'paper_data')
        if not os.path.exists(trainval_outdir):
            os.makedirs(trainval_outdir)
        new_train_paths = self.process_imgs(train_image_paths,Data_roi_dir)
        new_val_paths = self.process_imgs(val_image_paths, Data_roi_dir)
        #
        # ###和train、val一样使用切图切分，然后输出切图后的路径
        # new_test_paths = self.process_imgs(test_image_paths, Data_sahi_dir)
        # ###对test数据集不使用切图，直接给出原来一样的路径
        new_test_paths =test_image_paths
        #
        # 6. 保存新的 train.txt 和 val.txt 文件
        output_train_txt=os.path.join(trainval_outdir,'train.txt')
        output_val_txt=os.path.join(trainval_outdir,'val.txt')
        output_test_txt = os.path.join(trainval_outdir, 'test.txt')
        self.save_image_paths(new_train_paths, output_train_txt)
        self.save_image_paths(new_val_paths, output_val_txt)
        self.save_image_paths(new_test_paths, output_test_txt)
        # 7. 更新 YAML 文件
        self.output_yaml_path=os.path.join(Data_roi_dir,'mydata.yaml')
        self.update_yaml(output_train_txt, output_val_txt,output_test_txt)

    # ##predict_slice_imgs切分文件夹所有图片
    # def predict_slice_imgs(self, image_paths):
    #     sliced_images = []  # 存储切割后的图片数据
    #     for image_path in os.listdir(image_paths):
    #         # 获取图片格式
    #         sliced_image=[]
    #         image_path = os.path.join(image_paths,image_path)
    #         with Image.open(image_path) as img:
    #             width, height = img.size
    #             self.calculate_slice_regions(image_height=height, image_width=width,roi=self.roi)
    #
    #             for slice_region, index in self.slice_regions:
    #                 slice_x, slice_y, slice_w, slice_h = slice_region
    #                 slice_img = img.crop((slice_x, slice_y, slice_x + slice_w, slice_y + slice_h))
    #
    #                 # 将切割的图像保存为 numpy 数组（或直接传递到模型支持的格式）
    #                 slice_img_array = np.array(slice_img)
    #                 sliced_image.append(slice_img_array)
    #         sliced_images.append(sliced_image)
    #     # 返回所有切割后的图片列表
    #     return sliced_images
    #
    # ##predict_slice_oneimg切分单个文件图片
    # def predict_slice_oneimg(self, image_path_or_image):
    #     # 根据参数的类型来决定如何处理
    #     if isinstance(image_path_or_image, str):
    #         sliced_images = []  # 存储切割后的图片数据
    #         image_path=image_path_or_image
    #         with Image.open(image_path) as img:
    #             width, height = img.size
    #             self.calculate_slice_regions(image_height=height, image_width=width,roi=self.roi)
    #
    #             for slice_region, index in self.slice_regions:
    #                 slice_x, slice_y, slice_w, slice_h = slice_region
    #                 slice_img = img.crop((slice_x, slice_y, slice_x + slice_w, slice_y + slice_h))
    #
    #                 # 将切割的图像保存为 numpy 数组（或直接传递到模型支持的格式）
    #                 slice_img_array = np.array(slice_img)
    #                 sliced_images.append(slice_img_array)
    #         # 返回所有切割后的图片列表
    #         return sliced_images
    #     elif isinstance(image_path_or_image, Image.Image):
    #         sliced_images = []  # 存储切割后的图片数据
    #         img = image_path_or_image
    #         width, height = img.size
    #         self.calculate_slice_regions(image_height=height, image_width=width,roi=self.roi)
    #
    #         for slice_region, index in self.slice_regions:
    #             slice_x, slice_y, slice_w, slice_h = slice_region
    #             slice_img = img.crop((slice_x, slice_y, slice_x + slice_w, slice_y + slice_h))
    #
    #             # 将切割的图像保存为 numpy 数组（或直接传递到模型支持的格式）
    #             slice_img_array = np.array(slice_img)
    #             sliced_images.append(slice_img_array)
    #         # 返回所有切割后的图片列表
    #         return sliced_images
    #     else:
    #         raise TypeError("image_path_or_image 必须是字符串或 PIL.Image.Image")

