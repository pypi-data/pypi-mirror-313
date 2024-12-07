import easyocr
import cv2
import numpy as np
import matplotlib.pyplot as plt
from py2ls.ips import (
    strcmp,
    detect_angle,
)  # Ensure this function is defined in your 'ips' module
from spellchecker import SpellChecker
import re

from PIL import Image, ImageDraw, ImageFont
import PIL.PngImagePlugin
import pytesseract
from paddleocr import PaddleOCR
import logging

logging.getLogger("ppocr").setLevel(
    logging.WARNING
)  # or logging.ERROR to show only error messages

"""
    Optical Character Recognition (OCR)
"""

# Valid language codes
lang_valid = {
    "easyocr": {
        "english": "en",
        "thai": "th",
        "chinese_traditional": "ch_tra",
        "chinese": "ch_sim",
        "japanese": "ja",
        "korean": "ko",
        "tamil": "ta",
        "telugu": "te",
        "kannada": "kn",
        "german": "de",
    },
    "paddleocr": {
        "chinese": "ch",
        "chinese_traditional": "chinese_cht",
        "english": "en",
        "french": "fr",
        "german": "de",
        "korean": "korean",
        "japanese": "japan",
        "russian": "ru",
        "italian": "it",
        "portuguese": "pt",
        "spanish": "es",
        "polish": "pl",
        "dutch": "nl",
        "arabic": "ar",
        "vietnamese": "vi",
        "tamil": "ta",
        "turkish": "tr",
    },
    "pytesseract": {
        "afrikaans": "afr",
        "amharic": "amh",
        "arabic": "ara",
        "assamese": "asm",
        "azerbaijani": "aze",
        "azerbaijani_cyrillic": "aze_cyrl",
        "belarusian": "bel",
        "bengali": "ben",
        "tibetan": "bod",
        "bosnian": "bos",
        "breton": "bre",
        "bulgarian": "bul",
        "catalan": "cat",
        "cebuano": "ceb",
        "czech": "ces",
        "chinese": "chi_sim",
        "chinese_vertical": "chi_sim_vert",
        "chinese_traditional": "chi_tra",
        "chinese_traditional_vertical": "chi_tra_vert",
        "cherokee": "chr",
        "corsican": "cos",
        "welsh": "cym",
        "danish": "dan",
        "danish_fraktur": "dan_frak",
        "german": "deu",
        "german_fraktur": "deu_frak",
        "german_latf": "deu_latf",
        "dhivehi": "div",
        "dzongkha": "dzo",
        "greek": "ell",
        "english": "eng",
        "middle_english": "enm",
        "esperanto": "epo",
        "math_equations": "equ",
        "estonian": "est",
        "basque": "eus",
        "faroese": "fao",
        "persian": "fas",
        "filipino": "fil",
        "finnish": "fin",
        "french": "fra",
        "middle_french": "frm",
        "frisian": "fry",
        "scottish_gaelic": "gla",
        "irish": "gle",
        "galician": "glg",
        "ancient_greek": "grc",
        "gujarati": "guj",
        "haitian_creole": "hat",
        "hebrew": "heb",
        "hindi": "hin",
        "croatian": "hrv",
        "hungarian": "hun",
        "armenian": "hye",
        "inuktitut": "iku",
        "indonesian": "ind",
        "icelandic": "isl",
        "italian": "ita",
        "old_italian": "ita_old",
        "javanese": "jav",
        "japanese": "jpn",
        "japanese_vertical": "jpn_vert",
        "kannada": "kan",
        "georgian": "kat",
        "old_georgian": "kat_old",
        "kazakh": "kaz",
        "khmer": "khm",
        "kyrgyz": "kir",
        "kurdish_kurmanji": "kmr",
        "korean": "kor",
        "korean_vertical": "kor_vert",
        "lao": "lao",
        "latin": "lat",
        "latvian": "lav",
        "lithuanian": "lit",
        "luxembourgish": "ltz",
        "malayalam": "mal",
        "marathi": "mar",
        "macedonian": "mkd",
        "maltese": "mlt",
        "mongolian": "mon",
        "maori": "mri",
        "malay": "msa",
        "burmese": "mya",
        "nepali": "nep",
        "dutch": "nld",
        "norwegian": "nor",
        "occitan": "oci",
        "oriya": "ori",
        "script_detection": "osd",
        "punjabi": "pan",
        "polish": "pol",
        "portuguese": "por",
    },
}


