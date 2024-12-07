from google_fonts.utils.font_data import get_font_names, fetch_ofl_list_json


def list_fonts(search_content: str = None):
    # 获取字体列表
    ofl_list = fetch_ofl_list_json()
    all_font_names = get_font_names(ofl_list)

    # 模糊匹配搜索
    if search_content is not None:
        all_font_names = [name for name in all_font_names if search_content.lower() in name.lower()]

    # 如果没有匹配结果
    if not all_font_names:
        print(f"No fonts found matching '{search_content}'")
        return

    # 设置每列的固定宽度
    column_width = max(len(name) for name in all_font_names) + 2  # 动态计算宽度，+2 用于额外间距

    # 按行打印，每行 5 个字体
    for i in range(0, len(all_font_names), 5):
        # 使用字符串的 ljust() 方法按固定宽度对齐
        print("\t".join(name.ljust(column_width) for name in all_font_names[i:i + 5]))


if __name__ == '__main__':
    list_fonts()
