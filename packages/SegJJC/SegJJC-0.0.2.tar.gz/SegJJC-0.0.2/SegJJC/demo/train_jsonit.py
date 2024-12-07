import os
import cv2
import torch
import numpy as np
from tqdm import tqdm
import json
from PIL import Image
import io
import base64
import copy
import random
import shutil
import yaml
import sys
from ultralytics import YOLO
from types import SimpleNamespace
from SegJJC.fcn import modelFCN
from SegJJC.EfficientNet import modelEfficient
from SegJJC.othermodules import HSAHI_det,PredictSahi_yolo,gen_wts,ROIT_det

def convert(size, box):
    dw = 1. / (size[0])
    dh = 1. / (size[1])
    x = (box[0] + box[1]) / 2.0 - 1
    y = (box[2] + box[3]) / 2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return x, y, w, h

def HdictDir(jsonpath, target_path, imgout_path):
    with open(jsonpath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    content = json.loads(content)
    image_dir = content.get("image_dir")
    class_names = content.get("class_names")
    new_paths_image = []
    new_paths_segment = []

    for sample in content.get("samples", []):
        image_file_name = sample.get("image_file_name")
        image_id = sample.get("image_id")

        image_saveid = image_file_name.split('/')[-1].split('.')[0]
        out_file = open(target_path + '/%s.txt' % (image_saveid), 'w')
        image_path = os.path.join(image_dir, image_file_name)

        with Image.open(image_path) as img:
            width, height = img.size
        bbox_label_ids = sample.get("bbox_label_id")
        bbox_rows1 = sample.get("bbox_row1")
        bbox_cols1 = sample.get("bbox_col1")
        bbox_rows2 = sample.get("bbox_row2")
        bbox_cols2 = sample.get("bbox_col2")

        if isinstance(bbox_label_ids, list):
            for i in range(len(bbox_label_ids)):
                bbox_label_id = bbox_label_ids[i]
                bbox_row1 = bbox_rows1[i]
                bbox_col1 = bbox_cols1[i]
                bbox_row2 = bbox_rows2[i]
                bbox_col2 = bbox_cols2[i]

                if bbox_col2 > width:
                    bbox_col2 = width
                if bbox_row2 > height:
                    bbox_row2 = height
                b = (bbox_col1, bbox_col2, bbox_row1, bbox_row2)
                bb = convert((width, height), b)
                out_file.write(str(bbox_label_id) + " " + " ".join([str(a) for a in bb]) + '\n')
        else:
            bbox_label_id = bbox_label_ids
            bbox_row1 = bbox_rows1
            bbox_col1 = bbox_cols1
            bbox_row2 = bbox_rows2
            bbox_col2 = bbox_cols2

            if bbox_col2 > width:
                bbox_col2 = width
            if bbox_row2 > height:
                bbox_row2 = height
            b = (bbox_col1, bbox_col2, bbox_row1, bbox_row2)
            bb = convert((width, height), b)
            out_file.write(str(bbox_label_id) + " " + " ".join([str(a) for a in bb]) + '\n')

        shutil.copy(image_path, imgout_path)
    return class_names

def yamlcreate(class_names, imgdiroupaths, yamlsavepath):
    names = {}
    ##########################优化部分##############################
    ##########################优化部分##############################
    ##########################优化部分##############################
    ##########################优化部分##############################
    ##########################优化部分##############################
    if isinstance(class_names,list):
        for i, class_name in enumerate(class_names):
            names[i] = class_name
            ncs=len(class_names)
    else:
        names[0]=class_names
        ncs = 1
    ##########################优化部分##############################
    ##########################优化部分##############################
    ##########################优化部分##############################
    ##########################优化部分##############################
    ##########################优化部分##############################
    traindirtxt = os.path.join(imgdiroupaths, "train.txt").replace("\\", "/")
    valdirtxt = os.path.join(imgdiroupaths, "val.txt").replace("\\", "/")
    data = {
        "train": traindirtxt,
        "val": valdirtxt,
        "names": names,
        "nc": len(class_names)
    }

    savepath = os.path.join(yamlsavepath, "mydata.yaml")
    with open(savepath, 'w', encoding='utf-8') as file:
        yaml.dump(data, file, default_flow_style=False, allow_unicode=True)
    return savepath

def split_train_val(jsonpath, txtsavepath, train_percent, trainval_percent):
    with open(jsonpath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    content = json.loads(content)
    samples = content.get("samples")
    num = len(samples)
    list_index = range(num)
    tv = int(num * trainval_percent)
    tr = int(tv * train_percent)
    trainval = random.sample(list_index, tv)
    train = random.sample(trainval, tr)

    file_trainval = open(txtsavepath + '/trainval.txt', 'w')
    file_test = open(txtsavepath + '/test.txt', 'w')
    file_train = open(txtsavepath + '/train.txt', 'w')
    file_val = open(txtsavepath + '/val.txt', 'w')

    for i in list_index:
        savename = samples[i]["image_file_name"].split('/')[-1]
        name = savename + '\n'
        if i in trainval:
            file_trainval.write(name)
            if i in train:
                file_train.write(name)
            else:
                file_val.write(name)
        else:
            file_test.write(name)

def saveimgdir(txtsavepath, imgdiroupath, imgdir_all):
    sets = ['train', 'val', 'test']
    for image_set in sets:
        image_ids = open(txtsavepath + '/%s.txt' % (image_set)).read().strip().split()
        list_file = open(imgdiroupath + '/%s.txt' % (image_set), 'w')

        for image_id in image_ids:
            list_file.write(imgdir_all + '/%s\n' % (image_id))

def halcon2yolos(params):
    alldir = params['data_alldir']
    jsonpath = params['data_jsonpath']
    if alldir is None:
        script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        default_alldir = os.path.join(script_dir, 'Data')
        if not os.path.exists(default_alldir):
            os.makedirs(default_alldir)
        alldir = default_alldir
    imgdiroupath = os.path.join(alldir, 'paper_data')
    txtsavepath = os.path.join(alldir, 'Imagesets')
    target_path = os.path.join(alldir, 'labels')
    imgout_path = os.path.join(alldir, 'images')
    imgdir_all = imgout_path.replace("\\", "/")
    if not os.path.exists(imgdiroupath):
        os.makedirs(imgdiroupath)
    if not os.path.exists(txtsavepath):
        os.makedirs(txtsavepath)
    if not os.path.exists(target_path):
        os.makedirs(target_path)
    if not os.path.exists(imgout_path):
        os.makedirs(imgout_path)
    trainval_percent = 1.0
    train_percent = 0.7
    split_train_val(jsonpath, txtsavepath, train_percent, trainval_percent)
    saveimgdir(txtsavepath, imgdiroupath, imgdir_all)
    class_names = HdictDir(jsonpath, target_path, imgout_path)
    yamldir = yamlcreate(class_names, imgdiroupath, alldir)
    return yamldir

def trainyolo(params,datadir):
    # 加载 default.yaml 文件
    from ultralytics.utils import DEFAULT_CFG,DEFAULT_CFG_DICT
    original_cfg = copy.deepcopy(DEFAULT_CFG)# 深拷贝初始配置
    original_cfg_dict=copy.deepcopy(DEFAULT_CFG_DICT)

    if (params["save_dir"]):
        ####创建训练输出子文件train####
        from ultralytics.utils.files import increment_path
        train_childdir=os.path.join(params["save_dir"],'train')
        train_dir = str(increment_path(train_childdir, exist_ok=False))
        ######
        setattr(DEFAULT_CFG,'save_dir',train_dir)
        DEFAULT_CFG_DICT['save_dir'] = train_dir
#######使用sahi预先对大图进行切图#####
#######使用sahi预先对大图进行切图#####
    if(params.get("sahi",True)):
        sahi=HSAHI_det(yaml_path=datadir,
                       slice_width=params["imgsz"],
                       slice_height=params["imgsz"],
                       overlap_height_ratio=params.get("sahi_overlapratio", 0.25),  # 使用get方法
                       overlap_width_ratio=params.get("sahi_overlapratio", 0.25),
                       sahi_datadir=params.get("sahi_datadir", None),
                       roi=params.get("roi", None))
        sahi.process_data()
        datadir=sahi.output_yaml_path
    if(params.get("roi",None)):
        RoiT=ROIT_det(yaml_path=datadir,
                      roi_datadir=params.get("roi_datadir", None),
                      roi=params.get("roi", None))
        RoiT.process_data()
        datadir=RoiT.output_yaml_path
#######使用sahi预先对大图进行切图#####
#######使用sahi预先对大图进行切图#####
    model = YOLO(params["modelpath"])
    model.train(data=datadir,
                epochs=params["epochs"],
                batch=params["batch"],
                workers=params["workers"],
                amp=params["amp"],
                imgsz=params["imgsz"],
                patience=params["patience"],
                device=params["device"],
                resume=params["resume"],
                save_period=params["save_period"],
                optimizer=params["optimizer"],
                seed=params["seed"],
                cos_lr=params["cos_lr"],
                close_mosaic=params["close_mosaic"],
                lr0=params["lr0"],
                lrf=params["lrf"],
                momentum=params["momentum"],
                weight_decay=params["weight_decay"],
                warmup_epochs=params["warmup_epochs"],
                warmup_momentum=params["warmup_momentum"],
                warmup_bias_lr=params["warmup_bias_lr"],
                box=params["box"],
                cls=params["cls"],
                dfl=params["dfl"],
                pose=params["pose"],
                kobj=params["kobj"],
                label_smoothing=params["label_smoothing"],
                nbs=params["nbs"],
                hsv_h=params["hsv_h"],
                hsv_s=params["hsv_s"],
                hsv_v=params["hsv_v"],
                degrees=params["degrees"],
                translate=params["translate"],
                scale=params["scale"],
                shear=params["shear"],
                perspective=params["perspective"],
                flipud=params["flipud"],
                fliplr=params["fliplr"],
                bgr=params["bgr"],
                mosaic=params["mosaic"],
                mixup=params["mixup"],
                copy_paste=params["copy_paste"],
                auto_augment=params["auto_augment"],
                erasing=params["erasing"],
                crop_fraction=params["crop_fraction"])
    ####更改val输出路径#####
    DEFAULT_CFG_DICT['save_dir']=os.path.join(model.trainer.save_dir,'val')
    model.overrides['save_dir']=os.path.join(model.trainer.save_dir,'val')
    ####
    metrics = model.val()
    modelsavedir = str(model.trainer.best)
    weightdir = str(model.trainer.wdir)
    if (params["save_dir"]):
        modeldirs=modelsavedir
    else:
        script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        modeldirs = os.path.join(script_dir, modelsavedir)

    # # 将配置还原回原来的样子
    DEFAULT_CFG=original_cfg
    DEFAULT_CFG_DICT=original_cfg_dict
    return modeldirs, weightdir,datadir

def export_yolo(params,model_path):
    model = YOLO(model_path)
    ####wts模型导出，目前默认detect，如果是其他的任务，就需要指定参数model_type=,以及修改gen_wts代码
    if params['export_format']=='wts':
        converter = gen_wts.from_args(
            weights=model_path,
        )
        converter.convert()
    else:
        model.export(format=params['export_format'], imgsz=params['imgsz_export'], half=params['half'], dynamic=params['dynamic'], simplify= params['simplify'])

def export_fcn(params,params_export,model_path):
    modelfcn_export=modelFCN(params)
    fcnmodel_toexport=modelfcn_export.export_model(model_path)
    output_onnx_path = model_path.split('.')[0]+'.'+params_export["export_format"]
    # ####输出模型
    # torch.save(fcnmodel_toexport, model_path.split('.')[0]+'xx.pth')
    # ####
    # 2. 定义输入张量
    if params_export["export_format"]=='onnx':
        imgsz_input=params_export["imgsz_export"]
        dummy_input = torch.randn(1, 3, imgsz_input[0],imgsz_input[1])  # 假设输入形状为 (batch_size, channels, height, width)
        torch.onnx.export(fcnmodel_toexport, dummy_input, output_onnx_path, verbose=params_export["export_detail"], opset_version=11)
    if params_export["export_format"] == 'wts':
        import struct
        f = open(output_onnx_path, 'w')
        f.write("{}\n".format(len(fcnmodel_toexport.state_dict().keys())))
        for k,v in fcnmodel_toexport.state_dict().items():
            if params_export["export_detail"]:
                print('key: ', k)
                print('value: ', v.shape)
            vr = v.reshape(-1).cpu().numpy()
            f.write("{} {}".format(k, len(vr)))
            for vv in vr:
                f.write(" ")
                f.write(struct.pack(">f", float(vv)).hex())
            f.write("\n")

def export_efficient(params,params_export,model_path):
    modeleffic_export=modelEfficient(params)
    efficmodel_toexport=modeleffic_export.export_model(model_path)
    output_onnx_path = model_path.split('.')[0] + '.' + params_export["export_format"]
    if params_export["export_format"]=='onnx':
        imgsz_input=params_export["imgsz_export"]
        dummy_input = torch.randn(1, 3, imgsz_input[0],imgsz_input[1])  # 假设输入形状为 (batch_size, channels, height, width)
        # 检查模型是否被封装在 DataParallel 中
        if isinstance(efficmodel_toexport, torch.nn.DataParallel):
            # 提取原始模型
            efficmodel_toexport = efficmodel_toexport.module
        elif isinstance(efficmodel_toexport.features, torch.nn.DataParallel):
            # 提取原始模型
            efficmodel_toexport = efficmodel_toexport.features.module
        torch.onnx.export(efficmodel_toexport, dummy_input, output_onnx_path, verbose=params_export["export_detail"], opset_version=11)
    if params_export["export_format"] == 'wts':
        import struct
        f = open(output_onnx_path, 'w')
        f.write("{}\n".format(len(efficmodel_toexport.state_dict().keys())))
        for k,v in efficmodel_toexport.state_dict().items():
            if params_export["export_detail"]:
                print('key: ', k)
                print('value: ', v.shape)
            vr = v.reshape(-1).cpu().numpy()
            f.write("{} {}".format(k, len(vr)))
            for vv in vr:
                f.write(" ")
                f.write(struct.pack(">f", float(vv)).hex())
            f.write("\n")

def testimage_yolo(params,yaml_datadir,infermodeldir,testformat):
    format = testformat
    if format == "onnx":
        infermodel = os.path.join(infermodeldir, "best.onnx")
    elif format == "openvino":
        infermodel = os.path.join(infermodeldir, "best_openvino_model")
    elif format == "engine":
        infermodel = os.path.join(infermodeldir, "best.engine")
    elif format == "pt" or format == "wts":
        infermodel = os.path.join(infermodeldir, "best.pt")

    predictor_test=PredictSahi_yolo(infermodel,params)
    ##判断yaml_datadir是否为None，即是否在测试之前就有训练步骤
    if yaml_datadir:
        predictor_test.predict_based_on_size(yaml_datadir)
    else:
        predictor_test.predict_based_on_size()

def trainfcn(params):
    modelfcn=modelFCN(params)
    modelfcn.train()
    return modelfcn.model_savedir

def trainEfficientNet(params):
    modelefficientNet=modelEfficient(params)
    modelefficientNet.train_Efficient()
    return modelefficientNet.model_savedir
def yoloit(alljsondir,aimode=None):
    with open(alljsondir, 'r',encoding='utf-8', errors='ignore') as f:
        Allparams = json.load(f)
    DefaultParams=Allparams["DefualtParams"]
    MakeDataParams = Allparams["MakeDataParams"]
    TrainParams = Allparams["TrainParams"]
    ExportParams = Allparams["ExportParams"]
    TestParams = Allparams["TestParams"]
    makedata = DefaultParams['ifmkdata']
    iftrain = DefaultParams['iftrain']
    ifexport = DefaultParams['ifexport']
    iftest = DefaultParams['iftest']
    modeltype = DefaultParams['modeltype']
    ##判断用哪个接口
    if aimode=='train':
        DefaultParams["iftrain"]=True
        iftrain=DefaultParams["iftrain"]
    if aimode=='export':
        DefaultParams["ifexport"]=True
        ifexport = DefaultParams["ifexport"]
    if aimode=='test':
        DefaultParams["iftest"]=True
        iftest = DefaultParams["iftest"]
    ###是否制作数据集
    if makedata:
        datadir = halcon2yolos(MakeDataParams)
        # datadir = halcon2yolos(jsonpath, alldir=alldir)
    else:
        datadir=None
    ###是否进行训练
    if iftrain:
        if modeltype=='yolo':
            YOLOParams=TrainParams['YOLOParams']
            modeldir, weightdir,yaml_datadir = trainyolo(YOLOParams,datadir=datadir if datadir else YOLOParams["datadir"])
            # modeldir, weightdir = trainyolo(datadir=datadir,
            #                                 modelpath=modelpath,
            #                                 epochs=epochs, batch=batch,
            #                                 workers=workers,
            #                                 amp=amp,
            #                                 imgsz=imgsz,
            #                                 patience=patience,
            #                                 device=device,
            #                                 resume=resume)
        if modeltype == 'fcn':
            FCNParams = TrainParams['FCNParams']
            modeldir=trainfcn(FCNParams)

        if modeltype == 'efficient':
            EfficientNetParams = TrainParams['EfficientNetParams']
            modeldir=trainEfficientNet(EfficientNetParams)
    else:
        modeldir, weightdir,yaml_datadir=None,None,None
    ###是否导出模型
    if ifexport:
        if modeltype == 'yolo':
            ExportParams=ExportParams["ExportParams_YOLO"]
            export_yolo(ExportParams,model_path=modeldir if modeldir else ExportParams["model_to_export"])
            weightdir_export=weightdir if weightdir else os.path.dirname(ExportParams["model_to_export"])
            exportmodel_format=ExportParams["export_format"]
        if modeltype == 'fcn':
            ExportParams = ExportParams["ExportParams_FCN"]
            export_fcn(FCNParams,ExportParams,model_path=modeldir)#######继续修改，怎么导出########
        if modeltype == 'efficient':
            ExportParams = ExportParams["ExportParams_EfficientNet"]
            export_efficient(EfficientNetParams,ExportParams,model_path=modeldir)#######继续修改，怎么导出########
    else:
        weightdir_export=None
        exportmodel_format = None
    ###是否进行测试
    if iftest:
        if modeltype == 'yolo':
            # testimage(cur_path=inferedimg, infermodeldir=weightdir_export if weightdir_export else params["infermodeldir"],
            #           testimgpath=testimg, format=format)
            ##如果训练时输出test图片的路径就放在训练输出一起，训练参数还需要添加一个“da_testimg”:true/false,如果json文件没有这个关键词，默认为True
            if weightdir and TrainParams.get("do_testimg",True):
                test_oudir=os.path.join(os.path.dirname(weightdir),'test')
                if not os.path.exists(test_oudir):
                    os.makedirs(test_oudir)
                autolabel_dir = os.path.join(test_oudir, 'autolabel')
                inferedimg_dir=os.path.join(test_oudir, 'inferedimg')
                if not os.path.exists(autolabel_dir):
                    os.makedirs(autolabel_dir)
                if not os.path.exists(inferedimg_dir):
                    os.makedirs(inferedimg_dir)
                TestParams["resultjson_path"]=autolabel_dir
                TestParams["inferedimg"] = inferedimg_dir
            ##如果训练时输出test图片的路径就放在训练输出一起
            testimage_yolo(TestParams,yaml_datadir,infermodeldir=weightdir_export if weightdir_export else TestParams["infermodeldir"],testformat=exportmodel_format if exportmodel_format else TestParams["infer_format"])

        if modeltype == 'fcn':
            print('fcn test not support now!! to developing')

        if modeltype == 'efficient':
            print('efficient test not support now!! to developing')

def yoloit_solo(alljsondir,aimode=None):
    with open(alljsondir, 'r',encoding='utf-8', errors='ignore') as f:
        Allparams = json.load(f)
    DefaultParams=Allparams["DefualtParams"]
    MakeDataParams = Allparams["MakeDataParams"]
    TrainParams = Allparams["TrainParams"]
    ExportParams = Allparams["ExportParams"]
    TestParams = Allparams["TestParams"]
    makedata = DefaultParams.get('ifmkdata', False)
    iftrain = DefaultParams.get('iftrain', False)
    ifexport = DefaultParams.get('ifexport', False)
    iftest = DefaultParams.get('iftest', False)
    modeltype = DefaultParams['modeltype']
    ##判断用哪个接口
    if aimode=='train':
        DefaultParams["ifmkdata"]=False
        ifmkdata=DefaultParams["ifmkdata"]
        DefaultParams["iftrain"]=True
        iftrain=DefaultParams["iftrain"]
        DefaultParams["ifexport"]=False
        ifexport=DefaultParams["ifexport"]
        DefaultParams["iftest"]=False
        iftest=DefaultParams["iftest"]
    if aimode=='export':
        DefaultParams["ifmkdata"]=False
        ifmkdata=DefaultParams["ifmkdata"]
        DefaultParams["iftrain"]=False
        iftrain=DefaultParams["iftrain"]
        DefaultParams["ifexport"]=True
        ifexport=DefaultParams["ifexport"]
        DefaultParams["iftest"]=False
        iftest=DefaultParams["iftest"]
    if aimode=='test':
        DefaultParams["ifmkdata"]=False
        ifmkdata=DefaultParams["ifmkdata"]
        DefaultParams["iftrain"]=False
        iftrain=DefaultParams["iftrain"]
        DefaultParams["ifexport"]=False
        ifexport=DefaultParams["ifexport"]
        DefaultParams["iftest"]=True
        iftest=DefaultParams["iftest"]
    ###是否制作数据集
    if makedata:
        datadir = halcon2yolos(MakeDataParams)
        # datadir = halcon2yolos(jsonpath, alldir=alldir)
    else:
        datadir=None
    ###是否进行训练
    if iftrain:
        if modeltype=='yolo':
            YOLOParams=TrainParams['YOLOParams']
            modeldir, weightdir,yaml_datadir = trainyolo(YOLOParams,datadir=datadir if datadir else YOLOParams["datadir"])
            # modeldir, weightdir = trainyolo(datadir=datadir,
            #                                 modelpath=modelpath,
            #                                 epochs=epochs, batch=batch,
            #                                 workers=workers,
            #                                 amp=amp,
            #                                 imgsz=imgsz,
            #                                 patience=patience,
            #                                 device=device,
            #                                 resume=resume)
        if modeltype == 'fcn':
            FCNParams = TrainParams['FCNParams']
            modeldir=trainfcn(FCNParams)

        if modeltype == 'efficient':
            EfficientNetParams = TrainParams['EfficientNetParams']
            modeldir=trainEfficientNet(EfficientNetParams)
    else:
        modeldir, weightdir,yaml_datadir=None,None,None
    ###是否导出模型
    if ifexport:
        if modeltype == 'yolo':
            ExportParams=ExportParams["ExportParams_YOLO"]
            export_yolo(ExportParams,model_path=modeldir if modeldir else ExportParams["model_to_export"])
            weightdir_export=weightdir if weightdir else os.path.dirname(ExportParams["model_to_export"])
            exportmodel_format=ExportParams["export_format"]
        if modeltype == 'fcn':
            ExportParams = ExportParams["ExportParams_FCN"]
            export_fcn(FCNParams,ExportParams,model_path=modeldir)#######继续修改，怎么导出########
        if modeltype == 'efficient':
            ExportParams = ExportParams["ExportParams_EfficientNet"]
            export_efficient(EfficientNetParams,ExportParams,model_path=modeldir)#######继续修改，怎么导出########
    else:
        weightdir_export=None
        exportmodel_format = None
    ###是否进行测试
    if iftest:
        if modeltype == 'yolo':
            # testimage(cur_path=inferedimg, infermodeldir=weightdir_export if weightdir_export else params["infermodeldir"],
            #           testimgpath=testimg, format=format)
            ##如果训练时输出test图片的路径就放在训练输出一起，训练参数还需要添加一个“da_testimg”:true/false,如果json文件没有这个关键词，默认为True
            if weightdir and TrainParams.get("do_testimg",True):
                test_oudir=os.path.join(os.path.dirname(weightdir),'test')
                if not os.path.exists(test_oudir):
                    os.makedirs(test_oudir)
                if TestParams.get("resultjson_path",False):
                    autolabel_dir = os.path.join(test_oudir, 'autolabel')
                    if not os.path.exists(autolabel_dir):
                        os.makedirs(autolabel_dir)
                inferedimg_dir = os.path.join(test_oudir, 'inferedimg')
                if not os.path.exists(inferedimg_dir):
                    os.makedirs(inferedimg_dir)
                TestParams["resultjson_path"]=autolabel_dir
                TestParams["inferedimg"] = inferedimg_dir
            ##如果训练时输出test图片的路径就放在训练输出一起
            testimage_yolo(TestParams,yaml_datadir,infermodeldir=weightdir_export if weightdir_export else TestParams["infermodeldir"],testformat=exportmodel_format if exportmodel_format else TestParams["infer_format"])

        if modeltype == 'fcn':
            print('fcn test not support now!! to developing')

        if modeltype == 'efficient':
            print('efficient test not support now!! to developing')
