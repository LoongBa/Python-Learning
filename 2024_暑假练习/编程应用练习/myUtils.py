import os

__is_debug__ = True  # 启用 debug 输出

def debug_print(message, color="yellow", level = 0, end_str="\r\n"):
    if __is_debug__ and level >= 0:
        print_color(f"[Debug]{level} {message}", color)
    else:
        pass
    return

def print_error(message):
    print_color(message, "red")
    return

def print_color(message, color="green", end_str="\r\n"):
    text = color_text(color, message)
    # 用 switch 判断常用的颜色，或者用 字典
    print(text, end=end_str)

def color_text(color, text):
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "purple": "\033[95m",
        "cyan": "\033[96m",
        "white": "\033[97m",
        "reset": "\033[0m",
    }

    if color in colors:
        return f"{colors[color]}{text}{colors['reset']}"
    else:
        return text

def run_file_by_default_app(file_path):
    if os.path.isfile(file_path):
        os.startfile(file_path)
    else:
        os.system(f"explorer.exe {file_path}")

    return
