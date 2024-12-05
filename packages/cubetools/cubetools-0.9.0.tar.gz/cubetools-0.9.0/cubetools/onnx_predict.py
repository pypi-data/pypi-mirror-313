# -*- coding: utf-8 -*-
import onnxruntime


# 基于ONNX Runtime封装的通用ONNX推理器
class Model(object):
    def __init__(self, model):
        providers = ['CUDAExecutionProvider', 'CPUExecutionProvider']
        self.session = onnxruntime.InferenceSession(model, providers=providers)

    def predict(self, input_list: list) -> list:
        input_dict = {}
        session_inputs = self.session.get_inputs()
        for i, data in enumerate(input_list):
            input_dict[session_inputs[i].name] = data

        output_list = self.session.run(None, input_dict)

        return output_list
