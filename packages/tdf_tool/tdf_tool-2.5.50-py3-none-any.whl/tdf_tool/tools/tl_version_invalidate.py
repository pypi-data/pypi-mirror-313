from tdf_tool.tools.env import EnvTool
from tdf_tool.tools.print import Print
import requests
from enum import Enum, unique


# 版本升级类型
# version1.version2.version3
@unique
class VersionUpgradeType(Enum):
    major = "重大更新"  # version1
    api = "api更新/bug修复"  # version2
    minor = "小功能更新"  # version3
    none = "无功能更新"  # 没有功能更新
    abnormal = "异常更新"  # 异常更新


class TLOwner:

    def __init__(self):
        self.tl_package_name = "tdf-tool"
        self.tl_current_version = EnvTool.tdfToolVersion()

    def check_for_package_updates(self):
        Print.title("tl 版本检测中...")
        try:
            # 获取GitHub上包的最新版本
            response = requests.get(f'https://mirrors.aliyun.com/pypi/{self.tl_package_name}/json')
            if response.status_code == 200:
                latest_version = response.json()['info']['version']
                result = self.__compare_version(latest_version, self.tl_current_version)
                if  result == VersionUpgradeType.minor:
                    Print.str("当前 tl 版本：{0}".format(self.tl_current_version))
                    Print.yellow(
                        "发现新版本：{0}（{1}），请使用 pip3 install tdf_tool --upgrade 命令升级，以使用最新功能。可通过'https://pypi.org/project/tdf_tool/'查看最新功能迭代".format(
                            latest_version, result.value))
                elif result == VersionUpgradeType.major or result == VersionUpgradeType.api:
                    Print.str("当前 tl 版本：{0}".format(self.tl_current_version))
                    Print.error(
                        "发现新版本：{0}（{1}），与新版本差别过大，请使用 pip3 install tdf_tool --upgrade 命令升级，以使用最新功能。可通过'https://pypi.org/project/tdf_tool/'查看最新功能迭代".format(
                            latest_version, result.value))
                elif result == VersionUpgradeType.abnormal:
                    Print.warning("当前版本{0}高于远端最新版本{1}".format(latest_version, self.tl_current_version))
                else:
                    Print.str("当前已是最新版本")
            else:
                Print.warning("远端版本获取失败：status_code：{0}，content：{1}".format(response.content))
        except Exception as e:
            Print.warning("版本获取异常：{0}".format(e))

    # 比较两个版本号的大小
    def __compare_version(self, version1: str, version2: str) -> VersionUpgradeType:
        v1 = list(map(int, version1.split('.')))
        v2 = list(map(int, version2.split('.')))

        for i in range(max(len(v1), len(v2))):
            num1 = v1[i] if i < len(v1) else 0
            num2 = v2[i] if i < len(v2) else 0

            if num1 > num2:
                if i == 0:
                    return VersionUpgradeType.major
                elif i == 1:
                    return VersionUpgradeType.api
                elif i == 2:
                    return VersionUpgradeType.minor
            elif num1 < num2:
                return VersionUpgradeType.abnormal

        return VersionUpgradeType.none
