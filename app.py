from argparse import ArgumentParser
from random import shuffle
from random import uniform
from time import sleep

from qidian import *
from qidian.tools import RangeString


def cli():
    parser = ArgumentParser(prog="backupqidian")
    parser.add_argument("bid", help="book ID", type=int)
    parser.add_argument(
        "--cookiefile", help="指定 cookies.txt", default="cookies.txt")
    parser.add_argument("-o", "--output", help="保存到文件", default="text.txt")
    parser.add_argument(
        "--vip", help="是否抓取 VIP 章节：默认 False", action="store_true")
    parser.add_argument("--range", help="页面范围，从 1 开始")
    parser.add_argument("--dry-run", help="看看会下载哪些章节", action="store_true")
    args = parser.parse_args()

    session = get_session(args.cookiefile)
    index = get_bookindex(session, args.bid)

    if args.dry_run:
        freecs, vipcs = get_chapter_titles(index)
    else:
        freecs, vipcs = find_chapter_links(index)

    if hasattr(args, "range"):
        RANGE = RangeString(args.range)
        GLOBAL_COUNTER = 0
        tmp = []
        for i in freecs:
            GLOBAL_COUNTER += 1
            if RANGE.match(GLOBAL_COUNTER):
                tmp.append(i)
        freecs = tmp
        tmp = []
        for i in vipcs:
            GLOBAL_COUNTER += 1
            if RANGE.match(GLOBAL_COUNTER):
                tmp.append(i)
        vipcs = tmp
    if args.dry_run:
        for c in freecs:
            print(c)
        if args.vip:
            for c in vipcs:
                print(c)
    else:
        outputfile = open(args.output, "at", encoding="utf-8")
        for c in freecs:
            download_free(session, c, outputfile)
        if args.vip:
            for c in vipcs:
                download_vip(session, c, outputfile)
        outputfile.close()
        print(f"saved at {args.outputfile}")


def download_free(session, link, outputfile):
    title, pars = parse_freechapter(get_freechapter(session, link))
    outputfile.write(f"# {title}\n\n")
    outputfile.write("\n\n".join(pars))
    outputfile.write("\n\n")

def download_vip(session, link, outputfile):
    title, pars = parse_vipchapter(get_vipchapter(session, link))
    outputfile.write(f"# {title}\n\n")
    outputfile.write("\n\n".join(pars))
    outputfile.write("\n\n")

if __name__ == "__main__":
    cli()
