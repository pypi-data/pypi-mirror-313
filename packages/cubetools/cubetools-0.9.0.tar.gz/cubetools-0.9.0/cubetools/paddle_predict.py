# -*- coding: utf-8 -*-
import os
import paddle


# 基于Paddle-Inference封装的通用Paddle推理器
class Model(object):
    def __init__(self, model, use_paddle_inference=True, output_lod=False, gpu_memory_pool_init_size_mb=100, gpu_device_id=0, cpu_num_threads=1):
        self.use_paddle_inference = use_paddle_inference
        self.output_lod = output_lod
        if self.use_paddle_inference:
            if model.endswith('.pdmodel'):
                config = paddle.inference.Config(model, model.replace('.pdmodel', '.pdiparams'))
            elif os.path.exists(model + '__model__') or os.path.exists(model + '/__model__'):
                config = paddle.inference.Config(model)
            else:
                raise Exception('PaddlePaddle预训练模型路径无效：' + model)

            if paddle.get_device().startswith('gpu'):
                config.enable_use_gpu(gpu_memory_pool_init_size_mb, gpu_device_id)
                config.enable_memory_optim()
                paddle.tensor.zeros([1]) # 空操作，会触发调用gpu_context.cc来初始化GPU...
            else:
                config.disable_gpu()
                config.set_cpu_math_library_num_threads(cpu_num_threads)
                config.enable_memory_optim()

            self.predictor = paddle.inference.create_predictor(config)
            input_names = self.predictor.get_input_names()
            self.input_handles = []
            for input_name in input_names:
                self.input_handles.append(self.predictor.get_input_handle(input_name))
            output_names = self.predictor.get_output_names()
            self.output_handles = []
            for output_name in output_names:
                output_handle = self.predictor.get_output_handle(output_name)
                self.output_handles.append(output_handle)
        else:
            self.predictor = paddle.jit.load(model)
            self.predictor.eval()

    def predict(self, input_list: list) -> list:
        if self.use_paddle_inference:
            for i in range(len(input_list)):
                self.input_handles[i].copy_from_cpu(input_list[i])

            self.predictor.run()

            output_list = []
            for output_handle in self.output_handles:
                value = output_handle.copy_to_cpu()
                if self.output_lod:
                    lod = output_handle.lod()
                    output_list.append({'value': value, 'lod': lod})
                else:
                    output_list.append(value)
            self.predictor.clear_intermediate_tensor()  # 释放中间Tensor
            self.predictor.try_shrink_memory()  # 释放内存池中的所有临时Tensor
            return output_list
        else:
            results = self.predictor(paddle.to_tensor(input_list[0]))

            # 只有一个返回值时，转换成列表
            if not isinstance(results, list):
                results = [results]

            output_list = []
            for result in results:
                output_list.append(result.numpy())
            return output_list
