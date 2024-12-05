# -*- coding: utf-8 -*-
import cv2
import time
import threading


class VideoCapture(object):

    def __init__(self):
        self.playlist = {}
        self.lock = threading.Lock()

    def capture_frame(self, url):
        if url in self.playlist:
            self.playlist[url]['last_pull'] = int(time.time())
            while 'frame' not in self.playlist[url]:
                time.sleep(0.01)
            with self.lock:
                frame = self.playlist[url]['frame']
            if frame is None:
                raise Exception(f'源自 {url} 的流媒体播放结束！')
            return frame

        camera = cv2.VideoCapture(url)
        if not camera.isOpened():
            raise Exception(f'从给定URL（{url}）获取流媒体数据失败！')

        thread = threading.Thread(
            target=self.gen_frames,
            args=(url, camera)
        )
        thread.setDaemon(True)
        thread.start()

        while url not in self.playlist:
            time.sleep(0.01)

        while 'frame' not in self.playlist[url]:
            time.sleep(0.01)

        with self.lock:
            frame = self.playlist[url]['frame']
        if frame is None:
            raise Exception(f'源自 {url} 的流媒体播放结束！')
        return frame

    def gen_frames(self, url, camera):
        fps = camera.get(cv2.CAP_PROP_FPS)
        if fps <= 0:
            fps = 60
        self.playlist[url] = {
            'last_pull': int(time.time()),
            'fps': fps
        }

        while camera and camera.isOpened():
            t1 = time.time()
            # 如果长时间（此处设为10秒）没有来自客户端关于该URL的请求，则不再捕获来自该URL的流媒体，并清空缓存
            if int(t1) - self.playlist[url]['last_pull'] > 10:
                break

            status, frame = camera.read()
            if status:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                with self.lock:
                    self.playlist[url]['frame'] = frame

                t2 = time.time()
                # time to wait [s] to fulfill input fps
                wait_time = 1.0 / self.playlist[url]['fps'] - (t2 - t1)
                # wait until
                time.sleep(max(0, wait_time))
            else:
                # 流媒体源播放结束
                with self.lock:
                    self.playlist[url]['frame'] = None
                time.sleep(0.1)

        camera.release()
        self.playlist.pop(url)
