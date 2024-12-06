# _*_ encoding: utf-8 _*_
'''
@File    :utils.py
@Desc    :
@Time    :2024/10/16 21:23:16
@Author  :caimmy@hotmail.com
@Version :0.1
'''

import os
import logging
import logging.handlers
import torch
import yaml
from ultralytics import YOLO
import supervision as sv
import cv2
from dotenv import load_dotenv
from pathlib import Path

env_file = Path("./.env").absolute()
load_dotenv(env_file)
debug_mode = os.getenv("DEBUG_MODE", "noset").lower()


logger_fmt = '%(asctime)s %(filename)s %(lineno)d %(levelname)s %(message)s'
logger_level = logging.DEBUG if "on" == debug_mode else logging.WARN

logging.basicConfig(level=logger_level,
    format=logger_fmt,
    datefmt='%a %d %b %Y %H:%M:%S')

logger = logging.getLogger(__name__)



def checkPathEmptyOrNull(path: str) -> bool:
    """检查路径是否为空或者不存在"""
    if os.path.exists(path) and len(os.listdir(path)) > 0:
        return False
    return True

def queryDeviceName() -> str:
    """获取训练设备标识"""
    device_name = "cpu"
    if torch.cuda.is_available():
        device_name = "cuda:0"
    elif torch.backends.mps.is_available():
        device_name = "mps"
    return device_name

def genYOLOModel(base_model: str, verbose=False, device=None):
    _model = YOLO(base_model, verbose=verbose)
    if not device:
        if torch.cuda.is_available():
            _model.to("cuda:0")
    else:
        _model.to(device)
    return _model

def train(train_cfg_file: str, base_model: str="yolov8n.pt", epochs: int=200, batch_size=16, device=None, verbose=False, hyper_parameters=None):
    """
    执行样本训练
    @param train_cfg_file str 训练配置文件的路径
    @param weights_file str 模型文件的路径
    """
    hp = {}
    if os.path.exists(hyper_parameters):
        with open(hyper_parameters, "r", encoding="utf-8") as rf:
            hp = yaml.safe_load(rf)
    if os.path.exists(train_cfg_file) and os.path.exists(train_cfg_file):
        model = genYOLOModel(base_model, verbose)
        if hp:
            logger.info(f"use special hyper_parameters. --> {hyper_parameters}")
        model.train(data=train_cfg_file, epochs=epochs, workers=0, batch=batch_size, verbose=verbose, device=device if device else queryDeviceName(), **hp)
        logger.info("------------ train completed ------------")
    else:
        logger.error(f"未找到训练配置文件路径。 {train_cfg_file}")

def tune(train_cfg_file: str, base_model: str, epochs: int=30, iterations: int=300, device: str=None, verbose: bool=False):
    """
    超参数调整
    """
    if os.path.exists(train_cfg_file) and os.path.exists(base_model):
        model = genYOLOModel(base_model, verbose, device)
        tune_result = model.tune(data=train_cfg_file, epochs=epochs, iterations=iterations, optimizer="AdamW", workers=0, plots=False, save=False, val=False, device=device)
        logger.info("------------ tune completed ------------")
        return tune_result
    else:
        logger.error(f"未找到训练配置文件路径。 {train_cfg_file}")
        return None

def _watch_sample(weight_file: str, image_file: str, label_file: str="", annotator = None, show: bool = True, output: str = ""):
    if not label_file:
        label_file = image_file.replace("images", "labels")
        label_file = image_file.replace("jpg", "txt")
        label_file = image_file.replace("jpeg", "txt")
    assert os.path.exists(image_file)
    assert os.path.exists(label_file)
    if not annotator:
        annotator = sv.BoxCornerAnnotator()
    label_annotator = sv.LabelAnnotator()
    
    model = genYOLOModel(weight_file)
    image = cv2.imread(image_file)
    results = model(image)[0]
    detections = sv.Detections.from_ultralytics(results)
    labels = [
        f"{class_name} {confidence:.2f}"
        for class_name, confidence
        in zip(detections['class_name'], detections.confidence)
    ]
    annotated_frame = annotator.annotate(image.copy(), detections)
    annotated_frame = label_annotator.annotate(annotated_frame, detections, labels=labels)
    if show:
        cv2.imshow("watch sample", annotated_frame)
        cv2.waitKey(0)

def _split_samples(src_path: str, dst_path: str, train_ratio: float, test_ratio: float) -> bool:
    """
    拆分样本数据集
    """
    # 源样本文件目录必须存在
    assert os.path.exists(src_path)
    # 目标样本文件目录必须不存在
    assert not os.path.exists(dst_path)
    # 训练样本率 + 测试样本率 必须小于1
    assert train_ratio + test_ratio < 1

    # for _root, _dir, _files in os.walk(src_path)