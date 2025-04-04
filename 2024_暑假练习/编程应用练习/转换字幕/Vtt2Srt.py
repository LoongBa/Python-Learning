import os
import sys

def vtt_to_srt(vtt_content):
    # 去除 VTT 文件的头部信息
    lines = vtt_content.splitlines()
    if lines and lines[0].startswith('WEBVTT'):
        lines = lines[1:]

    srt_content = ""
    index = 1
    for i, line in enumerate(lines):
        if "-->" in line:
            # 转换时间格式
            start_time, end_time = line.split(" --> ")
            start_time = start_time.replace('.', ',')
            end_time = end_time.replace('.', ',')
            srt_content += f"{index}\n{start_time} --> {end_time}\n"
            index += 1
        elif line.strip():
            srt_content += f"{line}\n"
        elif i > 0 and not line.strip():
            srt_content += "\n"
    return srt_content


def main():
    # 读取运行参数，取第一个作为文件名
    if len(sys.argv) <= 1:
        print("请提供 VTT 文件名")
        sys.exit(1)

    vtt_filename = sys.argv[1]
    # 检查文件是否存在
    if not os.path.exists(vtt_filename):
        print(f"文件 {vtt_filename} 不存在")
        sys.exit(1)
    # 如果是相对路径，转换为绝对路径
    vtt_filename = os.path.abspath(vtt_filename)
    srt_filename = vtt_filename.replace('.vtt', '.srt')

    with open(vtt_filename, 'r', encoding='utf-8') as f:
        vtt_content = f.read()
    srt_content = vtt_to_srt(vtt_content)
    with open(srt_filename, 'w', encoding='utf-8') as f:
        f.write(srt_content)

    return

if __name__ == '__main__':
    main()