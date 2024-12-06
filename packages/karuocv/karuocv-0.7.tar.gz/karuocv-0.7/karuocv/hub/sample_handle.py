# _*_ encoding: utf-8 _*_
'''
@文件    :sample_handle.py
@说明    :处理样本
@时间    :2024/10/15 22:12:40
@作者    :caimmy@hotmail.com
@版本    :0.1
'''

import os
import tqdm
from copy import deepcopy
import shutil
import cv2
import glob
import random
import math
from pathlib import Path
from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError as e:
    from yaml import Loader
from karuocv.utils import logger, checkPathEmptyOrNull
from karuocv.hub.inference import ImageAnalyser


class DatasetMixer:
    CFG_NAME = "data.yaml"


    def __init__(self, source_a: str, source_b: str, dest: str):
        self.source_a = source_a
        self.source_b = source_b
        self.dest = dest

    def _checkDatasource(self) -> bool:
        """
        混合两个训练样本集
        Args:
            source_a str 源数据集文件夹路径
            source_b str 源数据集文件夹路径
            dest str 目标数据集文件夹路径
        Return: bool
        """
        ret = False
        if os.path.exists(self.source_a) and os.path.exists(os.path.join(self.source_a, DatasetMixer.CFG_NAME)) and \
            os.path.exists(self.source_b) and os.path.exists(os.path.join(self.source_b, DatasetMixer.CFG_NAME)):
            assert checkPathEmptyOrNull(self.dest)
            os.makedirs(self.dest, exist_ok=True)
            ret = os.path.exists(self.dest)
        else:
            logger.error(f"please checkout source dir exists, {self.source_a} and {self.source_b}")
        
        return ret
    
    def _parse_two_yaml_file(self): 
        with open(os.path.join(self.source_a, DatasetMixer.CFG_NAME), mode="r", encoding="utf-8") as a_reader, \
            open(os.path.join(self.source_b, DatasetMixer.CFG_NAME), mode="r", encoding="utf-8") as b_reader:
        
            sample_A_cfg = load(a_reader, Loader=Loader)
            sample_B_cfg = load(b_reader, Loader=Loader)

            self.a_names = sample_A_cfg.get("names")
            self.b_names = sample_B_cfg.get("names")
            self.merged_names = deepcopy(self.a_names)
            for _name in self.b_names:
                if _name not in self.a_names:
                    self.merged_names.append(_name)

            # 设置标注数据编号和名称的映射数据，用于合并数据集时转换目标标识
            self.a_names_dict = {str(seq): val for seq, val in enumerate(self.a_names)}
            self.b_names_dict = {str(seq): val for seq, val in enumerate(self.b_names)}
            self.merged_names_dict = {val: str(seq) for seq, val in enumerate(self.merged_names)}

    def _move_sample_images(self, sample_path: str, subfolder: str):
        """
        首先处理图片样本的迁移
        Args:
            sample_path str 样本的根路径，分别传入要合并的两套数据的根目录
            subfolder str 样本的分类名称，分别传入train, test, valid
        """
        _src_folder_images = os.path.join(sample_path, subfolder, "images")
        _dest_folder_images = os.path.join(self.dest, subfolder, "images")
        os.makedirs(_dest_folder_images, exist_ok=True)
        assert os.path.exists(_dest_folder_images)
        for _cur_root, _, _cur_files in os.walk(_src_folder_images):
            for _file in tqdm.tqdm(_cur_files):
                _src_file = os.path.join(_cur_root, _file)
                _dest_file = os.path.join(_dest_folder_images, _file)
                shutil.copy(_src_file, _dest_file)
        logger.info(f"copied image file in subfold {subfolder}, total size is {len(_cur_files)}")

    def _move_sample_labels(self, sample_path: str, subfolder: str, sample_names: dict):
        """
        处理标注样本文件的迁移, 参数说明见 '''_move_sample_images
        Args: 
            sample_path str 样本的根路径，分别传入要合并的两套数据的根目录
            subfolder str 样本的分类名称，分别传入train, test, valid
            sample_name str 
        """
        _src_folder_labels = os.path.join(sample_path, subfolder, "labels")
        _dest_folder_labels = os.path.join(self.dest, subfolder, "labels")
        os.makedirs(_dest_folder_labels, exist_ok=True)
        _int_trans_cnt = 0
        for _cur_root, _, _cur_files in os.walk(_src_folder_labels):
            for _file in tqdm.tqdm(_cur_files):
                _src_file = os.path.join(_cur_root, _file)
                _dest_file = os.path.join(_dest_folder_labels, _file)

                _int_trans_cnt += self._trans_labeled_file(_src_file, _dest_file, sample_names)

        logger.info(f"copied label file in subfold {subfolder}, total size is {_int_trans_cnt}")

    def _trans_labeled_file(self, src_file: str, dest_file: str, sample_names: dict) -> int:
        """
        转写标注数据文件
        return:
            1: 转写完成
            0: 转写失败
        """
        ret_code = 0
        _transed_label_lines = []
        with open(src_file, mode="r", encoding="utf-8") as src_stream, \
            open(dest_file, mode="w") as dst_stream:
            for _line in src_stream.readlines():
                _data = _line.split(" ")
                if len(_data) == 5:
                    if str(_data[0]) in sample_names and sample_names[_data[0]] in self.merged_names_dict:
                        _transed = [self.merged_names_dict[sample_names[_data[0]]]]
                        _transed.extend(_data[1:])
                        _transed_label_lines.append(f"{' '.join(_transed)}")
            if len(_transed_label_lines) > 0:
                dst_stream.writelines(_transed_label_lines)
                ret_code = 1

        return ret_code


    def mixSamples(self):
        """
        执行混合样本操作
        Args:
            source_a str 源数据集文件夹路径
            source_b str 源数据集文件夹路径
            dest str 目标数据集文件夹路径
        """
        if self._checkDatasource():
            self._parse_two_yaml_file()
            # 首先处理A样本
            _targe_subfolder = ["test", "train", "valid"]
            for _subfolder in _targe_subfolder:
                self._move_sample_images(self.source_a, _subfolder)
                self._move_sample_labels(self.source_a, _subfolder, self.a_names_dict)

                self._move_sample_images(self.source_b, _subfolder)
                self._move_sample_labels(self.source_b, _subfolder, self.b_names_dict)
            # 写入样本配置文件
            config_yaml_data = []
            
            config_yaml_data.append(f"test: ../test,")
            config_yaml_data.append(f"train: ../train,")
            config_yaml_data.append(f"val: ../valid,")
            config_yaml_data.append("")
            config_yaml_data.append(f"names: [{', '.join(self.merged_names)}],")
            config_yaml_data.append(f"nc: {len(self.merged_names)},")
            train_yml_file = os.path.join(self.dest, "data.yaml")
            with open(train_yml_file, mode="w") as config_writer:
                config_writer.write("{\n")
                for _line in config_yaml_data:
                    config_writer.write(f"    {_line}\n")
                config_writer.write("}\n")
            logger.info(f"success, data.yaml position: {train_yml_file}")


