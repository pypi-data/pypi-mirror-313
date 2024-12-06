# _*_ encoding: utf-8 _*_
'''
@File    :sample_watch.py
@Desc    :
@Time    :2024/10/29 14:59:09
@Author  :caimmy@hotmail.com
@Version :0.1
'''

import os
import cv2
import numpy as np
import tqdm
import yaml
import shortuuid
from pathlib import Path
import pandas as pd
try:
    from yaml.loader import CLoader as Loader
except Exception as ImportError:
    from yaml.loader import Loader as Loader
from karuocv.hub.datautils import yolo_annotation_to_bbox

class SampleStatistics:
    def __init__(self, sample_path: str, dest_path: str = ""):
        self.sample_path = sample_path
        self.dest_path = dest_path if dest_path else os.path.join(self.sample_path, "statistic", "labels")
        Path(self.dest_path).mkdir(exist_ok=True)
        self.sample_configure = None
        self._parseDataYaml()

    def _parseDataYaml(self):
        _data_yaml = os.path.join(self.sample_path, "data.yaml")
        if os.path.exists(_data_yaml):
            with open(_data_yaml, mode="r", encoding="utf-8") as f:
                self.sample_configure = yaml.load(f, Loader=Loader)

    def CaptureLabels(self):
        if self.sample_configure:
            print(self.sample_configure)
        for sub in ["train", "test", "valid"]:
            self._walkSubPaths(sub)
        self.DoLabelsStatisticSummary()

    def _walkSubPaths(self, subpath: str):
        """遍历子目录，进行标注采样截图"""
        _worker_path = os.path.join(self.sample_path, "images", subpath)
        if os.path.exists(_worker_path):
            for _root, _, _files in os.walk(_worker_path):
                for _image_file in tqdm.tqdm(_files):
                    _pure_fname = _image_file.split(".")[0]
                    _image_abs_path = os.path.join(_root, _image_file)
                    _label_abs_path = os.path.join(self.sample_path, "labels", subpath, f"{_pure_fname}.txt")
                    if os.path.exists(_image_abs_path) and os.path.exists(_label_abs_path):
                        self._doSingleFileCapture(_image_abs_path, _label_abs_path, _pure_fname)

    def DoLabelsStatisticSummary(self):
        label_cnt_dict = {}
        subdirs = Path(self.dest_path).glob("*")
        for _subdir in subdirs:
            if _subdir.is_dir():
                label_name = _subdir.parts[-1]
                label_cnt = len(list(_subdir.glob("*.png")))
                label_cnt_dict.setdefault(label_name, label_cnt)
        statistic_df = pd.DataFrame(index=list(label_cnt_dict.keys()), columns=["数量"])
        statistic_df.loc[:, "数量"] = list(label_cnt_dict.values())
        statistic_df.to_excel(Path(self.dest_path).joinpath("summary.xlsx"))


    def _doSingleFileCapture(self, img_file: str, label_file: str, pure_name: str):
        _img_data = cv2.imread(img_file)
        _h, _w, _ = _img_data.shape
        _label_data = np.loadtxt(label_file)
        annotation_data = yolo_annotation_to_bbox(_label_data, _h, _w)
        merged_annotation_data = np.hstack([_label_data.reshape(-1, 5)[:, 0].reshape(-1, 1), annotation_data])
        for notation_item in merged_annotation_data:
            _name = self.sample_configure.get("names", [])[int(notation_item[0])]
            _dest_capture_img_path = os.path.join(self.dest_path, _name)
            os.makedirs(_dest_capture_img_path, exist_ok=True)
            x1, y1, x2, y2 = notation_item[1:]
            if x1 < 0: x1 = 0
            if y1 < 0: y1 = 0
            if x2 < 0: x2 = 0
            if y2 < 0: y2 = 0
            if x2 - x1 > 0 and y2 - y1 > 0:
                cv2.imwrite(os.path.join(_dest_capture_img_path, f"{pure_name}_{shortuuid.uuid()}.png"), _img_data[int(y1):int(y2), int(x1):int(x2)])
