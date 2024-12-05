import re, httpx, aiohttp, json, asyncio

from nonebot import on_keyword, logger
from nonebot.rule import Rule
from nonebot.adapters.onebot.v11 import Message, MessageEvent, Bot, MessageSegment
from urllib.parse import parse_qs, urlparse

from .filter import is_not_in_disable_group
from .utils import send_forward_both, make_node_segment, auto_video_send

from ..constant import COMMON_HEADER
from ..data_source.common import download_video, download_img
from ..config import *

# 小红书下载链接
XHS_REQ_LINK = "https://www.xiaohongshu.com/explore/"


xiaohongshu = on_keyword(keywords={"xiaohongshu.com", "xhslink.com"}, rule = Rule(is_not_in_disable_group))

@xiaohongshu.handle()
async def _(bot: Bot, event: MessageEvent):

    message: str = event.message.extract_plain_text().replace("&amp;", "&").strip()

    msg_url = re.search(r"(http:|https:)\/\/(xhslink|(www\.)xiaohongshu).com\/[A-Za-z\d._?%&+\-=\/#@]*",message)[0]
    # 如果没有设置xhs的ck就结束，因为获取不到
    xhs_ck = rconfig.r_xhs_ck
    if xhs_ck == "":
        await xiaohongshu.finish(f"{NICKNAME}解析 | 小红书 - 无法获取到管理员设置的小红书 cookie！")
    # 请求头
    headers = {
                  'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,'
                            'application/signed-exchange;v=b3;q=0.9',
                  'cookie': xhs_ck,
              } | COMMON_HEADER
    if "xhslink" in msg_url:
        msg_url = httpx.get(msg_url, headers=headers, follow_redirects=True).url
        msg_url = str(msg_url)
    xhs_id = re.search(r'/explore/(\w+)', msg_url)
    if not xhs_id:
        xhs_id = re.search(r'/discovery/item/(\w+)', msg_url)
    if not xhs_id:
        xhs_id = re.search(r'source=note&noteId=(\w+)', msg_url)
    xhs_id = xhs_id[1]

    # 解析 URL 参数
    parsed_url = urlparse(msg_url)
    params = parse_qs(parsed_url.query)
    # 提取 xsec_source 和 xsec_token
    xsec_source = params.get('xsec_source', [None])[0] or "pc_feed"
    xsec_token = params.get('xsec_token', [None])[0]

    html = httpx.get(f'{XHS_REQ_LINK}{xhs_id}?xsec_source={xsec_source}&xsec_token={xsec_token}', headers=headers).text
    # response_json = re.findall('window.__INITIAL_STATE__=(.*?)</script>', html)[0]
    try:
        response_json = re.findall('window.__INITIAL_STATE__=(.*?)</script>', html)[0]
    except IndexError:
        await xiaohongshu.send(
            Message(f"{NICKNAME}解析 | 小红书 - 当前ck已失效，请联系管理员重新设置的小红书 cookie！"))
        return
    response_json = response_json.replace("undefined", "null")
    response_json = json.loads(response_json)
    note_data = response_json['note']['noteDetailMap'][xhs_id]['note']
    type = note_data['type']
    note_title = note_data['title']
    note_desc = note_data['desc']
    await xiaohongshu.send(Message(
        f"{NICKNAME}解析 | 小红书 - {note_title}\n{note_desc}"))

    aio_task = []
    if type == 'normal':
        image_list = note_data['imageList']
        # 批量下载
        async with aiohttp.ClientSession() as session:
            for index, item in enumerate(image_list):
                aio_task.append(asyncio.create_task(
                    download_img(item['urlDefault'], img_name=f'{index}.jpg', session=session)))
            links_path = await asyncio.gather(*aio_task)
    elif type == 'video':
        # 这是一条解析有水印的视频
        logger.info(note_data['video'])

        video_url = note_data['video']['media']['stream']['h264'][0]['masterUrl']

        # ⚠️ 废弃，解析无水印视频video.consumer.originVideoKey
        # video_url = f"http://sns-video-bd.xhscdn.com/{note_data['video']['consumer']['originVideoKey']}"
        video_name = await download_video(video_url)
        # await xhs.send(Message(MessageSegment.video(path)))
        await auto_video_send(event, file_name = video_name)
        return
    # 发送图片
    links = make_node_segment(bot.self_id, [MessageSegment.image(plugin_cache_dir / img) for img in links_path])
    # 发送异步后的数据
    await send_forward_both(bot, event, links)


