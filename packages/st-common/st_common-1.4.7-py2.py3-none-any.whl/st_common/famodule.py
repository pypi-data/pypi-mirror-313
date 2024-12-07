# Two-factor authentication
import yaml
from paddleocr import PaddleOCR
import cv2

import base64
from PIL import Image
import io
import numpy as np
import requests
from st_common import ccookies
import logging
# 获取名为当前模块名称的logger
logger = logging.getLogger('main')
def kaptcha_text(ocr_yaml,img_path):
    with open(ocr_yaml, 'r', encoding='utf-8') as f:
        config_small = yaml.safe_load(f)
    logger.info(config_small)
    small_ocr = PaddleOCR(**config_small)
    # ocr = PaddleOCR(det=False,lang='ch')
    result = small_ocr.ocr(img_path)
    try:
        txts = [line[0][1][0] for line in result]
        target_text = list(txts[0])
    except:
        logger.error("ocr kaptcha is None")
        return None
    return target_text

def base642img(src_url):
    """
    base64 2 img
    :param src_url: str, like: 'data:image/png;base64, iVBORw0KGg...'
    :return: img,
    """
    tmp = src_url.split(',')[-1]
    img_bytes = base64.b64decode(tmp)
    img_bytes_io = io.BytesIO(img_bytes)
    # img = cv2.imread(img_bytes_io)
    img = Image.open(img_bytes_io)
    img = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)
    return img


def url2img(src_url):
    """
    url 2 img
    :param src_url: str,
    :return: img,
    """
    img = None
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6',
        'Upgrade-Insecure-Requests': '1',
    }
    try:
        resp = requests.get(src_url, headers=headers)
    except Exception as err:
        logger.error("url2img fail, msg: %s" % err)
    else:
        if resp.status_code == 200:
            img = Image.open(io.BytesIO(resp.content))
            img = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)
    return img


def format_style(style_str):
    """
    Parse the string to obtain the style attribute of the HTML tag
    :param style_str: str,
    :return: dict,
    """
    style_dict = ccookies.str2dict(style_str.replace(' ', ''), ';', ':')
    for ehkey in style_dict.keys():
        if ehkey in ['height', 'width', 'top', 'left']:
            style_dict[ehkey] = style_dict[ehkey].replace('px', '')
            style_dict[ehkey] = float(style_dict[ehkey])
            style_dict[ehkey] = round(style_dict[ehkey])
    return style_dict


def block_bg_distance(img_bg, img_block):
    """
    Recognition of the position of the slider gap and the distance of the slider movement
        : param img_ BG: Large verification code image, background image
        : param img_ Block: small slider (movable) image, slider image
    """

    image0 = cv2.Canny(img_bg, threshold1=100, threshold2=200)

    # image1 = cv2.imread(url_block)
    rows, cols, chanals = img_block.shape
    # Crop small slider (movable) image blank area, approximately 55 * 55 pixels
    min_x = 255
    min_y = 255
    max_x = 0
    max_y = 0
    for x in range(1, rows):
        for y in range(1, cols):
            t = set(img_block[x, y])
            if len(t) >= 2:
                if x <= min_x:
                    min_x = x
                elif x >= max_x:
                    max_x = x
                if y <= min_y:
                    min_y = y
                elif y >= max_y:
                    max_y = y
    image2 = img_block[min_x:max_x, min_y:max_y]

    can2 = cv2.Canny(image2, threshold1=100, threshold2=200)
    # Match gap position
    res = cv2.matchTemplate(image0, can2, cv2.TM_CCOEFF_NORMED)
    # Finding the Best Match : min_val, max_val, min_loc, max_loc 
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    # Max_ Loc is the two-dimensional coordinate of the top left corner of the notch with the best matching
    #   etc. max_loc  = （254，146）
    ''' Draw matching positions with boxes
    th, tw = image1.shape[:2]
    tl = max_loc  # Coordinates of the upper left corner point
    br = (tl[0] + tw, tl[1] + th)  # Coordinates of the lower right corner point
    # cv2.rectangle(image, tl, br, (0, 255, 0), 2)
    # cv2.imwrite('TEMP1.jpg', image)
    '''
    x = max_loc[0]
    height, width, channels = image2.shape
    if width == 55:
        Distance = round((x - 18) / 0.945)
    else:
        Distance = round((x - 6) / 0.945)
    return Distance
