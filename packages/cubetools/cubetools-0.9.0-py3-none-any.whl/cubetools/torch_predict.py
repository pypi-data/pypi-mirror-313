# -*- coding:utf-8 -*-
import gc
import torch
try:
    import torch_npu
except:
    pass
from copy import deepcopy


# 通用PyTorch推理框架
# 为了兼容之前版本，特新建一个文件
class Model(object):
    def __init__(self, net, model_path, device='auto', half=False, param_key=None, remove_key_prefix=None, strict=True,
                 cudnn_benchmark=False):
        if cudnn_benchmark:
            import torch.backends.cudnn as cudnn
            cudnn.benchmark = True

        if device == 'auto':
            device = 'cpu'
            if hasattr(torch, "npu") and torch.npu.is_available():
                device = 'npu'
            if torch.cuda.is_available():
                device = 'cuda'

        self.device = torch.device(device)
        self.cpu_device = torch.device('cpu')
        self.half = half and (self.device.type.startswith('cuda') or self.device.type.startswith('npu'))

        if net is not None:
            if model_path.endswith('.safetensors'):
                from safetensors.torch import load_file
                net_params = load_file(model_path)
            else:
                net_params = torch.load(model_path, map_location=self.cpu_device)
            if param_key is not None and param_key in net_params:
                net_params = net_params[param_key]

            # remove unnecessary key_prefix
            if remove_key_prefix is not None:
                for k, v in deepcopy(net_params).items():
                    if k.startswith(remove_key_prefix):
                        # remove_key_prefix 应为以“.”结尾的字符串，例如： 'module.', 'model.'
                        net_params[k[len(remove_key_prefix):]] = v
                        net_params.pop(k)

            net.load_state_dict(net_params, strict=strict)
            self.model = net
        else:
            self.model = torch.jit.load(model_path, map_location=self.cpu_device)

        if self.half:
            self.model = self.model.half()

        self.model.eval()
        self.model = self.model.to(self.device)

    def predict(self, inputs):
        inputs = self.to_device(inputs, self.device)

        with torch.no_grad():
            if isinstance(inputs, dict):
                results = self.model(**inputs)
            elif isinstance(inputs, list):
                results = self.model(*inputs)
            else:
                results = self.model(inputs)

        results = self.to_device(results, self.cpu_device)
        gc.collect()
        if self.device.type.startswith('cuda'):
            torch.cuda.empty_cache()
        if self.device.type.startswith('npu'):
            torch.npu.empty_cache()
        return results

    def to_device(self, data, device):
        if isinstance(data, tuple):
            data = list(data)

        if isinstance(data, torch.Tensor):
            if self.half:
                if device.type.startswith('cuda') or self.device.type.startswith('npu'):
                    data = data.half()
                else:  # to 'cpu' for results
                    data = data.float()
            data = data.to(device)
        elif isinstance(data, dict):
            for k, v in data.items():
                data[k] = self.to_device(v, device)
        elif isinstance(data, list):
            for i in range(len(data)):
                data[i] = self.to_device(data[i], device)

        return data
