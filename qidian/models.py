"""数据库结构

```
book 1--m volume
volume 1--m chapter
```
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy.types import Integer
from sqlalchemy.types import String
from sqlalchemy.types import Text
from sqlalchemy.types import DateTime
from sqlalchemy import create_engine

Model = declarative_base()

HASH_STRING_LENGTH = 16
# xxHASH 的 hexdigest 长度
#
# 为什么选择 xxHASH：
#     xxHASH 非常快。
#     虽然 xxHASH 宽度仅为 64 bit，即
#     $2^64 = 18446744073709551616 \approx 1.8 \times 10^{19}$ 种不同的 hash 值，
#     但对于我们要达成的目标：存储起点小说章节，这个宽度是远远过剩的。
#     假设每个章节被修改 4 次，每本书都像 “四十六亿重奏” 或 “临高启明” 那样写个 5000 章，
#     那也可以容纳 $9.2 \times 10^{14}$ 本书。
TITLE_MAXLENGTH = 128
# 章节名、卷名的最大长度


class Book(Model):
    __tablename__ = "book"

    id = Column(Integer(), primary_key=True)
    # 图书的索引页地址都是 f"/info/{id}" 的形式
    title = Column(String(HASH_STRING_LENGTH))
    # 书名
    description = Column(Text())
    # 书籍描述
    max_chapters = Column(Integer())
    # 本书总共有多少章

    def __repr__(self):
        return f"""Book(id={self.id}, title={self.title})"""

class Volume(Model):
    __tablename__ = "volume"
    id = Column(String(HASH_STRING_LENGTH), primary_key=True)
    # 唯一指定 书、卷
    from_book = Column(Integer())
    # 归属哪本书
    title = Column(String(TITLE_MAXLENGTH))
    # 卷名

    def __repr__(self):
        return f"Volume(id={self.id}, title={self.title})"

class Chapter(Model):
    __tablename__ = "chapter"
    id = Column(String(HASH_STRING_LENGTH), primary_key=True)
    # 唯一指定 书、卷、章
    from_volume = Column(String(HASH_STRING_LENGTH))
    # 归属哪章
    from_book = Column(Integer())
    # 归属哪本

    counter = Column(Integer())
    # 章节编号（每本书从 0 开始）
    captrue_date = Column(DateTime())
    # 抓取该章节的日期时间
    title = Column(String(TITLE_MAXLENGTH))
    # 标题
    bolb_name = Column(String(HASH_STRING_LENGTH))
    # 存储实际内容的文件名

    def __repr__(self):
        return f"Chapter(id={self.id}, title={self.title}, date={self.captrue_date})"


def init_model():
    from .settings import DefaultSettings
    if DefaultSettings.INDEX_DATABASE["dbtype"] == "sqlite3":
        engine = create_engine(f"sqlite:///{DefaultSettings.INDEX_DATABASE['dbpath']}")
        Model.metadata.create_all(engine)
    else:
        raise NotImplementedError
