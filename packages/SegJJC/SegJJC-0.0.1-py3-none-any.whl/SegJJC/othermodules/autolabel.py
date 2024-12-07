import os
import cv2
from ultralytics import YOLO
import time
import json
import torch

# # 设置保存图片的路径
# cur_path = r"E:\ALLvision\pycharmproject\pvk\autolabel\try\out\imgsave"
# # 训练好的模型权重路径
# model = YOLO(r"E:\ALLvision\pycharmproject\pvk\autolabel\try\model\best.pt")
# # 测试图片的路径
# file_pathname = r"E:\工作\钙钛矿玻璃\采图\2419LPL\Sourceimg_resizejpg\PL-蓝光\2024_11_15\Source"
# #json输出路径
# outjson_path=r"E:\ALLvision\pycharmproject\pvk\autolabel\try\out\datajson"
# # 存储推理结果的列表
# predictions = []
# file_pathnames=file_pathname+"\\"

class YOLOauto_label_det:
    def __init__(self,params,model,outjson_path=None,labelimg_path=None,labeled_imgdir=None):
        # 判断传入的 model 是 YOLO 实例还是文件路径
        if isinstance(model, YOLO):
            self.model = model  # 如果是 YOLO 实例，直接赋值
        elif isinstance(model, str) and os.path.isfile(model):  # 如果是路径并且文件存在
            self.model = YOLO(model)  # 加载路径对应的模型
        else:
            raise ValueError("Invalid model input. Must be a YOLO instance or a valid file path.")
        self.params=params
        self.outjson_path=params.get("outjson_path", None) if params.get("outjson_path", None) else outjson_path
        self.labelimg_path=params.get("labelimg_path", None) if params.get("labelimg_path", None) else labelimg_path
        self.file_pathnames=self.labelimg_path+"\\"
        self.labeled_imgdir=params.get("labeled_imgdir", None) if params.get("labeled_imgdir", None) else labeled_imgdir
    def extract_predictions(self,result, image_id, image_file_name):
        sample = []
        for det in result:
            # 将张量转换为列表
            xyxy_list = det.boxes.xyxy.tolist()
            # 初始化坐标列表
            col1_list = []
            row1_list = []
            col2_list = []
            row2_list = []
            # 遍历边界框坐标列表
            for box in xyxy_list:
                col1, row1, col2, row2 = box
                col1_list.append(col1)
                row1_list.append(row1)
                col2_list.append(col2)
                row2_list.append(row2)
            sample.append({
                "image_id": image_id,
                "image_file_name": image_file_name,
                "bbox_label_id": det.boxes.cls.to(torch.int).tolist(),
                "bbox_row1": row1_list,
                "bbox_col1": col1_list,
                "bbox_row2": row2_list,
                "bbox_col2": col2_list
            })
        return sample

    def labelit(self):
        # 存储推理结果的列表
        predictions = []
        # 存储JSON结果的列表
        json_results = {
            "class_ids": list(self.model.names.keys()),
            "class_names": list(self.model.names.values()),
            "image_dir": self.file_pathnames.replace("\\", "/"),
            "samples": []
        }
        # 处理文件夹中的每张图片
        for image_id, filename in enumerate(os.listdir(self.labelimg_path)):
            if filename.split('.')[-1] != 'txt':
                img = cv2.imread(os.path.join(self.labelimg_path, filename))
                # 进行推理
                result = self.model.predict(img, batch=self.params.get("batchsize",1), imgsz=1024)
                # 将推理结果存储到列表中
                predictions.append(result)
                # 提取并存储到JSON结果
                json_results["samples"].extend(self.extract_predictions(result, image_id + 1, filename))
                # t=json_results


        json_path = os.path.join(self.outjson_path, 'predictions.json')
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(json_results, f, ensure_ascii=False, indent=4)

        if self.labeled_imgdir:
            self.show_result(predictions)
    def show_result(self,predictions):
        # 创建窗口
        cv2.namedWindow("yolo", 0)
        cv2.resizeWindow("yolo", 640, 640)

        exit_flag = False  # 标志变量
        key = cv2.waitKey(0)
        for j, result in enumerate(predictions):
            if exit_flag:  # 检查是否应该退出外部循环
                break

            if isinstance(result, list):
                for res in result:
                    ann = res.plot()
                    if key == ord('q') and j != len(predictions) - 1:
                        cv2.imshow("yolo", ann)
                        key = cv2.waitKey(0)
                    elif key == ord('q') and j == len(predictions) - 1:
                        exit_flag = True  # 设置标志变量为 True
                        break
                    elif key == 27:
                        exit_flag = True  # 设置标志变量为 True
                        break
                    if not os.path.exists(self.labeled_imgdir):
                        os.mkdir(self.labeled_imgdir)
                    # cv2.imwrite(os.path.join(cur_path, f"out{j}.jpg"), ann)

            else:
                ann = result.plot()
                if key == ord('q') and j != len(predictions) - 1:
                    cv2.imshow("yolo", ann)
                    key = cv2.waitKey(0)
                elif key == ord('q') and j == len(predictions) - 1:
                    exit_flag = True  # 设置标志变量为 True
                    break
                elif key == 27:
                    exit_flag = True  # 设置标志变量为 True
                    break

                if not os.path.exists(self.labeled_imgdir):
                    os.mkdir(self.labeled_imgdir)
                cv2.imwrite(os.path.join(self.labeled_imgdir, f"out{j}.jpg"), ann)

        cv2.destroyAllWindows()


# ###使用
# # 设置保存图片的路径
# cur_path_s = r"E:\ALLvision\pycharmproject\Efficientnet\segjjc_clsseg_try\sahi_preprocess\1125\out\imgsave"
# # 训练好的模型权重路径
# model_s = r"E:\ALLvision\pycharmproject\pvk\autolabel\try\model\best.pt"
# # 测试图片的路径
# file_pathname_s = r"E:\工作\钙钛矿玻璃\采图\2419LPL\Sourceimg_resizejpg\PL-蓝光\2024_11_15\Source"
# #json输出路径
# outjson_path_s=r"E:\ALLvision\pycharmproject\Efficientnet\segjjc_clsseg_try\sahi_preprocess\1125\out\datajson"
# ##定义auto_label
# lit=auto_label(model_s,outjson_path_s,file_pathname_s,cur_path_s)
# #执行
# lit.labelit()