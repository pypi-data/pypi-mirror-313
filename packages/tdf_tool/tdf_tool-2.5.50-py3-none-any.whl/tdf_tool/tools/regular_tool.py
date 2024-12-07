import codecs
import re
from tdf_tool.tools.print import Print


class RegularTool:
    __replace_sign = r"#@^&#%&%*$#"

    # 删除埋点
    def delete_track(content: str) -> str:
        m = re.compile(r"TDFAnalytics.track.track\([^\(]*?\);")
        outtmp = re.sub(m, "", content)
        return outtmp

    # 删除备注
    def delete_remark(content: str) -> str:
        m = re.compile(r"//.*")
        outtmp = re.sub(m, "", content)
        return outtmp

    # 删除弃用
    def delete_deprecated(content: str) -> str:
        m = re.compile(r"@Deprecated\(.*?\)")
        outtmp = re.sub(m, "", content)
        return outtmp

    # 删除 @router 相关的文案
    def delete_router(content: str) -> str:
        m = re.compile(r"@TZRouter\([^\(]*?\)")
        outtmp = re.sub(m, "", content)
        return outtmp

    # 删除 @TZWidgetsDoc 相关的文案
    def delete_widgetsDoc(content: str) -> str:
        m = re.compile(r"@TZWidgetsDoc\([^\(]*?\)")
        outtmp = re.sub(m, "", content)
        return outtmp

    # 删除被 noTransl 包裹起来的代码
    def delete_noTranslDoc(content: str) -> str:
        m = re.compile(r"noTransl\([^\(]*?\)")
        outtmp = re.sub(m, "", content)
        return outtmp

    # 删除枚举，枚举中不能使用.intl
    def find_enums(content: str) -> str:
        pattern = r"enum \w* {[^\}]*"
        machs = re.findall(pattern, content)
        return machs

    # 寻找带中文常量字符串
    def find_chinese_const_str(content: str) -> list[str]:
        machs_d: list[str] = RegularTool.__match_str(
            content,
            r"\"",
            r'const *String *[a-zA-Z_ ]*= *"(?<=\")[^\"\f\n\r\t\v]*?[\u4E00-\u9FA5][^\"\f\n\r\t\v]*?(?=\")";',
        )
        return machs_d

    # 寻找带 .intl 后缀的文本，匹配出来是不带 "" 或者 '' 的字符
    def find_intl_str(content: str) -> list[str]:
        machs_d = RegularTool.__match_str(
            content,
            r"\"",
            r"(?<=\")[^\"\f\n\r\t\v]*?[\u4E00-\u9FA5][^\"\f\n\r\t\v]*?(?=\"\s*\.intl)",
        )
        # matchs_s = RegularTool.__match_str(
        #     content,
        #     r"\'",
        #     r"(?<=\')[^\'\f\n\r\t\v]*?[\u4E00-\u9FA5][^\'\f\n\r\t\v]*?(?=\'\s*\.intl)",
        # )
        return machs_d

    # 删除带 .intl 后缀的文本
    def delete_intl_str(content: str) -> str:
        outtmp = RegularTool.__delete_str(
            content,
            r"\"",
            r'"[^\"\f\n\r\t\v]*?[\u4E00-\u9FA5][^\"\f\n\r\t\v]*?"\s*\.intl',
        )
        # outtmp = RegularTool.__delete_str(
        #     outtmp,
        #     r"\'",
        #     r"'[^\'\f\n\r\t\v]*?[\u4E00-\u9FA5][^\'\f\n\r\t\v]*?'\s*\.intl",
        # )
        return outtmp

    # 寻找 intl 的单引号字符串
    def find_apostrophe_strs(content: str) -> list[str]:
        return RegularTool.find_apostrophe_intl(
            content
        ) + RegularTool.find_apostrophe_chinese(content)

    # 寻找 intl 的单引号字符串
    def find_apostrophe_intl(content: str) -> list[str]:
        matchs_s = RegularTool.__match_str(
            content,
            r"\'",
            r"(?<=\')[^\'\f\n\r\t\v]*?[\u4E00-\u9FA5][^\'\f\n\r\t\v]*?(?=\'\s*\.intl)",
        )
        return matchs_s

    def find_enum_name(content: str) -> str:
        matchs_s: list[str] = RegularTool.__match_str(
            content,
            r"\'",
            r"(?<=enum) *[a-zA-Z_]* *{",
        )
        if len(matchs_s) == 0:
            return
        enum_str = matchs_s[0]
        return enum_str.replace(" ", "").replace("{", "")

    def find_un_format(content: str) -> list[str]:
        matchs_s: list[str] = RegularTool.__match_str(
            content,
            r"\'",
            r"(?<!\\)\$",
        )
        matchs_s = list(map(lambda x: x.strip(), matchs_s))
        return matchs_s

    # 寻找没有国际化的单引号字符串
    def find_apostrophe_chinese(content: str) -> list[str]:
        matchs_s: list[str] = RegularTool.__match_str(
            content,
            r"\'",
            r"'[^\'\f\n\r\t\v]*?[\u4E00-\u9FA5][^\'\f\n\r\t\v]*?'(?!\.intl)",
        )
        matchs_s = list(map(lambda x: x.strip(r"'"), matchs_s))
        return matchs_s

    # 寻找没国际化的中文字符串，匹配出来是不带 "" 或者 '' 的字符
    def find_chinese_str(content: str) -> list[str]:
        matchs_d: list[str] = RegularTool.__match_str(
            content,
            r"\"",
            r'"[^\"\f\n\r\t\v]*?[\u4E00-\u9FA5][^\"\f\n\r\t\v]*?"(?!\.intl)',
        )
        matchs_d = list(map(lambda x: x.strip(r'"'), matchs_d))
        # matchs_s = RegularTool.__match_str(
        #     content,
        #     r"\'",
        #     r"'[^\'\f\n\r\t\v]*?[\u4E00-\u9FA5][^\'\f\n\r\t\v]*?'(?!\.intl)",
        # )
        # matchs_s = list(map(lambda x: x.strip(r"'"), matchs_s))
        return matchs_d

    # 删除const修复中文中的const
    def delete_const(content: str, strs: list[str]) -> str:
        for str in strs:
            r_str = str.replace("const", "", 1).lstrip()
            content = content.replace(str, r_str)

        return content

    # 替换单引号成双引号
    def replace_apostrophe_strs(content: str, strs: list[str]) -> str:
        for str in strs:
            m_str = r"'{0}'".format(str)
            content = content.replace(m_str, '"' + str + '"')

        return content

    # 批量替换 .intl
    def replace_chinese_strs(content: str, strs: list[str]) -> str:
        for str in strs:
            m_str = r'"{0}"'.format(str)
            content = content.replace(m_str, m_str + ".intl")

        return content

    # 替换掉多个 .intl 结尾的字符串
    def replace_multi_intl(content: str) -> str:
        def __delete_intl(matched):
            # 删除多余的 .intl
            tempstr: str = matched.group()  # 取查找到的字符/串
            c_str = tempstr.split(".intl")[0]
            tempstr = c_str + ".intl"  # 格式化7
            return tempstr

        q_sign = r"\""
        content = content.replace(q_sign, RegularTool.__replace_sign)
        m = re.compile(
            r'"[^\"\f\n\r\t\v]*?[\u4E00-\u9FA5][^\"\f\n\r\t\v]*?"\s*.intl[\.intl]*\.intl'
        )
        content = re.sub(m, __delete_intl, content)
        content = content.replace(RegularTool.__replace_sign, q_sign)
        return content

    # 没国际化的中文字符串 追加 .intl
    # def replace_chinese_str(content: str, old_str: str) -> str:

    #     q_sign = r"\""
    #     content = content.replace(q_sign, RegularTool.__replace_sign)
    #     m = re.compile(r'"[^\"\f\n\r\t\v]*?[\u4E00-\u9FA5][^\"\f\n\r\t\v]*?"(?!\.intl)')
    #     content: str = re.sub(m, RegularTool.__append_Suffix, content)
    #     content = content.replace(RegularTool.__replace_sign, q_sign)

    # s_sign = r"\'"
    # content = content.replace(s_sign, RegularTool.__replace_sign)
    # m = re.compile(r"'[^\'\f\n\r\t\v]*?[\u4E00-\u9FA5][^\'\f\n\r\t\v]*?'(?!\.intl)")
    # content = re.sub(m, RegularTool.__append_Suffix, content)
    # content = content.replace(RegularTool.__replace_sign, s_sign)

    # return content

    # def __append_Suffix(matched):
    #     # 找到字母，把原字母 添加 .intl
    #     tempstr = matched.group()  # 取查找到的字符/串
    #     tempstr = tempstr + ".intl"  # 格式化
    #     return tempstr

    # 删除匹配的字符串
    def __delete_str(content: str, sign: str, pattern: str) -> str:
        content = content.replace(sign, RegularTool.__replace_sign)
        m = re.compile(pattern)
        outtmp = re.sub(m, "", content)
        return outtmp

    # 匹配 字符串，无法处理的符号先替换，然后再处理
    def __match_str(content: str, sign: str, pattern: str) -> list[str]:
        match_strs = []
        content = content.replace(sign, RegularTool.__replace_sign)
        matchs: list[str] = re.findall(pattern, content)
        for m in matchs:
            new_str = m.replace(RegularTool.__replace_sign, sign)
            match_strs.append(new_str)
        return match_strs

    # 寻找 intl 的 import 字符
    def find_intl_imports(content: str) -> list[str]:
        pattern = r"import '.*_i18n.dart';"
        matchs = re.findall(pattern, content)
        return matchs

    # 替换 intl 的 import
    def replace_intl_imports(content: str, replace_str: str) -> str:
        m = re.compile(r"import '.*_i18n.dart';")
        outtmp = re.sub(m, replace_str, content)
        return outtmp

    # 去掉转义符
    def decode_escapes(s) -> str:
        ESCAPE_SEQUENCE_RE = re.compile(
            r"""
        ( \\U........      # 8-digit hex escapes
        | \\u....          # 4-digit hex escapes
        | \\x..            # 2-digit hex escapes
        | \\[0-7]{1,3}     # Octal escapes
        | \\N\{[^}]+\}     # Unicode characters by name
        | \\[\\'"abfnrtv]  # Single-character escapes
        )""",
            re.UNICODE | re.VERBOSE,
        )

        def decode_match(match):
            return codecs.decode(match.group(0), "unicode-escape")

        return ESCAPE_SEQUENCE_RE.sub(decode_match, s)
