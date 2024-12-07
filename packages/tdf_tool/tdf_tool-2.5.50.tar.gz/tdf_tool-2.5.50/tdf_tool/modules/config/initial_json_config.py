import json
import os
from typing import Tuple
from tdf_tool.tools.print import Print
from tdf_tool.tools.shell_dir import ShellDir


class InitialJsonConfig:
    
    def __init__(self):
        config = self.__getInitialConfig()
        self.featureBranch = config[0]
        self.shellName = config[1]
        self.moduleNameList = config[2]

    # 获取环境配置文件
    def __getInitialConfig(self) -> Tuple:
        ShellDir.goInShellDir()
        if os.path.exists("tdf_cache") is not True:
            Print.error("读取项目环境配置文件initial_config.json失败")
        os.chdir("tdf_cache")

        jsonData = dict
        with open("initial_config.json", "r", encoding="utf-8") as rf:
            jsonData = json.loads(rf.read())
            rf.close()
            if (
                isinstance(jsonData, dict)
                and jsonData.__contains__("featureBranch")
                and jsonData.__contains__("shellName")
                and jsonData.__contains__("moduleNameList")
            ):    
                self.__initialDepsEnhancement(jsonData)
                return (
                    jsonData["featureBranch"],
                    jsonData["shellName"],
                    jsonData["moduleNameList"],
                )
            else:
                Print.error("读取项目环境配置文件initial_config.json失败")
    
    def __initialDepsEnhancement(self, jsonData: dict):
        self.forceOverrides: list = []
        if (jsonData.__contains__("depsEnhancement")):
            innerJson = jsonData["depsEnhancement"]
            if isinstance(innerJson, dict) and innerJson.__contains__("forceOverrides"):
                overrideJson = innerJson["forceOverrides"]
                if isinstance(overrideJson, dict):
                    print(overrideJson)
                    self.forceOverrides = [{item: overrideJson[item]} for item in overrideJson]
                    
           