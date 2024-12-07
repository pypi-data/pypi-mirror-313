# -*- coding: UTF-8 -*-

from ast import Str
import re
import base64

from tdf_tool.modules.translate.ios.tools.ios_translate_pattern import (
    iOSTranslatePattern,
)

simple_decode_key = "dsfsf7w9e76f87ew6f87ew6f8we"


class StringUtil:
    def simpleEncode(data: str) -> str:
        # base编码
        data = (simple_decode_key + data).encode()
        res = base64.b64encode(data)
        res = bytes.decode(res)
        return res

    def simpleDecode(data: str) -> str:
        # base64解码
        # print('解码前'+data)
        res = base64.b64decode(data)
        res = bytes.decode(res)
        res = res.replace(simple_decode_key, "")
        # print('解码后'+res)

        return res

    def get_chinese_string(
        text: str, pattern_str: str, spical_strs: list[str], except_list=[]
    ) -> list[str]:
        for except_str in except_list:
            text = re.sub(except_str, "", text)

        text = StringUtil.get_replaced_str(text, spical_strs)
        pattern = re.compile(r"%s" % (pattern_str))
        result = pattern.findall(text)

        newResult: list[str] = []
        for item in result:
            if len(item) > 0:
                str = StringUtil.get_origin_str(item, spical_strs)
                newResult.append(str)

        return newResult

    def get_changed_chinese_string(
        text: str, pattern_str: str, spical_strs: list[str], repl
    ) -> str:

        pattern = re.compile(r"%s" % (iOSTranslatePattern.pattern_filter_track_str))
        track_result = pattern.findall(text)
        spical_strs.extend(track_result)

        pattern = re.compile(r"%s" % (iOSTranslatePattern.pattern_filter_router_str))
        router_result = pattern.findall(text)
        spical_strs.extend(router_result)

        text = StringUtil.get_replaced_str(text, spical_strs)
        pattern = re.compile(r"%s" % (pattern_str))

        def new_repl(matched):
            return repl(StringUtil.get_origin_str(matched.group(), spical_strs))

        result = re.sub(pattern, new_repl, text)
        result = StringUtil.get_origin_str(result, spical_strs)
        return result

    # 特殊的字符会先被替换，然后正则匹配，最后替换回来，减少正则复杂度，提高效率
    # 获取特殊字符加密后的字符串
    def get_replaced_str(oldStr: str, spical_strs: list[str]) -> str:
        for text in spical_strs:
            if len(text) > 0:
                oldStr = oldStr.replace(text, StringUtil.simpleEncode(text))

        return oldStr

    # 获取特殊字符被解密后的字符串
    def get_origin_str(oldStr: str, spical_strs: list[str]) -> str:
        for text in spical_strs:
            if len(text) > 0:
                oldStr = oldStr.replace(
                    StringUtil.get_replaced_str(text, spical_strs), text
                )

        return oldStr
