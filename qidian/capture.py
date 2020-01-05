"""抓取并解析

同步版本
"""

from pathlib import Path
from time import localtime, strftime
from typing import List, Tuple, Iterable

import requests as r
from bs4 import BeautifulSoup

from .log import logger

PARINDENT_STR = "　　"


def get_session(cookiepath: str) -> r.Session:
    """获得一个登录了用 cookie 登录的起点帐号的会话

    :param str cookiepath: 指向 cookie.txt 数据库的绝对路径, cookie 格式为 JavaScript 里的 :code:`key=value; k2=v2`
    """
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0"
    }
    with open(cookiepath) as cookiefile:
        content = cookiefile.read().rstrip()
    cookiejar = dict([pair.split("=") for pair in content.split("; ")])
    session = r.Session()
    session.headers.update(HEADERS)
    session.cookies.update(cookiejar)
    return session


def get_bookindex(session: r.Session, id: int) -> dict:
    """获取一本书的目录信息
    """
    _csrfToken = session.cookies.get("_csrfToken")
    url = f"https://book.qidian.com/ajax/book/category"
    resp = session.get(url, params={
        "_csrfToken": _csrfToken,
        "bookId": id,
    })
    if resp.status_code in (200, 304):
        obj = resp.json()
        if obj["code"] == 0 and obj["msg"] == "suc":
            # 成功
            data = obj["data"]
            logger.debug(f"get book {id}")
            data["bId"] = id
            return data


def find_chapter_links(data: dict) -> Tuple[List[str], List[str]]:
    """返回免费章节与 VIP 章节链接

    :returns: (免费章节链接, VIP章节链接)
    """
    # note: data 是被修改过的，添加了 bId（书籍 Id）值用于构造 VIP 章节的 url
    volumes = data["vs"]
    freev = list(filter(lambda v: v["vS"] == 0, volumes))
    vipv = list(filter(lambda v: v["vS"] == 1, volumes))
    freec = [c['cU'] for v in freev for c in v['cs']]
    vipcid = (c['id'] for v in vipv for c in v['cs'])
    vipc = [f"{data['bId']}/{i}" for i in vipcid]
    return (freec, vipc)


def get_freechapter(session: r.Session, subpath: str) -> BeautifulSoup:
    """获取免费章节的内容
    """
    url = f"https://read.qidian.com/chapter/{subpath}"
    resp = session.get(url)
    if resp.status_code in (200, 304):
        text = resp.text
    logger.debug(f"get chapter {url}")
    return BeautifulSoup(text, "lxml")


def parse_freechapter(html: BeautifulSoup) -> Tuple[str, Iterable[str]]:
    """解析免费章节内容

    return (标题: str, 内容: str)
    """
    el_title = html.select_one(
        ".text-wrap[id|=chapter] > div.main-text-wrap > div.text-head > h3.j_chapterName > span.content-wrap"
    )
    el_content = html.select_one(
        ".text-wrap[id|=chapter] > div.main-text-wrap > div.read-content"
    )
    # span.content-wrap 是 js 添加的（猜测是段评功能的副作用）
    el_paragraphes = el_content.select("p")
    title = el_title.text
    pars = [p.text.lstrip(PARINDENT_STR) for p in el_paragraphes]
    return title, pars


def get_vipchapter(session: r.Session, subpath: str) -> BeautifulSoup:
    """获取 VIP 章节的内容
    """
    url = f"https://vipreader.qidian.com/chapter/{subpath}"
    resp = session.get(url)
    if resp.status_code in (200, 304):
        text = resp.text
    logger.debug(f"get chapter {url}")
    return BeautifulSoup(text, "lxml")


def parse_vipchapter(html: BeautifulSoup) -> Tuple[str, Iterable[str]]:
    """解析 VIP 章节内容

    return (标题: str, 内容: str)
    """
    el_title = html.select_one(
        ".text-wrap[id|=chapter] > div.main-text-wrap > div.text-head > h3.j_chapterName > span.content-wrap"
    )
    el_content = html.select_one(
        ".text-wrap[id|=chapter] > div.main-text-wrap > div.read-content"
    )
    # span.content-wrap 是 js 添加的（猜测是段评功能的副作用）
    el_paragraphes = el_content.select("p")
    title = el_title.text
    pars = [p.text.lstrip(PARINDENT_STR) for p in el_paragraphes]
    return title, pars
