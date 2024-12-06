# coding=utf-8
from typing import Iterable, Any, Optional

from .color import _Color, Color


class CellValue:
    """
    单元格的值
    """

    def __init__(
            self, rawValue: Any, row: int, column: int, width: int, height: int,
            color: str | tuple[int, int, int] = 'black',
            font=None  # PIL.ImageFont.FreeTypeFont
    ):
        """
        初始化单元格
        :param rawValue: 初始的值
        :param row: 所在的行
        :param column: 所在的列
        :param width: 宽度
        :param height: 高度
        :param color: 颜色
        :param font: 字体
        """
        self.rawValue = rawValue
        self.row = row
        self.column = column
        self.width = width
        self.height = height
        self.color = color
        self.font = font
        self.value = rawValue


class TableColumn:
    def __init__(self, width: int | None = None, color: str | tuple[int, int, int] = 'black'):
        self.color = color
        self._autoWidth = width is None  # None则自动计算宽度
        self.width = width if width is not None else 10

    def setWidth(self, width: int):
        if self._autoWidth:
            self.width = max(self.width, width)


class ConsoleTable:

    def __init__(self, data: Iterable[dict[str, Any]], max_width=100, caption='',
                 caption_color=Color.yellow, title_color=Color.thin_cyan, colorize=True):
        def init_value(val):
            if isinstance(val, str | _Color):
                return val
            if val is None:
                return ''
            return str(val)

        self.colorize = colorize
        self.caption = caption
        self.caption_color = caption_color
        self.title_color = title_color
        self.data = [{str(k): init_value(v) for k, v in row.items()} for row in data]
        self.header = list(self.data[0].keys()) if data else []
        self.max_width = max_width
        self.col_width = []
        self._table_str = ""
        self.col_width = self._get_widths()
        self._table_str = self.make_table_str() if self.colorize else self.make_table_str_without_color()

    @staticmethod
    def _get_string_width(val: str | _Color):
        w = 0
        for v in val:
            if u'\u4e00' <= v <= u'\u9fff' or v in '【】（）—…￥！·、？。，《》：；‘“':
                w += 2
            else:
                w += 1
        return w

    def _get_widths(self):
        """获取列宽度，列宽度为整列数据中的最大数据宽度"""

        col_width = [self._get_string_width(key) for key in self.header]
        for row in self.data:
            for i, key in enumerate(self.header):
                value = row.get(key, '')
                width = min(self._get_string_width(value), self.max_width)
                col_width[i] = max(col_width[i], width)
        return col_width

    def _initValueByWidth(self, val: str, width: int):
        newVal = ""
        curWidth = 0
        for v in val:
            w = self._get_string_width(v)
            if curWidth + w > width:
                return newVal[:-3] + '...'
            curWidth += w
            newVal += v
        return newVal

    def make_table_str(self):
        def format_str(val, width):
            val = self._initValueByWidth(val, width)
            length = self._get_string_width(val)
            left = (width - length) // 2
            right = (width - length) - left
            return f'{" " * left}{val}{" " * right}'

        header = ' | '.join(str(self.title_color(format_str(key, w))) for w, key in zip(self.col_width, self.header))
        if self.caption:
            caption = self.caption_color(format_str(self.caption, sum(self.col_width) + (len(self.col_width) - 1) * 3))
            header = caption + '\n' + header
        rows = [' | '.join(format_str(row.get(key, ""), w) for w, key in zip(self.col_width, self.header)) for row in
                self.data]
        return '\n'.join([header, '=' * (sum(self.col_width) + (len(self.col_width) - 1) * 3)] + rows)

    def make_table_str_without_color(self):
        def format_str(val, width):
            length = self._get_string_width(val)
            left = (width - length) // 2
            right = (width - length) - left
            return f'{" " * left}{val}{" " * right}'

        def get_value(row, key):
            val = row.get(key, "")
            if isinstance(val, _Color):
                return val.raw
            return val

        header = ' | '.join(str(format_str(key, w)) for w, key in zip(self.col_width, self.header))
        if self.caption:
            caption = format_str(self.caption, sum(self.col_width) + (len(self.col_width) - 1) * 3)
            header = caption + '\n' + header
        rows = [' | '.join(format_str(get_value(row, key), w) for w, key in zip(self.col_width, self.header)) for row in
                self.data]
        return '\n'.join([header, '=' * (sum(self.col_width) + (len(self.col_width) - 1) * 3)] + rows)

    def __str__(self):
        return self._table_str

    __repr__ = __str__

    def to_image(
            self,
            *,
            odd_row_color='#f8f9fa', even_row_color='white', header_color='#B4DCFF',
            cell_char_size=40,
            font_path: str | None = None, title_font_path: str | None = None,
            font_size=12, title_font_size: Optional[int] = None
    ):
        """
        将表格转换为图片
        :param odd_row_color: 偶数行颜色，默认为 #f8f9fa
        :param even_row_color: 奇数行颜色，默认为 white
        :param header_color: 表头颜色，默认为 #B4DCFF
        :param cell_char_size: 单元格中的单行文本字符数，默认为40，超过这个长度的文本将会被换行显示
        :param font_path: 字体文件路径，一般采用
        :param title_font_path: 表头字体文件路径，一般采用加粗字体
        :param font_size: 字体大小，默认为12
        :param title_font_size: 表头字体大小，默认为font_size + 2
        :return:
        """
        try:
            from PIL import Image, ImageDraw, ImageFont
        except ModuleNotFoundError:
            raise ModuleNotFoundError('请先安装pillow（pip install pillow -U）')

        def split(value, size):
            v = str(value)
            return '\n'.join(('\n'.join(j[i:i + size] for i in range(0, len(j), size))) for j in v.split('\n'))

        data = self.data

        baseImg = Image.new('RGB', (1920, 1080))
        baseDraw = ImageDraw.Draw(baseImg)
        # 初始化字体
        font_path = font_path or 'simhei.ttf'
        title_font_path = title_font_path or font_path or 'msyhbd.ttc'
        font = ImageFont.truetype(font_path, size=font_size)
        bFont = ImageFont.truetype(title_font_path, size=title_font_size or (font_size + 2))

        captionW, captionH = 0, 0
        if self.caption:
            _, _, captionW, captionH = baseDraw.textbbox((0, 0), self.caption, font=bFont)
            captionW, captionH = int(captionW), int(captionH)
        if not data:
            _, _, w, h = baseDraw.textbbox((0, 0), '暂无数据', font=font)
            totalWidth, totalHeight = max(captionW, int(w)) + 20, int(h) + captionH + 15 + 20
            image = Image.new('RGB', (totalWidth, totalHeight), color=(255, 255, 255))
            draw = ImageDraw.Draw(image)
            if self.caption:
                draw.text(((totalWidth - captionW) // 2, 10), self.caption, font=bFont, fill=(0, 0, 0))
                x1, x2, y1, y2 = (totalWidth - captionW) // 2, (
                        totalWidth + captionW) // 2, 12 + captionH, 14 + captionH
                draw.line(((x1, y1), (x2, y1)), fill=(0, 0, 0))
                draw.line(((x1, y2), (x2, y2)), fill=(0, 0, 0))
            draw.text(((totalWidth - int(w)) // 2, 15 + captionH + 10), '暂无数据', font=font, fill='#3E3F41')
            return image
        table: list[list[CellValue]] = [[] for _ in range(len(data) + 1)]
        widths, heights = [10] * len(data[0].keys()), [10] * (len(data) + 1)
        for i, key in enumerate(data[0].keys()):
            val = split(str(key), cell_char_size)
            _, _, w, h = baseDraw.textbbox((0, 0), val, font=bFont)
            table[0].append(CellValue(val, row=0, column=i, width=int(w), height=int(h) + 2, font=bFont))
            heights[0] = max(heights[0], int(h) + 2)
            widths[i] = max(widths[i], int(w))

        for i, row in enumerate(data, start=1):
            for j, key in enumerate(data[0].keys()):
                rawVal = row.get(key)
                color = 'black'
                if rawVal is None:
                    val = ''
                elif isinstance(rawVal, _Color):
                    val = rawVal.raw
                    color = rawVal.hexValue
                else:
                    val = str(rawVal)
                _, _, w, h = baseDraw.textbbox((0, 0), val, font=font)
                table[i].append(
                    CellValue(val, row=i, column=j, width=int(w), height=int(h) + 2, color=color, font=font)
                )
                widths[j] = max(widths[j], int(w))
                heights[i] = max(heights[i], int(h) + 2)

        totalWidth = max(sum(widths) + (len(widths) + 1) * 10, captionW)
        totalHeight = sum(heights) + (len(heights) + 1) * 12 + (captionH + 15 if self.caption else 0)
        img = Image.new('RGB', (totalWidth, totalHeight), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)
        pHeight = 0
        if self.caption:
            draw.text(((totalWidth - captionW) // 2, 10), self.caption, font=bFont, fill=(0, 0, 0))
            x1, x2, y1, y2 = (totalWidth - captionW) // 2, (totalWidth + captionW) // 2, 12 + captionH, 14 + captionH
            draw.line(((x1, y1), (x2, y1)), fill=(0, 0, 0))
            draw.line(((x1, y2), (x2, y2)), fill=(0, 0, 0))
            pHeight = 15 + captionH
        for i, row in enumerate(table, start=1):
            curHeight = pHeight + i * 12 + sum(heights[:i - 1])
            if i > 1:
                draw.rectangle(
                    [(5, curHeight - 5), (totalWidth - 5, curHeight + heights[i - 1] + 5)],
                    fill=odd_row_color if i % 2 == 1 else even_row_color
                )
            else:
                draw.rectangle(
                    [(5, curHeight - 5), (totalWidth - 5, curHeight + heights[i - 1] + 5)],
                    fill=header_color
                )
            for j, val in enumerate(row, start=1):
                curWidth = j * 10 + sum(widths[:j - 1])
                draw.text(
                    (curWidth, curHeight), val.value,
                    font=val.font,
                    fill=val.color)

            draw.line(
                [(5, curHeight + heights[i - 1] + 5), (totalWidth - 5, curHeight + heights[i - 1] + 5)]
                , fill=(0, 0, 0) if i == 1 else (202, 202, 202),
                width=2)
        return img



if __name__ == '__main__':
    table = ConsoleTable(
        [{'server_name': 'intelligent-platform-product', 'status': Color.green('成功'), 'message': '构建成功'}],
        caption='构建结果',
    )
    print(table)
