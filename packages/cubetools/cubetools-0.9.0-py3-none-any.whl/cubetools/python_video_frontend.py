import random
import gradio as gr
from serviceboot.serviceboot import serviceboot_client, gen_api_docs


class PythonVideoFrontend(object):

    # 在__init__中定义Python前端界面
    def __init__(self,
                 model_name_cn,
                 model_name_en=None,
                 local_image=True,
                 local_video=True,
                 streaming_video=True,
                 show_image_results=False,
                 results2text=lambda x: x,
                 image_examples=[],
                 local_video_examples=[],
                 streaming_video_examples=[],
                 readme='README.md'
                 ):
        self.results2text = results2text if results2text else lambda x: x
        title = f'CubeAI应用示范——{model_name_cn}'
        if model_name_en:
            url_model_zoo = 'https://openi.pcl.ac.cn/cubeai-model-zoo/cubeai-model-zoo'
            url_model = f'https://openi.pcl.ac.cn/cubeai-model-zoo/{model_name_en}'
            description = f'源自 [《CubeAI模型示范库》]({url_model_zoo}) 项目： [{model_name_cn}]({url_model})'

        with gr.Blocks(title=title) as self.demo:
            gr.Markdown('<br/>')
            gr.Markdown(f'# <center>{title}</center>')
            gr.Markdown('<br/>')
            if model_name_en:
                gr.Markdown(description)
                gr.Markdown('<br/>')

            if local_image:
                with gr.Tab("本地图片"):
                    with gr.Row():
                        img1 = gr.Image(show_label=False).style(height='auto')
                        img2 = gr.Image(show_label=False)
                    btn_predict = gr.Button(value='预测')
                    image_results = gr.Textbox(label='预测结果：', visible=show_image_results)
                    self.error_image = gr.Textbox(label='出错了：', visible=False)
                    btn_predict.click(self.predict,
                                      inputs=[img1], outputs=[img2, image_results, self.error_image, self.error_image],
                                      preprocess=False, postprocess=False)
                    examples = [[example] for example in image_examples]
                    if examples:
                        gr.Examples(label='示例', examples=examples, inputs=[img1])

            if local_video:
                with gr.Tab("本地视频"):
                    playing_local_video = gr.Number(visible=False, value=0)
                    played_local_video = gr.Number(visible=False, value=0)  # 用于在一帧图像播放结束后触发一事件，继续获取下一帧
                    self.url_local_video = gr.Textbox(visible=False)
                    with gr.Row():
                        local_video = gr.Video(show_label=False)
                        img_local_video = gr.Image(show_label=False)
                    self.btn_play_local_video = gr.Button(value='循环播放')
                    self.btn_stop_local_video = gr.Button(value='暂停', visible=False)
                    self.error_local_video = gr.Textbox(label='出错了：', visible=False, interactive=False)

                    self.btn_play_local_video.click(self.play_local_video,
                                                    inputs=[local_video],
                                                    outputs=[img_local_video, self.url_local_video, playing_local_video,
                                                             played_local_video,
                                                             self.error_local_video, self.error_local_video,
                                                             self.btn_play_local_video, self.btn_stop_local_video],
                                                    show_progress=True, preprocess=True, postprocess=False)
                    local_video.play(self.play_local_video,
                                     inputs=[local_video],
                                     outputs=[img_local_video, self.url_local_video, playing_local_video,
                                              played_local_video,
                                              self.error_local_video, self.error_local_video,
                                              self.btn_play_local_video, self.btn_stop_local_video],
                                     show_progress=True, preprocess=True, postprocess=False)

                    self.btn_stop_local_video.click(self.stop_local_video,
                                                    outputs=[playing_local_video,
                                                             self.btn_play_local_video, self.btn_stop_local_video],
                                                    show_progress=False)
                    local_video.pause(self.stop_local_video,
                                      outputs=[playing_local_video,
                                               self.btn_play_local_video, self.btn_stop_local_video],
                                      show_progress=False)
                    local_video.stop(self.stop_local_video,
                                     outputs=[playing_local_video,
                                              self.btn_play_local_video, self.btn_stop_local_video],
                                     show_progress=False)

                    played_local_video.change(self.on_played_local_video,
                                              inputs=[playing_local_video, self.url_local_video],
                                              outputs=[img_local_video, played_local_video, self.error_local_video,
                                                       self.error_local_video],
                                              show_progress=False, preprocess=False, postprocess=False)
                    self.error_local_video.change(self.on_error_local_video,
                                                  inputs=[self.error_local_video],
                                                  outputs=[playing_local_video,
                                                           self.btn_play_local_video, self.btn_stop_local_video],
                                                  show_progress=False, preprocess=False, postprocess=False)

                    examples = [[example] for example in local_video_examples]
                    if examples:
                        gr.Examples(label='示例', examples=examples, inputs=[local_video])

            if streaming_video:
                with gr.Tab("云流媒体"):
                    playing_streaming_video = gr.Number(visible=False, value=0)
                    played_streaming_video = gr.Number(visible=False, value=0)  # 用于在一帧图像播放结束后触发一事件，继续获取下一帧
                    self.url_streaming_video = gr.Textbox(label='流媒体URL', value='rtsp://localhost:8554/stream')
                    self.btn_play_streaming_video = gr.Button(value='播放')
                    self.btn_stop_streaming_video = gr.Button(value='停止', visible=False)
                    img_streaming_video = gr.Image(show_label=False).style(height='auto')
                    self.error_video_streaming = gr.Textbox(label='出错了：', visible=False, interactive=False)

                    self.btn_play_streaming_video.click(self.play_streaming_video,
                                                        inputs=[self.url_streaming_video],
                                                        outputs=[img_streaming_video, playing_streaming_video,
                                                                 played_streaming_video,
                                                                 self.error_video_streaming, self.error_video_streaming,
                                                                 self.url_streaming_video,
                                                                 self.btn_play_streaming_video,
                                                                 self.btn_stop_streaming_video],
                                                        show_progress=True, preprocess=False, postprocess=False)
                    self.btn_stop_streaming_video.click(self.stop_streaming_video,
                                                        outputs=[playing_streaming_video, self.url_streaming_video,
                                                                 self.btn_play_streaming_video,
                                                                 self.btn_stop_streaming_video],
                                                        show_progress=False)
                    played_streaming_video.change(self.on_played_streaming_video,
                                                  inputs=[playing_streaming_video, self.url_streaming_video],
                                                  outputs=[img_streaming_video, played_streaming_video,
                                                           self.error_video_streaming,
                                                           self.error_video_streaming],
                                                  show_progress=False, preprocess=False, postprocess=False)
                    self.error_video_streaming.change(self.on_error_streaming_video,
                                                      inputs=[self.error_video_streaming],
                                                      outputs=[playing_streaming_video, self.url_streaming_video,
                                                               self.btn_play_streaming_video,
                                                               self.btn_stop_streaming_video],
                                                      show_progress=False, preprocess=False, postprocess=False)

                    examples = [['rtsp://localhost:8554/stream'], ['rtmp://localhost/stream/live']]
                    for example in streaming_video_examples:
                        examples.append([example])
                    gr.Examples(label='URL示例', examples=examples, inputs=[self.url_streaming_video])

            gr.Markdown('<br/>')
            args = []
            if local_image:
                args.append(self.predict)
            if streaming_video:
                args.append(self.predict_video)
            api_text = gen_api_docs(*args)
            btn_show_api = gr.Button(value='显示API文档')
            btn_hide_api = gr.Button(value='隐藏API文档', visible=False)
            api_docs = gr.Markdown(api_text, visible=False)
            btn_show_api.click(lambda: (btn_show_api.update(visible=False),
                                        btn_hide_api.update(visible=True),
                                        api_docs.update(visible=True)),
                               outputs=[btn_show_api, btn_hide_api, api_docs])
            btn_hide_api.click(lambda: (btn_show_api.update(visible=True),
                                        btn_hide_api.update(visible=False),
                                        api_docs.update(visible=False)),
                               outputs=[btn_show_api, btn_hide_api, api_docs])

            gr.Markdown('<br/>')
            if readme:
                gr.Markdown(open(readme).read())

    # 在launch方法中启动Python前端服务，必须存在
    def launch(self, **kwargs):
        self.demo.launch(**kwargs)

    def predict(self, img):
        result = serviceboot_client('predict', img=img)
        if result['status'] == 'ok':
            results, img = result['value']
            return img, self.results2text(results), '', self.error_image.update(visible=False)
        return None, '', result['value'], self.error_image.update(visible=True)

    def predict_video(self, url):
        return serviceboot_client('predict_video', url=url)['value']

    def play_local_video(self, local_video):
        url = 'file://' + local_video
        img_or_err = self.predict_video(url)
        if img_or_err.startswith('data:image'):
            return img_or_err, url, 1, random.random(), '', \
                   self.error_local_video.update(visible=False), \
                   self.btn_play_local_video.update(visible=False), \
                   self.btn_stop_local_video.update(visible=True)
        return None, url, 0, 0, img_or_err, \
               self.error_local_video.update(visible=True), \
               self.btn_play_local_video.update(visible=True), \
               self.btn_stop_local_video.update(visible=False)

    def on_played_local_video(self, playing, url):
        if playing:
            img_or_err = self.predict_video(url)
            if img_or_err.startswith('data:image'):
                return img_or_err, random.random(), '', self.error_local_video.update(visible=False)
            return None, 0, img_or_err, self.error_local_video.update(visible=True)
        return None  # 这里会抛出异常，因为正常返回值应该是多个。为了在按停止按钮后仍保留视频画面，故意这样写的。

    def stop_local_video(self):
        return 0, \
               self.btn_play_local_video.update(visible=True), \
               self.btn_stop_local_video.update(visible=False)

    def on_error_local_video(self, error):
        if error:
            return 0, \
                   self.btn_play_local_video.update(visible=True), \
                   self.btn_stop_local_video.update(visible=False)
        return None  # 这里会抛出异常，因为正常返回值应该是多个。为了在主动清空error时不改变状态，故意这样写的。

    def play_streaming_video(self, url):
        img_or_err = self.predict_video(url)
        if img_or_err.startswith('data:image'):
            return img_or_err, 1, random.random(), '', \
                   self.error_video_streaming.update(visible=False), \
                   self.url_streaming_video.update(interactive=False), \
                   self.btn_play_streaming_video.update(visible=False), \
                   self.btn_stop_streaming_video.update(visible=True)
        return None, 0, 0, img_or_err, \
               self.error_video_streaming.update(visible=True), \
               self.url_streaming_video.update(interactive=True), \
               self.btn_play_streaming_video.update(visible=True), \
               self.btn_stop_streaming_video.update(visible=False)

    def on_played_streaming_video(self, playing_streaming_video, url):
        if playing_streaming_video:
            img_or_err = self.predict_video(url)
            if img_or_err.startswith('data:image'):
                return img_or_err, random.random(), '', self.error_video_streaming.update(visible=False)
            return None, 0, img_or_err, self.error_video_streaming.update(visible=True)
        return None  # 这里会抛出异常，因为正常返回值应该是多个。为了在按停止按钮后仍保留视频画面，故意这样写的。

    def stop_streaming_video(self):
        return 0, \
               self.url_streaming_video.update(interactive=True), \
               self.btn_play_streaming_video.update(visible=True), \
               self.btn_stop_streaming_video.update(visible=False)

    def on_error_streaming_video(self, error):
        if error:
            return 0, \
                   self.url_streaming_video.update(interactive=True), \
                   self.btn_play_streaming_video.update(visible=True), \
                   self.btn_stop_streaming_video.update(visible=False)
        return None  # 这里会抛出异常，因为正常返回值应该是多个。为了在主动清空error时不改变状态，故意这样写的。