def lang_auto_detect(
    lang,
    model="easyocr",  # "easyocr" or "pytesseract"
):
    models = ["easyocr", "paddleocr", "pytesseract"]
    model = strcmp(model, models)[0]
    res_lang = []
    if isinstance(lang, str):
        lang = [lang]
    for i in lang:
        res_lang.append(lang_valid[model][strcmp(i, list(lang_valid[model].keys()))[0]])
    return res_lang


def determine_src_points(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Sort contours by area and pick the largest one
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:5]
    src_points = None

    for contour in contours:
        epsilon = 0.02 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        if len(approx) == 4:  # We need a quadrilateral
            src_points = np.array(approx, dtype="float32")
            break

    if src_points is not None:
        # Order points in a specific order (top-left, top-right, bottom-right, bottom-left)
        src_points = src_points.reshape(4, 2)
        rect = np.zeros((4, 2), dtype="float32")
        s = src_points.sum(axis=1)
        diff = np.diff(src_points, axis=1)
        rect[0] = src_points[np.argmin(s)]
        rect[2] = src_points[np.argmax(s)]
        rect[1] = src_points[np.argmin(diff)]
        rect[3] = src_points[np.argmax(diff)]
        src_points = rect
    else:
        # If no rectangle is detected, fallback to a default or user-defined points
        height, width = image.shape[:2]
        src_points = np.array(
            [[0, 0], [width - 1, 0], [width - 1, height - 1], [0, height - 1]],
            dtype="float32",
        )
    return src_points


def get_default_camera_matrix(image_shape):
    height, width = image_shape[:2]
    focal_length = width
    center = (width / 2, height / 2)
    camera_matrix = np.array(
        [[focal_length, 0, center[0]], [0, focal_length, center[1]], [0, 0, 1]],
        dtype="float32",
    )
    dist_coeffs = np.zeros((4, 1))  # Assuming no distortion
    return camera_matrix, dist_coeffs


def correct_perspective(image, src_points):
    # Define the destination points for the perspective transform
    width, height = 1000, 1000  # Adjust size as needed
    dst_points = np.array(
        [[0, 0], [width - 1, 0], [width - 1, height - 1], [0, height - 1]],
        dtype="float32",
    )

    # Calculate the perspective transform matrix
    M = cv2.getPerspectiveTransform(src_points, dst_points)
    # Apply the perspective transform
    corrected_image = cv2.warpPerspective(image, M, (width, height))
    return corrected_image


def detect_text_orientation(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)

    if lines is None:
        return 0

    angles = []
    for rho, theta in lines[:, 0]:
        angle = theta * 180 / np.pi
        if angle > 90:
            angle -= 180
        angles.append(angle)

    median_angle = np.median(angles)
    return median_angle


