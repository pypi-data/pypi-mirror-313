# -*- coding:utf-8 -*-
import mindspore_lite as mslite


# 基于MindSporeLite推理引擎封装的通用MindSporeLite推理器
# MindSporeLite模型加载步骤参见： https://www.mindspore.cn/lite/docs/zh-CN/r2.0.0-alpha/quick_start/quick_start_python.html
class Model(object):
    def __init__(self, model, device='CPU', thread_num=1, thread_affinity_mode=2, device_id=0):
        device = device.lower()
        if device == 'cpu':
            device_info = mslite.CPUDeviceInfo(enable_fp16=False)
        elif device == 'gpu':
            device_info = mslite.GPUDeviceInfo(device_id=device_id, enable_fp16=False)
        elif device == 'ascend':
            device_info = mslite.AscendDeviceInfo(device_id=device_id)
            cpu_device_info = mslite.CPUDeviceInfo(enable_fp16=False)
        else:
            raise Exception('Unsupported device: ' + device)

        context = mslite.Context(thread_num=thread_num, thread_affinity_mode=thread_affinity_mode)
        context.append_device_info(device_info)
        if device == 'ascend':
            context.append_device_info(cpu_device_info)

        self.model = mslite.Model()
        self.model.build_from_file(model, mslite.ModelType.MINDIR_LITE, context)


    def predict(self, input_list: list) -> list:
        model_inputs = self.model.get_inputs()
        model_outputs = self.model.get_outputs()
        for i, input_data in enumerate(input_list):
            model_inputs[i].set_data_from_numpy(input_data)

        self.model.predict(model_inputs, model_outputs)

        output_list = []
        for output in model_outputs:
            output_list.append(output.get_data_to_numpy())

        return output_list
