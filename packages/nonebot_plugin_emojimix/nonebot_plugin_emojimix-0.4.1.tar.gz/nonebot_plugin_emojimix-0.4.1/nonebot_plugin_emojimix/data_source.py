import traceback
from typing import Optional, Union

import httpx
from nonebot.log import logger

from .config import emoji_config
from .emoji_data import dates, emojis

API = "https://www.gstatic.com/android/keyboard/emojikitchen/"


def create_url(date: str, emoji1: list[int], emoji2: list[int]) -> str:
    def emoji_code(emoji: list[int]):
        return "-".join(f"u{c:x}" for c in emoji)

    u1 = emoji_code(emoji1)
    u2 = emoji_code(emoji2)
    return f"{API}{date}/{u1}/{u1}_{u2}.png"


def find_emoji(emoji_code: str) -> Optional[list[int]]:
    emoji_num = ord(emoji_code)
    for e in emojis:
        if emoji_num in e:
            return e
    return None


async def mix_emoji(emoji_code1: str, emoji_code2: str) -> Union[str, bytes]:
    emoji1 = find_emoji(emoji_code1)
    emoji2 = find_emoji(emoji_code2)
    if not emoji1:
        return f"不支持的emoji：{emoji_code1}"
    if not emoji2:
        return f"不支持的emoji：{emoji_code2}"

    urls: list[str] = []
    for date in dates:
        urls.append(create_url(date, emoji1, emoji2))
        urls.append(create_url(date, emoji2, emoji1))

    try:
        async with httpx.AsyncClient(
            proxy=emoji_config.http_proxy, timeout=20
        ) as client:
            for url in urls:
                resp = await client.get(url)
                if resp.status_code == 200:
                    return resp.content
            return "出错了，可能不支持该emoji组合"
    except Exception:
        logger.warning(traceback.format_exc())
        return "下载出错，请稍后再试"
