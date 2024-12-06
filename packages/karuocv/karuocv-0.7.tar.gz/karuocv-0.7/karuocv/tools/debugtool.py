# _*_ encoding: utf-8 _*_
'''
@File    :debugtool.py
@Desc    :
@Time    :2024/10/20 22:19:22
@Author  :caimmy@hotmail.com
@Version :0.1
'''
import logging
from typing import Union
from math import ceil
from pathlib import Path
import supervision as sv
import tqdm
import cv2
import imageio
import matplotlib.pyplot as plt
from karuocv.hub.inference import ImageAnnotator

logger = logging.getLogger(__file__)

class VideoRecorderTool(object):

    # 录制器类型
    RECORDER_IMAGE_IO = "imageio"
    RECORDER_SV_SINK = "sv_sink"
    RECORDER_CV2 = "cv2"


    def __init__(self, video_info: sv.VideoInfo, dest: str, recoder: str, record_fps: int=0):
        """
        Args:
            fps int 录像码率
            dest str 录像文件的存放地址
            recoder str 录制器类型
            record_fps int 录制帧率
        """
        self.video_info = video_info
        self.recoder = recoder
        self.dest = Path(dest).absolute()
        self._image_io_saver = None
        self._sv_sink_saver = None
        self._cv2_saver = None
        self.record_fps = record_fps if record_fps > 0 else video_info.fps

        self._start_saver()

    def _start_saver(self):
        match self.recoder:
            case self.RECORDER_IMAGE_IO:
                logger.debug("start imageio recorder")
                self._image_io_saver = imageio.get_writer(self.dest, fps=self.record_fps)
            case self.RECORDER_SV_SINK:
                logger.debug("start vidio_sink recorder")
                self.video_info.fps = self.record_fps
                self._sv_sink_saver = sv.VideoSink(target_path=self.dest, video_info=self.video_info)
            case self.RECORDER_CV2:
                logger.debug("start cv2 recorder")
                fourcc = cv2.VideoWriter_fourcc(*'MJPG')
                self._cv2_saver = cv2.VideoWriter(str(self.dest), fourcc, self.video_info.fps, (self.video_info.width, self.video_info.height))
            case _:
                pass

    def WriteFrame(self, frame):
        """
        录像
        Args:
            frame MatLike 
        """
        match self.recoder:
            case self.RECORDER_IMAGE_IO:
                self._image_io_saver.append_data(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            case self.RECORDER_SV_SINK:
                self._sv_sink_saver.write_frame(frame)
            case self.RECORDER_CV2:
                self._cv2_saver.write(frame)
            case _:
                pass

    def CloseRecorder(self):
        """
        关闭记录器
        """
        match self.recoder:
            case self.RECORDER_IMAGE_IO:
                logger.debug("close imageio recorder")
                self._image_io_saver.close()
            case self.RECORDER_SV_SINK:
                logger.debug("close sv_sink recorder")
                self._sv_sink_saver.__writer.release()
            case self.RECORDER_CV2:
                logger.debug("close cv2 recorder")
                self._cv2_saver.release()
            case _:
                pass

    def __enter__(self):
        self._start_saver()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.CloseRecorder()
        logger.debug("exit video_recorder_tool")
        logger.debug("exc_type: {}".format(exc_type))
        logger.debug("exc_val: {}".format(exc_val))
        logger.debug("exc_tb: {}".format(exc_tb))
        return True


def group_watch_images(matimg: dict, colsize: int=8):
    _imgsize = len(matimg)
    if _imgsize > colsize:
        rowsize = ceil(_imgsize / colsize)
    else:
        rowsize = 1
        colsize = _imgsize
    
    index = 1
    for _title in matimg:
        plt.subplot(rowsize, colsize, index)
        plt.imshow(matimg[_title])
        plt.title(_title)

        index += 1
    plt.show()


def vcd_inferenced_video(
        weight_file: str, 
        source_video: str, 
        output_video: str, 
        recorder: str = "imageio", 
        verbose: bool = False, 
        imshow=False, 
        device=None,
        legend=False,
        confidence_threshold=0.3
    ) -> Union[None | sv.VideoInfo]:
    """
    推理录像
    Args:
        weight_file str 模型文件
        source_video str 被推理视频文件
        output_video str 推理录像的保存地址
    """
    def _inference_frame(generator, total, annotator, box, labels):
        for frame in tqdm.tqdm(generator, total=total):
            yield annotator.fullAnnotateImage(frame, box, labels)


    ret_info = None
    try:
        annotator = ImageAnnotator(weight_file, confidence_threshold, verbose=verbose, device=device)
        video_info = sv.VideoInfo.from_video_path(source_video)
        frames_generator = sv.get_video_frames_generator(source_video)

        _box_annotator = sv.BoxAnnotator()
        _label_annotator = sv.LabelAnnotator()
        
        recorder = recorder if recorder in (VideoRecorderTool.RECORDER_CV2, VideoRecorderTool.RECORDER_IMAGE_IO, VideoRecorderTool.RECORDER_SV_SINK) else VideoRecorderTool.RECORDER_CV2
        with VideoRecorderTool(video_info, output_video, recorder, 0) as vcd_tool:
            for annotated_frame in _inference_frame(frames_generator, video_info.total_frames, annotator, _box_annotator, _label_annotator):
                annotated_frame = annotator.fullAnnotateImage(annotated_frame, _box_annotator, _label_annotator, legend)
                vcd_tool.WriteFrame(annotated_frame)
                if imshow:
                    cv2.imshow("", annotated_frame)
                    cv2.waitKey(1)
            
            ret_info = video_info
    except Exception as e:
        logger.error(e)
    finally:
        if imshow:
            cv2.destroyAllWindows()
    return ret_info

def detect_image(weight_file: str, image_uri: str, output_file: str = None):
    ia = ImageAnnotator(weight_file)
    img = cv2.imread(image_uri)
    img_mat = ia.fullAnnotateImage(img)
    if output_file:
        cv2.imwrite(output_file, img_mat)
    else:
        cv2.imshow("detect_image", img_mat)