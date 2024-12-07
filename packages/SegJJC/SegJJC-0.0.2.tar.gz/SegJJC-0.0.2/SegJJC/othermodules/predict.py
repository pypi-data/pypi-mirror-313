import copy
import os
import torch
from torchvision.ops import nms
from PIL import Image
import numpy as np
from .Hsahi import HSAHI_det
from ultralytics import YOLO
import cv2
from ultralytics.engine.results import Results, Boxes
import json
import re
import ctypes
import sys

class PredictSahi_yolo:
    def __init__(self, model_path,params):
        # 初始化模型路径、文件路径、保存路径
        self.modelpath=model_path
        self.model = YOLO(model_path)
        self.trueimgsize=params["inferimgsz"]
        self.sahi = HSAHI_det(slice_width=params["inferimgsz"][0],
                              slice_height=params["inferimgsz"][1],
                              overlap_width_ratio=params.get("sahi_overlapratio",0.25),
                              overlap_height_ratio=params.get("sahi_overlapratio",0.25),
                              roi=params.get("sahi_roi",None))
        self.file_pathname = params['testimg']
        self.cur_path = params['inferedimg']
        self.inferedimg_onedir=params.get("inferedimg_onedir",True)
        self.predictions = []
        self.result_dict = []
        self.resultjson_filetype=params.get("resultjson_filetype","json")
        self.import_HALCONdll=params.get("import_HALCONdll",True)
        self.resultjson_path = params.get("resultjson_path", None)
        self.auto_label=params.get("auto_label",False)
        self.m_probability_threshold = params.get("prob_thresh",0.25)
        self.m_nms_threshold = params.get("nms_thresh",0.45)
        self.inferbatch=params.get("inferbatch",1)
        self.inferimgsz=params["inferimgsz"][0]
        self.inferdevicehandle=params.get("inferdevicehandle",0)
        if self.inferdevicehandle=='gpu':
            self.inferdevicehandle=0
        self.sahi_roi=params.get("sahi_roi",None)
        self.roi = params.get("roi", None)
        self.roi_padding=params.get("roi_padding", False)
        self.ifroiimg = params.get("ifroiimg", False)
        self.resize_before_roi=params.get("resize_before_roi", False)
        self.sahiinfer=params.get("sahiinfer",True)

    def process_detections_nms(self, it_sliceed, img):
        for q in range(len(it_sliceed)):
            # 获取当前切片的边界框、置信度和类别信息
            boxes = it_sliceed[q].boxes.xyxy  # 获取xyxy格式的边界框
            scores = it_sliceed[q].boxes.conf  # 置信度
            class_ids = it_sliceed[q].boxes.cls  # 类别ID

            # 过滤掉置信度低于阈值的框
            valid_indices = scores > self.m_probability_threshold
            boxes = boxes[valid_indices]
            scores = scores[valid_indices]
            class_ids = class_ids[valid_indices]

            # 进行 NMS
            if len(boxes) > 0:
                indices = nms(boxes, scores, self.m_nms_threshold)
                selected_boxes = boxes[indices]
                selected_scores = scores[indices]
                selected_class_ids = class_ids[indices]

                # 更新 it_sliceed[q].boxes
                new_data = torch.cat((selected_boxes, selected_scores.unsqueeze(1), selected_class_ids.unsqueeze(1)), dim=1)
                it_sliceed[q].boxes = Boxes(new_data, it_sliceed[q].boxes.orig_shape)

            imgori = np.array(img)
            it_sliceed[q].orig_img = imgori

        return it_sliceed

    # region greedy_nmm函数实现
    def nmm_calculate_box_union(self,bbox1, bbox2):
        """
        计算两个边界框的并集。
        :param bbox1: 第一个边界框 [x1, y1, x2, y2]
        :param bbox2: 第二个边界框 [x1, y1, x2, y2]
        :return: 并集边界框 [x1, y1, x2, y2]
        """
        union_bbox = np.zeros(4)
        union_bbox[0] = min(bbox1[0], bbox2[0])  # x1
        union_bbox[1] = min(bbox1[1], bbox2[1])  # y1
        union_bbox[2] = max(bbox1[2], bbox2[2])  # x2
        union_bbox[3] = max(bbox1[3], bbox2[3])  # y2
        return union_bbox

    def greedy_nmm(self, object_predictions, match_metric="IOU", match_threshold=0):
        """
        贪心NMS算法，用于合并重叠的边界框。
        :param object_predictions: 检测结果列表，每个元素包含 bbox, class_id, conf
        :param match_metric: 匹配标准（"IOU"）
        :param match_threshold: 匹配阈值
        :return: 合并后的检测结果列表
        """
        # 以置信度降序排序
        object_predictions = sorted(object_predictions, key=lambda x: x['conf'], reverse=True)
        selected = [False] * len(object_predictions)
        merged_predictions = []

        for i, pred in enumerate(object_predictions):
            if selected[i]:
                continue

            merged = pred.copy()  # 初始化合并的预测框
            selected[i] = True
            to_merge = [i]

            while to_merge:
                current_index = to_merge.pop(0)

                for j in range(len(object_predictions)):
                    if selected[j] or object_predictions[current_index]['class_id'] != object_predictions[j][
                        'class_id']:
                        continue

                    bbox1 = merged['bbox']
                    bbox2 = object_predictions[j]['bbox']

                    # 计算 IOU
                    xx1 = max(bbox1[0], bbox2[0])
                    yy1 = max(bbox1[1], bbox2[1])
                    xx2 = min(bbox1[2], bbox2[2])
                    yy2 = min(bbox1[3], bbox2[3])

                    w = max(0.0, xx2 - xx1)
                    h = max(0.0, yy2 - yy1)
                    inter = w * h

                    area1 = (bbox1[2] - bbox1[0]) * (bbox1[3] - bbox1[1])
                    area2 = (bbox2[2] - bbox2[0]) * (bbox2[3] - bbox2[1])
                    union_area = area1 + area2 - inter

                    iou = inter / union_area if union_area > 0 else 0.0

                    # 如果 IOU 大于阈值，则合并
                    if match_metric == "IOU" and iou > match_threshold:
                        selected[j] = True

                        # 合并框
                        union_bbox = self.nmm_calculate_box_union(bbox1, bbox2)
                        merged['bbox'] = union_bbox
                        merged['conf'] = max(merged['conf'], object_predictions[j]['conf'])
                        merged['class_id'] = merged['class_id'] if merged['conf'] > object_predictions[j]['conf'] else \
                        object_predictions[j]['class_id']

                        # 合并掩码（如果有）
                        if 'mask' in merged and 'mask' in object_predictions[j]:
                            # 如果掩码为None，初始化为空矩阵
                            if merged['mask'] is None:
                                merged['mask'] = np.zeros_like(object_predictions[j]['mask'])
                            if object_predictions[j]['mask'] is None:
                                object_predictions[j]['mask'] = np.zeros_like(merged['mask'])

                            # 合并掩码
                            merged['mask'] |= object_predictions[j]['mask']  # 假设掩码是二进制位图，使用位运算合并

                        to_merge.append(j)

            merged_predictions.append(merged)

        return merged_predictions
    def process_detections_with_nmm(self, it_sliceed,img):
        for q in range(len(it_sliceed)):
            boxes = it_sliceed[q].boxes.xyxy  # 获取经过 NMS 后的框
            scores = it_sliceed[q].boxes.conf  # 置信度
            class_ids = it_sliceed[q].boxes.cls  # 类别ID
            # 进行 NMM
            if len(boxes) > 0:
                # 准备 greedy_nmm 函数需要的输入格式
                object_predictions = []
                for i in range(len(boxes)):
                    object_predictions.append({
                        'bbox': boxes[i].cpu().numpy().tolist(),  # 转为list
                        'conf': scores[i].cpu().item(),  # 取值
                        'class_id': int(class_ids[i].cpu().item()),  # 转为整型
                        'mask': None  # 如果有掩码，这里可以加入掩码数据
                    })

                # 调用 greedy_nmm 函数进行合并
                merged_predictions = self.greedy_nmm(object_predictions, match_threshold=0)

                # 转回 YOLO 格式并更新结果
                merged_boxes = [pred['bbox'] for pred in merged_predictions]
                merged_scores = [pred['conf'] for pred in merged_predictions]
                merged_class_ids = [pred['class_id'] for pred in merged_predictions]

                # 更新 it_sliceed[q].boxes
                new_data = torch.cat((
                    torch.tensor(merged_boxes),
                    torch.tensor(merged_scores).unsqueeze(1),
                    torch.tensor(merged_class_ids).unsqueeze(1)
                ), dim=1)
                it_sliceed[q].boxes = Boxes(new_data, it_sliceed[q].boxes.orig_shape)

            imgori = np.array(img)
            it_sliceed[q].orig_img = imgori

        return it_sliceed

    def process_detections_with_nmsm(self, it_sliceed, img):
        for q in range(len(it_sliceed)):
            # 获取经过NMS的边界框、置信度和类别信息
            boxes = it_sliceed[q].boxes.xyxy  # 获取xyxy格式的边界框
            scores = it_sliceed[q].boxes.conf  # 置信度
            class_ids = it_sliceed[q].boxes.cls  # 类别ID

            # 过滤掉置信度低于阈值的框
            valid_indices = scores > self.m_probability_threshold
            boxes = boxes[valid_indices]
            scores = scores[valid_indices]
            class_ids = class_ids[valid_indices]

            # NMS 处理后的框
            if len(boxes) > 0:
                indices = nms(boxes, scores, self.m_nms_threshold)
                selected_boxes = boxes[indices]
                selected_scores = scores[indices]
                selected_class_ids = class_ids[indices]

                # 准备 greedy_nmm 函数需要的输入格式
                object_predictions = []
                for i in range(len(selected_boxes)):
                    object_predictions.append({
                        'bbox': selected_boxes[i].cpu().numpy().tolist(),  # 转为list
                        'conf': selected_scores[i].cpu().item(),  # 取值
                        'class_id': int(selected_class_ids[i].cpu().item()),  # 转为整型
                        'mask': None  # 如果有掩码，这里可以加入掩码数据
                    })

                # 调用 greedy_nmm 函数进行合并
                merged_predictions = self.greedy_nmm(object_predictions, match_threshold=0.5)

                # 转回 YOLO 格式并更新 it_sliceed[q].boxes
                merged_boxes = [pred['bbox'] for pred in merged_predictions]
                merged_scores = [pred['conf'] for pred in merged_predictions]
                merged_class_ids = [pred['class_id'] for pred in merged_predictions]

                new_data = torch.cat((
                    torch.tensor(merged_boxes),
                    torch.tensor(merged_scores).unsqueeze(1),
                    torch.tensor(merged_class_ids).unsqueeze(1)
                ), dim=1)
                it_sliceed[q].boxes = Boxes(new_data, it_sliceed[q].boxes.orig_shape)

            imgori = np.array(img)
            it_sliceed[q].orig_img = imgori

        return it_sliceed
    # endregion

    def merge_slices(self, it_sliced, img, shift_params,img_name):
        result_merged = []
        all_boxes_data = []

        for slice_idx, result in enumerate(it_sliced):
            boxes_data = result.boxes.data.clone()
            boxes_xyxy = boxes_data[:, :4].clone()

            # 对xyxy坐标进行偏移
            shift_x = shift_params[slice_idx][0][0]
            shift_y = shift_params[slice_idx][0][1]
            boxes_xyxy[:, 0] += shift_x  # x1
            boxes_xyxy[:, 1] += shift_y  # y1
            boxes_xyxy[:, 2] += shift_x  # x2
            boxes_xyxy[:, 3] += shift_y  # y2

            boxes_data[:, :4] = boxes_xyxy
            all_boxes_data.append(boxes_data)

        if all_boxes_data:
            merged_boxes_data = torch.cat(all_boxes_data, dim=0)
        else:
            merged_boxes_data = None

        oriimg = np.array(img)
        if merged_boxes_data is not None:
            result_merged.append(Results(oriimg, path=img_name, names=self.model.names, boxes=merged_boxes_data))

        return result_merged

    def recover_Roied(self, it_roied, img, shift_params,img_name):
        result_roied = []
        all_boxes_data = []

        for slice_idx, result in enumerate(it_roied):
            boxes_data = result.boxes.data.clone()
            boxes_xyxy = boxes_data[:, :4].clone()

            # 对xyxy坐标进行偏移
            shift_x = shift_params[0][0]
            shift_y = shift_params[0][1]
            shift_scale_x = shift_params[1][0]
            shift_scale_y = shift_params[1][1]
            boxes_xyxy[:, 0] += shift_x  # x1
            boxes_xyxy[:, 1] += shift_y  # y1
            boxes_xyxy[:, 2] += shift_x  # x2
            boxes_xyxy[:, 3] += shift_y  # y2
            ##scale如果有比例缩放，除以还原比例
            boxes_xyxy[:, 0] *= (1.0/shift_scale_x)  # x1
            boxes_xyxy[:, 1] *= (1.0/shift_scale_y)  # y1
            boxes_xyxy[:, 2] *= (1.0/shift_scale_x)  # x2
            boxes_xyxy[:, 3] *= (1.0/shift_scale_y)  # y2

            boxes_data[:, :4] = boxes_xyxy
            all_boxes_data.append(boxes_data)

        if all_boxes_data:
            roied_boxes_data = torch.cat(all_boxes_data, dim=0)
        else:
            roied_boxes_data = None

        oriimg = np.array(img)
        if roied_boxes_data is not None:
            result_roied.append(Results(oriimg, path=img_name, names=self.model.names, boxes=roied_boxes_data))

        return result_roied
    def recover_Roi_filled(self, it_roied, img, shift_params,img_name):
        result_roied = []
        all_boxes_data = []

        for slice_idx, result in enumerate(it_roied):
            boxes_data = result.boxes.data.clone()
            boxes_xyxy = boxes_data[:, :4].clone()

            # 对xyxy坐标进行偏移
            shift_scale_x = shift_params[1][0]
            shift_scale_y = shift_params[1][1]
            ##scale如果有比例缩放，除以还原比例
            boxes_xyxy[:, 0] *= (1.0/shift_scale_x)  # x1
            boxes_xyxy[:, 1] *= (1.0/shift_scale_y)  # y1
            boxes_xyxy[:, 2] *= (1.0/shift_scale_x)  # x2
            boxes_xyxy[:, 3] *= (1.0/shift_scale_y)  # y2

            boxes_data[:, :4] = boxes_xyxy
            all_boxes_data.append(boxes_data)

        if all_boxes_data:
            roied_boxes_data = torch.cat(all_boxes_data, dim=0)
        else:
            roied_boxes_data = None

        oriimg = np.array(img)
        if roied_boxes_data is not None:
            result_roied.append(Results(oriimg, path=img_name, names=self.model.names, boxes=roied_boxes_data))

        return result_roied
    def recover_Roi_nofilled(self, it_roied, img, shift_params,img_name):
        result_roied = []
        all_boxes_data = []

        for slice_idx, result in enumerate(it_roied):
            boxes_data = result.boxes.data.clone()
            boxes_xyxy = boxes_data[:, :4].clone()

            # 对xyxy坐标进行偏移
            shift_x = shift_params[0][0]
            shift_y = shift_params[0][1]
            shift_scale_x = shift_params[1][0]
            shift_scale_y = shift_params[1][1]
            ##scale如果有比例缩放，除以还原比例
            boxes_xyxy[:, 0] *= (1.0/shift_scale_x)  # x1
            boxes_xyxy[:, 1] *= (1.0/shift_scale_y)  # y1
            boxes_xyxy[:, 2] *= (1.0/shift_scale_x)  # x2
            boxes_xyxy[:, 3] *= (1.0/shift_scale_y)  # y2
            boxes_xyxy[:, 0] += shift_x  # x1
            boxes_xyxy[:, 1] += shift_y  # y1
            boxes_xyxy[:, 2] += shift_x  # x2
            boxes_xyxy[:, 3] += shift_y  # y2
            boxes_data[:, :4] = boxes_xyxy
            all_boxes_data.append(boxes_data)

        if all_boxes_data:
            roied_boxes_data = torch.cat(all_boxes_data, dim=0)
        else:
            roied_boxes_data = None

        oriimg = np.array(img)
        if roied_boxes_data is not None:
            result_roied.append(Results(oriimg, path=img_name, names=self.model.names, boxes=roied_boxes_data))

        return result_roied

    def roi_result_intersect(self, it_roied, img, roi_scaled, img_name):
        result_roied = []
        all_boxes_data = []
        # 提取ROI的坐标
        x1, y1, x2, y2 = roi_scaled
        for slice_idx, result in enumerate(it_roied):
            boxes_data = result.boxes.data.clone()
            boxes_xyxy = boxes_data[:, :4].clone()  # 提取前四列坐标 (x1, y1, x2, y2)
            scores_and_classes = boxes_data[:, 4:]  # 提取置信度和类别数据

            # 存储有效的检测框
            valid_boxes = []
            valid_scores_and_classes = []

            # 计算交集与ROI的交集部分
            for i in range(len(boxes_xyxy)):
                # 提取检测框的坐标
                det_x1, det_y1, det_x2, det_y2 = boxes_xyxy[i]

                # 计算交集区域
                intersect_x1 = max(det_x1, x1)
                intersect_y1 = max(det_y1, y1)
                intersect_x2 = min(det_x2, x2)
                intersect_y2 = min(det_y2, y2)

                # 如果交集区域有效，则保留这个检测框
                if intersect_x1 < intersect_x2 and intersect_y1 < intersect_y2:
                    # 更新检测框为交集部分
                    valid_boxes.append(torch.tensor([intersect_x1, intersect_y1, intersect_x2, intersect_y2]))
                    valid_scores_and_classes.append(scores_and_classes[i])  # 保留对应的置信度和类别

            # 如果有有效的检测框，更新 boxes_data
            if valid_boxes:
                valid_boxes = torch.stack(valid_boxes)
                valid_scores_and_classes = torch.stack(valid_scores_and_classes)
                # 确保 valid_boxes 和 valid_scores_and_classes 在同一设备上
                device = valid_scores_and_classes.device  # 获取 valid_boxes 所在设备
                valid_boxes= valid_boxes.to(device)  # 将 valid_scores_and_classes 转移到 valid_boxes 所在设备

                # 将有效的框坐标与对应的置信度、类别结合
                valid_boxes_data = torch.cat([valid_boxes, valid_scores_and_classes], dim=1)

                all_boxes_data.append(valid_boxes_data)

        # 合并所有有效的检测框
        if all_boxes_data:
            roied_boxes_data = torch.cat(all_boxes_data, dim=0)
        else:
            roied_boxes_data = None

        # 将图像转换为 NumPy 数组
        oriimg = np.array(img)

        # 如果有有效的检测框，保存到结果中
        if roied_boxes_data is not None:
            result_roied.append(Results(oriimg, path=img_name, names=self.model.names, boxes=roied_boxes_data))
        # 合并所有有效的检测框
        # roied_boxes_data = torch.cat(all_boxes_data, dim=0)
        # # 将图像转换为 NumPy 数组
        # oriimg = np.array(img)
        # # 如果有有效的检测框，保存到结果中
        # result_roied.append(Results(oriimg, path=img_name, names=self.model.names, boxes=roied_boxes_data))

        return result_roied
    def recover_Roi_intersect(self, it_roied, img, shift_params,img_name):
        result_roied = []
        all_boxes_data = []

        for slice_idx, result in enumerate(it_roied):
            boxes_data = result.boxes.data.clone()
            boxes_xyxy = boxes_data[:, :4].clone()

            # 对xyxy坐标进行偏移
            shift_scale_x = shift_params[0][0]
            shift_scale_y = shift_params[0][1]
            ##scale如果有比例缩放，除以还原比例
            boxes_xyxy[:, 0] *= (1.0/shift_scale_x)  # x1
            boxes_xyxy[:, 1] *= (1.0/shift_scale_y)  # y1
            boxes_xyxy[:, 2] *= (1.0/shift_scale_x)  # x2
            boxes_xyxy[:, 3] *= (1.0/shift_scale_y)  # y2
            boxes_data[:, :4] = boxes_xyxy
            all_boxes_data.append(boxes_data)

        if all_boxes_data:
            roied_boxes_data = torch.cat(all_boxes_data, dim=0)
        else:
            roied_boxes_data = None

        oriimg = np.array(img)
        if roied_boxes_data is not None:
            result_roied.append(Results(oriimg, path=img_name, names=self.model.names, boxes=roied_boxes_data))

        return result_roied

    # def predict_sahi(self):
    #     for filename in os.listdir(self.file_pathname):
    #         if filename.split('.')[-1] != 'txt':
    #             image_path = os.path.join(self.file_pathname, filename)
    #             with Image.open(image_path) as img:
    #                 sliced_images_one = self.sahi.predict_slice_oneimg(img)
    #                 result = self.model.predict(sliced_images_one, batch=self.inferbatch, imgsz=self.inferimgsz,
    #                                             device=self.inferdevicehandle)
    #                 merged_result = self.merge_slices(result, img, self.sahi.slice_regions, img_name=filename)
    #                 it_sliceed = self.process_detections_nms(merged_result, img)
    #                 self.predictions.append(it_sliceed)
    #
    #     self.save_results()
    #
    # def predict_oriimg(self):
    #     for filename in os.listdir(self.file_pathname):
    #         if filename.split('.')[-1] != 'txt':
    #             image_path = os.path.join(self.file_pathname, filename)
    #             with Image.open(image_path) as img:
    #                 result = self.model.predict(img, batch=self.inferbatch, imgsz=self.inferimgsz,
    #                                             device=self.inferdevicehandle)
    #                 self.predictions.append(result)
    #     self.save_results()

    # def predict_sahi(self,img,filename):
    #
    #     sliced_images_one = self.sahi.predict_slice_oneimg(img)
    #     result = self.model.predict(sliced_images_one, batch=self.inferbatch, imgsz=self.inferimgsz,
    #                                 device=self.inferdevicehandle)
    #     merged_result = self.merge_slices(result, img, self.sahi.slice_regions, img_name=filename)
    #     it_sliceed = self.process_detections_nms(merged_result, img)
    #     self.predictions.append(it_sliceed)
    #
    #     # self.save_results()
    def predict_sahi(self,img,filename):

        sliced_images_one = self.sahi.predict_slice_oneimg(img)
        dynamic_if=self.getmodel_inputbatch()
        if not dynamic_if and len(sliced_images_one)>1:
            result=[]
            for tt in range(0,len(sliced_images_one)):
                result_one = self.model.predict(sliced_images_one[tt], batch=self.inferbatch, imgsz=self.inferimgsz,
                                            device=self.inferdevicehandle)
                result.extend(result_one)
        else:
            result = self.model.predict(sliced_images_one, batch=self.inferbatch, imgsz=self.inferimgsz,
                                        device=self.inferdevicehandle)
        merged_result = self.merge_slices(result, img, self.sahi.slice_regions, img_name=filename)
        ###是否考虑将这nms、nmm只给切多图的，即len(sliced_images_one)>1，因为普通的可能无需后续操作###
        it_sliceed = self.process_detections_nms(merged_result, img)
        it_sliceed = self.process_detections_with_nmm(it_sliceed, img)
        ###是否考虑将这nms、nmm只给切多图的，即len(sliced_images_one)>1，因为普通的可能无需后续操作###
        self.predictions.append(it_sliceed)

        # self.save_results()

    def predict_oriimg(self,img):
        # 获取图像的宽度和高度
        img_width, img_height = img.size
        # 计算使用的图像尺寸
        effective_imgsz = self.inferimgsz
        if effective_imgsz >= img_width or effective_imgsz>= img_height:
            effective_imgsz = (img_width, img_height)
        else:
            effective_imgsz = (self.inferimgsz, self.inferimgsz)

        # 调用预测
        result = self.model.predict(img, batch=self.inferbatch, imgsz=effective_imgsz,
                                    device=self.inferdevicehandle)
        self.predictions.append(result)
        # result = self.model.predict(img, batch=self.inferbatch, imgsz=self.inferimgsz,
        #                             device=self.inferdevicehandle)
        # self.predictions.append(result)
        # # self.save_results()

    def predict_oriimg_noshai(self,img):
        # 调用预测
        result = self.model.predict(img, batch=self.inferbatch, imgsz=self.inferimgsz,
                                    device=self.inferdevicehandle)
        self.predictions.append(result)
        # result = self.model.predict(img, batch=self.inferbatch, imgsz=self.inferimgsz,
        #                             device=self.inferdevicehandle)
        # self.predictions.append(result)
        # # self.save_results()


    def predict_sahi_roi(self,img,filename,roi):
        self.sahiROI = HSAHI_det(slice_width=roi[2],
                              slice_height=roi[3],
                              overlap_width_ratio=0,
                              overlap_height_ratio=0,
                              roi=roi)
        sliced_images_one = self.sahiROI.predict_slice_oneimg(img)
        dynamic_if=self.getmodel_inputbatch()
        if not dynamic_if and len(sliced_images_one)>1:
            result=[]
            for tt in range(0,len(sliced_images_one)):
                result_one = self.model.predict(sliced_images_one[tt], batch=self.inferbatch, imgsz=self.inferimgsz,
                                            device=self.inferdevicehandle)
                result.extend(result_one)
        else:
            result = self.model.predict(sliced_images_one, batch=self.inferbatch, imgsz=self.inferimgsz,
                                        device=self.inferdevicehandle)
        merged_result = self.merge_slices(result, img, self.sahiROI.slice_regions, img_name=filename)
        ###是否考虑将这nms、nmm只给切多图的，即len(sliced_images_one)>1，因为普通的可能无需后续操作###
        it_sliceed = self.process_detections_nms(merged_result, img)
        it_sliceed = self.process_detections_with_nmm(it_sliceed, img)
        ###是否考虑将这nms、nmm只给切多图的，即len(sliced_images_one)>1，因为普通的可能无需后续操作###
        self.predictions.append(it_sliceed)

        # self.save_results()

    def predict_oriimg_roi_filled(self,img,filename,roi):
        # 确保图像是 RGB 模式
        if img.mode != "RGB":
            img = img.convert("RGB")
        # 转换 PIL 图像为 NumPy 数组
        img_np = np.array(img)
        # 提取 ROI 坐标
        x1, y1, x2, y2 = roi
        # 处理图像，将 ROI 外的部分填充为 0 值
        masked_img = np.zeros_like(img_np)  # 创建与 img 同大小的全 0 图像
        masked_img[y1:y2, x1:x2] = img_np[y1:y2, x1:x2]  # 仅保留 ROI 区域的像素值
        #shift-params计算
        shift_params=[]
        shift_params.append(roi)
        #只有roi，没有resize，比例则为1
        shift_params.append([1,1])
        # 调用预测
        result = self.model.predict(masked_img, batch=self.inferbatch, imgsz=self.inferimgsz,
                                    device=self.inferdevicehandle)
        #对结果做偏移(针对是边缘填充的)
        roied_result = self.recover_Roi_filled(result, img, shift_params, img_name=filename)
        ###是否考虑将这nms、nmm只给切多图的，即len(sliced_images_one)>1，因为普通的可能无需后续操作###
        it_roied = self.process_detections_nms(roied_result, img)
        it_roied = self.process_detections_with_nmm(it_roied, img)
        ###是否考虑将这nms、nmm只给切多图的，即len(sliced_images_one)>1，因为普通的可能无需后续操作###
        self.predictions.append(it_roied)

    # def predict_oriimg_resize_before_roi(self,img,filename,resize_imgsize,roi):
    #     # 确保图像是 RGB 模式
    #     if img.mode != "RGB":
    #         img = img.convert("RGB")
    #     # 调整图像大小为 1024x1024
    #     width,height=img.size
    #
    #     resized_img = img.resize((resize_imgsize[0], resize_imgsize[1]), Image.Resampling.LANCZOS)
    #     # 转换 PIL 图像为 NumPy 数组
    #     img_np = np.array(resized_img)
    #     # 提取 ROI 坐标
    #     x1, y1, x2, y2 = roi
    #     scale_roi_x=resize_imgsize[0]/width
    #     scale_roi_y=resize_imgsize[1]/height
    #     roi_x1=int(x1*scale_roi_x+0.5)
    #     roi_x2=int(x2*scale_roi_x+0.5)
    #     roi_y1=int(y1*scale_roi_y+0.5)
    #     roi_y2=int(y2*scale_roi_y+0.5)
    #     # 处理图像，将 ROI 外的部分填充为 0 值
    #     masked_img = np.zeros_like(img_np)  # 创建与 img 同大小的全 0 图像
    #     masked_img[roi_y1:roi_y2, roi_x1:roi_x2] = img_np[roi_y1:roi_y2, roi_x1:roi_x2]  # 仅保留 ROI 区域的像素值
    #     #shift-params计算
    #     scaled_roi=[roi_x1, roi_y1, roi_x2, roi_y2]
    #     shift_params=[]
    #     shift_params.append(scaled_roi)
    #     #只有roi，没有resize，比例则为1
    #     shift_params.append([scale_roi_x,scale_roi_y])
    #     # 调用预测
    #     result = self.model.predict(masked_img, batch=self.inferbatch, imgsz=self.inferimgsz,
    #                                 device=self.inferdevicehandle)
    #     #对结果做偏移(针对是边缘填充的)
    #     roied_result = self.recover_Roi_filled(result, img, shift_params, img_name=filename)
    #     ###是否考虑将这nms、nmm只给切多图的，即len(sliced_images_one)>1，因为普通的可能无需后续操作###
    #     it_roied = self.process_detections_nms(roied_result, img)
    #     it_roied = self.process_detections_with_nmm(it_roied, img)
    #     ###是否考虑将这nms、nmm只给切多图的，即len(sliced_images_one)>1，因为普通的可能无需后续操作###
    #     self.predictions.append(it_roied)
    def predict_oriimg_resize_before_roi(self,img,filename,resize_imgsize,roi,mode):
        # 确保图像是 RGB 模式
        if img.mode != "RGB":
            img = img.convert("RGB")
        # 调整图像大小为 1024x1024
        width,height=img.size
        if mode:
            resized_img = img.resize((resize_imgsize[0], resize_imgsize[1]), Image.Resampling.LANCZOS)
            # 转换 PIL 图像为 NumPy 数组
            img_np = np.array(resized_img)
            # 提取 ROI 坐标
            x1, y1, x2, y2 = roi
            scale_roi_x=resize_imgsize[0]/width
            scale_roi_y=resize_imgsize[1]/height
            roi_x1=int(x1*scale_roi_x+0.5)
            roi_x2=int(x2*scale_roi_x+0.5)
            roi_y1=int(y1*scale_roi_y+0.5)
            roi_y2=int(y2*scale_roi_y+0.5)
            # 处理图像，将 ROI 外的部分填充为 0 值
            masked_img = np.zeros_like(img_np)  # 创建与 img 同大小的全 0 图像
            masked_img[roi_y1:roi_y2, roi_x1:roi_x2] = img_np[roi_y1:roi_y2, roi_x1:roi_x2]  # 仅保留 ROI 区域的像素值
            #shift-params计算
            scaled_roi=[roi_x1, roi_y1, roi_x2, roi_y2]
            shift_params=[]
            shift_params.append(scaled_roi)
            #只有roi，没有resize，比例则为1
            shift_params.append([scale_roi_x,scale_roi_y])
            # 调用预测
            result = self.model.predict(masked_img, batch=self.inferbatch, imgsz=self.inferimgsz,
                                        device=self.inferdevicehandle)
            #对结果做偏移(针对是边缘填充的)
            roied_result = self.recover_Roi_filled(result, img, shift_params, img_name=filename)
            ###是否考虑将这nms、nmm只给切多图的，即len(sliced_images_one)>1，因为普通的可能无需后续操作###
            it_roied = self.process_detections_nms(roied_result, img)
            it_roied = self.process_detections_with_nmm(it_roied, img)
            ###是否考虑将这nms、nmm只给切多图的，即len(sliced_images_one)>1，因为普通的可能无需后续操作###
            self.predictions.append(it_roied)
        else:
            # 转换 PIL 图像为 NumPy 数组
            img_np = np.array(img)
            # 提取 ROI 坐标
            x1, y1, x2, y2 = roi
            x1 = max(0, min(x1, width - 1))
            x2 = max(0, min(x2, width - 1))
            y1 = max(0, min(y1, height - 1))
            y2 = max(0, min(y2, height - 1))
            # 裁剪图像到 ROI 区域
            roi_img = img.crop((x1, y1, x2, y2))  # 裁剪 ROI 区域
            longer_l=max((x2-x1),(y2-y1))
            scale_roi_x=resize_imgsize[0]/ longer_l
            scale_roi_y = resize_imgsize[1] / longer_l
            resized_roiw=int(((x2-x1)*scale_roi_x)+0.5)
            resized_roih=int(((y2-y1)*scale_roi_y)+0.5)
            resized_img=roi_img.resize((resized_roiw, resized_roih), Image.Resampling.LANCZOS)

            # shift-params计算
            scaled_roi = [x1, y1, x2, y2]
            shift_params = []
            shift_params.append(scaled_roi)
            # 比例
            shift_params.append([scale_roi_x, scale_roi_y])
            # 调用预测
            result = self.model.predict(resized_img, batch=self.inferbatch, imgsz=self.inferimgsz,
                                        device=self.inferdevicehandle)
            # 对结果做偏移(针对是边缘填充的)
            roied_result = self.recover_Roi_nofilled(result, img, shift_params, img_name=filename)
            ###是否考虑将这nms、nmm只给切多图的，即len(sliced_images_one)>1，因为普通的可能无需后续操作###
            it_roied = self.process_detections_nms(roied_result, img)
            it_roied = self.process_detections_with_nmm(it_roied, img)
            ###是否考虑将这nms、nmm只给切多图的，即len(sliced_images_one)>1，因为普通的可能无需后续操作###
            self.predictions.append(it_roied)
    # region PIL版predict_resizeimg_then_roi
    # def predict_resizeimg_then_roi(self,img,filename,resize_imgsize,roi):
    #     # 确保图像是 RGB 模式
    #     if img.mode != "RGB":
    #         img = img.convert("RGB")
    #     # 调整图像大小为 1024x1024
    #     width,height=img.size
    #
    #     resized_img = img.resize((resize_imgsize[0], resize_imgsize[1]), Image.Resampling.BILINEAR)
    #     # 转换 PIL 图像为 NumPy 数组
    #     img_np = np.array(resized_img)
    #     # 提取 ROI 坐标
    #     x1, y1, x2, y2 = roi
    #     scale_roi_x = resize_imgsize[0] / width
    #     scale_roi_y = resize_imgsize[1] / height
    #     roi_x1 = int(x1 * scale_roi_x + 0.5)
    #     roi_x2 = int(x2 * scale_roi_x + 0.5)
    #     roi_y1 = int(y1 * scale_roi_y + 0.5)
    #     roi_y2 = int(y2 * scale_roi_y + 0.5)
    #     scaled_roi = [roi_x1, roi_y1, roi_x2, roi_y2]
    #     # shift-params计算
    #     shift_params = []
    #     shift_params.append([scale_roi_x, scale_roi_y])
    #     # 调用预测
    #     result = self.model.predict(img_np, batch=self.inferbatch, imgsz=self.inferimgsz,
    #                                 device=self.inferdevicehandle)
    #     #对结果做偏移(针对是边缘填充的)
    #     roiinter_result = self.roi_result_intersect(result, img, scaled_roi, img_name=filename)
    #     roied_result = self.recover_Roi_intersect(roiinter_result, img, shift_params, img_name=filename)
    #     ###是否考虑将这nms、nmm只给切多图的，即len(sliced_images_one)>1，因为普通的可能无需后续操作###
    #     it_roied = self.process_detections_nms(roied_result, img)
    #     it_roied = self.process_detections_with_nmm(it_roied, img)
    #     ###是否考虑将这nms、nmm只给切多图的，即len(sliced_images_one)>1，因为普通的可能无需后续操作###
    #     self.predictions.append(it_roied)
    # endregion
    # region opencv版predict_resizeimg_then_roi
    def predict_resizeimg_then_roi(self, img, filename, resize_imgsize, roi):
        # 将 PIL 图像转换为 NumPy 数组
        img_np = np.array(img)

        # 确保图像是 RGB 模式，如果是其他模式先转换为 RGB
        if img.mode != "RGB":
            img = img.convert("RGB")
            img_np = np.array(img)

        # 获取原图的宽高
        height, width, _ = img_np.shape

        # 使用 OpenCV 的 resize 调整图像大小
        resized_img = cv2.resize(img_np, (resize_imgsize[0], resize_imgsize[1]), interpolation=cv2.INTER_LINEAR)

        # 提取 ROI 坐标
        x1, y1, x2, y2 = roi
        scale_roi_x = resize_imgsize[0] / width
        scale_roi_y = resize_imgsize[1] / height
        roi_x1 = int(x1 * scale_roi_x + 0.5)
        roi_x2 = int(x2 * scale_roi_x + 0.5)
        roi_y1 = int(y1 * scale_roi_y + 0.5)
        roi_y2 = int(y2 * scale_roi_y + 0.5)
        scaled_roi = [roi_x1, roi_y1, roi_x2, roi_y2]

        # shift-params计算
        shift_params = []
        shift_params.append([scale_roi_x, scale_roi_y])

        # 调用预测
        result = self.model.predict(resized_img, batch=self.inferbatch, imgsz=self.inferimgsz,
                                    device=self.inferdevicehandle)

        # 对结果做偏移（针对是边缘填充的）
        roiinter_result = self.roi_result_intersect(result, img, scaled_roi, img_name=filename)
        roied_result = self.recover_Roi_intersect(roiinter_result, img, shift_params, img_name=filename)

        # 是否考虑将这些 NMS 和 NMM 只给切割的多图操作
        it_roied = self.process_detections_nms(roied_result, img)
        it_roied = self.process_detections_with_nmm(it_roied, img)

        # 将结果保存到 predictions 中
        self.predictions.append(it_roied)
    # endregion
    def getmodel_inputbatch(self):
        ####判断输入batch是多少，然后确定每次训练个数###
        ###判断模型格式
        from ultralytics.nn.autobackend import AutoBackend
        ws = str(self.model.model[0] if isinstance(self.model.model, list) else self.model.model)
        nn_module = isinstance(ws, torch.nn.Module)
        (
            pt,
            jit,
            onnx,
            xml,
            engine,
            coreml,
            saved_model,
            pb,
            tflite,
            edgetpu,
            tfjs,
            paddle,
            ncnn,
            triton,
        ) = AutoBackend._model_type(ws)
        ###获取pt模型batch
        from ultralytics.nn.tasks import DetectionModel
        if  isinstance(self.model.model,DetectionModel):
            ifdynamic = True
        ###获取onnx模型batch
        if onnx:
            import onnxruntime
            providers = ["CUDAExecutionProvider", "CPUExecutionProvider"]
            session = onnxruntime.InferenceSession(ws, providers=providers)
            onnx_input_batch=session.get_inputs()[0].shape[0]##'batch'/1
            if onnx_input_batch=='batch':
                ifdynamic=True
            elif onnx_input_batch==1:
                ifdynamic=False
        ###获取openvino模型batch
        if xml:
            import openvino as ov
            from pathlib import Path
            w = Path(ws)
            if not w.is_file():  # if not *.xml
                w = next(w.glob("*.xml"))
            core = ov.Core()
            ov_model = core.read_model(model=str(w), weights=w.with_suffix(".bin"))
            ov_dynamic_batch = ov_model.dynamic##true/false
            ifdynamic=ov_dynamic_batch
        ###继续写，debug DoAi.py，定位到openvino的获取，json文件"infermodeldir"那个路径，train7为onnx dynamic=false，
        ####train8 为onnx dynamic=true，train9 为openvino dynamic=true ，train10为openvino dynamic=false
        ####判断输入batch是多少，然后确定每次训练个数###
        ###最后给出ifdynamic
        return  ifdynamic
    def save_results(self):
        original_filenames=os.listdir(self.file_pathname)
        for j, result in enumerate(self.predictions):
            # 获取原图的文件名
            original_filename = original_filenames[j] if j < len(original_filenames) else f"result_{j}"

            if isinstance(result, list):
                for res in result:
                    ann = res.plot()
                    if not os.path.exists(self.cur_path):
                        os.mkdir(self.cur_path)
                    # 根据原图文件名加后缀命名
                    output_filename = f"{os.path.splitext(original_filename)[0]}_result_{j}.jpg"
                    cv2.imwrite(os.path.join(self.cur_path, output_filename), ann)
            else:
                ann = result.plot()
                if not os.path.exists(self.cur_path):
                    os.mkdir(self.cur_path)
                # 根据原图文件名加后缀命名
                output_filename = f"{os.path.splitext(original_filename)[0]}_result_{j}.jpg"
                cv2.imwrite(os.path.join(self.cur_path, output_filename), ann)
    def save_results_oneout(self,test_image_paths):
        original_filenames=self.nooverlap_imgnames(test_image_paths)
        # original_filenames=os.listdir(self.file_pathname)
        for j, result in enumerate(self.predictions):
            # 获取原图的文件名
            original_filename = original_filenames[j] if j < len(original_filenames) else f"result_{j}"

            if isinstance(result, list):
                for res in result:
                    ann = res.plot()
                    if not os.path.exists(self.cur_path):
                        os.mkdir(self.cur_path)
                    # 根据原图文件名加后缀命名
                    output_filename = f"{os.path.splitext(original_filename)[0]}_result_{j}.jpg"
                    cv2.imwrite(os.path.join(self.cur_path, output_filename), ann)
            else:
                ann = result.plot()
                if not os.path.exists(self.cur_path):
                    os.mkdir(self.cur_path)
                # 根据原图文件名加后缀命名
                output_filename = f"{os.path.splitext(original_filename)[0]}_result_{j}.jpg"
                cv2.imwrite(os.path.join(self.cur_path, output_filename), ann)
        print(f"检测结果图已保存到：{self.cur_path}")
    def save_results_mulout(self,test_image_paths,non_common_files):
        for j, result in enumerate(self.predictions):
            # 获取原图的文件名
            original_filename = os.path.basename(test_image_paths[j]) if j < len(test_image_paths) else f"result_{j}"

            if isinstance(result, list):
                for res in result:
                    ann = res.plot()
                    if not os.path.exists(self.cur_path):
                        os.mkdir(self.cur_path)
                    # 根据原图文件名加后缀命名
                    output_filename = f"{os.path.splitext(original_filename)[0]}_result_{j}.jpg"
                    # 拼接保存路径
                    save_path = os.path.join(self.cur_path, os.path.dirname(non_common_files[j]))
                    # 确保保存路径存在
                    if not os.path.exists(save_path):
                        os.makedirs(save_path)
                    cv2.imwrite(os.path.join(save_path, output_filename), ann)
            else:
                ann = result.plot()
                if not os.path.exists(self.cur_path):
                    os.mkdir(self.cur_path)
                # 根据原图文件名加后缀命名
                output_filename = f"{os.path.splitext(original_filename)[0]}_result_{j}.jpg"
                # 拼接保存路径
                save_path = os.path.join(self.cur_path, os.path.dirname(non_common_files[j]))
                # 确保保存路径存在
                if not os.path.exists(save_path):
                    os.makedirs(save_path)
                cv2.imwrite(os.path.join(save_path, output_filename), ann)
        print(f"检测结果图已保存到：{self.cur_path}")
    # def predict_based_on_size(self):
    #     for filename in os.listdir(self.file_pathname):
    #         if filename.split('.')[-1] != 'txt':
    #             image_path = os.path.join(self.file_pathname, filename)
    #             with Image.open(image_path) as img:
    #                 width, height = img.size
    #                 # 判断图像大小
    #                 if width > self.trueimgsize[0] and height > self.trueimgsize[1]:
    #                     self.predict_sahi()
    #                 else:
    #                     self.predict_oriimg()
    def predict_sahiauto(self):
        for filename in os.listdir(self.file_pathname):
            if filename.split('.')[-1] != 'txt':
                image_path = os.path.join(self.file_pathname, filename)
                with Image.open(image_path) as img:
                    sliced_images_one = self.sahi.predict_slice_oneimg(img)
                    result = self.model.predict(sliced_images_one, batch=self.inferbatch, imgsz=self.inferimgsz,
                                                device=self.inferdevicehandle)
                    merged_result = self.merge_slices(result, img, self.sahi.slice_regions, img_name=filename)
                    it_sliceed = self.process_detections_nms(merged_result, img)
                    it_sliceed = self.process_detections_with_nmm(it_sliceed, img)
                    self.predictions.append(it_sliceed)

        self.save_results()
    # ###原版predict_based_on_size
    # def predict_based_on_size(self):
    #     for filename in os.listdir(self.file_pathname):
    #         if filename.split('.')[-1] != 'txt':
    #             image_path = os.path.join(self.file_pathname, filename)
    #             with Image.open(image_path) as img:
    #                 width, height = img.size
    #                 # 判断图像大小
    #                 if width > self.trueimgsize[0] or height > self.trueimgsize[1]:
    #                     self.predict_sahi(img,filename)
    #                 else:
    #                     self.predict_oriimg(img)
    #     self.save_results()
    ###重写predict_based_on_size，通过yaml里面的test路径读取图片
    def predict_based_on_size(self,yaml_datadir=None):
        if yaml_datadir:
            import  yaml
            with open(yaml_datadir, 'r', encoding='utf-8') as file:
                config = yaml.safe_load(file)
            if 'test' not in config or not config['test']:
                raise ValueError("'test' key is missing or its value is empty in the YAML file.Please remake mydata.yaml")
            test_txt_path = config['test']
            test_image_paths = [line.strip() for line in open(test_txt_path, 'r')]
        else:
            # test_image_paths=os.listdir(self.file_pathname)
            #对于一个文件夹里面好多分支，就不能简单使用os.listdir，而使用下面的
            test_image_paths=self.list_all_images_in_path(self.file_pathname)
        imgcommon_path=self.find_common_path(test_image_paths)
        image_id_dict=1
        non_common_files=[]
        for image_path in test_image_paths:
            # 标准化路径分隔符为 `/`
            standardized_path = "/".join(re.split(r"[\\/]", image_path))
            # 标准化公共路径分隔符为 `/`
            standardized_common_path = "/".join(re.split(r"[\\/]", imgcommon_path))

            # 获取非公共部分路径
            if standardized_path.startswith(standardized_common_path):
                non_common_part = standardized_path[len(standardized_common_path):].lstrip("/")
            else:
                non_common_part = standardized_path  # 如果路径不包含公共部分，直接使用原路径
            #读取尾缀为图片格式的图像
            filename=os.path.basename(image_path)
            imgfile_extension=(os.path.basename(filename).split('.')[-1]).lower()
            if imgfile_extension in {'jpg', 'jpeg', 'png', 'bmp', 'gif', 'tiff', 'webp'}:
                # image_path = os.path.join(self.file_pathname, filename)
                with Image.open(image_path) as img:
                    width, height = img.size
                    # 判断图像大小
                    if self.sahiinfer:
                        # if self.sahi_roi:
                        #     self.predict_sahi_roi(img, filename,self.sahi_roi)
                        if self.roi:
                            self.predict_sahi_roi(img, filename,self.roi)
                        else:
                            if width > self.trueimgsize[0] or height > self.trueimgsize[1]:
                                self.predict_sahi(img,filename)
                            else:
                                self.predict_oriimg(img)
                    else:
                        if self.roi:
                            # # if self.resize_before_roi:
                            # #     self.predict_oriimg_resize_before_roi(img,filename,self.trueimgsize,self.roi,self.roi_padding)
                            # # else:
                            # #     if self.roi_padding:
                            # #         self.predict_oriimg_roi_filled(img,filename, self.roi)
                            # #     else:
                            # #         self.predict_oriimg_resize_before_roi(img, filename, self.trueimgsize, self.roi,
                            # #                                               self.roi_padding)
                            if self.ifroiimg:
                                self.predict_oriimg_resize_before_roi(img, filename, self.trueimgsize, self.roi,
                                                                      self.roi_padding)
                            else:
                                self.predict_resizeimg_then_roi(img, filename, self.trueimgsize, self.roi)
                        else:
                            self.predict_oriimg_noshai(img)
                    self.result_dict.append([self.predictions[image_id_dict-1],image_id_dict,non_common_part])
                    image_id_dict+=1
                    non_common_files.append(non_common_part)
        if self.auto_label:
            self.auto_labelit(imgcommon_path)
        ##考虑是否存在图片路径完全没有公共部分的！！！！
        if self.inferedimg_onedir:
            self.save_results_oneout(test_image_paths)
        else:
            self.save_results_mulout(test_image_paths,non_common_files)
    def auto_labelit(self,common_image_dir):
        # 存储JSON结果的列表
        file_pathnames=common_image_dir+"\\"
        json_results = {
            "class_ids": list(self.model.names.keys()),
            "class_names": list(self.model.names.values()),
            "image_dir": file_pathnames.replace("\\", "/"),
            "samples": []
        }
        for result,imageid_dict,filename_label in self.result_dict:
            # 提取并存储到JSON结果
            json_results["samples"].extend(self.extract_predictions(result, imageid_dict, filename_label))
        ##没有文件夹创建
        if not os.path.exists(self.resultjson_path):
            os.makedirs(self.resultjson_path)
        ##判断输出是哪种（hdict/json）
        if self.resultjson_filetype=='json':
            json_path = os.path.join(self.resultjson_path, 'predictions.json')
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(json_results, f, ensure_ascii=False, indent=4)
        elif self.resultjson_filetype=='hdict':
            # 初始化 HALCON 环境
            if self.import_HALCONdll:
                self.setup_halcon_environment()
            import halcon as ha
            hdict_path = os.path.join(self.resultjson_path, 'predictions.hdict')
            Dict_ori = ha.from_python_dict(json_results)
            ha.write_dict(Dict_ori, hdict_path, [], [])
            print(f"检测标注hdict已成功导出到：{hdict_path}")

    def setup_halcon_environment(self):
        """
        设置 HALCON 运行环境，包括动态加载 DLL 和许可证检查。
        """
        # 获取当前脚本路径
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # DLL 文件夹路径（假设 DLL 文件夹在脚本的上一级目录）
        dll_path = os.path.join(os.path.dirname(current_dir), 'dll')

        # 动态添加 DLL 路径到 PATH 环境变量
        if dll_path not in os.environ['PATH']:
            os.environ['PATH'] = dll_path + os.pathsep + os.environ['PATH']

        # 手动加载 HALCON 主 DLL，确保动态库可用
        try:
            ctypes.windll.LoadLibrary(os.path.join(dll_path, "halcon.dll"))  # 替换为实际 DLL 文件名
            print("HALCON DLL 加载成功")
        except Exception as e:
            print(f"HALCON DLL 加载失败: {e}")
            sys.exit(1)  # 退出脚本，提示用户检查 DLL 配置

    def extract_predictions(self, result, image_id, image_file_name):
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

    def list_all_images_in_path(self,base_path):
        # 定义支持的图片格式
        valid_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.gif')

        # 存储所有图片路径的列表
        all_image_paths = []

        # 遍历 base_path 目录及其子目录
        for root, dirs, files in os.walk(base_path):
            for file in files:
                # 检查文件扩展名是否为支持的图片格式
                if file.lower().endswith(valid_extensions):
                    # 构造完整文件路径
                    full_path = os.path.join(root, file)
                    all_image_paths.append(full_path)

        return all_image_paths
    def find_common_path(self,lines):
        # 分解每个路径为列表
        split_paths = [re.split(r"[\\/]", line) for line in lines]
        # 寻找公共部分
        common_parts = []
        for parts in zip(*split_paths):
            if all(part == parts[0] for part in parts):
                common_parts.append(parts[0])
            else:
                break
        # 拼接公共路径
        common_path = "\\".join(common_parts)
        return common_path

    def nooverlap_imgnames(self,test_image_paths):
        # 创建一个字典存储文件名和对应的路径信息
        name_to_path = {}
        final_names = []

        for image_path in test_image_paths:
            # 获取路径的各级部分
            path_parts = re.split(r"[\\/]", image_path.strip())
            # 最底层文件名
            current_name = path_parts[-1]
            # 检查文件名是否唯一
            temp_name = current_name
            index = -2  # 从倒数第二级目录开始
            while temp_name in name_to_path:
                # 如果重复，向前取上一级目录并加上前缀
                if abs(index) > len(path_parts):
                    raise ValueError(f"Cannot generate a unique name for: {image_path}")
                temp_name = f"{path_parts[index]}_{current_name}"
                index -= 1
            # 记录最终唯一名字
            name_to_path[temp_name] = image_path
            final_names.append(temp_name)

        # 返回图片名称列表，顺序与原列表一致
        return final_names
    # def save_results(self):
    #     for j, result in enumerate(self.predictions):
    #         if isinstance(result, list):
    #             for res in result:
    #                 ann = res.plot()
    #                 if not os.path.exists(self.cur_path):
    #                     os.mkdir(self.cur_path)
    #                 cv2.imwrite(os.path.join(self.cur_path, f"out{j}.jpg"), ann)
    #         else:
    #             ann = result.plot()
    #             if not os.path.exists(self.cur_path):
    #                 os.mkdir(self.cur_path)
    #             cv2.imwrite(os.path.join(self.cur_path, f"out{j}.jpg"), ann)

# 使用示例
# predictor = PredictSahi_yolo(
#     model_path=r"E:\ALLvision\pycharmproject\Efficientnet\segjjc_clsseg_try\sahi_preprocess\1014\try\traintry\runs\detect\train3\weights\best.pt",
#     yaml_path=r'E:\ALLvision\pycharmproject\Efficientnet\segjjc_clsseg_try\sahi_preprocess\1014\try\Data_pest\mydata2\mydata.yaml',
#     file_pathname=r"E:\ALLvision\pycharmproject\Efficientnet\segjjc_clsseg_try\sahi_preprocess\1014\predicttry\imgtest",
#     cur_path=r"E:\ALLvision\pycharmproject\Efficientnet\segjjc_clsseg_try\sahi_preprocess\1014\predicttry\imgsave"
# )
#
# predictor.predict_sahi()
