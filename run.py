import os
import click
import math
from PIL import Image, ImageDraw, ImageFont

currrent_dir = (os.path.dirname(__file__)
                if "__file__" in locals() else os.getcwd())

# 边距的x坐标
OFFSET_X = 60
# 边距的y坐标
OFFSET_Y = 45
# 列宽
WIDTH = 116
# 行高
HEIGHT = 114.4
# 字体颜色
DARK = (0, 0, 0)
# 描摹字体颜色
LIGHT = (192, 192, 192)


@click.command()
@click.option("--fl", prompt="请输入文件名", help="需要输出的字帖文件名")
@click.option(
    "--blank_line",
    "-bl",
    prompt="是否增加空行",
    is_flag=True,
    expose_value=True,
    help="是否需要增加空行便于临摹",
)
@click.option(
    "--trace",
    prompt="是否需要描摹，开启空行时有效",
    is_flag=True,
    expose_value=True,
    help="是否添加描摹示例，仅在空行模式开启时有效",
)
# 字体
@click.option("--fn", default="zqcwxybxs.ttf", help="指定字体，字体文件放于安装文件夹的fonts目录中")
def main(fl, blank_line, trace, fn):
    # 设置字体字号
    font = ImageFont.truetype(os.path.join(currrent_dir, "fonts", fn), 100)

    # 如果有空行，文字数量减半
    if blank_line:
        max_char = int(16 * 24 / 2)
    else:
        max_char = 16 * 24

    #读取文件
    with open(fl, 'r', encoding='utf-8') as f:
        text = f.read()
    
    file_name = os.path.basename(fl)

    print('正在写入字帖...')

    # 分页写入
    for index, txt_index in enumerate(range(0, len(text), max_char)):
        # 写入米字格模板
        out = Image.open(os.path.join(currrent_dir, "template.png"))

        draw = ImageDraw.Draw(out)

        for i, c in enumerate(text[txt_index:txt_index + max_char]):
            # 计算x,y坐标
            x = OFFSET_X + (i % 16) * WIDTH
            y = OFFSET_Y + HEIGHT * (math.ceil((i + 1) / 16) - 1) * (2 if blank_line else 1)

            draw.text((x, y), c, DARK, font)

            # 如果启用空行跟描摹
            if blank_line and trace:
                draw.text((x, y + HEIGHT), c, LIGHT, font)

        # 写入图片
        draw = ImageDraw.Draw(out)
        out_file_name = "%s_%s.png" % (file_name, index)
        image_path = os.path.join(currrent_dir, "outputs", out_file_name)
        out.save(image_path)

    print('字帖生成完毕.')


if __name__ == "__main__":
    main()
