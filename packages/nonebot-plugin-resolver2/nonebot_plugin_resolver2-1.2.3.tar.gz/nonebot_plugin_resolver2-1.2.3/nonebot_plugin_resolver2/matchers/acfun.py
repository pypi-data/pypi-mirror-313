import re
import asyncio, aiofiles
import subprocess
import httpx
import json

from nonebot import on_keyword
from nonebot.rule import Rule
from nonebot.adapters.onebot.v11 import Message, MessageEvent

from .filter import is_not_in_disable_group
from .utils import get_video_seg
from ..config import plugin_cache_dir, NICKNAME

acfun = on_keyword(keywords={"acfun.cn"}, rule = Rule(is_not_in_disable_group))

@acfun.handle()
async def _(event: MessageEvent) -> None:
    """
        acfun解析
    :param event:
    :return:
    """
    # 消息
    inputMsg: str = event.message.extract_plain_text().strip()

    # 短号处理
    if "m.acfun.cn" in inputMsg:
        inputMsg = f"https://www.acfun.cn/v/ac{re.search(r'ac=([^&?]*)', inputMsg)[1]}"

    url_m3u8s, video_name = parse_url(inputMsg)
    await acfun.send(Message(f"{NICKNAME}解析 | 猴山 - {video_name}"))
    m3u8_full_urls, ts_names, output_file_name = parse_m3u8(url_m3u8s)
    # logger.info(output_folder_name, output_file_name)
    await asyncio.gather(*[download_m3u8_videos(url, i) for i, url in enumerate(m3u8_full_urls)])
    await merge_ac_file_to_mp4(ts_names, output_file_name)
    await acfun.send(await get_video_seg(output_file_name))

headers = {
    'referer': 'https://www.acfun.cn/',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83'
}


def parse_url(url: str):
    """
        解析acfun链接
    :param url:
    :return:
    """
    url_suffix = "?quickViewId=videoInfo_new&ajaxpipe=1"
    url = url + url_suffix
    # print(url)

    raw = httpx.get(url, headers=headers).text
    strs_remove_header = raw.split("window.pageInfo = window.videoInfo =")
    strs_remove_tail = strs_remove_header[1].split("</script>")
    str_json = strs_remove_tail[0]
    str_json_escaped = escape_special_chars(str_json)
    video_info = json.loads(str_json_escaped)
    # print(video_info)
    video_name = parse_video_name_fixed(video_info)
    ks_play_json = video_info['currentVideoInfo']['ksPlayJson']
    ks_play = json.loads(ks_play_json)
    representations = ks_play['adaptationSet'][0]['representation']
    # 这里[d['url'] for d in representations]，从4k~360，此处默认720p
    url_m3u8s = [d['url'] for d in representations][3]
    # print([d['url'] for d in representations])
    return url_m3u8s, video_name


def parse_m3u8(m3u8_url: str):
    """
        解析m3u8链接
    :param m3u8_url:
    :return:
    """
    m3u8_file = httpx.get(m3u8_url, headers=headers).text
    # 分离ts文件链接
    raw_pieces = re.split(r"\n#EXTINF:.{8},\n", m3u8_file)
    # print(raw_pieces)
    # 过滤头部\
    m3u8_relative_links = raw_pieces[1:]
    # print(m3u8_relative_links)
    # 修改尾部 去掉尾部多余的结束符
    patched_tail = m3u8_relative_links[-1].split("\n")[0]
    m3u8_relative_links[-1] = patched_tail
    # print(m3u8_relative_links)

    # 完整链接，直接加m3u8Url的通用前缀
    m3u8_prefix = "/".join(m3u8_url.split("/")[0:-1])
    m3u8_full_urls = [m3u8_prefix + "/" + d for d in m3u8_relative_links]
    # aria2c下载的文件名，就是取url最后一段，去掉末尾url参数(?之后是url参数)
    ts_names = [d.split("?")[0] for d in m3u8_relative_links]
    output_folder_name = ts_names[0][:-9]
    output_file_name = output_folder_name + ".mp4"
    return m3u8_full_urls, ts_names, output_file_name


async def download_m3u8_videos(m3u8_full_url, i):
    """
        批量下载m3u8
    :param m3u8_full_urls:
    :return:
    """
    async with httpx.AsyncClient() as client:
        async with client.stream("GET", m3u8_full_url, headers=headers) as resp:
            with open(plugin_cache_dir / f"{i}.ts", "wb") as f:
                async for chunk in resp.aiter_bytes():
                    f.write(chunk)


def escape_special_chars(str_json):
    return str_json.replace('\\\\"', '\\"').replace('\\"', '"')


def parse_video_name(video_info: json):
    """
        获取视频信息
    :param video_info:
    :return:
    """
    ac_id = "ac" + video_info['dougaId'] if video_info['dougaId'] is not None else ""
    title = video_info['title'] if video_info['title'] is not None else ""
    author = video_info['user']['name'] if video_info['user']['name'] is not None else ""
    upload_time = video_info['createTime'] if video_info['createTime'] is not None else ""
    desc = video_info['description'] if video_info['description'] is not None else ""

    raw = '_'.join([ac_id, title, author, upload_time, desc])[:101]
    return raw


async def merge_ac_file_to_mp4(ts_names, file_name):
    concat_str = '\n'.join([f"file {i}.ts" for i, d in enumerate(ts_names)])

    filetxt = plugin_cache_dir / 'file.txt'
    filepath = plugin_cache_dir / file_name
    async with aiofiles.open(filetxt, 'w') as f:
        await f.write(concat_str)
    command = f'ffmpeg -y -f concat -safe 0 -i {filetxt} -c copy "{filepath}"'
    stdout = subprocess.DEVNULL
    stderr = subprocess.DEVNULL
    await asyncio.get_event_loop().run_in_executor(
        None,
        lambda: subprocess.call(command, shell=True, stdout=stdout, stderr=stderr)
    )

def parse_video_name_fixed(video_info: json):
    """
        校准文件名
    :param video_info:
    :return:
    """
    f = parse_video_name(video_info)
    t = f.replace(" ", "-")
    return t