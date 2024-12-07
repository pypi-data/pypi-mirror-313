# -*- coding: utf-8 -*-
from os import makedirs
from os.path import join
import fitz
import pdfplumber
from loguru import logger
from PIL import Image
from io import BytesIO

class ReadPdf:
    """
    读取pdf字符信息、文本块信息、保存图片
    """

    def __init__(self, pdf_路径):
        """读取pdf字符信息、文本块信息、保存图片
        :param pdf_路径:pdf文件存放路径
        """
        self.pdf_路径 = pdf_路径
        self.pdf = None

    def 读取PDF(self):
        self.pdf = pdfplumber.open(self.pdf_路径)
        self.pdf_页面列表 = self.pdf.pages
        self.总页数 = len(self.pdf.pages)

    def 读取PDF中的单个字符信息(self, 起始页=1, 结束页: int = None) -> dict:
        self.读取PDF()
        for 页码, 页面 in enumerate(self.pdf_页面列表[起始页 - 1:结束页 or self.总页数], start=起始页):
            页面字符信息 = []
            for 字符信息 in 页面.chars:
                页面字符信息.append({
                    '文字': 字符信息.get('text').replace('\u2009', ' '),
                    '字体': 字符信息.get('fontname'),
                    '字号': 字符信息.get('size'),
                    '位置': [字符信息.get('x0'), 字符信息.get('x1'), 字符信息.get('y0'), 字符信息.get('y1'), '左右上下'],# x0字符左侧到页面左侧的距离，x1字符右侧到页面左侧的距离，y0字符底部到页面底部的距离，y1字符顶部到页面底部的距离。
                    '宽度': 字符信息.get('width'),
                    '高度': 字符信息.get('height'),
                    '字符占用宽度比例': 字符信息.get('adv'),
                    '直立': 字符信息.get('upright'),  # 字符方向是否是直立的。
                    '字符id': 字符信息.get('mcid'),  # 该字符的部分ID(如果有的话)(否则None). 实验属性。
                    '标记': 字符信息.get('tag'),  # 该字符的部分标记(如果有)(否则None). 实验属性。
                    '字符轮廓颜色': 字符信息.get('stroking_color'),  # 字符轮廓的颜色。
                    '字符填充颜色': 字符信息.get('non_stroking_color'),  # 字符内部填充的颜色。
                    '页码': 页面.page_number, '页面宽度': 页面.width, '页面高度': 页面.height
                })

            yield 页面字符信息

    def 读取PDF中的文本块信息(self, 起始页=1, 结束页: int = None) -> dict:
        self.读取PDF()
        for 页码, 页面 in enumerate(self.pdf_页面列表[起始页 - 1:结束页 or self.总页数], start=起始页):
            页面文本块信息 = []
            for 文本块信息 in 页面.extract_words():
                页面文本块信息.append({
                    '文本': 文本块信息.get('text').replace('\u2009', ' '),
                    '位置': [文本块信息.get('x0'), 文本块信息.get('x1'), 文本块信息.get('top'), 文本块信息.get('bottom'), '左右上下'],# x0文本块左侧到页面左侧的距离，x1文本块右侧到页面左侧的距离，top文本块底部到页面底部的距离，bottom文本块顶部到页面底部的距离。
                    '宽度': 文本块信息.get('width'),
                    '高度': 文本块信息.get('height'),
                    '直立': 文本块信息.get('upright'),  # 文本块方向是否是直立的。
                    '文本块方向': {"ttb": "从上到下", "btt": "从下到上", "ltr": "从左到右", "rtl": "从右到左"}.get(文本块信息.get('direction')),  # “ttb”(从上到下)、“btt”(从下到上)、“ltr”(从左到右)和“rtl”(从右到左)。
                    '页码': 页面.page_number, '页面宽度': 页面.width, '页面高度': 页面.height
                })

            yield 页面文本块信息

    def 保存PDF中的图片(self, 起始页=1, 结束页: int = None, 图片修正角度:int=None,图片保存文件夹=None) -> None:
        """
        :param 图片修正角度:图片提取出来时角度错误，如顺时针旋转90度传入角度值90，逆时针旋转90度传入角度值-90，
        :param 图片保存文件夹:当不传入时，默认在pdf所在目录下创建与pdf相同名称的文件夹，并将图片保存在该文件夹下
        """
        if not 图片保存文件夹:
            图片保存文件夹 = self.pdf_路径[:-4]
            makedirs(图片保存文件夹, exist_ok=True)

        # 使用PyMuPDF获取页面
        pdf文件 = fitz.open(self.pdf_路径)

        for 页码, 页面 in enumerate(pdf文件[起始页 - 1:结束页 or len(pdf文件)], start=起始页):
            # 获取页面上的所有图像
            图片列表 = pdf文件[页码 - 1].get_images(full=True)

            # 保存页面上的所有图像
            for i, 图片 in enumerate(图片列表):
                图片 = pdf文件.extract_image(图片[0])
                图片后缀 = 图片.get('ext', 'png').lower()
                if 图片后缀 == 'jpeg': 图片后缀 = 'jpg'
                图片保存名称 = f"第{页码}页_第{i + 1}张图.{图片后缀}"
                图片保存路径 = join(图片保存文件夹, 图片保存名称)
                if 图片修正角度:
                    # 使用 BytesIO 将二进制数据转换为文件对象
                    图片_流数据 = BytesIO(图片["image"])
                    # 打开图像文件对象并加载为 Image 对象
                    图片 = Image.open(图片_流数据)
                    # 旋转图像
                    旋转的图片 = 图片.rotate(-图片修正角度, expand=True)  # expand=True 确保旋转后图像不会被裁剪
                    旋转的图片.save(图片保存路径)
                    图片_流数据.close()
                else:
                    with open(图片保存路径, "wb") as 图片文件:
                        图片文件.write(图片["image"])

                logger.success(f"{图片保存名称}已保存")

        logger.info(rf"图片保存文件夹：{图片保存文件夹}\ ".strip())
        pdf文件.close()

    def __del__(self):
        if self.pdf:
            self.pdf.close()