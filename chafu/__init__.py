from nonebot import on_command
from services.log import logger
from utils.message_builder import image
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, MessageSegment, GroupMessageEvent, Message
from nonebot.typing import T_State
from utils.http_utils import AsyncHttpx
from ping3 import ping
import ast, base64

__zx_plugin_name__ = "我的世界查服"
__plugin_usage__ = """
usage：
    我的世界服务器状态查询
    用法：
        <以下仅限Java服务器>
        查服 [ip]?[端口]
        查服 ip:端口(端口必须五位)
        <以上仅限Java服务器>
        <以下仅限基岩版服务器>
        查 ip:端口
        [若不响应消息，请@bot或在文字前加上bot的名字]
    tips:汉字与ip间可以有空格
""".strip()
__plugin_des__ = "用法：查服 ip:port"
__plugin_type__ = ("一些工具",)
__plugin_cmd__ = ["查服","查"]
__plugin_version__ = 0.6
__plugin_author__ = "YiRanEL"#觉得还是写GitHub名称比较好
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["查服",'查'],
}
__plugin_cd_limit__ = {
    "cd": 10,   
    "rst": "查坏了...再等等吧"
}
##自定义错误信息
error = "查服发生了一些错误..."
##自定义错误信息
chafu = on_command("查服", priority=5, block=True)

@chafu.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    n = '查服'
    n = str(n)
    q = str(event.get_message()).strip()
    t = q.find(n)
    if t == (-1):
       u = str(q)
    else:
       s = q[2:].strip()
       s = s[:-6].strip()
       port = q[-5:]
       ip = str(s)
    
    url = "https://mcapi.us/server/status?ip=" + ip + "&port=" + port
####判断端口是否全部为数字，防止有人捣乱##
    temp = str(port.isdigit())#防君子不防小人
##################################
    try:
        data = (await AsyncHttpx.get(url, timeout=5)).json()#若获取无结果，请修改timeout=后的数字
        if temp == "False":
          result = "\n输入信息不完整\n请重新输入"
          await chafu.send(Message(result), at_sender=True)
        else:
        #############获取数据######
           ##获取延迟####
           ms = ping(ip)
           if ms != None:
             ms = int(ms * 1000)
           else:
             ms = "超时"
           ms = f'{ms}ms'
           ##获取延迟####
           temp = f'{data["players"]}'
           tmp = temp.index("sample") - 3
           tmp = temp[:tmp]
           temp = tmp[1:]
           tmp = temp.index(",") + 1
           q = temp[:tmp]
           tmp = tmp +1
           s = temp[tmp:]
           temp = q + s
###########重构变量##############
           players = "{" + temp + "}"
           players = ast.literal_eval(players)
           temp = f'{data["server"]}'
           temp = ast.literal_eval(temp)
###########字典查询###############
           server = str(temp["name"])
           max = str(players["max"])
           now = str(players["now"])
           status = str(f'{data["status"]}')
           ####整理文字###
           result = "\n名称：" + server + "\n地址：" + ip + "\n端口：" + port + f'\n延迟：{ms}' +  f'\n在线：{data["online"]}\nmotd：{data["motd"]}' + f'\n人数：{now}/{max}' + f'\n状态码：{data["status"]}' + "\nFavicon:"
           ######发送favicon###
           if status != "error":
             base0 = str(f'{data["favicon"]}')
             if base0 != "null":
               base = base0[22:]
               img = base64.b64decode(base)
               #########
               end = Message ([
                  MessageSegment.text(result),
                  MessageSegment.image(img)
               ])
           else:
             end = result
           await chafu.send(Message(end), at_sender=True)
           #await chafu.send(image(img), at_sender=True)
           logger.info(
              f"(USER {event.user_id}, GROUP {event.group_id if isinstance(event, GroupMessageEvent) else 'private'}) 发送信息:\n"
            + result 
           )
    except:
      await chafu.send(Message(error), at_sender=True)
      logger.info(error)
      
##以下为基岩服务器查询

bds = on_command("查", priority=5, block=True)

@bds.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    host = "查"
    host = str(host)
    q = str(event.get_message()).strip()
    temp = q.find(host)
    if temp == (-1):
       host = str(q)
    else:
       host = q[1:].strip()
    
    url = "https://motdbe.blackbe.xyz/api?host=" + host
####判断是否存在端口，防止有人捣乱##
    temp = host.find(":")
##################################
    try:
        data = (await AsyncHttpx.get(url, timeout=5)).json()#若获取无结果，请修改timeout=后的数字
        data = str(data)
        if temp == (-1):
          result = "\n输入信息有误\n请检查"
          await bds.send(Message(result), at_sender=True)
        else:
        #############获取数据######
           data = ast.literal_eval(data) #转换成字典
           ####整理文字###
           result = f'\n版本：{data["version"]}\n地址：{data["host"]}\n延迟：{data["delay"]}ms\nmotd：{data["motd"]}\n人数：{data["online"]}/{data["max"]}\n存档名：{data["level_name"]}\n游戏模式：{data["gamemode"]}\n状态码：{data["status"]}'
           await bds.send(Message(result), at_sender=True)
           logger.info(
              f"(USER {event.user_id}, GROUP {event.group_id if isinstance(event, GroupMessageEvent) else 'private'}) 发送信息:\n"
            + result 
           )
    except:
      await bds.send(Message(error), at_sender=True)
      logger.info(error)
