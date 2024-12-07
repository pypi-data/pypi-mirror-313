from abc import ABCMeta, abstractmethod
from enum import Enum
from googletrans import Translator
import requests
import random
from hashlib import md5
from tdf_tool.tools.print import Print


class LanguageType(Enum):
    EN = 1  # 英文
    TH = 2  # 泰语
    ZH = 3  # 简体中文
    CHT = 4  # 繁体中文
    ES = 5  # 西班牙语

    def init(string_type: str):
        if "zh-Hant" in string_type:
            return LanguageType.CHT
        elif "en" in string_type:
            return LanguageType.EN
        elif "th" in string_type:
            return LanguageType.TH
        elif "es" in string_type:
            return LanguageType.ES
        else:
            return LanguageType.ZH

    def baidu(self) -> str:
        if self.name == LanguageType.EN.name:
            return "en"
        elif self.name == LanguageType.TH.name:
            return "th"
        elif self.name == LanguageType.ZH.name:
            return "zh"
        elif self.name == LanguageType.ES.name:
            return "es"
        else:
            return "cht"

    def google(self) -> str:
        if self.name == LanguageType.EN.name:
            return "en"
        elif self.name == LanguageType.TH.name:
            return "th"
        elif self.name == LanguageType.ZH.name:
            return "zh-cn"
        elif self.name == LanguageType.ES.name:
            return "es"
        else:
            return "zh-tw"

    def str(self) -> str:
        if self.name == LanguageType.EN.name:
            return "en_US"
        elif self.name == LanguageType.TH.name:
            return "th_TH"
        elif self.name == LanguageType.CHT.name:
            return "zh_TW"
        elif self.name == LanguageType.ES.name:
            return "es"
        else:
            return "zh_CN"

    def ios_str(self) -> str:
        if self.name == LanguageType.EN.name:
            return "en"
        elif self.name == LanguageType.TH.name:
            return "th"
        elif self.name == LanguageType.ZH.name:
            return "zh-Hans"
        elif self.name == LanguageType.ES.name:
            return "es"
        else:
            return "zh-Hant"


class TranslateType(Enum):
    BAIDU = 1  # 百度翻译，百度翻译 %d \n 这类符号翻译出来有问题，还是使用谷歌翻译比较好
    GOOGLE = 2  # 谷歌翻译


class Translate(metaclass=ABCMeta):
    @abstractmethod
    def translate(self, text: str, dest=LanguageType.EN, src=LanguageType.ZH) -> str:
        pass


class TranslateTool(Translate):
    def __init__(self, type=TranslateType.BAIDU):
        self.__translator = self.__generate_translate(type)

    def translate(
        self,
        text: str,
        dest=LanguageType.EN,
        src=LanguageType.ZH,
    ) -> str:
        if src == dest:
            return text
        has_double_quotes = False
        # 翻译前去掉 前后双引号
        if text.startswith('"') and text.endswith('"'):
            has_double_quotes = True
            text = text[1:-1]
        if dest == LanguageType.EN or dest == LanguageType.TH:
            # 处理 《》【】“”，因为这些在外语会翻译成双引号，需要加转义符
            text = text.replace("《", r"\"")
            text = text.replace("》", r"\"")
            text = text.replace("【", r"\"")
            text = text.replace("】", r"\"")
            text = text.replace("“", r"\"")
            text = text.replace("”", r"\"")
            text = text.replace("＂", r"\"")
        text = self.__translator.translate(text, src=src, dest=dest)
        # 偶尔会出现 \" 翻译成 \ "，需要检查替换一下
        text = text.replace('\ "', '\\"')
        if has_double_quotes:
            # 翻译完再加上 前后双引号
            text = '"' + text + '"'
        return text

    def __generate_translate(self, type) -> Translate:
        if type == TranslateType.BAIDU:
            return BaiduTranslate()
        else:
            return GoogleTranslate()


class BaiduTranslate(Translate):

    __appid = "20220505001202987"
    __appkey = "qmWBUEi75he1iVZQgqPg"
    __endpoint = "http://api.fanyi.baidu.com"
    __path = "/api/trans/vip/translate"
    __url = __endpoint + __path

    def translate(self, text: str, dest=LanguageType.EN, src=LanguageType.ZH) -> str:
        salt = random.randint(32768, 65536)
        sign = self.__make_md5(self.__appid + text + str(salt) + self.__appkey)

        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        payload = {
            "appid": self.__appid,
            "q": text,
            "from": src.baidu(),
            "to": dest.baidu(),
            "salt": salt,
            "sign": sign,
        }

        r = requests.post(self.__url, params=payload, headers=headers)
        result: dict = r.json()
        error_code = result.get("error_code")
        if error_code != None:
            error_msg = result.get("error_msg")
            Print.error(
                "{0}翻译失败, error_code：{1}，error_msg：{2}".format(
                    text, error_code, error_msg
                )
            )
        trans_result: dict = result["trans_result"]
        return trans_result["dst"]

    def __make_md5(self, s: str, encoding="utf-8"):
        return md5(s.encode(encoding)).hexdigest()


class GoogleTranslate(Translate):
    def translate(self, text: str, dest=LanguageType.EN, src=LanguageType.ZH) -> str:
        try:
            translator = Translator()
            result_text = translator.translate(
                text, src=src.google(), dest=dest.google()
            ).text
            if result_text == text and dest != LanguageType.CHT:
                Print.warning("{0} 翻译失败, 查看是否有开启代理".format(text))
                # 空字符串, 代表翻译失败
                return ""
            else:
                return result_text
        except ValueError as e:
            Print.warning("{0} 翻译失败, 查看是否有开启代理：{1}".format(text, e))
            # 空字符串, 代表翻译失败
            return ""
