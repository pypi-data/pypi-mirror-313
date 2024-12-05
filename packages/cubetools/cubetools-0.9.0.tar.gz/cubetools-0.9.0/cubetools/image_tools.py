# -*- coding: utf-8 -*-
import io
import re
import base64
import cv2
import numpy as np
from PIL import Image, ExifTags, ImageDraw, ImageFont


def read_img(img):
    """
    从输入参数读取图像，转换成二进制字节流格式
    :param img:
        存在6种可能形式：
            - PIL Image
            - np.ndarray格式的图像数据（默认为RGB格式）
            - 图像文件路径名
            - 图像文件二进制字节流
            - 图像文件二进制字节流的base64编码字符串
            - 图像文件二进制字节流的base64编码URL字符串
    :return: (PIL.Image格式的图像对象, np.ndarray格式的图像数据(RGB格式))
    """
    try:
        if isinstance(img, Image.Image):
            return img, np.asarray(img)

        if isinstance(img, np.ndarray):
            return np2pil(img), img

        if isinstance(img, bytes):
            img_pil = bin2pil(img)
            img = np.asarray(img_pil)
            return img_pil, img

        if not isinstance(img, str):
            return None, None

        if img.endswith('.jpg') or img.endswith('.jpeg') or img.endswith('.png') or img.endswith('.gif') or img.endswith('.bmp'):
            with open(img, 'rb') as file:
                img = file.read()
                img_pil = bin2pil(img)
                img = np.asarray(img_pil)
                return img_pil, img

        if img.startswith('data:image/'):
            img = re.sub('^data:image/.+;base64,', '', img)
        img = base64.b64decode(img.encode())
        img_pil = bin2pil(img)
        img = np.asarray(img_pil)
        return img_pil, img
    except:
        return None, None


def bin2pil(img):
    img = Image.open(io.BytesIO(img))

    # 自动按拍摄时相机的重心旋转图像
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break
        exif = dict(img._getexif().items())
        if exif[orientation] == 3:
            img = img.rotate(180, expand=True)
        elif exif[orientation] == 6:
            img = img.rotate(270, expand=True)
        elif exif[orientation] == 8:
            img = img.rotate(90, expand=True)
    except:
        pass

    if not img.mode == 'RGB':
        img = img.convert('RGB')

    return img


def pil2np(img):
    return np.asarray(img)


def np2pil(img):
    return Image.fromarray(np.uint8(img))


def pil2url(img, format='JPEG'):
    if format.lower() == 'jpg':
        format = 'JPEG'

    output_buffer = io.BytesIO()
    img.save(output_buffer, format=format.upper())
    return 'data:image/{};base64,'.format(format.lower()) + str(base64.b64encode(output_buffer.getvalue()), encoding='utf-8')


def bin2base64(img):
    return str(base64.b64encode(img), encoding='utf-8')


def bin2url(img, format='JPEG'):
    return pil2url(Image.open(io.BytesIO(img)), format=format)


def url2pil(url):
    img_base64 = re.sub('^data:image/.+;base64,', '', url)
    return Image.open(io.BytesIO(base64.b64decode(img_base64.encode())))


def np2url(img, format='JPEG'):
    return pil2url(Image.fromarray(np.uint8(img)), format=format)


def resize_pil(img, new_size=1024):
    img_w, img_h = img.size
    if img_w > new_size:
        ratio = new_size / img_w
        img = img.resize((int(ratio * img_w), int(ratio * img_h)), Image.BICUBIC)
    elif img_h > new_size:
        ratio = new_size / img_h
        img = img.resize((int(ratio * img_w), int(ratio * img_h)), Image.BICUBIC)
    return img


# box中坐标格式为： x1, y1, w, h
def draw_all_box_and_label_pil(img, boxes, outline='red', width=2, text_color='white', text_bg_color='red', text_size=24, font_path='app/fonts/wqy-zenhei.ttc'):
    draw = ImageDraw.Draw(img)
    for (label, box) in boxes:
        x, y, w, h = box
        draw.rectangle((x, y, x + w, y + h), outline=outline, width=width)

    font = ImageFont.truetype(font_path, text_size)

    for (label, box) in boxes:
        x1 = max(box[0], 0)
        y1 = max(box[1] - text_size - 3, 0)
        point = (x1, y1)
        try:
            text_width = len(label.encode('gb2312'))
        except:
            text_width = len(label) + 1
        draw.rectangle((x1, y1, x1 + text_size * text_width / 2, y1 + text_size + 3), fill=text_bg_color)
        draw.text(point, label, text_color, font=font)  # 参数1：打印坐标，参数2：文本，参数3：字体颜色，参数4：字体

    return img


