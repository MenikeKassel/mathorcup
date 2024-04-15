from matplotlib import font_manager

def list_fonts():
    fonts = font_manager.findSystemFonts(fontpaths=None, fontext='ttf')
    # 创建一个字典来存储字体名称和路径
    font_dict = {}

    for font_path in fonts:
        font_prop = font_manager.FontProperties(fname=font_path)
        font_name = font_prop.get_name()
        # 将字体名称和路径添加到字典中
        font_dict[font_name] = font_path

    return font_dict

def print_chinese_fonts(font_dict):
    # 打印出所有中文字体的名称和路径
    print("中文字体列表:")
    for name, path in font_dict.items():
        if 'CJK' in name or 'Song' in name or 'Heiti' in name or 'Kai' in name or 'SimHei' in name or 'SimSun' in name:
            print(f"{name}: {path}")

# 获取字体字典
fonts = list_fonts()
# 打印所有中文字体
print_chinese_fonts(fonts)
