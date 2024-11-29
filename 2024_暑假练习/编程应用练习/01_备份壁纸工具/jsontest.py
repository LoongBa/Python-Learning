import json

# JSON数据字符串
backup_logs = '''
[
    {"Name":"xxxxxxxxxxxxxxxx1", "Hash":"zzzzzzzzzzzzzzzzzz1", "IsCopied": true, "DateTime": "", "BackupFilename":"file1.jpg"},
    {"Name":"xxxxxxxxxxxxxxxx2", "Hash":"zzzzzzzzzzzzzzzzzz2", "IsCopied": true, "DateTime": "", "BackupFilename":"file2.jpg"}
]
'''

# 解析JSON数据
backup_logs = json.loads(backup_logs)

def is_jpg_file_Copied(filename):
    result = [item for item in backup_logs if item["IsCopied"] and item["Name"] == filename]
    return len(result) > 0

def set_jpg_file_Copied(filename):
    result = [item for item in backup_logs if item["Name"] == filename]
    if len(result) > 0:
        result["IsCopied"] = True
    else:
        # 新增一条记录
        pass
    return result

# 打印解析后的数据
for log in backup_logs:
    #print(log)
    print(log["Name"], log["Hash"], log["IsCopied"], log["DateTime"], log["BackupFilename"])