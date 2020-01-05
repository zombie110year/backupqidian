"""起点小说备份

在小说被和谐之前下载下来

Example:

>>> session = get_session("cookies.起点帐号已登录.txt")
>>> index = get_bookindex(session, "书籍 ID")
>>> freecs, vipcs = find_chapter_links(index)
>>> for fc in freecs:
>>>     c = get_freechapter(session, fc)
>>>     title, pars = parse_freechapter(c)
>>>     print(f"# {title}")
>>>     for paragraph in pars:
>>>         print(f"    {paragraph}")
"""

from .capture import *
__version__ = "0.1.0"
