# _*_ encoding: utf-8 _*_
'''
@文件    :__init__.py
@说明    :
@时间    :2024/10/15 14:53:15
@作者    :caimmy@hotmail.com
@版本    :0.1
'''

"""
@version 0.1 [2024-10-15] start project
@version 0.3 [2024-10-30] 加入标注统计截图功能 task=statistic-labels
@version 0.5 [2024-11-18] 优化录像功能，增加对imageio压缩的支持。
@version 0.6 [2024-11-19] command arg imshow type is str.
@version 0.62 [2024-11-22] 增加了屏幕监控的指令 --task=monitor-screen
@version 0.65 [2024-11-28] 增加k-folder交叉验证方法，增加了yolo数据集保存方法
@version 0.7 [2024-12-05] 增加推理时传入置信度阈值控制参数。
"""

__version__ = "0.7"

from karuocv.utils import (train)
from karuocv.hub.inference import ImageAnalyser
from karuocv.tools.debugtool import (
    vcd_inferenced_video, 
    detect_image
)
from karuocv.hub.sample_handle import DatasetRaw2YOLO
from karuocv.tools.validatortool import KFolderCrossVal

all = (
    __version__,
    train,
    ImageAnalyser,
    vcd_inferenced_video,
    detect_image,
    DatasetRaw2YOLO,
    KFolderCrossVal
)