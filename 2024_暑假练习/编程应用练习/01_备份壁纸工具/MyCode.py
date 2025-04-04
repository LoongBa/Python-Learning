def print_error(message):
    print_color(f"Error: {message}", "red")
    return

# 带颜色输出信息
def print_color(message, color_name = "green"):
    # 根据 color_name 设置 color_code 不同的颜色代码
    color_code = {
        'red': '\033[91m',      # 红色
        'green': '\033[92m',    # 绿色
        'yellow': '\033[93m',   # 黄色
        'blue': '\033[94m',     # 蓝色
        'magenta': '\033[95m',  # 品红色
        'cyan': '\033[96m',     # 青色
        'default': '\033[0m'           # 重置颜色
    }
    # 输出
    color_prefix = color_code.get(color_name, color_code['default'])
    color_postfix = color_code['default']
    print(f"{color_prefix}{message}{color_postfix}")
    return