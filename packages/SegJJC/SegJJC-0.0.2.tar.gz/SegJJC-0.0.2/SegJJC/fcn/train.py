import os
import time
import datetime
import  yaml
import torch
import shutil

from SegJJC.fcn.src import fcn_resnet50
from .train_utils import train_one_epoch, evaluate, create_lr_scheduler
from .my_dataset import myDataset_yaml
import SegJJC.fcn.transforms as T
import torchvision.models.segmentation as models

class modelFCN:
    def __init__(self, params):
        self.params = params
        ###读取train、val的images路径
        with open(self.params["data_yaml_dir"], 'r', encoding='utf-8') as file:
            datayaml = yaml.safe_load(file)
        self.num_classes = datayaml['nc'] + 1
        # 提取 train 和 val 路径
        self.train_path = datayaml['train']
        self.val_path = datayaml['val']
        self.aux=self.params["aux"]
        self.model_savedir=None
        self.best_miou_allcls=0

    class SegmentationPresetTrain:
        def __init__(self, base_size, crop_size, hflip_prob=0.5, mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)):
            min_size = int(0.5 * base_size)
            max_size = int(2.0 * base_size)

            trans = [T.RandomResize(min_size, max_size)]
            if hflip_prob > 0:
                trans.append(T.RandomHorizontalFlip(hflip_prob))
            trans.extend([
                T.RandomCrop(crop_size),
                T.ToTensor(),
                T.Normalize(mean=mean, std=std),
            ])
            self.transforms = T.Compose(trans)

        def __call__(self, img, target):
            return self.transforms(img, target)

    class SegPresetTrain:
        def __init__(self, imgsz,crop_size=None, hflip_prob=0.5, mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)):

            trans = [T.imgResize((imgsz[0], imgsz[1]))]
            if hflip_prob > 0:
                trans.append(T.RandomHorizontalFlip(hflip_prob))
            # 根据 crop_size 是否存在来决定是否添加 T.RandomCrop
            if crop_size is not None:
                trans.append(T.RandomCrop(crop_size))
            trans.extend([
                T.ToTensor(),
                T.Normalize(mean=mean, std=std),
            ])
            self.transforms = T.Compose(trans)

        def __call__(self, img, target):
            return self.transforms(img, target)
    # class SegPresetEval:
    #     def __init__(self, imgsz, mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)):
    #         self.transforms = T.Compose([
    #             T.imgResize((imgsz[0], imgsz[1])),
    #             T.ToTensor(),
    #             T.Normalize(mean=mean, std=std),
    #         ])
    #
    #     def __call__(self, img, target):
    #         return self.transforms(img, target)
    class SegPresetEval:
        def __init__(self, imgsz,crop_size=None, mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)):
            # 根据 crop_size 是否存在来决定是否添加 T.RandomCrop
            trans=[T.imgResize((imgsz[0], imgsz[1]))]
            if crop_size is not None:
                trans.append(T.RandomCrop(crop_size))
            trans.extend([
                T.ToTensor(),
                T.Normalize(mean=mean, std=std),
            ])
            self.transforms = T.Compose(trans)

        def __call__(self, img, target):
            return self.transforms(img, target)

    class SegmentationPresetEval:
        def __init__(self, base_size, mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)):
            self.transforms = T.Compose([
                T.RandomResize(base_size, base_size),
                T.ToTensor(),
                T.Normalize(mean=mean, std=std),
            ])

        def __call__(self, img, target):
            return self.transforms(img, target)
    def get_transform_seg(self,imgsz,train,crop_size=None):
        return self.SegPresetTrain(imgsz,crop_size=crop_size) if train else self.SegPresetEval(imgsz,crop_size=crop_size)

    def get_transform(self,train):
        base_size = 520
        crop_size = 480

        return self.SegmentationPresetTrain(base_size, crop_size) if train else self.SegmentationPresetEval(base_size)

    def create_model(self,aux, num_classes, pretrain=None):
        # model = fcn_resnet50(aux=aux, num_classes=num_classes)
        if self.params["arch"]=='fcn_resnet50':
            model = fcn_resnet50(aux=aux, num_classes=num_classes)
        else:
            model = models.__dict__[self.params["arch"]](pretrained=False, pretrained_backbone=False, num_classes=num_classes,aux_loss=aux)
        if pretrain:
            # weights_dict = torch.load("./fcn_resnet50_coco.pth", map_location='cpu')
            weights_dict = torch.load(pretrain, map_location='cpu')
            if num_classes != 21:
                # 官方提供的预训练权重是21类(包括背景)
                # 如果训练自己的数据集，将和类别相关的权重删除，防止权重shape不一致报错
                for k in list(weights_dict.keys()):
                    if "classifier.4" in k:
                        del weights_dict[k]
            if "model" in weights_dict:
                ###获取与训练模型最佳分数
                best_miou_allcls = weights_dict['best_miou_allcls']
                if self.params["device"] is not None:
                    # best_acc1 may be from a checkpoint from a different GPU
                    self.best_miou_allcls = best_miou_allcls.to(self.params["device"])
                ###获取与训练模型最佳分数
                missing_keys, unexpected_keys = model.load_state_dict(weights_dict["model"].state_dict(), strict=False)
            else:
                missing_keys, unexpected_keys = model.load_state_dict(weights_dict, strict=False)
            if len(missing_keys) != 0 or len(unexpected_keys) != 0:
                print("missing_keys: ", missing_keys)
                print("unexpected_keys: ", unexpected_keys)

        return model

    def export_model(self,export_modeldict):
        # model = fcn_resnet50(aux=self.aux, num_classes=self.num_classes)
        # weights_dict = torch.load(export_modeldict, map_location='cpu')
        # model.load_state_dict(weights_dict, strict=False)
        # return model
        model=torch.load(export_modeldict, map_location='cpu')['model']
        return model

    def train(self):
        deviceid="cuda:0" if self.params["device"] is None else f"cuda:{self.params['device']}"
        device = torch.device(deviceid if torch.cuda.is_available() else "cpu")
        batch_size = self.params["batch_size"]
        # segmentation nun_classes + background
        crop_size=self.params["crop_size"]

        # with open(self.params["data_yaml_dir"], 'r', encoding='utf-8') as file:
        #     datayaml = yaml.safe_load(file)
        # num_classes = datayaml['nc'] + 1
        # # 提取 train 和 val 路径
        # train_path = datayaml['train']
        # val_path = datayaml['val']
        # # train_dataset = myDataset_yaml(train_path,transforms=get_transform(train=True))
        train_dataset = myDataset_yaml(self.train_path, transforms=self.get_transform_seg(self.params["imgsz"],train=True,crop_size=crop_size))
        # VOCdevkit -> VOC2012 -> ImageSets -> Segmentation -> val.txt
        # val_dataset = myDataset_yaml(val_path,transforms=get_transform(train=False))
        val_dataset = myDataset_yaml(self.val_path, transforms=self.get_transform_seg(self.params["imgsz"],train=False,crop_size=crop_size))

        num_workers = min([os.cpu_count(), batch_size if batch_size > 1 else 0, 8])
        train_loader = torch.utils.data.DataLoader(train_dataset,
                                                   batch_size=batch_size,
                                                   num_workers=num_workers,
                                                   shuffle=True,
                                                   pin_memory=True,
                                                   collate_fn=train_dataset.collate_fn)

        val_loader = torch.utils.data.DataLoader(val_dataset,
                                                 batch_size=1,
                                                 num_workers=num_workers,
                                                 pin_memory=True,
                                                 collate_fn=val_dataset.collate_fn)

        model = self.create_model(self.params["aux"], self.num_classes,self.params["pretrained_model"])
        model.to(device)

        params_to_optimize = [
            {"params": [p for p in model.backbone.parameters() if p.requires_grad]},
            {"params": [p for p in model.classifier.parameters() if p.requires_grad]}
        ]

        if self.params["aux"]:
            params = [p for p in model.aux_classifier.parameters() if p.requires_grad]
            params_to_optimize.append({"params": params, "lr": self.params["lr"] * 10})

        optimizer = torch.optim.SGD(
            params_to_optimize,
            lr=self.params["lr"], momentum=self.params["momentum"], weight_decay=self.params["weight_decay"]
        )

        scaler = torch.cuda.amp.GradScaler() if self.params["amp"] else None

        # 创建学习率更新策略，这里是每个step更新一次(不是每个epoch)
        lr_scheduler = create_lr_scheduler(optimizer, len(train_loader), self.params["epochs"], warmup=True)
        start_epoch=0
        if self.params["resume"]:
            checkpoint = torch.load(self.params["pretrained_model"], map_location='cpu')
            model.load_state_dict(checkpoint['model'].state_dict())
            optimizer.load_state_dict(checkpoint['optimizer'])
            lr_scheduler.load_state_dict(checkpoint['lr_scheduler'])
            start_epoch = checkpoint['epoch'] + 1
            if self.params["amp"]:
                scaler.load_state_dict(checkpoint["scaler"])
            train_dir = checkpoint['outdir']
            epochs_all=checkpoint['epoch_all']
        else:
            # 用来保存训练以及验证过程中信息
            ####创建训练输出子文件train####
            from ultralytics.utils.files import increment_path
            train_childdir=os.path.join(self.params["save_dir"],'FCNtrain')
            train_dir = str(increment_path(train_childdir, exist_ok=False)).replace("\\",'/')
            ######
            if not os.path.exists(self.params["save_dir"]):
                os.mkdir(self.params["save_dir"])
            if not os.path.exists(train_dir):
                os.mkdir(train_dir)
            epochs_all = self.params["epochs"]

        # results_file = train_dir+"/results{}.txt".format(datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
        results_file = train_dir + "/results.txt"
        # ###读取train、val的images路径

        start_time = time.time()
        for epoch in range(start_epoch, epochs_all):
            mean_loss, lr = train_one_epoch(model, optimizer, train_loader, device, epoch,
                                            lr_scheduler=lr_scheduler, print_freq=self.params["traininfo_printepoch"], scaler=scaler)

            confmat ,miou_allcls= evaluate(model, val_loader, device=device, num_classes=self.num_classes)
            #判断是否为best——model
            is_best = miou_allcls > self.best_miou_allcls
            self.best_miou_allcls = max(miou_allcls,self.best_miou_allcls)
            # 判断是否为best——model
            val_info = str(confmat)
            print(val_info)
            # write into txt
            with open(results_file, "a") as f:
                # 记录每个epoch对应的train_loss、lr以及验证集各指标
                train_info = f"[epoch: {epoch}]\n" \
                             f"train_loss: {mean_loss:.4f}\n" \
                             f"lr: {lr:.6f}\n"
                f.write(train_info + val_info + "\n\n")
            #原来的save_file 里"model": model.state_dict(),现改为model
            save_file = {"model": model,
                         "optimizer": optimizer.state_dict(),
                         "lr_scheduler": lr_scheduler.state_dict(),
                         "epoch": epoch,
                         "epoch_all": self.params["epochs"],
                         "outdir":train_dir,
                         "best_miou_allcls": self.best_miou_allcls,
                         "args": self.params}
            if self.params["amp"]:
                save_file["scaler"] = scaler.state_dict()
            if not os.path.exists(train_dir+'/weights'):
                os.mkdir(train_dir+'/weights')
            # fcnmodel_savedir=train_dir+'/weights'+"/model_{}.pth".format(epoch)
            # self.model_savedir=fcnmodel_savedir
            # torch.save(save_file, fcnmodel_savedir)
            fcnmodel_savedir=train_dir+'/weights'
            lastpath = fcnmodel_savedir + "/last.pth"
            bestpath = fcnmodel_savedir + "/best.pth"
            torch.save(save_file, lastpath)
            if is_best or (not os.path.exists(bestpath)):
                shutil.copyfile(lastpath, bestpath)
            self.model_savedir=bestpath

        total_time = time.time() - start_time
        total_time_str = str(datetime.timedelta(seconds=int(total_time)))
        print("training time {}".format(total_time_str))


#


# if __name__ == '__main__':
#     args = parse_args()
#
#     if not os.path.exists("./save_weights"):
#         os.mkdir("./save_weights")
#
#     main(args)
