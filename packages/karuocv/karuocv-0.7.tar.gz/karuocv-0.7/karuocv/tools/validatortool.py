# -*- encoding: utf-8 -*-
'''
@文件    :validatortool.py
@说明    :
@时间    :2024/10/25 16:18:36
@作者    :caimiao@kingsoft.com
@版本    :0.1
'''

import os
import sys
import tqdm
import datetime
from ultralytics import YOLO
import cv2
from pathlib import Path 
import yaml
import pandas as pd
import supervision as sv
import numpy as np
import matplotlib.pyplot as plt
from karuocv.hub.datautils import yolo_annotation_to_bbox
from karuocv.hub.inference import ImageAnnotator
from collections import Counter
from sklearn.model_selection import KFold
import shutil
from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError as e:
    from yaml import Loader
import logging

logger = logging.getLogger(__file__)


class RegressionAnnotationTool:
    """
    把所有的标注样本信息都显示出来，分别显示标注信息和推理信息
    """
    def __init__(self, base_model: str, dataset: str, dest: str = None) -> None:
        self.base_model = base_model
        self.dataset = Path(dataset).absolute()
        _dest = dest if dest else os.path.join(dataset, "checks")
        self.dest = Path(_dest).absolute()
        self.annotator = None
        self.dataset_names = {}
        self.split_flag = '\\' if sys.platform == "win32" else "/"

    def _annotation(self, image_file: str, label_file: str, mixer_file: str):
        cv_img = cv2.imread(f"{image_file}")
        inference_img = cv_img.copy()
        _label_boxes = np.loadtxt(f"{label_file}") 
        _h, _w, _dtp = cv_img.shape
        _label_boxes = _label_boxes.reshape(-1, 5)
        _label_list = _label_boxes[:, 0]
        boxes_list = yolo_annotation_to_bbox(_label_boxes, _h, _w)
        logger.debug("flag data:")
        for _label, _box in zip(_label_list, boxes_list):
            _label_id = int(_label)
            logger.debug(f"label id: {_label_id} -> label_name: {self.dataset_names.get(_label_id)}")
            _x1, _y1, _x2, _y2 = _box
            cv2.rectangle(cv_img, (_x1, _y1), (_x2, _y2), (0, 255, 0), 2)
            cv2.putText(cv_img, f"{self.dataset_names.get(_label_id)}[id: {_label_id}]", (_x1, _y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            cv2.putText(cv_img, f"ori: {image_file.split(self.split_flag)[-1]}", (15, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        
        dest_img = np.ones((_h, _w * 2, _dtp), dtype=np.uint8) * 255
        _annotated_image = self.annotator.fullAnnotateImage(inference_img, legend=True)
        cv2.putText(_annotated_image, f"inference: {image_file.split(self.split_flag)[-1]}", (15, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        sv.draw_image(dest_img, cv_img, 1, sv.Rect(0, 0, _w, _h))
        sv.draw_image(dest_img, _annotated_image, 1, sv.Rect(_w, 0, _w, _h))
        cv2.imwrite(mixer_file, dest_img)

    def _loadObjectNames(self, cfg_file: str):
        """
        从当前数据集的配置文件中获取对象名称列表
        """
        names = {}
        with open(cfg_file, "r", encoding="utf-8") as f:
            data_configure = load(f, Loader=Loader)
            names = data_configure.get("names", [])
            
        return names

    def walkCheckDataset(self):
        self.annotator = ImageAnnotator(self.base_model)
        if os.path.exists(self.dataset):
            configure_yaml = os.path.join(self.dataset, "data.yaml")
            if os.path.exists(configure_yaml):
                self.dataset_names = self._loadObjectNames(configure_yaml)
                os.makedirs(self.dest, exist_ok=True)
                subdirs = ["train", "test", "valid"]
                for _sub in subdirs:
                    _image_path = os.path.join(self.dataset, "images", _sub)
                    _label_path = os.path.join(self.dataset, "labels", _sub)
                    if os.path.exists(_image_path) and os.path.exists(_label_path):
                        logger.info(f"check image path {_sub}")
                        for _root, _, _files in os.walk(_image_path):
                            for _f in tqdm.tqdm(_files):
                                _fname = _f.split(".")[0]
                                _image_file = os.path.join(_root, _f)
                                _label_file = os.path.join(_label_path, f"{_fname}.txt")
                                if os.path.exists(_image_file) and os.path.exists(_label_file):
                                    self._annotation(_image_file, _label_file, os.path.join(self.dest, f"{_sub}_{_fname}.jpg"))
            else:
                logger.error(f"please confirm configure file data.yaml exists!")
        else:
            logger.info(f"please checkout path valid {self.dataset}")


class KFolderCrossVal:
    def __init__(self, base_model: str, k: int, dataset_path: str, random_state: int = None):
        """
        Args:
            base_model str : 底座模型的路径
            k int : 分割数量
            dataset_path str : yolo数据集的路径
            random_state int : 随机种子
        """
        self._weight_file = base_model
        self.dataset_path = Path(dataset_path)
        self.k = k
        self._random_state = random_state
        self.classes = {}
        self.labels = []
        self.cls_idx = []
        self._cache_df_file = self.dataset_path / "./k_folder_cross_val_labels_df.pkl"
        self.ds_yamls = []
        self._project_name = f"{datetime.date.today().isoformat()}_{self.k}-Fold_Cross-val"
        self.labels_df = None
        self.labels_df = self._dataframe_init()
    
    def _dataframe_init(self):
        self.labels = sorted(self.dataset_path.rglob("labels/*/*.txt"))
        yaml_file = os.path.join(self.dataset_path, "data.yaml")
        with open(yaml_file, "r", encoding="utf-8") as y:
            self.classes = yaml.safe_load(y)["names"]
        self.cls_idx = sorted(self.classes.keys())

        indx = [label.stem for label in self.labels]
        labels_df = pd.DataFrame([], columns=self.cls_idx, index=indx)

        if self._cache_df_file.exists():
            labels_df = pd.read_pickle(self._cache_df_file)
        else:
            for label in tqdm.tqdm(self.labels):
                lbl_counter = Counter()
                with open(label, "r") as lf:
                    lines = lf.readlines()
                for line in lines:
                    lbl_counter[int(line.split(" ")[0])] += 1
                labels_df.loc[label.stem] = lbl_counter
            labels_df = labels_df.fillna(0.0)
            labels_df.to_pickle(self._cache_df_file)
        return labels_df

    def PrepareDataset(self):
        """
        分析yolo数据集，并进行数据拆分
        """
        self.labels = sorted(self.dataset_path.rglob("labels/*/*.txt"))
        indx = self.labels_df.index.to_list()
        cls_idx = self.labels_df.columns.to_list()
        kf = KFold(n_splits=self.k, shuffle=True, random_state=self._random_state)
        kfolds = list(kf.split(self.labels_df))

        folds = [f"split_{n}" for n in range(1, self.k + 1)]
        folds_df = pd.DataFrame(index=indx, columns=folds)
        for idx, (train, val) in enumerate(kfolds, start=1):
            folds_df[f"split_{idx}"].loc[self.labels_df.iloc[train].index] = "train"
            folds_df[f"split_{idx}"].loc[self.labels_df.iloc[val].index] = "val"

        fold_lbl_distrb = pd.DataFrame(index=folds, columns=cls_idx)
        for n, (train_indices, val_indices) in enumerate(kfolds, start=1):
            train_totals = self.labels_df.iloc[train_indices].sum()
            val_totals = self.labels_df.iloc[val_indices].sum()

            ratio = val_totals / (train_totals + 1e-7)
            fold_lbl_distrb.loc[f"split_{n}"] = ratio

        supported_extensions = [".jpg", ".jpeg", ".png"]

        images = []

        for ext in supported_extensions:
            images.extend(sorted((self.dataset_path / "images").rglob(f"*{ext}")))

        save_path = Path(self.dataset_path / self._project_name)
        save_path.mkdir(parents=True, exist_ok=True)

        for split in folds_df.columns:
            split_dir = save_path / split
            split_dir.mkdir(parents=True, exist_ok=True)
            (split_dir / "train" / "images").mkdir(parents=True, exist_ok=True)
            (split_dir / "train" / "labels").mkdir(parents=True, exist_ok=True)
            (split_dir / "val" / "images").mkdir(parents=True, exist_ok=True)
            (split_dir / "val" / "labels").mkdir(parents=True, exist_ok=True)

            dataset_yaml = split_dir / f"{split}_dataset.yaml"
            self.ds_yamls.append(dataset_yaml)

            with open(dataset_yaml, "w") as ds_y:
                yaml.safe_dump(
                    {
                        "path": split_dir.as_posix(),
                        "train": "train",
                        "val": "val",
                        "names": self.classes
                    },
                    ds_y
                )

        for image, label in tqdm.tqdm(zip(images, self.labels), total=len(images)):
            for split, k_split in folds_df.loc[image.stem].items():
                img_to_path = save_path / split / k_split / "images"
                lbl_to_path = save_path / split / k_split / "labels"

                shutil.copy(image, img_to_path / image.name)
                shutil.copy(label, lbl_to_path / label.name)

        folds_df.to_csv(save_path / "kfold_datasplit.csv")
        fold_lbl_distrb.to_csv(save_path / "kfold_label_distribution.csv")


    def train(self, epochs: int = 100, batch=16, device: str="cpu"):
        """
        基于k-folder进行训练
        Args:
            epochs int : 训练批次
            batch int : 批次大小
            device str : 训练设备
        """
        results = {}

        for k in range(self.k):
            datase_configure_file = self.ds_yamls[k]
            model = YOLO(self._weight_file)
            model.train(data=datase_configure_file, epochs=epochs, project=self._project_name, batch=batch, device=device)

            results[k] = model.metrics

        pd.read_json(results).to_csv(self.dataset_path / "metrics.csv")