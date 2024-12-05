# -*- coding: utf-8 -*-
import cv2
import time
import threading


class VideoPredict2(object):

    def __init__(self, callback_predict, with_url=False, callback_clean_buf=None):
        self.callback_predict = callback_predict
        self.predict_with_url = with_url
        self.callback_clean_buf = callback_clean_buf
        self.playlist = {}

    def read_predict(self, url):
        if url in self.playlist:
            if self.playlist[url]['frame_buffer'] is None:
                raise Exception(f'源自 {url} 的流媒体播放结束！')

            self.playlist[url]['last_pull'] = time.time()

            current_frame = self.playlist[url]['frame_buffer'][0]
            for result in self.playlist[url]['result_buffer'][::-1]:
                if current_frame[0] >= result[0]:
                    return current_frame[1], result[1]

            return current_frame[1], None

        camera = cv2.VideoCapture(url)
        if not camera.isOpened():
            raise Exception(f'从给定URL（{url}）获取流媒体数据失败！')

        thread = threading.Thread(
            target=self.loop_capture_video,
            args=(url, camera)
        )
        thread.setDaemon(True)
        thread.start()

        # 处理第一帧请求
        while url not in self.playlist:
            time.sleep(0.01)

        # 等待第一个有效推理结果
        while len(self.playlist[url]['result_buffer']) < 1 or self.playlist[url]['result_buffer'][0] is None:
            time.sleep(0.01)

        return self.playlist[url]['frame_buffer'][0][1], self.playlist[url]['result_buffer'][0][1]

    def loop_capture_video(self, url, camera):
        fps = camera.get(cv2.CAP_PROP_FPS)
        if fps <= 0 or fps > 30:
            fps = 30

        self.playlist[url] = {
            'last_pull': time.time(),
            'frame_duration': 1.0 / fps,
            'frame_overtime': 0,
            'frame_buffer': [],  # 视频帧缓冲队列， 每个元素为一个元组： (帧编号, 帧图像）
            'current_frame_no': 0,
            'predcting_frame_no': -1,
            'result_buffer': [],  # 推理结果缓冲队列， 每个元素为一个元组： (帧编号, 帧图像推理结果）
            'valid_result_count': 0,
        }

        thread = threading.Thread(
            target=self.loop_predict_video,
            args=(url, )
        )
        thread.setDaemon(True)
        thread.start()

        while camera and camera.isOpened():
            t1 = time.time()
            # 如果长时间（此处设为10秒）没有来自客户端关于该URL的请求，则不再捕获来自该URL的流媒体，并清空缓存
            if t1 - self.playlist[url]['last_pull'] > 10:
                break

            status, frame = camera.read()
            if status:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                current_frame = (self.playlist[url]['current_frame_no'], frame)
                self.playlist[url]['current_frame_no'] += 1
                self.playlist[url]['frame_buffer'].append(current_frame)

                # 当获得1个以上有效推理结果之后，在每次读取一帧新图像之后，从缓冲队列头部移除一帧，并移除过时的推理结果
                if self.playlist[url]['valid_result_count'] > 0:
                    if len(self.playlist[url]['frame_buffer']) > 0:
                        poped_frame_no = self.playlist[url]['frame_buffer'][0][0]
                        self.playlist[url]['frame_buffer'].pop(0)
                        # 移除过时的推理结果
                        if len(self.playlist[url]['result_buffer']) > 1 and self.playlist[url]['result_buffer'][1][0] <= poped_frame_no:
                            self.playlist[url]['result_buffer'].pop(0)

                t2 = time.time()
                # time to wait [s] to fulfill input fps
                wait_time = self.playlist[url]['frame_duration'] - (t2 - t1)

                if wait_time >= 0:
                    # wait until
                    time.sleep(wait_time)
                else:
                    # 本场景下这种情况基本不会发生，暂保留代码
                    self.playlist[url]['frame_overtime'] -= wait_time
                    while self.playlist[url]['frame_overtime'] > self.playlist[url]['frame_duration']:
                        # 超时，跳帧
                        camera.read()
                        self.playlist[url]['frame_overtime'] -= self.playlist[url]['frame_duration']
            else:
                # 流媒体源播放结束
                if url.startswith('file://'):
                    break

                self.playlist[url]['frame_buffer'] = None  # 用于标记播放结束
                time.sleep(0.1)

        camera.release()
        self.playlist.pop(url)
        if self.callback_clean_buf is not None:
            self.callback_clean_buf(url)

    def loop_predict_video(self, url):
        while url in self.playlist and self.playlist[url]['frame_buffer'] is not None:
            while len(self.playlist[url]['frame_buffer']) < 1:
                time.sleep(0.01)

            # 每次循环取出视频帧缓冲区中的最后一帧图像进行推理
            predicting_frame = self.playlist[url]['frame_buffer'][-1]

            # 避免对同一帧图像进行重复推理
            if len(self.playlist[url]['result_buffer']) < 1 or predicting_frame[0] > self.playlist[url]['result_buffer'][-1][0]:
                self.playlist[url]['predcting_frame_no'] = predicting_frame[0]
                try:
                    if self.predict_with_url:
                        predict_result = self.callback_predict(predicting_frame[1], url)
                    else:
                        predict_result = self.callback_predict(predicting_frame[1])
                    self.playlist[url]['valid_result_count'] += 1
                except:
                    predict_result = None

                if predict_result is not None and url in self.playlist:
                    self.playlist[url]['result_buffer'].append((predicting_frame[0], predict_result))
            else:
                time.sleep(0.01)