class DatasetPrefab:
    """
    对数据集进行预置化处理
    将样本全部转化为灰度图或者轮廓图重新存放
    """
    HANDLE_GRAY = "gray"
    HANDLE_CONTOUR = "contour"
    def __init__(self, path: str, handletype: str) -> None:
        assert os.path.exists(path)
        self._dataset_path = path
        self._handletype = handletype

        self._ori_train_path = ""
        self._dst_train_path = ""
        self._ori_test_path = ""
        self._dst_test_path = ""
        self._ori_valid_path = ""
        self._dst_valid_path = ""
        self._dst_data_yaml = ""
        self._origin_data_yaml_cfg = None

        self._parse_yaml()

    def _parse_yaml(self):
        cfg_file_path = os.path.join(self._dataset_path, "data.yaml")
        assert os.path.exists(cfg_file_path)
        with open(cfg_file_path, mode="r") as f:
            self._origin_data_yaml_cfg = load(f, Loader=Loader)
        self._ori_test_path: str = self._origin_data_yaml_cfg.get("test")
        self._ori_train_path: str = self._origin_data_yaml_cfg.get("train")
        self._ori_valid_path: str = self._origin_data_yaml_cfg.get("val")
        if not self._ori_test_path.startswith("/"): self._ori_test_path = os.path.join(self._dataset_path, self._ori_test_path)
        if not self._ori_valid_path.startswith("/"): self._ori_valid_path = os.path.join(self._dataset_path, self._ori_valid_path)
        if not self._ori_train_path.startswith("/"): self._ori_train_path = os.path.join(self._dataset_path, self._ori_train_path)
        

        if os.path.exists(self._ori_test_path) and \
            os.path.exists(self._ori_valid_path) and \
            os.path.exists(self._ori_train_path):
            self._dst_test_path = f"{self._ori_test_path[:-1] if self._ori_test_path.endswith('/') else self._ori_test_path}_{self._handletype}" 
            self._dst_valid_path = f"{self._ori_valid_path[:-1] if self._ori_valid_path.endswith('/') else self._ori_valid_path}_{self._handletype}" 
            self._dst_train_path = f"{self._ori_train_path[:-1] if self._ori_train_path.endswith('/') else self._ori_train_path}_{self._handletype}" 
                

    def _prefab_subpath_image(self, frompath: str, topath: str) -> bool:
        """
        预处理样本子目录的图片
        Args:
            frompath str 源目录
            topath str 目的目录 
        """
        ret_code = False
        frompath = os.path.join(frompath, "images")
        topath = os.path.join(topath, "images")
        if not os.path.exists(topath):
            os.makedirs(topath)
        if os.path.exists(frompath):
            for _root, _, _files in os.walk(frompath):
                for _filename in tqdm.tqdm(_files):
                    _image = cv2.imread(os.path.join(_root, _filename))
                    _dst_image = None
                    match self._handletype:
                        case DatasetPrefab.HANDLE_CONTOUR:
                            _dst_image, _, _ = ImageAnalyser(_image).drawContourPicture()
                        case DatasetPrefab.HANDLE_GRAY:
                            _dst_image = ImageAnalyser(_image).drawGrayPicture()
                    if _dst_image is not None:
                        cv2.imwrite(os.path.join(topath, _filename), _dst_image)

        return ret_code
    
    def _prefab_subpath_labels(self, frompath: str, topath: str) -> bool:
        """
        预处理样本子目录的标注数据
        Args:
            frompath str 源目录
            topath str 目的目录 
        """
        ret_code = False
        ret_code = False
        frompath = os.path.join(frompath, "labels")
        topath = os.path.join(topath, "labels")
        if not os.path.exists(topath):
            os.makedirs(topath)
        if os.path.exists(frompath):
            for _root, _, _files in os.walk(frompath):
                for _filename in tqdm.tqdm(_files):
                    shutil.copy(
                        os.path.join(_root, _filename),
                        os.path.join(topath, _filename)
                    )
        return ret_code
    
    def _write_data_yml(self):
        _dest_data_yaml_path = os.path.join(self._dataset_path, f"data_{self._handletype}.yaml")
        _write_content = []
        _write_content.append("{\n")
        _write_content.append(f"  train: {self._dst_train_path},\n")
        _write_content.append(f"  test: {self._dst_test_path},\n")
        _write_content.append(f"  val: {self._dst_valid_path},\n")
        _write_content.append(f"  nc: {self._origin_data_yaml_cfg.get('nc')},\n")
        _write_content.append(f"  names: {self._origin_data_yaml_cfg.get('names')},\n")
        _write_content.append("}\n")
        with open(_dest_data_yaml_path, mode="w", encoding="utf-8") as wf:
            wf.writelines(_write_content)
    
    def __call__(self):
        self.Prefab()
    
    def Prefab(self):
        logger.info("handle test images")
        self._prefab_subpath_image(
            self._ori_test_path,
            self._dst_test_path
        )
        logger.info("handle valid images")
        self._prefab_subpath_image(
            self._ori_valid_path,
            self._dst_valid_path
        )
        logger.info("handle train images")
        self._prefab_subpath_image(
            self._ori_train_path,
            self._dst_train_path
        )

        logger.info("handle test labels")
        self._prefab_subpath_labels(
            self._ori_test_path,
            self._dst_test_path
        )
        logger.info("handle valid labels")
        self._prefab_subpath_labels(
            self._ori_valid_path,
            self._dst_valid_path
        )
        logger.info("handle train labels")
        self._prefab_subpath_labels(
            self._ori_train_path,
            self._dst_train_path
        )
        self._write_data_yml()
        logger.info(f"prefab dataset to {self._handletype} completed!")


