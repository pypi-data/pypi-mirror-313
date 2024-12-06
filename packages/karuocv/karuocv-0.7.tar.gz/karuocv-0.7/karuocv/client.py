# _*_ encoding: utf-8 _*_
'''
@文件    :client.py
@说明    :
@时间    :2024/10/15 22:37:26
@作者    :caimmy@hotmail.com
@版本    :0.1
'''

import argparse
import logging
from karuocv.utils import logger

def init_command_args():
    parser = argparse.ArgumentParser(description="SACP object train tools")

    parser.add_argument("--task", required=True, help="指定任务 train, inference, mix_datasets, ETC")
    parser.add_argument("--base_model", type=str, help="底座模型的路径")
    parser.add_argument("--device", type=str, default=None, help="select one in the list which contains cpu, cuda and mps")
    parser.add_argument("--epochs", type=int, default=30, help="训练迭代周期")
    parser.add_argument("--iterations", type=int, default=10, help="The number of generations to run the evolution for.")
    parser.add_argument("--batch_size", type=int, default=8, help="the batch size of train.")
    parser.add_argument("--path", type=str, help="some path parameter.")
    parser.add_argument("--verbose", default=False, action="store_true", help="show log for inference or not")
    parser.add_argument("--format", default="", help="format parameter, in vcd task, format param selected from [imageio, sv_sink, cv2]")

    parser.add_argument("--threshold", type=float, help="set some threshold value, conficence_threshold etc.")
    parser.add_argument("--source_a", type=str)
    parser.add_argument("--source_b", type=str)
    parser.add_argument("--fps", type=int, default=25, help="fps of video")
    parser.add_argument("--width", type=int, help="param with set width")
    parser.add_argument("--height", type=int, help="param with set height")
    parser.add_argument("--imshow", default=False, action="store_true", help="是否通过cv2显示图片")
    parser.add_argument("--dest", default="", type=str, help="the output files destnation path.")
    parser.add_argument("--legend", default=False, action="store_true", help="图片推理时是否需要标注图例")
    parser.add_argument("--hyperparameters", default=None, help="use hyperparameters configure file.")

    args = parser.parse_args()
    return args

def client_command():
    command_line_args = init_command_args()
    if command_line_args.verbose:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.WARN)
    print(command_line_args)
    if command_line_args.verbose:
        command_line_args.verbose = True
    match command_line_args.task:
        case "mixdatasets":
            from karuocv.hub.sample_handle import DatasetMixer
            mixer = DatasetMixer(command_line_args.source_a, command_line_args.source_b, command_line_args.dest)
            mixer.mixSamples()
        case "train":
            from karuocv.utils import train
            if command_line_args.path:
                train(
                    command_line_args.path, 
                    command_line_args.base_model, 
                    command_line_args.epochs, 
                    command_line_args.batch_size, 
                    command_line_args.device, 
                    command_line_args.verbose,
                    command_line_args.hyperparameters
                )
        case "tune":
           from karuocv.utils import tune
           res = tune(
               command_line_args.path, 
               command_line_args.base_model, 
               command_line_args.epochs, 
               command_line_args.iterations,
               command_line_args.device,
               command_line_args.verbose
            )
           print("tune completed")
           print(res)
        case "vcd":
            """推理录像"""
            from karuocv.tools.debugtool import vcd_inferenced_video
            video_infor = vcd_inferenced_video(
                command_line_args.base_model, 
                command_line_args.path, 
                command_line_args.dest, 
                command_line_args.format, 
                command_line_args.verbose,
                command_line_args.imshow,
                command_line_args.device,
                command_line_args.legend,
                command_line_args.threshold
            )
            if video_infor:
                print(video_infor)
        case "detect_image":
            from karuocv.tools.debugtool import detect_image
            detect_image(command_line_args.base_model, command_line_args.path, command_line_args.dest)
            logger.info("ok")
        case "regression-annotation":
            """注解回测：生成新的图片，左图打印标注图像，右图打印推理图像"""
            from karuocv.tools.validatortool import RegressionAnnotationTool
            RegressionAnnotationTool(command_line_args.base_model, command_line_args.path, command_line_args.dest).walkCheckDataset()
        case "statistic-labels":
            """标签统计： 对标注框进行截图保存"""
            from karuocv.hub.sample_watch import SampleStatistics
            SampleStatistics(command_line_args.path, command_line_args.dest).CaptureLabels()
        case "monit-screen":
            from karuocv.tools.realtime_monitor import monit_screen
            monit_screen(command_line_args.base_model, command_line_args.width, command_line_args.dest)
        case "test":
            import os
            from pathlib import Path
            from dotenv import load_dotenv
            curpath = Path("./.env").absolute()
            print(curpath)
            load_dotenv(curpath)
            a = os.getenv("DEBUG_MODE", "notset")
            print(a)
        case _:
            logger.info("no matched task command")


if __name__ == "__main__":
    client_command()