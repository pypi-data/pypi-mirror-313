import gradio as gr
from serviceboot.serviceboot import serviceboot_client, gen_api_docs


class PythonChatFrontend(object):

    # 在__init__中定义Python前端界面
    def __init__(self, model_name_cn, model_name_en=None, readme='README.md'):
        title = f'CubeAI应用示范——{model_name_cn}'
        if model_name_en:
            url_model_zoo = 'https://openi.pcl.ac.cn/cubeai-model-zoo/cubeai-model-zoo'
            url_model = f'https://openi.pcl.ac.cn/cubeai-model-zoo/{model_name_en}'
            description = f'源自 [《CubeAI模型示范库》]({url_model_zoo}) 项目： [{model_name_cn}]({url_model})'

            with gr.Blocks(title=title) as self.demo:
                gr.Markdown('<br/>')
                gr.Markdown(f'# <center>{title}</center>')
                gr.Markdown('<br/>')
                gr.Markdown(description)

                history = gr.Chatbot(label='聊天室')
                text = gr.Textbox(label='提问')
                text.submit(self.predict, inputs=[text, history], outputs=[history, text])

                gr.Markdown('<br/>')
                api_text = gen_api_docs(self.predict)
                btn_show_api = gr.Button(value='显示API文档')
                btn_hide_api = gr.Button(value='隐藏API文档', visible=False)
                api_docs = gr.Markdown(api_text, visible=False)
                btn_show_api.click(lambda: (
                btn_show_api.update(visible=False), btn_hide_api.update(visible=True), api_docs.update(visible=True)),
                                   outputs=[btn_show_api, btn_hide_api, api_docs])
                btn_hide_api.click(lambda: (
                btn_show_api.update(visible=True), btn_hide_api.update(visible=False), api_docs.update(visible=False)),
                                   outputs=[btn_show_api, btn_hide_api, api_docs])

                gr.Markdown('<br/>')
                if readme:
                    gr.Markdown(open(readme).read())

    # 在launch方法中启动Python前端服务，必须存在
    def launch(self, **kwargs):
        self.demo.launch(**kwargs)

    def predict(self, text, history):
        result = serviceboot_client('predict', text=text, history=history)

        if result['status'] == 'ok':
            history.append((text, result['value']['response']))
            return history, ''

        raise gr.Error(result['value'])