# box中坐标格式为： x1, y1, x2, y2
def draw_all_box_and_label_pil2(img, boxes, outline='red', width=2, text_color='white', text_bg_color='red', text_size=24, font_path='app/fonts/wqy-zenhei.ttc'):
    draw = ImageDraw.Draw(img)
    for (label, box) in boxes:
        x1, y1, x2, y2 = box
        draw.rectangle((x1, y1, x2, y2), outline=outline, width=width)

    font = ImageFont.truetype(font_path, text_size)

    for (label, box) in boxes:
        x1 = max(box[0], 0)
        y1 = max(box[1] - text_size - 3, 0)
        point = (x1, y1)
        try:
            text_width = len(label.encode('gb2312'))
        except:
            text_width = len(label) + 1
        draw.rectangle((x1, y1, x1 + text_size * text_width / 2, y1 + text_size + 3), fill=text_bg_color)
        draw.text(point, label, text_color, font=font)  # 参数1：打印坐标，参数2：文本，参数3：字体颜色，参数4：字体

    return img


# box中坐标格式为： x1, y1, w, h
def draw_all_box(img, boxes, outline='red', width=2):
    draw = ImageDraw.Draw(img)
    for box in boxes:
        x, y, w, h = box
        draw.rectangle((x, y, x + w, y + h), outline=outline, width=width)

    return img


# box中坐标格式为： x1, y1, x2, y2
def draw_all_box2(img, boxes, outline='red', width=2):
    draw = ImageDraw.Draw(img)
    for box in boxes:
        x1, y1, x2, y2 = box
        draw.rectangle((x1, y1, x2, y2), outline=outline, width=width)

    return img


def draw_labels(img, labels, text_color='white', text_bg_color='red', text_size=24, font_path='app/fonts/wqy-zenhei.ttc'):
    draw = ImageDraw.Draw(img)  # 图片上打印
    font = ImageFont.truetype(font_path, text_size)

    for (label, point) in labels:
        x1 = max(point[0], 0)
        y1 = max(point[1], 0)
        point = (x1, y1)
        try:
            text_width = len(label.encode('gb2312'))
        except:
            text_width = len(label) + 1
        draw.rectangle((x1, y1, x1 + text_size * text_width / 2, y1 + text_size + 3), fill=text_bg_color)
        draw.text(point, label, text_color, font=font)  # 参数1：打印坐标，参数2：文本，参数3：字体颜色，参数4：字体

    return img


def draw_points(img, points, color='red'):
    draw = ImageDraw.Draw(img)
    for point in points:
        draw.ellipse((point[0] - 2, point[1] - 2, point[0] + 2, point[1] + 2), fill=color, outline=color)

    return img


class Resize(object):
    """resize image by target_size and max_size
    Args:
        target_size (int): the target size of image
        keep_ratio (bool): whether keep_ratio or not, default true
        interp (int): method of resize
    """

    def __init__(self, target_size, keep_ratio=False, interpolation=cv2.INTER_LINEAR):
        if isinstance(target_size, int):
            target_size = [target_size, target_size]
        self.target_size = target_size
        self.keep_ratio = keep_ratio
        self.interpolation = interpolation

    def __call__(self, im):
        """
        Args:
            im (np.ndarray): image (np.ndarray)
        Returns:
            im (np.ndarray):  processed image (np.ndarray)
            im_info (dict): info of processed image
        """
        assert len(self.target_size) == 2
        assert self.target_size[0] > 0 and self.target_size[1] > 0
        im_scale_y, im_scale_x = self.generate_scale(im)
        im = cv2.resize(
            im,
            None,
            None,
            fx=im_scale_x,
            fy=im_scale_y,
            interpolation=self.interpolation)

        scale_factor = np.array([im_scale_y, im_scale_x]).astype('float32')
        return im, scale_factor

    def generate_scale(self, im):
        """
        Args:
            im (np.ndarray): image (np.ndarray)
        Returns:
            im_scale_x: the resize ratio of X
            im_scale_y: the resize ratio of Y
        """
        origin_shape = im.shape[:2]
        if self.keep_ratio:
            im_size_min = np.min(origin_shape)
            im_size_max = np.max(origin_shape)
            target_size_min = np.min(self.target_size)
            target_size_max = np.max(self.target_size)
            im_scale = float(target_size_min) / float(im_size_min)
            if np.round(im_scale * im_size_max) > target_size_max:
                im_scale = float(target_size_max) / float(im_size_max)
            im_scale_x = im_scale
            im_scale_y = im_scale
        else:
            resize_h, resize_w = self.target_size
            im_scale_y = resize_h / float(origin_shape[0])
            im_scale_x = resize_w / float(origin_shape[1])
        return im_scale_y, im_scale_x


class Normalize(object):
    """normalize image
    Args:
        mean (list): im - mean
        std (list): im / std
        is_scale (bool): whether need im / 255
        norm_type (str): type in ['mean_std', 'none']
    """

    def __init__(self, mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225), is_scale=True, norm_type='mean_std'):
        self.mean = mean
        self.std = std
        self.is_scale = is_scale
        self.norm_type = norm_type

    def __call__(self, im):
        """
        Args:
            im (np.ndarray): image (np.ndarray)
        Returns:
            im (np.ndarray):  processed image (np.ndarray)
        """
        im = im.astype(np.float32, copy=False)
        if self.is_scale:
            scale = 1.0 / 255.0
            im *= scale

        if self.norm_type == 'mean_std':
            mean = np.array(self.mean)[np.newaxis, np.newaxis, :]
            std = np.array(self.std)[np.newaxis, np.newaxis, :]
            im -= mean
            im /= std
        return im
