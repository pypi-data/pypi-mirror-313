"""
Evaluate on ImageNet. Note that at the moment, training is not implemented (I am working on it).
that being said, evaluation is working.
"""

import argparse
import os
import random
import shutil
import time
import warnings
import PIL
import datetime

import torch
import torch.nn as nn
import torch.nn.parallel
import torch.backends.cudnn as cudnn
import torch.distributed as dist
import torch.optim
import torch.multiprocessing as mp
import torch.utils.data
import torch.utils.data.distributed
import torchvision.transforms as transforms
import torchvision.datasets as datasets
import torchvision.models as models
from torch.optim.lr_scheduler import LambdaLR

from .efficientnet_pytorch import EfficientNet,T_cls


def compute_lr_lambda(epoch, warmup_epochs, num_epochs, power, base_values, eta_min):
    if epoch < warmup_epochs:
        return (1.0 / (warmup_epochs + 1)) * (epoch + 1)

    factor = (1 - (epoch - warmup_epochs) / float(num_epochs - warmup_epochs)) ** power
    return [(base_lr - eta_min) * factor + eta_min for base_lr in base_values][0]

best_acc1=0
class modelEfficient:
    def __init__(self, params):
        self.params = params
        self.model_savedir = None
        # self.best_acc1 = 0

    class ClsPresetTrain:
        def __init__(self, imgsz, hflip_prob=0.5, mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)):

            trans = [T_cls.imgResize((imgsz[0], imgsz[1]))]
            if hflip_prob > 0:
                trans.append(T_cls.RandomHorizontalFlip(hflip_prob))
            trans.extend([
                T_cls.ToTensor(),
                T_cls.Normalize(mean=mean, std=std),
            ])
            self.transforms = T_cls.Compose(trans)

        def __call__(self, img, target=None):
            # 确保 img 和 target 都传递给变换
            if target is None:
                return self.transforms(img)
            else:
                # 将 img 和 target 作为元组传递给变换
                return self.transforms((img, target))

    class ClsPresetEval:
        def __init__(self, imgsz, mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)):
            # 根据 crop_size 是否存在来决定是否添加 T.RandomCrop
            trans=[T_cls.imgResize((imgsz[0], imgsz[1]))]
            trans.extend([
                T_cls.ToTensor(),
                T_cls.Normalize(mean=mean, std=std),
            ])
            self.transforms = T_cls.Compose(trans)

        def __call__(self, img, target=None):
            # 确保 img 和 target 都传递给变换
            if target is None:
                return self.transforms(img)
            else:
                # 将 img 和 target 作为元组传递给变换
                return self.transforms((img, target))

    def get_transform_cls(self,imgsz,train):
        return self.ClsPresetTrain(imgsz) if train else self.ClsPresetEval(imgsz)

    def train_Efficient(self):
        if self.params["seed"] is not None:
            random.seed(self.params["seed"])
            torch.manual_seed(self.params["seed"])
            cudnn.deterministic = True
            warnings.warn('You have chosen to seed training. '
                          'This will turn on the CUDNN deterministic setting, '
                          'which can slow down your training considerably! '
                          'You may see unexpected behavior when restarting '
                          'from checkpoints.')

        if self.params["device"] is not None:
            warnings.warn('You have chosen a specific GPU. This will completely '
                          'disable data parallelism.')

        if self.params["dist_url"] == "env://" and self.params["world_size"] == -1:
            self.params["world_size"] = int(os.environ["WORLD_SIZE"])

        self.params["distributed"] = self.params["world_size"] > 1 or self.params["multiprocessing_distributed"]

        ngpus_per_node = torch.cuda.device_count()
        if self.params["multiprocessing_distributed"]:
            # Since we have ngpus_per_node processes per node, the total world_size
            # needs to be adjusted accordingly
            self.params["world_size"] = ngpus_per_node * self.params["world_size"]
            # Use torch.multiprocessing.spawn to launch distributed processes: the
            # main_worker process function
            mp.spawn(self.main_worker, nprocs=ngpus_per_node, args=(ngpus_per_node, self.params))
        else:
            # Simply call main_worker function
            self.main_worker(self.params["device"], ngpus_per_node, self.params)
    def main_worker(self,gpu, ngpus_per_node, params_mw):
        global best_acc1
        params_mw["device"] = gpu
        if params_mw["device"] is not None:
            print("Use GPU: {} for training".format(params_mw["device"]))

        if params_mw["distributed"]:
            if params_mw["dist_url"] == "env://" and params_mw["rank"] == -1:
                params_mw["rank"] = int(os.environ["RANK"])
            if params_mw["multiprocessing_distributed"]:
                # For multiprocessing distributed training, rank needs to be the
                # global rank among all the processes
                params_mw["rank"]  =params_mw["rank"]  * ngpus_per_node + gpu
            dist.init_process_group(backend=params_mw["dist_backend"], init_method=params_mw["dist_url"],
                                    world_size=params_mw["world_size"], rank=params_mw["rank"])
        # create model
        if 'efficientnet' in params_mw["arch"]:  # NEW
            if params_mw["pretrained"]:
                if params_mw["pretrained_model"]:
                    model = EfficientNet.from_pretrained(params_mw["arch"], weights_path=params_mw["pretrained_model"],advprop=params_mw["advprop"])
                    print("=> using pre-trained model '{}'".format(params_mw["pretrained_model"]))
                else:
                    model = EfficientNet.from_pretrained(params_mw["arch"], advprop=params_mw["advprop"])
                    print("=> using pre-trained model '{}'".format(params_mw["arch"]))
            else:
                print("=> creating model '{}'".format(params_mw["arch"]))
                model = EfficientNet.from_name(params_mw["arch"])

        else:
            if params_mw["pretrained"]:
                if params_mw["pretrained_model"]:
                    print('Loading pretrained weights for {}'.format(params_mw["arch"]))
                    print("=> using pre-trained model '{}'".format(params_mw["pretrained_model"]))
                    model=torch.load(params_mw["pretrained_model"])['state_dict']
                else:
                    print("=> using pre-trained model '{}'".format(params_mw["arch"]))
                    model = models.__dict__[params_mw["arch"]](pretrained=True)
            else:
                print("=> creating model '{}'".format(params_mw["arch"]))
                model = models.__dict__[params_mw["arch"]](pretrained=False)

        if params_mw["distributed"]:
            # For multiprocessing distributed, DistributedDataParallel constructor
            # should always set the single device scope, otherwise,
            # DistributedDataParallel will use all available devices.
            if params_mw["device"] is not None:
                torch.cuda.set_device(params_mw["device"])
                model.cuda(params_mw["device"])
                # When using a single GPU per process and per
                # DistributedDataParallel, we need to divide the batch size
                # ourselves based on the total number of GPUs we have
                params_mw["batch_size"] = int(params_mw["batch_size"] / ngpus_per_node)
                params_mw["workers"] = int(params_mw["workers"] / ngpus_per_node)
                model = torch.nn.parallel.DistributedDataParallel(model, device_ids=[params_mw["device"]])
            else:
                model.cuda()
                # DistributedDataParallel will divide and allocate batch_size to all
                # available GPUs if device_ids are not set
                model = torch.nn.parallel.DistributedDataParallel(model)
        elif params_mw["device"] is not None:
            torch.cuda.set_device(params_mw["device"])
            model = model.cuda(params_mw["device"])
        else:
            # DataParallel will divide and allocate batch_size to all available GPUs
            if params_mw["arch"].startswith('alexnet') or params_mw["arch"].startswith('vgg'):
                model.features = torch.nn.DataParallel(model.features)
                model.cuda()
            else:
                model = torch.nn.DataParallel(model).cuda()

        # define loss function (criterion) and optimizer
        criterion = nn.CrossEntropyLoss().cuda(params_mw["device"])

        optimizer = torch.optim.SGD(model.parameters(), params_mw["lr"],
                                    momentum=params_mw["momentum"],
                                    weight_decay=params_mw["weight_decay"])

        # optionally resume from a checkpoint
        if params_mw["resume"]:
            if os.path.isfile(params_mw["resume_model"]):
                print("=> loading checkpoint '{}'".format(params_mw["resume_model"]))
                checkpoint = torch.load(params_mw["resume_model"])
                params_mw["start_epoch"] = checkpoint['epoch']
                best_acc1 = checkpoint['best_acc1']
                if params_mw["device"] is not None:
                    # best_acc1 may be from a checkpoint from a different GPU
                    best_acc1 = best_acc1.to(params_mw["device"])
                model.load_state_dict(checkpoint['state_dict'].state_dict())
                # optimizer.load_state_dict(checkpoint['optimizer'])


                modelsavedir=checkpoint['outdir']
                epochs_all=checkpoint['epoch_all']
                print("=> loaded checkpoint '{}' (epoch {})"
                      .format(params_mw["resume_model"], checkpoint['epoch']))
            else:
                print("=> no checkpoint found at '{}'".format(params_mw["resume_model"]))
        else:
            ##创建结果txt
            modelsavedir = self.make_childdir()
            epochs_all =params_mw["epochs"]

        results_file = modelsavedir + "/results.txt"

        cudnn.benchmark = True

        # Data loading code
        traindir = os.path.join(params_mw["datadir"], 'train')
        valdir = os.path.join(params_mw["datadir"], 'val')
        if params_mw["advprop"]:
            normalize = transforms.Lambda(lambda img: img * 2.0 - 1.0)
        else:
            normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                             std=[0.229, 0.224, 0.225])
        if params_mw["ifefficient_defaultsize"]:
            if 'efficientnet' in params_mw["arch"]:
                image_size = EfficientNet.get_image_size(params_mw["arch"])
            else:
                image_size = params_mw["image_size"]
        else:
            image_size = params_mw["image_size"]
        if params_mw["crop_size"]:
            train_transforms =transforms.Compose([
                transforms.RandomResizedCrop(image_size),
                transforms.RandomHorizontalFlip(),
                transforms.ToTensor(),
                normalize,
            ])
            val_transforms = transforms.Compose([
                transforms.Resize(image_size, interpolation=PIL.Image.BICUBIC),
                transforms.CenterCrop(image_size),
                transforms.ToTensor(),
                normalize,
            ])
        else:
            train_transforms = self.get_transform_cls([image_size, image_size], train=True)
            val_transforms = self.get_transform_cls([image_size, image_size], train=False)
        #     train_transforms =transforms.Compose([
        #         T_cls.imgResize((image_size, image_size)),
        #         transforms.RandomHorizontalFlip(),
        #         transforms.ToTensor(),
        #         normalize,
        #     ])
        #     val_transforms = transforms.Compose([
        #         T_cls.imgResize((image_size, image_size)),
        #         transforms.CenterCrop(image_size),
        #         transforms.ToTensor(),
        #         normalize,
        #     ])
        train_dataset = datasets.ImageFolder(
            traindir,
            train_transforms)

        if params_mw["distributed"]:
            train_sampler = torch.utils.data.distributed.DistributedSampler(train_dataset)
        else:
            train_sampler = None

        train_loader = torch.utils.data.DataLoader(
            train_dataset, batch_size=params_mw["batch_size"], shuffle=(train_sampler is None),
            num_workers=params_mw["workers"], pin_memory=True, sampler=train_sampler)

        print('Using image size', image_size)

        val_loader = torch.utils.data.DataLoader(
            datasets.ImageFolder(valdir, val_transforms),
            batch_size=params_mw["batch_size"], shuffle=False,
            num_workers=params_mw["workers"], pin_memory=True)

        if params_mw["evaluate"]:
            res = self.validate(val_loader, model, criterion, params_mw)
            with open('res.txt', 'w') as f:
                print(res, file=f)
            return

        scheduler = self.create_lr_scheduler(
            optimizer,
            num_step=len(train_loader),
            epochs=epochs_all,
            method=params_mw["lr_scheduler"],  # 可以选择 "step" 或 "poly"
            params_alr=params_mw
        )
        if params_mw["resume"]:
            if os.path.isfile(params_mw["resume_model"]):
                optimizer.load_state_dict(checkpoint['optimizer'])
                scheduler.load_state_dict(checkpoint['lr_scheduler'])
                # scheduler.step()

        for epoch in range(params_mw["start_epoch"],epochs_all):
            if params_mw["distributed"]:
                train_sampler.set_epoch(epoch)
            # self.adjust_learning_rate(optimizer, epoch, params_mw)

            # train for one epoch
            result_progress_train=self.train(train_loader, model, criterion, optimizer, epoch,epochs_all, params_mw)
            scheduler.step()
            # evaluate on validation set
            result_top1,result_top5,result_progress_val = self.validate(val_loader, model, criterion, params_mw)
            acc1=result_top1.avg
            # result_progress_train=result_progress_train.print_write(len(train_loader))
            # result_progress_val=result_progress_val.print_write(len(val_loader))
            # remember best acc@1 and save checkpoint
            is_best = acc1 > best_acc1
            best_acc1 = max(acc1, best_acc1)
            ##################
            # write into txt
            with open(results_file, "a") as f:
                # 记录每个epoch对应的train_loss、lr以及验证集各指标
                # val_info = f"[epoch: {epoch}]\n" \
                #              f"accuracy: {acc1:.4f}\n"
                # f.write(val_info + "\n\n")
                val_info = f"{result_progress_train}\n" \
                           f"{result_progress_val}\n" \
                           f"* Acc@1 {result_top1.avg:.3f} Acc@5 {result_top5.avg:.3f}\n"
                f.write(val_info + "\n\n")
            #################
            if not params_mw["multiprocessing_distributed"] or (params_mw["multiprocessing_distributed"]
                    and params_mw["rank"] % ngpus_per_node == 0):
                # modelsavedir=self.make_childdir()
                self.model_savedir=self.save_checkpoint({
                    'epoch': epoch + 1,
                    'epoch_all': params_mw["epochs"],
                    'arch': params_mw["arch"],
                    'state_dict': model,
                    'best_acc1': best_acc1,
                    'optimizer' : optimizer.state_dict(),
                    'lr_scheduler':scheduler.state_dict(),
                    'outdir':modelsavedir,
                }, is_best,filename=modelsavedir)

    def train(self,train_loader, model, criterion, optimizer, epoch, epochs_all,params_t):
        batch_time = self.AverageMeter('Time', ':6.3f')
        data_time = self.AverageMeter('Data', ':6.3f')
        losses = self.AverageMeter('Loss', ':.4e')
        top1 = self.AverageMeter('Acc@1', ':6.2f')
        top5 = self.AverageMeter('Acc@5', ':6.2f')
        progress = self.ProgressMeter(len(train_loader), batch_time, data_time, losses, top1,
                                 top5, prefix="Epoch: [{}/{}]".format(epoch,epochs_all))

        # switch to train mode
        model.train()

        end = time.time()
        for i, (images, target) in enumerate(train_loader):
            # measure data loading time
            data_time.update(time.time() - end)

            if params_t['device'] is not None:
                images = images.cuda(params_t['device'], non_blocking=True)
            target = target.cuda(params_t['device'], non_blocking=True)

            # compute output
            output = model(images)
            loss = criterion(output, target)

            # measure accuracy and record loss
            acc1, acc5 = self.accuracy(output, target, topk=(1, 5))
            losses.update(loss.item(), images.size(0))
            top1.update(acc1[0], images.size(0))
            top5.update(acc5[0], images.size(0))

            # compute gradient and do SGD step
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            # measure elapsed time
            batch_time.update(time.time() - end)
            end = time.time()

            # if i % params_t["traininfo_printepoch"] == 0:
            #     progress.print(i)
            if params_t["traininfo_printepoch"]:
                if i % params_t["traininfo_printepoch"] == 0:
                    progress.print(i)
                    progress_out=progress.print_write(i)
            else:
                if (i % (len(train_loader)-1) == 0) & i>0:
                    progress.print(i)
                    progress_out = progress.print_write(i)
        return progress_out

    def validate(self,val_loader, model, criterion, params_v):
        batch_time = self.AverageMeter('Time', ':6.3f')
        losses = self.AverageMeter('Loss', ':.4e')
        top1 = self.AverageMeter('Acc@1', ':6.2f')
        top5 = self.AverageMeter('Acc@5', ':6.2f')
        progress =self.ProgressMeter(len(val_loader), batch_time, losses, top1, top5,
                                 prefix='Test: ')

        # switch to evaluate mode
        model.eval()

        with torch.no_grad():
            end = time.time()
            for i, (images, target) in enumerate(val_loader):
                if params_v['device'] is not None:
                    images = images.cuda(params_v['device'], non_blocking=True)
                target = target.cuda(params_v['device'], non_blocking=True)

                # compute output
                output = model(images)
                loss = criterion(output, target)

                # measure accuracy and record loss
                acc1, acc5 = self.accuracy(output, target, topk=(1, 5))
                losses.update(loss.item(), images.size(0))
                top1.update(acc1[0], images.size(0))
                top5.update(acc5[0], images.size(0))

                # measure elapsed time
                batch_time.update(time.time() - end)
                end = time.time()

                # if i % params_v["traininfo_printepoch"] == 0:
                #     progress.print(i)
                if params_v["traininfo_printepoch"]:
                    if i % params_v["traininfo_printepoch"] == 0:
                        progress.print(i)
                        progress_out=progress.print_write(i)
                else:
                    if (i % (len(val_loader)-1) == 0) & i>0:
                        progress.print(i)
                        progress_out = progress.print_write(i)
            # TODO: this should also be done with the ProgressMeter
            print(' * Acc@1 {top1.avg:.3f} Acc@5 {top5.avg:.3f}'
                  .format(top1=top1, top5=top5))

        # return top1.avg
        return top1,top5,progress_out
    def save_checkpoint(self,state, is_best, filename='checkpoint.pth'):
        efficientmodel_savedir = filename + '/weights'
        if not os.path.exists(efficientmodel_savedir):
            os.mkdir(efficientmodel_savedir)
        lastpath=efficientmodel_savedir+ "/last.pth"
        bestpath=efficientmodel_savedir+ "/best.pth"
        torch.save(state, lastpath)
        if is_best or (not os.path.exists(bestpath)):
            shutil.copyfile(lastpath, bestpath)
        return bestpath
    def make_childdir(self):
        # 用来保存训练以及验证过程中信息
        ####创建训练输出子文件train####
        from ultralytics.utils.files import increment_path
        train_childdir=os.path.join(self.params["save_dir"],'Efficientrain')
        train_dir = str(increment_path(train_childdir, exist_ok=False)).replace("\\",'/')
        ######
        if not os.path.exists(self.params["save_dir"]):
            os.mkdir(self.params["save_dir"])
        if not os.path.exists(train_dir):
            os.mkdir(train_dir)
        return train_dir

    def export_model(self,export_modeldict):
        model=torch.load(export_modeldict, map_location='cpu')['state_dict']
        return model

    class AverageMeter(object):
        """Computes and stores the average and current value"""
        def __init__(self, name, fmt=':f'):
            self.name = name
            self.fmt = fmt
            self.reset()

        def reset(self):
            self.val = 0
            self.avg = 0
            self.sum = 0
            self.count = 0

        def update(self, val, n=1):
            self.val = val
            self.sum += val * n
            self.count += n
            self.avg = self.sum / self.count

        def __str__(self):
            fmtstr = '{name} {val' + self.fmt + '} ({avg' + self.fmt + '})'
            return fmtstr.format(**self.__dict__)

    class ProgressMeter(object):
        def __init__(self, num_batches, *meters, prefix=""):
            self.batch_fmtstr = self._get_batch_fmtstr(num_batches)
            self.meters = meters
            self.prefix = prefix

        def print(self, batch):
            # entries = [self.prefix + self.batch_fmtstr.format(batch)]
            entries = [self.prefix + self.batch_fmtstr.format(batch+1)]
            entries += [str(meter) for meter in self.meters]
            print('\t'.join(entries))

        def print_write(self, batch):
            # entries = [self.prefix + self.batch_fmtstr.format(batch)]
            entries = [self.prefix + self.batch_fmtstr.format(batch + 1)]
            entries += [str(meter) for meter in self.meters]
            write_str='\t'.join(entries)
            return write_str

        def _get_batch_fmtstr(self, num_batches):
            num_digits = len(str(num_batches // 1))
            fmt = '{:' + str(num_digits) + 'd}'
            return '[' + fmt + '/' + fmt.format(num_batches) + ']'

    class PolyLRRatio(LambdaLR):
        def __init__(self, optimizer, eta_min=0, eta_min_ratio=None, power=1.0, num_epochs=100, warmup_epochs=0,
                     last_epoch=-1):
            self.eta_min = eta_min
            self.eta_min_ratio = eta_min_ratio
            self.power = power
            self.num_epochs = num_epochs
            self.warmup_epochs = warmup_epochs
            self.base_values = [group['lr'] for group in optimizer.param_groups]
            self.last_epoch = last_epoch
            super().__init__(optimizer, self._get_lr_lambda(), last_epoch)

        def _get_lr_lambda(self):
            return lambda epoch: compute_lr_lambda(epoch, self.warmup_epochs, self.num_epochs, self.power,
                                                   self.base_values, self.eta_min)

        def _get_value(self):
            param_groups_value = []
            for base_value, param_group in zip(self.base_values, self.optimizer.param_groups):
                eta_min = self.eta_min if self.eta_min_ratio is None else base_value * self.eta_min_ratio
                step_ratio = (1 - 1 / (self.num_epochs - self.last_epoch + 1)) ** self.power
                step_value = (param_group['lr'] - eta_min) * step_ratio + eta_min
                param_groups_value.append(step_value)
            return param_groups_value
    # class PolyLRRatio(LambdaLR):
    #     def __init__(self, optimizer, eta_min=0, eta_min_ratio=None, power=1.0, num_epochs=100, warmup_epochs=0,
    #                  last_epoch=-1):
    #         self.eta_min = eta_min
    #         self.eta_min_ratio = eta_min_ratio
    #         self.power = power
    #         self.num_epochs = num_epochs
    #         self.warmup_epochs = warmup_epochs
    #         self.base_values = [group['lr'] for group in optimizer.param_groups]
    #
    #         # Define the lambda function here
    #         self.lr_lambda = self._get_lr_lambda()
    #         super().__init__(optimizer, self.lr_lambda, last_epoch)
    #
    #     def _get_lr_lambda(self):
    #         # Return a function or a list of functions for LambdaLR
    #         def lr_lambda(epoch):
    #             if epoch < self.warmup_epochs:
    #                 return (1.0 / (self.warmup_epochs + 1)) * (epoch + 1)
    #
    #             factor = (1 - (epoch - self.warmup_epochs) / float(self.num_epochs - self.warmup_epochs)) ** self.power
    #             return [(base_lr - self.eta_min) * factor + self.eta_min for base_lr in self.base_values][0]
    #
    #         return lr_lambda
    #
    #     def _get_value(self):
    #         param_groups_value = []
    #         for base_value, param_group in zip(self.base_values, self.optimizer.param_groups):
    #             eta_min = self.eta_min if self.eta_min_ratio is None else base_value * self.eta_min_ratio
    #             step_ratio = (1 - 1 / (self.num_epochs - self.last_epoch + 1)) ** self.power
    #             step_value = (param_group['lr'] - eta_min) * step_ratio + eta_min
    #             param_groups_value.append(step_value)
    #         return param_groups_value
    def adjust_learning_rate(self,optimizer, epoch, params_alr,step_size):
        """Sets the learning rate to the initial LR decayed by 10 every 30 epochs"""
        lr = params_alr["lr"] * (0.1 ** (epoch // step_size))
        for param_group in optimizer.param_groups:
            param_group['lr'] = lr

    def create_lr_scheduler(self,optimizer, num_step, epochs, method="poly", warmup=True, warmup_epochs=1,
                            warmup_factor=1e-3, params_alr=None):
        if method == "step":
            def f(x):
                self.adjust_learning_rate(optimizer, x, params_alr,num_step)
                return optimizer.param_groups[0]['lr'] / params_alr['lr']

            return torch.optim.lr_scheduler.LambdaLR(optimizer, lr_lambda=f)
        elif method == "poly":
            return self.PolyLRRatio(optimizer, eta_min=0, eta_min_ratio=0.1, power=0.9, num_epochs=epochs,
                               warmup_epochs=warmup_epochs)
        else:
            raise ValueError(f"Unknown learning rate method: {method}")


    def accuracy(self,output, target, topk=(1,)):
        """Computes the accuracy over the k top predictions for the specified values of k"""
        with torch.no_grad():
            maxk = max(topk)
            batch_size = target.size(0)

            _, pred = output.topk(maxk, 1, True, True)
            pred = pred.t()
            correct = pred.eq(target.view(1, -1).expand_as(pred))

            res = []
            for k in topk:
                correct_k = correct[:k].reshape(-1).float().sum(0, keepdim=True)
                res.append(correct_k.mul_(100.0 / batch_size))
            return res


