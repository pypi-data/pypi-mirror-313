# -*- coding:utf-8 -*-
from openvino.runtime import Core


# 基于OpenVino推理引擎封装的通用OpenVino推理器
class Model(object):
    def __init__(self, model, device='AUTO', input_shape=None):
        self.core = Core()
        self.model = self.core.read_model(model=model)
        if input_shape is not None:
            self.model.reshape(input_shape)
        self.compiled_model = self.core.compile_model(model=self.model, device_name=device)
        self.input_keys = self.compiled_model.inputs
        self.output_keys = self.compiled_model.outputs

    def predict(self, input_list: list) -> list:
        results = self.compiled_model(input_list)

        output_list = []
        for output_key in self.output_keys:
            output_list.append(results[output_key])

        return output_list
