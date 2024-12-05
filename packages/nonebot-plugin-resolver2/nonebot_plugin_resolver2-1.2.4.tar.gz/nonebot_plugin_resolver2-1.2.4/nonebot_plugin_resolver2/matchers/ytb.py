import re

from nonebot import on_keyword
from nonebot.adapters.onebot.v11 import MessageEvent, Message, MessageSegment, Bot
from nonebot.typing import T_State
from nonebot.params import Arg
from nonebot.rule import Rule
from .filter import is_not_in_disable_group
from .utils import get_video_seg, upload_both, get_file_seg
from ..data_source.ytdlp import *
from ..config import *

ytb = on_keyword(keywords = {"youtube.com", "youtu.be"}, rule = Rule(is_not_in_disable_group))

@ytb.handle()
async def _(event: MessageEvent, state: T_State):
    message = event.message.extract_plain_text().strip()
    url = re.search(
        r"(?:https?:\/\/)?(www\.)?youtube\.com\/[A-Za-z\d._?%&+\-=\/#]*|(?:https?:\/\/)?youtu\.be\/[A-Za-z\d._?%&+\-=\/#]*",
        message)[0]
    try:
        info_dict = await get_video_info(url, YTB_COOKIES_FILE)
        title = info_dict.get('title', "未知")
        await ytb.send(f"{NICKNAME}解析 | 油管 - {title}")
    except Exception as e:
        await ytb.send(f"{NICKNAME}解析 | 油管 - 标题获取出错: {e}")
    state["url"] = url

@ytb.got("type", prompt="您需要下载音频(0)，还是视频(1)")
async def _(bot: Bot, event: MessageEvent, state: T_State, type: Message = Arg()):
    url: str = state["url"]
    will_delete_id = (await ytb.send("开始下载..."))["message_id"]
    try:
        if int(type.extract_plain_text()) == 1:
            video_name = await ytdlp_download_video(url = url, cookiefile = YTB_COOKIES_FILE)
            await ytb.send(await get_video_seg(video_name))
        else: 
            audio_name = await ytdlp_download_audio(url = url, cookiefile = YTB_COOKIES_FILE)
            await ytb.send(MessageSegment.record(plugin_cache_dir / audio_name))
            await ytb.send(get_file_seg(audio_name))
    except Exception as e:
        await ytb.send(f"下载失败 | {e}")
    finally:
        await bot.delete_msg(message_id = will_delete_id)