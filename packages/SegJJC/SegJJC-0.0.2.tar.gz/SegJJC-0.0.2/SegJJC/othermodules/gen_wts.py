import os
import struct
import torch

class gen_wts:
    def __init__(self, weights, output, model_type):
        self.weights = weights
        self.output = output
        self.model_type = model_type

    @classmethod
    def from_args(cls, weights, output=None, model_type='detect'):
        if not os.path.isfile(weights):
            raise ValueError('Invalid input file')
        if not output:
            output = os.path.splitext(weights)[0] + '.wts'
        elif os.path.isdir(output):
            output = os.path.join(output, os.path.splitext(os.path.basename(weights))[0] + '.wts')
        return cls(weights, output, model_type)

    def convert(self):
        print(f'Generating .wts for {self.model_type} model')
        print(f'Loading {self.weights}')

        device = 'cpu'
        # Load model
        #判断模型中是否有model或ema
        themodel = torch.load(self.weights, map_location=device)
        if themodel['model'] is not None:
            thismodel = themodel['model']
        elif themodel['ema'] is not None:
            thismodel = themodel['ema']
        else:
            raise ValueError("Both 'model' and 'ema' are None.")
        # 判断模型中是否有model或ema
        model = thismodel.float()  # load to FP32model = torch.load(pt_file, map_location=device)['model'].float()  # load to FP32
        # model = torch.load(self.weights, map_location=device)['model'].float()

        if self.model_type in ['detect', 'seg']:
            anchor_grid = model.model[-1].anchors * model.model[-1].stride[..., None, None]
            delattr(model.model[-1], 'anchors')

        model.to(device).eval()

        with open(self.output, 'w') as f:
            f.write('{}\n'.format(len(model.state_dict().keys())))
            for k, v in model.state_dict().items():
                vr = v.reshape(-1).cpu().numpy()
                f.write('{} {} '.format(k, len(vr)))
                for vv in vr:
                    f.write(' ')
                    f.write(struct.pack('>f', float(vv)).hex())
                f.write('\n')

# # Example usage
# converter = gen_wts.from_args(
#     weights=r'E:\ALLvision\pycharmproject\Efficientnet\segjjc_clsseg_try\sahi_preprocess\1014\try\segjjc\yoloout\train12\weights\best.pt',
# )
# converter.convert()
