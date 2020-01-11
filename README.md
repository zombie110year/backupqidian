# 起点备份

将起点中文网的小说内容下载到一个独立的 txt 文件中。

关于这个工具，你需要知道的是：

1.  这个工具不能用于侵犯权利的行为：对于免费章节，它可以无条件获取；
    对于 VIP 章节，需要一个起点帐号，并且此帐号订阅了目标章节。
2.  txt 文件使用了 Markdown 语法，章节标题为1级标题，段落内容以空行划分。
    并且内容与样式分离，段落用于缩进的 CJK 空格字符被删除，如果需要制造段首缩进的效果，
    可以在格式化 Markdown 时使用 `p: { text-indent: 2em; }` 的 CSS 样式。
3.  同步下载，一章大概花费 1 秒时间。
4.  未刻意模仿人类操作，不保证不被起点察觉并封号（TODO：有时间分析一下起点 mobile 端批量下载功能的实现）。

## 使用方法

本脚本依赖 BeautfulSoup4, requests, coloredlogs 库，可以先通过

```
pip install -r requirements.txt
```

下载依赖。

### 下载免费章节

提供命令行接口：

```
python app.py 1010868264
```

将会把起点 1010868264 号书籍（诡秘之主）的免费章节下载到 `text.txt` 文件中。
书籍 ID 解释书籍主页的 URL 最后一部分，例如： <https://book.qidian.com/info/1010868264>

### 下载 VIP 章节

如果要下载 VIP 章节，你需要一个已经登录的起点帐号，并且订阅了相关章节
（如果下载到未订阅章节，那么解析器可能提取到错误的内容，未测试）

首先，登录浏览器，登录起点帐号，然后在 F12 开发者工具中切换到 Console（控制台）标签，
JavaScript 变量 `document.cookie` 的内容就是所需的 cookie，将其保存到 `cookies.txt` 文件中。

然后在命令行中指定 `--vip` 选项。

```
python app.py 1010868264 --vip
```

### 其他选项

```
usage: python app.py [-h] [--cookiefile COOKIEFILE] [-o OUTPUT] [--vip] [--range RANGE] [--dry-run] bid

positional arguments:
  bid                   book ID

optional arguments:
  -h, --help            show this help message and exit
  --cookiefile COOKIEFILE
                        指定 cookies.txt 路径
  -o OUTPUT, --output OUTPUT
                        指定保存文件路径
  --vip                 是否抓取 VIP 章节：默认 False
  --range RANGE         章节范围，从 1 开始
  --dry-run             看看会下载哪些章节，仅预览，不实际下载
```
