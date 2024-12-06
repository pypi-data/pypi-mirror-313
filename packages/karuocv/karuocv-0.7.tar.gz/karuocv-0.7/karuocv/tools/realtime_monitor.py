# _*_ encoding: utf-8 _*_
'''
@File    :realtime_monitor.py
@Desc    :
@Time    :2024/11/22 14:37:26
@Author  :caimmy@hotmail.com
@Version :0.1
'''

import mss
import cv2
import numpy as np
import supervision as sv
from PIL import Image
from karuocv.hub.inference import ImageAnnotator
import ctypes

def monit_screen(base_model: str, review_width: int = 1200, output: str = None, monitor_size: tuple = None):
    user32 = ctypes.windll.user32
    if not monitor_size:
        user32 = ctypes.windll.user32
        #单显示器屏幕宽度和高度:
        monitor_size = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        #对于多显示器设置,您可以检索虚拟显示器的组合宽度和高度:
        # screen_size1 = user32.GetSystemMetrics(78), user32.GetSystemMetrics(79)
    monitor_width, monitor_height = monitor_size
    review_height = int(monitor_height / (monitor_width / review_width))
    monitor = {"top":0, "left":0, "width": monitor_size[0], "height": monitor_size[1]}
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    fps = 20
    video = cv2.VideoWriter('output.avi', fourcc, fps, (review_width, review_height)) if output else None

    annotator = ImageAnnotator(base_model, verbose=False)
    _box_annotator = sv.BoxAnnotator()
    _label_annotator = sv.LabelAnnotator()
    
    with mss.mss() as sct:
        # 设置一个区域，top为距离屏幕左上角的垂直方向上的距离，left是水平方向的距离，后面2个分别是宽和高
        while True:
            image_sct = sct.grab(monitor)
            image_cv = np.asarray(image_sct)
            image_cv = cv2.resize(image_cv, (review_width, review_height))
            image_cv = cv2.cvtColor(image_cv, cv2.COLOR_BGRA2BGR)
            annotated_frame = annotator.fullAnnotateImage(image_cv, _box_annotator, _label_annotator)
            if video: video.write(annotated_frame)
            cv2.imshow("stream analysis", annotated_frame)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()
    if video:
        video.release()