def rotate_image(image, angle):
    center = (image.shape[1] // 2, image.shape[0] // 2)
    rot_mat = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated_image = cv2.warpAffine(
        image, rot_mat, (image.shape[1], image.shape[0]), flags=cv2.INTER_LINEAR
    )
    return rotated_image


def correct_skew(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    coords = np.column_stack(np.where(gray > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(
        image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE
    )
    return rotated


def undistort_image(image, camera_matrix, dist_coeffs):
    return cv2.undistort(image, camera_matrix, dist_coeffs)


def add_text_pil(
    image,
    text,
    position,
    font_size=12,
    color=(0, 0, 0),
    bg_color=(133, 203, 245, 100),
):
    # Convert the image to PIL format
    pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB)).convert("RGBA")
    # Define the font (make sure to use a font that supports Chinese characters)
    overlay = Image.new("RGBA", pil_image.size, (255, 255, 255, 0))
    # Create a drawing context
    draw = ImageDraw.Draw(overlay)

    try:
        font = ImageFont.truetype(
            "/System/Library/Fonts/Supplemental/Songti.ttc", font_size
        )
    except IOError:
        font = ImageFont.load_default()

    # cal top_left position
    # Measure text size using textbbox
    text_bbox = draw.textbbox((0, 0), text, font=font)
    # # 或者只画 text, # Calculate text size
    # text_width, text_height = draw.textsize(text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    # Draw background rectangle
    x, y = position
    # Calculate 5% of the text height for upward adjustment
    offset = int(
        0.1 * text_height
    )  # 这就不再上移动了; # int(0.5 * text_height)  # 上移动 50%

    # Adjust position to match OpenCV's bottom-left alignment
    adjusted_position = (position[0], position[1] - text_height - offset)

    background_rect = [
        adjusted_position[0],
        adjusted_position[1],
        x + text_width,
        y + text_height,
    ]
    draw.rectangle(background_rect, fill=bg_color)
    # Add text to the image
    draw.text(adjusted_position, text, font=font, fill=color)
    # Ensure both images are in RGBA mode for alpha compositing
    if pil_image.mode != "RGBA":
        pil_image = pil_image.convert("RGBA")
    if overlay.mode != "RGBA":
        overlay = overlay.convert("RGBA")
    combined = Image.alpha_composite(pil_image, overlay)
    # Convert the image back to OpenCV format
    image = cv2.cvtColor(np.array(combined), cv2.COLOR_RGBA2BGR)
    return image


def preprocess_img(
    image,
    grayscale=True,
    threshold=True,
    threshold_method="adaptive",
    rotate="auto",
    skew=False,
    blur=True,
    blur_ksize=(5, 5),
    morph=True,
    morph_op="open",
    morph_kernel_size=(3, 3),
    enhance_contrast=True,
    clahe_clip=2.0,
    clahe_grid_size=(8, 8),
    edge_detection=False,
):
    """
    预处理步骤:

    转换为灰度图像: 如果 grayscale 为 True，将图像转换为灰度图像。
    二值化处理: 根据 threshold 和 threshold_method 参数，对图像进行二值化处理。
    降噪处理: 使用高斯模糊对图像进行降噪。
    形态学处理: 根据 morph_op 参数选择不同的形态学操作（开运算、闭运算、膨胀、腐蚀），用于去除噪声或填补孔洞。
    对比度增强: 使用 CLAHE 技术增强图像对比度。
    边缘检测: 如果 edge_detection 为 True，使用 Canny 边缘检测算法。

    预处理图像以提高 OCR 识别准确性。
    参数:
    image: 输入的图像路径或图像数据。
    grayscale: 是否将图像转换为灰度图像。
    threshold: 是否对图像进行二值化处理。
    threshold_method: 二值化方法，可以是 'global' 或 'adaptive'。
    denoise: 是否对图像进行降噪处理。
    blur_ksize: 高斯模糊的核大小。
    morph: 是否进行形态学处理。
    morph_op: 形态学操作的类型，包括 'open'（开运算）、'close'（闭运算）、'dilate'（膨胀）、'erode'（腐蚀）。
    morph_kernel_size: 形态学操作的内核大小。
    enhance_contrast: 是否增强图像对比度。
    clahe_clip: CLAHE（对比度受限的自适应直方图均衡）的剪裁限制。
    clahe_grid_size: CLAHE 的网格大小。
    edge_detection: 是否进行边缘检测。
    """
    if isinstance(image, PIL.PngImagePlugin.PngImageFile):
        image = np.array(image)
    if isinstance(image, str):
        image = cv2.imread(image)
    if not isinstance(image, np.ndarray):
        image = np.array(image)
    try:
        if image.shape[1] == 4:  # Check if it has an alpha channel
            # Drop the alpha channel (if needed), or handle it as required
            image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)
        else:
            # Convert RGB to BGR for OpenCV compatibility
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    except:
        pass

    # Rotate image
    if rotate == "auto":
        angle = detect_angle(image, by="fft")
        img_preprocessed = rotate_image(image, angle)
    else:
        img_preprocessed = image

    # Correct skew
    if skew:
        img_preprocessed = correct_skew(image)

    # Convert to grayscale
    if grayscale:
        img_preprocessed = cv2.cvtColor(img_preprocessed, cv2.COLOR_BGR2GRAY)

    # Thresholding
    if threshold:
        if threshold_method == "adaptive":
            image = cv2.adaptiveThreshold(
                img_preprocessed,
                255,
                cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY,
                11,
                2,
            )
        elif threshold_method == "global":
            _, img_preprocessed = cv2.threshold(
                img_preprocessed, 127, 255, cv2.THRESH_BINARY
            )

    # Denoise by Gaussian Blur
    if blur:
        img_preprocessed = cv2.GaussianBlur(img_preprocessed, blur_ksize, 0)

    # 形态学处理
    if morph:
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, morph_kernel_size)
        if morph_op == "close":  # 闭运算
            # 目的： 闭运算用于填补前景物体中的小孔或间隙，同时保留其形状和大小。
            # 工作原理： 闭运算先进行膨胀，然后进行腐蚀。膨胀步骤填补小孔或间隙，腐蚀步骤恢复较大物体的形状。
            # 效果：
            # 填补前景物体中的小孔和间隙。
            # 平滑较大物体的边缘。
            # 示例用途： 填补物体中的小孔或间隙。
            img_preprocessed = cv2.morphologyEx(
                img_preprocessed, cv2.MORPH_CLOSE, kernel
            )
        elif morph_op == "open":  # 开运算
            # 目的： 开运算用于去除背景中的小物体或噪声，同时保留较大物体的形状和大小。
            # 工作原理： 开运算先进行腐蚀，然后进行膨胀。腐蚀步骤去除小规模的噪声，膨胀步骤恢复剩余物体的大小。
            # 效果：
            # 去除前景中的小物体。
            # 平滑较大物体的轮廓。
            # 示例用途： 去除小噪声或伪影，同时保持较大物体完整。
            img_preprocessed = cv2.morphologyEx(
                img_preprocessed, cv2.MORPH_OPEN, kernel
            )
        elif morph_op == "dilate":  # 膨胀
            # 目的： 膨胀操作在物体边界上添加像素。它可以用来填补物体中的小孔或连接相邻的物体。
            # 工作原理： 内核在图像上移动，每个位置上的像素值被设置为内核覆盖区域中的最大值。
            # 效果：
            # 物体变大。
            # 填补物体中的小孔或间隙。
            # 示例用途： 填补物体中的小孔或连接断裂的物体部分。
            img_preprocessed = cv2.dilate(img_preprocessed, kernel)
        elif morph_op == "erode":  # 腐蚀
            # 目的： 腐蚀操作用于去除物体边界上的像素。它可以用来去除小规模的噪声，并将靠近的物体分开。
            # 工作原理： 内核（结构元素）在图像上移动，每个位置上的像素值被设置为内核覆盖区域中的最小值。
            # 效果：
            # 物体变小。
            # 去除图像中的小白点（在白色前景/黑色背景的图像中）。
            # 示例用途： 去除二值图像中的小噪声或分离相互接触的物体
            img_preprocessed = cv2.erode(img_preprocessed, kernel)

    # 对比度增强
    if enhance_contrast:
        clahe = cv2.createCLAHE(clipLimit=clahe_clip, tileGridSize=clahe_grid_size)
        img_preprocessed = clahe.apply(img_preprocessed)

    # 边缘检测
    if edge_detection:
        img_preprocessed = cv2.Canny(img_preprocessed, 100, 200)

    return img_preprocessed