class DatasetRaw2YOLO:
    """
    把从sacp下载的原始数据存放成yolo数据集格式
    """
    def __init__(self, src: str, dest: str):
        self.src = Path(src).absolute()
        self.dest = Path(dest).absolute()
        self.names = {}


    @classmethod
    def fromYaml(cls, src_path: str, dest_path: str):
        _obj = DatasetRaw2YOLO(src_path, dest_path)
        _obj.analysis_configure()
        return _obj
    
    @classmethod
    def fromSummaryTxt(cls, src_path: str, dest_path: str):
        _obj = DatasetRaw2YOLO(src_path, dest_path)
        _obj.analysis_label_summary_txt()
        return _obj

    def analysis_configure(self):
        src_configure_file = os.path.join(self.src, "data.yaml")
        if os.path.isfile(src_configure_file):
            with open(src_configure_file, "r", encoding="utf-8") as f:
                cfg_data = load(f, Loader=Loader)
                if "names" in cfg_data:
                    self.names = {seq: val for seq, val in enumerate(cfg_data['names'])}

    def analysis_label_summary_txt(self):
        src_configure_file = Path(self.src) / "raw" / "label_summary.txt"
        if src_configure_file.exists():
            with open(src_configure_file, "r", encoding="utf-8") as rf:
                self.names = {seq: val for seq, val in enumerate(rf.read().split(" "))}
    
    def _analysis_radio(self, radio: int):
        """
        解析数据集拆分比例
        return 
        train_radio, val_radio, test_radio
        """
        radio_val = [int(t) for t in list(str(radio))]
        if len(radio_val) == 3 and sum(radio_val) == 10:
            return radio_val
        return None

    def splitAnnotations(self, radio: int):
        """
        Args:
            radio  int 分配比例，按照, 数字必须是3位正整数，每位数字相加必须为0， 如721，表示训练集7，验证集2，测试集3；622表示训练集6，验证集2，测试集2
        """
        radio_val = self._analysis_radio(radio)
        if radio_val:
            train_radio, val_radio, test_radio = radio_val
            label_files = glob.glob(os.path.join(self.src,"raw", "*.txt"))
            mount_size = len(label_files)
            if mount_size > 100:
                random.shuffle(label_files)
                train_size = math.ceil(train_radio / 10 * mount_size)
                val_size = math.ceil(val_radio / 10 * mount_size)
                if train_size > 0 and val_size > 0:
                    for ftype in ("images", "labels"):
                        for catalog in ("train", "val", "test"):
                            os.makedirs(os.path.join(self.dest, ftype, catalog), exist_ok=True)
                    _file_seq = 0
                    for _curfile in tqdm.tqdm(label_files):
                        _raw_path, _label_file_name = os.path.split(_curfile)
                        _raw_file_name, _ = _label_file_name.split(".")
                        _spec_image_file = os.path.join(_raw_path, f"{_raw_file_name}.jpeg")
                        if os.path.exists(_spec_image_file):
                            if _file_seq < train_size:
                                # 当作训练数据处理
                                shutil.copyfile(_spec_image_file, os.path.join(self.dest, "images", "train", f"{_raw_file_name}.jpeg"))
                                shutil.copyfile(_curfile, os.path.join(self.dest, "labels", "train", f"{_raw_file_name}.txt"))
                            elif _file_seq >= train_size and _file_seq < train_size + val_size:
                                # 当作验证数据处理
                                shutil.copyfile(_spec_image_file, os.path.join(self.dest, "images", "val", f"{_raw_file_name}.jpeg"))
                                shutil.copyfile(_curfile, os.path.join(self.dest, "labels", "val", f"{_raw_file_name}.txt"))
                            else:
                                # 当作测试数据处理
                                shutil.copyfile(_spec_image_file, os.path.join(self.dest, "images", "test", f"{_raw_file_name}.jpeg"))
                                shutil.copyfile(_curfile, os.path.join(self.dest, "labels", "test", f"{_raw_file_name}.txt"))
                        _file_seq += 1
                    # write yaml file
                    with open(os.path.join(self.dest, "data.yaml"), mode="w", encoding="utf-8") as wf:
                        # wf.write(f"path: {self.dest}\n")
                        wf.write(f"path: {self.dest.as_posix()}\n")
                        wf.writelines([
                            "train: images/train\n",
                            "val: images/val\n",
                            "test: images/test\n"
                        ])
                        wf.write("names: ")
                        obj_list = [f"{_v}: {self.names[_v]}" for _v in self.names]
                        wf.writelines("\n    " + "\n    ".join(obj_list))
            else:
                raise RuntimeError(f"the number of samples is too small to effectively trained. [{len(label_files)}]")
        else:
            raise ValueError(f"radio value error, 3 vals and sum is 10, [{radio}]")