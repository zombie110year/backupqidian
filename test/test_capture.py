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

def test_parse诡秘之主VIP第一章(client, 诡秘之主目录):
    free, vip = find_chapter_links(诡秘之主目录)
    c1cU = vip[0]
    c1 = get_freechapter(client, c1cU)
    title, pars = parse_vipchapter(c1)
    assert title == "第一百三十章 贝克兰德的隐秘聚会（第一更）"
    assert pars[0] == "望了望站在怪物尸体前的斯维因，又侧头看着刚才负责牵制的“代罚者”搀扶起半昏迷的同伴，克莱恩忽然有种难以言喻的悲伤。"
    assert pars[-2] == "“那是A先生，一位强大的非凡者，本次隐秘聚会的召集者。”"
