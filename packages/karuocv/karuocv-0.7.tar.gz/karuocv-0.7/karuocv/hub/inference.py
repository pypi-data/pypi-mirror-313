# _*_ encoding: utf-8 _*_
'''
@文件    :inference.py
@说明    :
@时间    :2024/10/15 17:57:32
@作者    :caimmy@hotmail.com
@版本    :0.1
'''

import os
import cv2
import numpy as np
import collections
import supervision as sv
from karuocv.utils import genYOLOModel

class ImageAnalyser:
    def __init__(self, image_data: cv2.typing.MatLike):
        self._origin_image = image_data

    @classmethod
    def fromImageFile(cls, path: str):
        assert os.path.exists(path)
        img_data = cv2.imread(path)
        return ImageAnalyser(img_data)
    
    def drawGrayPicture(self):
        """转灰度图"""
        return cv2.cvtColor(self._origin_image, cv2.COLOR_BGR2GRAY)
    
    def drawContourPicture(self, dest_img: cv2.typing.MatLike = None, color: tuple=(0, 0, 0)):
        """
        寻找并绘制轮廓
        Arg:
            dest_img MatLike 输出图片数据，为空则新建一个白底图片
            color tuple 绘制轮廓的颜色
        Return:
            image_data MatLike
            contours Sequence[MatLike]
            hierarchy MatLike
        """
        if not dest_img:
            dest_img = np.ones(self._origin_image.shape, dtype=np.uint8) * 255
        gray_img = cv2.cvtColor(self._origin_image, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray_img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        assert ret
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(dest_img, contours, -1, color, 1)
        return dest_img, contours, hierarchy
    

class ImageAnnotator:
    def __init__(self, weights_file, confidence_threshold: float = 0.3, verbose: bool = False, device: str = None) -> None:
        """
        Args:
            weights_file str 模型文件的地址
        """
        self._weights_file = weights_file
        self._verbose = verbose
        self._model = genYOLOModel(self._weights_file, verbose, device)
        self._condidence_threshold = confidence_threshold

    def fullAnnotateImage(self, image: cv2.typing.MatLike, box_annotator: sv.BoxAnnotator = None, label_annotator: sv.LabelAnnotator = None, legend: bool = False) -> cv2.typing.MatLike:
        """
        对一幅图片进行完整注解
        Args:
            image MatLike 图片
            box_annotator 框选注解器
        Return:
            MatLike
        """
        result = self._model(image, verbose=self._verbose)[0]
        detections = sv.Detections.from_ultralytics(result)
        detections = detections[detections.confidence > self._condidence_threshold]
        if not box_annotator:
            box_annotator = sv.BoxAnnotator()
        if not label_annotator:
            label_annotator = sv.LabelAnnotator()
        labels = [
            f"{class_name} {confidence:.2f}"
            for class_name, confidence
            in zip(detections['class_name'], detections.confidence)
        ]
        annotated_frame = box_annotator.annotate(
            scene=image.copy(), 
            detections=detections
        )
        annotated_frame = label_annotator.annotate(
            scene=annotated_frame,
            detections=detections,
            labels=labels
        )
        if legend:
            annotated_frame = self.legendFrame(annotated_frame, detections, sv.Point(200, 200))
        return annotated_frame
    
    def legendFrame(self, frame, detections, archor_point: sv.Point):
        """
        为图片绘制图例
        """
        y_step_pix = 40
        _detection_objects = collections.Counter([str(n) for n in detections["class_name"]])

        for _item in _detection_objects:
            frame = sv.draw_text(
                frame, 
                f"{_item}: {_detection_objects[_item]}", 
                archor_point,
                sv.Color.WHITE,
                sv.calculate_optimal_text_scale(frame.shape[0:2]),
                background_color=sv.Color.BLUE
            )
            archor_point.y += y_step_pix

        return frame