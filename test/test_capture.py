from os import getenv

import pytest

from qidian.capture import *


@pytest.fixture(scope="module")
def client():
    cookiepath = getenv("FIREFOXCOOKIEPATH", "cookies.txt")
    client = get_session(cookiepath)
    return client


@pytest.fixture(scope="module")
def 诡秘之主目录(client):
    index = get_bookindex(client, 1010868264)
    return index


def test_parse诡秘之主第一章(client, 诡秘之主目录):
    free, vip = find_chapter_links(诡秘之主目录)
    c1cU = free[0]
    c1 = get_freechapter(client, c1cU)
    title, pars = parse_freechapter(c1)
    assert title == "第一章 绯红"
    assert pars[0] == "痛！"
    assert pars[1] == "好痛！"
    assert pars[2] == "头好痛！"
    assert pars[-2] == "清晰倒映的镜子如实呈现，一个狰狞的伤口盘踞在他的太阳穴位置，边缘是烧灼的痕迹，周围沾满了血污"
