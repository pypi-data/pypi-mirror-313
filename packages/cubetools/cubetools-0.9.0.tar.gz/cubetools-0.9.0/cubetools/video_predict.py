# -*- coding: utf-8 -*-
import cv2
import time
import threading


class VideoPredict(object):

    def __init__(self, callback_predict, with_url=False, callback_clean_buf=None):
        self.callback_predict = callback_predict
        self.predict_with_url = with_url
        self.callback_clean_buf = callback_clean_buf
        self.playlist = {}
        self.lock = threading.Lock()

    def read_predict(self, url):
        if url in self.playlist:
            self.playlist[url]['last_pull'] = int(time.time())
            while 'predict_results' not in self.playlist[url]:
                time.sleep(0.01)
            with self.lock:
                predict_results = self.playlist[url]['predict_results']
            if predict_results is None:
                raise Exception(f'源自 {url} 的流媒体播放结束！')
            return predict_results

        camera = cv2.VideoCapture(url)
        if not camera.isOpened():
            raise Exception(f'从给定URL（{url}）获取流媒体数据失败！')

        thread = threading.Thread(
            target=self.capture_and_predict,
            args=(url, camera)
        )
        thread.setDaemon(True)
        thread.start()

        while url not in self.playlist:
            time.sleep(0.01)

        while 'predict_results' not in self.playlist[url]:
            time.sleep(0.01)

        with self.lock:
            predict_results = self.playlist[url]['predict_results']
        if predict_results is None:
            raise Exception(f'源自 {url} 的流媒体播放结束！')
        return predict_results

    def capture_and_predict(self, url, camera):
        fps = camera.get(cv2.CAP_PROP_FPS)
        if fps <= 0 or fps > 30:
            fps = 30

        self.playlist[url] = {
            'last_pull': int(time.time()),
            'frame_duration': 1.0 / fps,
            'frame_overtime': 0
        }

        while camera and camera.isOpened():
            t1 = time.time()
            # 如果长时间（此处设为10秒）没有来自客户端关于该URL的请求，则不再捕获来自该URL的流媒体，并清空缓存
            if int(t1) - self.playlist[url]['last_pull'] > 10:
                break

            status, frame = camera.read()
            if status:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                try:
                    predict_results = self.callback_predict(frame, url) if self.predict_with_url else self.callback_predict(frame)
                except:
                    predict_results = None

                if predict_results is not None:
                    with self.lock:
                        self.playlist[url]['predict_results'] = predict_results

                t2 = time.time()
                # time to wait [s] to fulfill input fps
                wait_time = self.playlist[url]['frame_duration'] - (t2 - t1)

                if wait_time >= 0:
                    # wait until
                    time.sleep(max(0, wait_time))
                else:
                    self.playlist[url]['frame_overtime'] -= wait_time
                    while self.playlist[url]['frame_overtime'] > self.playlist[url]['frame_duration']:
                        # 推理超时，跳帧
                        camera.read()
                        self.playlist[url]['frame_overtime'] -= self.playlist[url]['frame_duration']
            else:
                # 流媒体源播放结束
                if url.startswith('file://'):
                    break

                with self.lock:
                    self.playlist[url]['predict_results'] = None
                time.sleep(0.1)

        camera.release()
        self.playlist.pop(url)
        if self.callback_clean_buf is not None:
            self.callback_clean_buf(url)
