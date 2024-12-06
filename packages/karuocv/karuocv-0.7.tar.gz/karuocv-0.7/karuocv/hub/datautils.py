# -*- encoding: utf-8 -*-
'''
@文件    :datautils.py
@说明    :
@时间    :2024/10/25 22:06:08
@作者    :caimmy@hotmail.com
@版本    :0.1

YOLO的数据格式是 cls_id x_center y_center w h
系统标注的数据格式是 cls_id x1 y1 x2 y2

系统坐标标注 转 YOLO标注
    x_center = (x1 + x2) / 2
    y_center = (y1 + y2) / 2

    w = (x2 - x1) / image_width
    h = (y2 - y1) / image_height


YOLO标注 转 系统坐标标注：
    x1 + x2 = 2 * x_center
    x2 - x1 = image_width * w
    y1 + y2 = 2 * y_center
    y2 - y1 = image_height * h

    --->

    x2 = (2 * x_center + image_width * w) / 2
    x1 = 2 * x_center - x2
    y2 = (2 * y_center + image_height * h) / 2
    y1 = 2 * y_center - y2
'''

def yolo_annotation_to_bbox_one_line(annotation, img_height, img_width):
    c_x, c_y, w, h = annotation[1:]
    x1 = ((c_x - w/2)*img_width).astype(int)
    x2 = ((c_x + w/2)*img_width).astype(int)
    y1 = ((c_y - h/2)*img_height).astype(int)
    y2 = ((c_y + h/2)*img_height).astype(int)

    return [x1, y1, x2, y2]

def bbox_to_yolo_annotation_one_line(xyxy, img_height, img_width):
    x1, y1, x2, y2 = xyxy[1:]
    c_x = (x1 + x2) / 2.0 / img_width
    c_y = (y1 + y2) / 2.0 / img_height
    w = (x2 - x1) / img_width
    h = (y2 - y1) / img_height
    return [c_x, c_y, w, h]

def bbox_to_yolo_annotation(xyxy, img_height, img_width):
    sh = xyxy.shape
    if len(sh) == 0:
        print("No bbox found")
    if len(sh) == 1:
        xyxy = xyxy.reshape(1, -1)
    num_box = len(xyxy)
    xyxy_list = []
    for idx in range(num_box):
        xyxy_list.append(bbox_to_yolo_annotation_one_line(xyxy[idx], img_height, img_width))
    return xyxy_list


def yolo_annotation_to_bbox(annotation, img_height, img_width):
    """
    Converts Yolo annotations to bounding box coordinates
    Input:
    annotation: str, annotation file in .txt format
    img_height: int, image height
    img_width: int, image width
    Output:
    class: list, List of labels in the image
    bbox_list: list, List of bounding boxes in an image
    """
    sh = annotation.shape
    if len(sh)==0:
        print("No bounding box found")
    if len(sh)==1:
        annotation = annotation.reshape(1, -1)
    num_bbox = len(annotation)
    bbox_list = []
    for idx in range(num_bbox):
        c_x, c_y, w, h = annotation[idx][1:]
        x1 = ((c_x - w/2)*img_width).astype(int)
        x2 = ((c_x + w/2)*img_width).astype(int)
        y1 = ((c_y - h/2)*img_height).astype(int)
        y2 = ((c_y + h/2)*img_height).astype(int)
        bbox_list.append([x1, y1, x2, y2])
    return bbox_list
