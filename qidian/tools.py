import re


class RangeString:
    """类似于 -3,5-6,9,10- 这样的字符串，用来表示一系列数字
    （连续或不连续的开或闭的区间）

    满足其中一条规则则通过
    """
    CC = re.compile(r"(\d+)-(\d+)")
    CO = re.compile(r"(\d+)-")
    OC = re.compile(r"-(\d+)")
    D = re.compile(r"(\d+)")
    OO = re.compile(r"-")

    def __init__(self, string: str):
        if "," not in string:
            pairs = [string, ]
        else:
            pairs = string.split(",")

        self.rules = []

        for pair in pairs:
            if m := self.CC.fullmatch(pair):
                self.rules.append((int(m[1]), int(m[2])))
            elif m := self.CO.fullmatch(pair):
                self.rules.append((int(m[1]), None))
            elif m := self.OC.fullmatch(pair):
                self.rules.append((None, int(m[1])))
            elif m := self.D.fullmatch(pair):
                self.rules.append(int(m[1]))
            elif m := self.OO.fullmatch(pair):
                self.rules.append(None)

    def match(self, num: int) -> bool:
        for rule in self.rules:
            if rule is None:
                return True
            elif isinstance(rule, int):
                if num == rule:
                    return True
            elif isinstance(rule, tuple):
                if rule[0] is None:
                    if num <= rule[1]:
                        return True
                elif rule[1] is None:
                    if num >= rule[0]:
                        return True
                else:
                    if rule[0] <= num <= rule[1]:
                        return True
        else:
            return False