def text_postprocess(
    text,
    spell_check=True,
    clean=True,
    filter=dict(min_length=2),
    pattern=None,
    merge=True,
):

    def correct_spelling(text_list):
        spell = SpellChecker()
        corrected_text = [spell.candidates(word) for word in text_list]
        return corrected_text

    def clean_text(text_list):
        cleaned_text = [re.sub(r"[^\w\s]", "", text) for text in text_list]
        return cleaned_text

    def filter_text(text_list, min_length=2):
        filtered_text = [text for text in text_list if len(text) >= min_length]
        return filtered_text

    def extract_patterns(text_list, pattern):
        pattern = re.compile(pattern)
        matched_text = [text for text in text_list if pattern.search(text)]
        return matched_text

    def merge_fragments(text_list):
        merged_text = " ".join(text_list)
        return merged_text

    results = text
    print(results)
    if spell_check:
        results = correct_spelling(results)
    if clean:
        results = clean_text(results)
    if filter:
        results = filter_text(
            results, min_length=postprocess["filter"].get("min_length", 2)
        )
    if pattern:
        results = extract_patterns(results, postprocess["pattern"])
    if merge:
        results = merge_fragments(results)


# https://www.jaided.ai/easyocr/documentation/
# extract text from an image with EasyOCR
def get_text(
    image,
    lang=["ch_sim", "en"],
    model="paddleocr",  # "pytesseract","paddleocr","easyocr"
    thr=0.1,
    gpu=True,
    decoder="wordbeamsearch",  #'greedy', 'beamsearch' and 'wordbeamsearch'(hightly accurate)
    output="txt",
    preprocess=None,
    postprocess="not ready",
    show=True,
    ax=None,
    cmap=cv2.COLOR_BGR2RGB,  # draw_box
    font=cv2.FONT_HERSHEY_SIMPLEX,
    font_scale=0.8,
    thickness_text=2,  # Line thickness of 2 px
    box_color=(0, 255, 0),  # draw_box
    font_color=(0, 0, 0),
    bg_color=(133, 203, 245, 100),
    usage=False,
    **kwargs,
):
    """
    功能: 该函数使用 EasyOCR 进行文本识别，并允许自定义图像预处理步骤和结果展示。
    参数:
    image: 输入的图像路径或图像数据。
    lang: OCR 语言列表。
    thr: 置信度阈值，低于此阈值的检测结果将被过滤。
    gpu: 是否使用 GPU。
    output: 输出类型，可以是 'all'（返回所有检测结果）、'text'（返回文本）、'score'（返回置信度分数）、'box'（返回边界框）。
    preprocess: 预处理参数字典，传递给 preprocess_img 函数。
    show: 是否显示结果图像。
    ax: 用于显示图像的 Matplotlib 子图。
    cmap: 用于显示图像的颜色映射。
    box_color: 边界框的颜色。
    font_color: 文本的颜色。
    kwargs: 传递给 EasyOCR readtext 函数的其他参数。

    # Uage
    """
    if usage:
        print(
            """
        image_path = 'car_plate.jpg'  # 替换为你的图像路径
        results = get_text(
            image_path,
            lang=["en"],
            gpu=False,
            output="text",
            preprocess={
                "grayscale": True,
                "threshold": True,
                "threshold_method": 'adaptive',
                "blur": True,
                "blur_ksize": (5, 5),
                "morph": True,
                "morph_op": 'close',
                "morph_kernel_size": (3, 3),
                "enhance_contrast": True,
                "clahe_clip": 2.0,
                "clahe_grid_size": (8, 8),
                "edge_detection": False
            },
            adjust_contrast=0.7
        )
    """
        )

    models = ["easyocr", "paddleocr", "pytesseract"]
    model = strcmp(model, models)[0]
    lang = lang_auto_detect(lang, model)
    if isinstance(image, str):
        image = cv2.imread(image)

    # Ensure lang is always a list
    if isinstance(lang, str):
        lang = [lang]

    # ! preprocessing img
    if preprocess is None:
        preprocess = {}
    image_process = preprocess_img(image, **preprocess)
    if "easy" in model.lower():
        print(f"detecting language(s):{lang}")
        # Perform OCR on the image
        reader = easyocr.Reader(lang, gpu=gpu)
        detections = reader.readtext(image_process, decoder=decoder, **kwargs)
        if postprocess is None:
            postprocess = dict(
                spell_check=True,
                clean=True,
                filter=dict(min_length=2),
                pattern=None,
                merge=True,
            )
            text_corr = []
            [
                text_corr.extend(text_postprocess(text, **postprocess))
                for _, text, _ in detections
            ]
        if show:
            if ax is None:
                ax = plt.gca()
            for bbox, text, score in detections:
                if score > thr:
                    top_left = tuple(map(int, bbox[0]))
                    bottom_right = tuple(map(int, bbox[2]))
                    image = cv2.rectangle(image, top_left, bottom_right, box_color, 2)
                    # image = cv2.putText(
                    #     image, text, top_left, font, font_scale, font_color, thickness_text
                    # )
                    image = add_text_pil(
                        image,
                        text,
                        top_left,
                        font_size=font_scale * 32,
                        color=font_color,
                    )
            # img_cmp = cv2.cvtColor(image, cmap)
            ax.imshow(image)
            ax.axis("off")
            # plt.show()
            # 根据输出类型返回相应的结果
            if output == "all":
                return ax, detections
            elif "t" in output.lower() and "x" in output.lower():
                # 提取文本，过滤低置信度的结果
                text = [text_ for _, text_, score_ in detections if score_ >= thr]
                if postprocess:
                    return ax, text
                else:
                    return text_corr
            elif "score" in output.lower() or "prob" in output.lower():
                # 提取分数
                scores = [score_ for _, _, score_ in detections]
                return ax, scores
            elif "box" in output.lower():
                # 提取边界框，过滤低置信度的结果
                bboxes = [bbox_ for bbox_, _, score_ in detections if score_ >= thr]
                return ax, bboxes
            else:
                # 默认返回所有检测信息
                return ax, detections
        else:
            # 根据输出类型返回相应的结果
            if output == "all":
                return detections
            elif "t" in output.lower() and "x" in output.lower():
                # 提取文本，过滤低置信度的结果
                text = [text_ for _, text_, score_ in detections if score_ >= thr]
                return text
            elif "score" in output.lower() or "prob" in output.lower():
                # 提取分数
                scores = [score_ for _, _, score_ in detections]
                return scores
            elif "box" in output.lower():
                # 提取边界框，过滤低置信度的结果
                bboxes = [bbox_ for bbox_, _, score_ in detections if score_ >= thr]
                return bboxes
            else:
                # 默认返回所有检测信息
                return detections
    elif "pad" in model.lower():
        ocr = PaddleOCR(
            use_angle_cls=True,
            cls=True,
        )  # PaddleOCR supports only one language at a time
        result = ocr.ocr(image_process, **kwargs)
        detections = []
        for line in result[0]:
            bbox, (text, score) = line
            detections.append((bbox, text, score))
        if postprocess is None:
            postprocess = dict(
                spell_check=True,
                clean=True,
                filter=dict(min_length=2),
                pattern=None,
                merge=True,
            )
            text_corr = []
            [
                text_corr.extend(text_postprocess(text, **postprocess))
                for _, text, _ in detections
            ]
        if show:
            if ax is None:
                ax = plt.gca()
            for bbox, text, score in detections:
                if score > thr:
                    top_left = tuple(map(int, bbox[0]))
                    bottom_left = tuple(
                        map(int, bbox[1])
                    )  # Bottom-left for more accurate placement
                    bottom_right = tuple(map(int, bbox[2]))
                    image = cv2.rectangle(image, top_left, bottom_right, box_color, 2)
                    # image = cv2.putText(
                    #     image, text, top_left, font, font_scale, font_color, thickness_text
                    # )
                    image = add_text_pil(
                        image,
                        text,
                        top_left,
                        font_size=font_scale * 32,
                        color=font_color,
                        bg_color=bg_color,
                    )
            img_cmp = cv2.cvtColor(image, cmap)
            ax.imshow(image)
            ax.axis("off")
            # plt.show()
            # 根据输出类型返回相应的结果
            if output == "all":
                return ax, detections
            elif "t" in output.lower() and "x" in output.lower():
                # 提取文本，过滤低置信度的结果
                text = [text_ for _, text_, score_ in detections if score_ >= thr]
                if postprocess:
                    return ax, text
                else:
                    return text_corr
            elif "score" in output.lower() or "prob" in output.lower():
                # 提取分数
                scores = [score_ for _, _, score_ in detections]
                return ax, scores
            elif "box" in output.lower():
                # 提取边界框，过滤低置信度的结果
                bboxes = [bbox_ for bbox_, _, score_ in detections if score_ >= thr]
                return ax, bboxes
            else:
                # 默认返回所有检测信息
                return ax, detections
        else:
            # 根据输出类型返回相应的结果
            if output == "all":
                return detections
            elif "t" in output.lower() and "x" in output.lower():
                # 提取文本，过滤低置信度的结果
                text = [text_ for _, text_, score_ in detections if score_ >= thr]
                return text
            elif "score" in output.lower() or "prob" in output.lower():
                # 提取分数
                scores = [score_ for _, _, score_ in detections]
                return scores
            elif "box" in output.lower():
                # 提取边界框，过滤低置信度的结果
                bboxes = [bbox_ for bbox_, _, score_ in detections if score_ >= thr]
                return bboxes
            else:
                # 默认返回所有检测信息
                return detections

    else:  # "pytesseract"
        if ax is None:
            ax = plt.gca()
        text = pytesseract.image_to_string(image_process, lang="+".join(lang), **kwargs)
        bboxes = pytesseract.image_to_boxes(image_process, **kwargs)
        if show:
            # Image dimensions
            h, w, _ = image.shape

            for line in bboxes.splitlines():
                parts = line.split()
                if len(parts) == 6:
                    char, left, bottom, right, top, _ = parts
                    left, bottom, right, top = map(int, [left, bottom, right, top])

                    # Convert Tesseract coordinates (bottom-left and top-right) to (top-left and bottom-right)
                    top_left = (left, h - top)
                    bottom_right = (right, h - bottom)

                    # Draw the bounding box
                    image = cv2.rectangle(image, top_left, bottom_right, box_color, 2)
                    image = add_text_pil(
                        image,
                        char,
                        left,
                        font_size=font_scale * 32,
                        color=font_color,
                    )
            img_cmp = cv2.cvtColor(image, cmap)
            ax.imshow(img_cmp)
            ax.axis("off")
            if output == "all":
                # Get verbose data including boxes, confidences, line and page numbers
                detections = pytesseract.image_to_data(image_process)
                return ax, detections
            elif "t" in output.lower() and "x" in output.lower():
                return ax, text
            elif "box" in output.lower():
                return ax, bboxes
            else:
                # Get information about orientation and script detection
                return pytesseract.image_to_osd(image_process, **kwargs)
        else:
            if output == "all":
                # Get verbose data including boxes, confidences, line and page numbers
                detections = pytesseract.image_to_data(image_process, **kwargs)
                return detections
            elif "t" in output.lower() and "x" in output.lower():
                return text
            elif "box" in output.lower():
                return bboxes
            else:
                # Get information about orientation and script detection
                return pytesseract.image_to_osd(image_process, **kwargs)


def draw_box(
    image,
    detections=None,
    thr=0.25,
    cmap=cv2.COLOR_BGR2RGB,
    box_color=(0, 255, 0),  # draw_box
    font_color=(0, 0, 255),  # draw_box
    font_scale=0.8,
    show=True,
    ax=None,
    **kwargs,
):

    if ax is None:
        ax = plt.gca()
    if isinstance(image, str):
        image = cv2.imread(image)
    if detections is None:
        detections = get_text(image=image, show=0, output="all", **kwargs)

    for bbox, text, score in detections:
        if score > thr:
            top_left = tuple(map(int, bbox[0]))
            bottom_right = tuple(map(int, bbox[2]))
            image = cv2.rectangle(image, top_left, bottom_right, box_color, 2)
            # image = cv2.putText(
            #     image, text, top_left, font, font_scale, font_color, thickness_text
            # )
            image = add_text_pil(
                image, text, top_left, font_size=font_scale * 32, color=font_color
            )

    img_cmp = cv2.cvtColor(image, cmap)
    if show:
        ax.imshow(img_cmp)
        ax.axis("off")
        # plt.show()
    return img_cmp
