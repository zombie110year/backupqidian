################################################################################
########################### BackupQidian 的配置文件 ############################
################################################################################

class DefaultSettings:
    # 要监听（下载）的小说目录页网址
    TARGET_INDICES = [
        "https://book.qidian.com/info/1010868264"
    ]
    # 下载到的章节内容存储地址
    BOLB_STORED_DIR = "./bolbs"
    # 文件名预处理器
    FILENAME_PREPRECESSOR = "md5"
    # 索引（书名、卷名、章名）数据库
    INDEX_DATABASE = {
        "dbtype": "sqlite3",
        "dbpath": "./bookindex.sqlite",
    }
    # 检查更新的时间间隔，单位：秒（画饼）
    QUERY_INTERVAL = 600
    # cookies 文件位置（用于登录帐号）
    COOKIE_SQLITE = "./cookies.sqlite"
