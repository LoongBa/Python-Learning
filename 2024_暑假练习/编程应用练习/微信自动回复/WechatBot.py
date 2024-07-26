from pathlib import Path
import pandas
import numpy
from uiautomation import WindowControl, MenuControl

# 绑定微信主窗口
wechat = WindowControl(
    Name="微信"
    # searchDepth=1
)
print(wechat)
# 切换窗口
wechat.SwitchToThisWindow()
# 寻找会话控件绑定
session = wechat.ListControl(Name="会话")
print("寻找会话控件绑定", session)
# 通过 pandas 读取数据
# 获取当前脚本所在目录
currentFolder = Path(__file__).parent
dataFilenamme = currentFolder / "ReplyMessage.csv"
csvSheet = pandas.read_csv(dataFilenamme, encoding="utf-8")

while True:
    # 查找未读消息
    newMessages = session.TextControl(searchDepth=4)
    # print('查找未读消息'，we)
    # 死循环维持，没有超时报错
    while not newMessages.Exists(0):
        pass
    print("查找未读消息", newMessages)
    # 存在未读消息
    if newMessages.Name:
        # 点击未读消息
        newMessages.Click(simulateMove=False)
    # 读取最后一条消息
    lastMessage = wechat.ListControl(Name="消息").GetChildren()[-1].Name
    print("读取最后一条消息", lastMessage)
    # 根据关键字获取自动回复的消息
    replyMessage = csvSheet.apply(
        lambda x: x["回复内容"] if x["关键词"] in lastMessage else None, axis=1
    )  
    # 数据筛选，移除空数据
    replyMessage.dropna(axis=0, how="any", inplace=True)
    ar = numpy.array(replyMessage).tolist() # 转换成为列表

    # 能够匹配到数据时
    if ar:
    # 将数据输入
    #替换换行符号
        wechat.SendKeys(ar[0].replace('{br}','{Shift}{Enter}'), waitTime=0)
    # 发送消息
        wechat.SendKeys('{Enter}', waitTime=0)
        #通过消息匹配检索会话栏的联系人
        wechat.TextControl(SubName=ar[0][:5]).RightClick()
    else:   # 没有匹配到数据时
        wechat.SendKeys('我没有理解你的意思',waitTime=0)
        wechat.SendKeys('{Enter}',waitTime=0)
        wechat.TextControl(SubName=lastMessage[:5]).RightClick()
        # 匹配右击控件
        # ment =MenuControl(ClassName='CMenuWnd')
        #点击右键控件中的不显示聊天
        # ment.TextControl(Name='不显示聊天').Click()
        