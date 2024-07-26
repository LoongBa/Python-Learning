# 3个自然数之间进行有意义的四则运算。
# 运算结果中，最大的自然数结果与最小的自然数结果相差35，
# 请问这三个自然数是多少？

import tqdm

def is_natural_number(n):
    return n == int(n) and n >= 0

def find_numbers():
    result = []
    for a in tqdm.tqdm(range(2, max_number + 1), desc="进度"):
        for b in range(min_number + 1, a):
            for c in range(min_number, b):
                temp_array = []
                external_result = []
                if c > 0:
                    # c > 1 时， a * b * c 最大，否则 a * (b + 1) > a * b * 1
                    if c == 1:
                        max_result = a * (b + 1)
                        temp_array = [a - b - 1, a - b, a * (b - 1), b * (a - 1)]
                        temp = a/b
                        if(is_natural_number(temp)):
                            external_result.append(int(temp))       # a/b/c
                    else:
                        max_result = a * b * c
                        temp_array = [a - b - c, a * c - b, a - b * c, a * (b - c), b * (a - c), c * (a - b)]
                        temp = a/b/c
                        if(is_natural_number(temp)):
                            external_result.append(int(temp))       # a/b/c
                        temp = a/c
                        if(is_natural_number(temp)):
                            temp = int(temp)
                            external_result.append(temp + b)   # a/c + b
                            external_result.append(temp - b)   # a/c - b
                        temp = b/c
                        if(is_natural_number(temp)):
                            external_result.append(int(temp) + a)   # b/c + a
                            external_result.append(int(temp) - a)   # b/c - a
                        temp = a/b
                        if(is_natural_number(temp)):
                            temp = int(temp)
                            external_result.append(temp + c)       # a/b + c
                            external_result.append(temp - c)       # a/b - c

                else:   # c == 0
                    max_result = max([a * b, a + b])
                    temp_array = [0]

                temp_array.extend(external_result)
                middle_array = [result for result in temp_array if is_natural_number(result)]
                if len(middle_array) == 0:
                    print(f"没有符合条件的数据：", temp_array)
                    continue
                else:
                    min_result = min(middle_array)
                
                if not is_natural_number(max_result) or not is_natural_number(min_result):
                    print(f"非自然数解: max_result = {max_result}, min_result = {min_result}")
                    continue

                # 如果最大结果和最小结果相差 difference，返回这三个数
                if max_result - min_result == difference:
                    result.append((a, b, c, middle_array, max_result, min_result, temp_array, external_result))
    return result

difference = 33
max_number = difference * 2     # 限制最大数值范围
min_number = 0                  # 限制最小数值范围
isDebug = True
#isDebug = False

if __name__ == "__main__":
    print("三个自然数之间进行有意义的四则运算。")
    print(f"运算结果中，最大的自然数结果与最小的自然数结果相差 {difference}，")
    print("请问这三个自然数是多少？\r\n")

    # 调用函数并打印结果
    result = find_numbers()

    print(f"\r\n从 {min_number} 到 {max_number} 找到的自然数组合个数: {len(result)}")
    count = 0
    for r in result:
        count += 1
        print(f"{count} 找到的自然数组合: ({r[0]}, {r[1]}, {r[2]})")
        if isDebug:
            print(f"\tmax_result = {r[4]}, min_result = {r[5]}")
            print(f"\ttemp_result = {r[6]}, external_result = {r[7]}")