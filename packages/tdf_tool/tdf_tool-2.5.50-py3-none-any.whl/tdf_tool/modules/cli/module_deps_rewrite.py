#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# 模块重写脚本

import os, json
import subprocess
from ruamel import yaml
from tdf_tool.modules.config.initial_json_config import InitialJsonConfig
from tdf_tool.modules.cli.bean.deps_item import DepsAnalysisUtil, DepsRecord
from tdf_tool.modules.cli.utils.yaml_utils import YamlFileUtils
from tdf_tool.tools.dependencies_analysis import DependencyAnalysis
from tdf_tool.tools.print import Print
from tdf_tool.modules.module.module_tools import ModuleTools
from tdf_tool.tools.shell_dir import ShellDir


class ModuleDependenciesRewriteUtil:
    def __init__(self):
        Print.stage("Upgrade 操作")
        Print.line()
        self.moduleJsonData = ModuleTools.getModuleJsonData()
        self.moduleNameList = ModuleTools.getModuleNameList()
        self.initJsonData = ModuleTools.getInitJsonData()
        self.initialConfig = InitialJsonConfig()

    # 分析lock文件，获取所有的packages
    def _analysisLock(self):
        os.chdir(self.__moduleGenPath)
        # 分析前先执行pub upgrade
        os.popen("flutter pub upgrade").read()

        # 读取lock内容
        with open("pubspec.lock", encoding="utf-8") as f:
            doc = yaml.round_trip_load(f)
            if isinstance(doc, dict) and doc.__contains__("packages"):
                f.close()
                return doc["packages"]

    # 是否是壳模块
    def _isShellModule(self):
        return self.moduleJsonData[self.__moduleName]["type"] == "app"

    # 确认哪些依赖需要重写
    def _confirmRewriteDependencies(self, isShell):
        if isShell:  # 壳模块重写所有配置的依赖
            for item in self.moduleNameList:
                if item != self.__moduleName:  # 壳自己不加入重写列表
                    self.__needRewriteDependencies.append(item)
        else:  # 如果不是壳模块，则进行lock文件内的package列表和开发模块匹配，匹配上则添加到override列表
            for package in self.__moduleDependenciesMap:
                for module in self.moduleNameList:
                    if package == module:
                        self.__needRewriteDependencies.append(module)

        Print.stage("{0}中以下依赖将被override".format(self.__moduleName))
        Print.debug(self.__needRewriteDependencies)

    def _addOverrideDependencies(self):
        mDict = dict()
        for item in self.__needRewriteDependencies:
            mDict[item] = {"path": "../{0}/".format(item)}

        return mDict

    def _rewriteDependencies(self, isShell):
        # 添加dependency_overrides
        os.chdir(self.__moduleGenPath)
        with open("pubspec.yaml", encoding="utf-8") as f:
            doc = yaml.round_trip_load(f)
            if isinstance(doc, dict):
                self._confirmRewriteDependencies(isShell)
                if (
                    doc.__contains__("dependency_overrides")
                    and doc["dependency_overrides"] is not None
                ):
                    doc["dependency_overrides"] = None

                # 重写依赖
                overrideDict = dict()
                for item in self.__needRewriteDependencies:
                    if isShell:
                        overrideDict[item] = {
                            "path": "../.tdf_flutter/{0}/".format(item)
                        }
                    else:
                        overrideDict[item] = {"path": "../{0}/".format(item)}
                if len(self.__needRewriteDependencies) > 0:
                    doc["dependency_overrides"] = overrideDict

                with open("pubspec.yaml", "w+", encoding="utf-8") as reW:
                    yaml.round_trip_dump(
                        doc,
                        reW,
                        default_flow_style=False,
                        encoding="utf-8",
                        allow_unicode=True,
                    )
                    reW.close()
                    # 依赖重写完，执行pub upgrade更新lock文件
                    os.popen("flutter pub upgrade").read()
                    Print.debug("lock文件已更新")
            f.close()

    # 添加dependency_overrides，如果已存在模块的override，则不修改

    def _rewriteDependenciesIfUpdate(self, isShell):
        os.chdir(self.__moduleGenPath)
        with open("pubspec.yaml", encoding="utf-8") as f:
            doc = yaml.round_trip_load(f)
            if isinstance(doc, dict):
                self._confirmRewriteDependencies(isShell)

                global existUpdate
                existUpdate = False

                # 删除不存在于重写依赖列表中的key
                if (
                    doc.__contains__("dependency_overrides")
                    and doc["dependency_overrides"] is not None
                    and isinstance(doc["dependency_overrides"], dict)
                ):
                    keyList = list(doc["dependency_overrides"].keys())
                    for item in keyList:
                        if item not in self.__needRewriteDependencies:
                            Print.debug("${0}依赖被删除".format(item))
                            existUpdate = True
                            del doc["dependency_overrides"][item]

                if doc.__contains__("dependency_overrides"):
                    overrideDict = doc["dependency_overrides"]
                    if overrideDict is None:
                        overrideDict = dict()
                else:
                    overrideDict = dict()
                for item in self.__needRewriteDependencies:
                    if (
                        doc.__contains__("dependency_overrides")
                        and doc["dependency_overrides"] is not None
                        and isinstance(doc["dependency_overrides"], dict)
                        and doc["dependency_overrides"].get(item, -1) != -1
                    ):
                        Print.debug("${0}依赖已存在（不予修改）".format(item))
                    else:
                        Print.debug("${0}依赖不存在（添加）".format(item))
                        existUpdate = True
                        if isShell:
                            overrideDict[item] = {
                                "path": "../.tdf_flutter/{0}/".format(item)
                            }
                        else:
                            overrideDict[item] = {"path": "../{0}/".format(item)}
                doc["dependency_overrides"] = overrideDict
                if existUpdate:
                    with open("pubspec.yaml", "w+", encoding="utf-8") as reW:
                        yaml.round_trip_dump(
                            doc,
                            reW,
                            default_flow_style=False,
                            encoding="utf-8",
                            allow_unicode=True,
                        )
                        reW.close()
                        # 依赖重写完，执行pub upgrade更新lock文件
                        os.popen("flutter pub upgrade").read()
                        Print.debug("lock文件已更新")
                else:
                    Print.debug("yaml无更新")

            f.close()

    def existOverride(self, moduleName: str) -> bool:
        forceOverrides = self.initialConfig.forceOverrides
        for forceItem in forceOverrides:
            _key = list(forceItem.keys())[0]
            if moduleName == _key:
                return True
        return False

    def _recursionDeps(self, deps: dict) -> dict:
        temp = {}
        for node in deps:
            if self.moduleNameList.__contains__(node["name"]):
                module = node["name"]
                depsModules = self._recursion(module, deps)
                temp[module] = depsModules
        formatted_json = json.dumps(temp, indent=4, ensure_ascii=False)
        Print.step(formatted_json)
        return temp

    # 递归分析依赖
    def _recursion(self, moduleName: str, deps: dict) -> list:
        if [item["name"] for item in deps].__contains__(moduleName):
            modules = [
                item
                for item in deps
                if isinstance(item, dict) and item["name"] == moduleName
            ]  # 只会存在一个

            depsModules = [
                item
                for item in modules[0]["dependencies"]
                if self.moduleNameList.__contains__(item) or self.existOverride(item)
            ]
            resultModule = depsModules
            for module in depsModules:
                resultModule = resultModule + [
                    item
                    for item in self._recursion(module, deps)
                    if resultModule.__contains__(item) is not True
                ]
            return resultModule
        return []

    # 重写依赖 本地依赖

    def rewrite(self, reWriteOnlyChange=False):
        ShellDir.goInShellDir()

        # 壳在生成package_config.json后，执行deps --json获取依赖树
        # os.system('flutter pub upgrade')
        # 重写壳
        Print.step("在壳中重写所有模块")
        self._reWriteInShell()
        os.popen("flutter pub upgrade").read()
        Print.step("依赖分析...")
        depsJson = json.loads(os.popen("flutter pub deps --json").read())
        packageConfigJson = self._recursionDeps(depsJson["packages"])  # 依赖树维护

        depsRecordList: list[DepsRecord] = []

        for module in self.moduleNameList:
            record = DepsRecord(module)
            for _key in packageConfigJson:
                if _key == module:
                    moduleDeps: list[str] = packageConfigJson[_key]
                    for depsItemName in moduleDeps:
                        if depsItemName in self.moduleNameList:
                            record.addDepsItemName(depsItemName)
            depsRecordList.append(record)

        depsUtils = DepsAnalysisUtil(depsRecordList)

        depsSortedList = depsUtils.analysis()

        Print.yellow(f"依赖顺序: {depsSortedList}")

        forceOverrides = self.initialConfig.forceOverrides
        for index, module in enumerate(depsSortedList):
            Print.step(f"更新{module}, 进度:({index}/{len(depsSortedList)})")

            _modulePath = "../.tdf_flutter/" + module

            depsMap = []
            forceOverrides = self.initialConfig.forceOverrides
            for moduleName in packageConfigJson[module]:
                if self.moduleNameList.__contains__(moduleName):
                    depsMap.append({moduleName: {"path": "../{0}".format(moduleName)}})
                else:
                    for forceItem in forceOverrides:
                        _key = list(forceItem.keys())[0]
                        if moduleName == _key:
                            depsMap.append(forceItem)
            print("重写节点数据：====》")
            formatted_json = json.dumps(depsMap, indent=4, ensure_ascii=False)
            print(formatted_json)
            self._writeNewDeps(_modulePath, depsMap, False)

        # 重写壳
        Print.step("更新壳, 进度:(1/1)")
        self._reWriteInShell()

    def _loadModuleLock(self, modulePath: str) -> dict:
        try:
            with open(
                os.path.join(modulePath, "pubspec.lock"), "r", encoding="utf-8"
            ) as f:
                data = yaml.round_trip_load(f)
                return data["packages"]
        except:
            return {}

    def _reWriteInShell(self):
        forceOverrides = self.initialConfig.forceOverrides

        allShellDeps = [
            {key: {"path": "../.tdf_flutter/{0}".format(key)}}
            for key in self.moduleNameList
        ]
        combinedList = allShellDeps + forceOverrides
        deduplicatedList: list = []
        for item in combinedList:
            if item not in deduplicatedList:
                deduplicatedList.append(item)

        self._writeNewDeps("./", deduplicatedList)

    def _writeNewDeps(self, modulePath: str, deps: list[dict], isShell: bool = True):
        yamlFileUtils = YamlFileUtils(modulePath)
        depsKeys = yamlFileUtils.readOverrideDepsKeys()

        # 比对yaml的重写库是否有更新
        # 使用列表推导式获取所有字典的键
        overrideKeys = [list(item.keys())[0] for item in deps]
        # print(overrideKeys)
        isYamlOverrideSame = sorted(depsKeys) == sorted(overrideKeys)
        # 比对lock文件和package_config.json文件的重写库是否有更新
        isLockAndYamlOverrideSame = self.validate_lock_and_yaml_file(
            modulePath, overrideKeys
        )

        # 重写的依赖不一致，则需要重写并执行pub upgrade
        if isYamlOverrideSame and isLockAndYamlOverrideSame:
            Print.str("deps pass.")
        else:
            if isYamlOverrideSame is not True:
                Print.yellow("yaml文件有更新")

            if isLockAndYamlOverrideSame is not True:
                Print.yellow("lock内重写库和yaml重写库不一致")
            Print.yellow("exec: flutter pub upgrade")

            yamlFileUtils.writeOverrideDepsByDict(deps, isShell=isShell)
            # 依赖重写完，执行pub upgrade更新lock文件
            command = "flutter pub upgrade"
            result = subprocess.run(
                command, shell=True, capture_output=True, text=True, cwd=modulePath
            )
            if result.returncode == 0:
                print("command ’flutter pub upgrade‘ exec successfully!")
                Print.str("lock文件已更新")
            else:
                Print.error("Command failed!", shouldExit=False)
                Print.error("Error output:" + result.stderr)

    # 是否执行过flutter pub upgrade（判断条件为是否存在lock文件和package_config.json文件）
    # def existDepsResult(self, modulePath) -> bool:
    #     packageConfigFilePath = os.path.join(modulePath, ".dart_tool/package_config.json")
    #     lockFilePath = os.path.join(modulePath, "pubspec.lock")
    #     return os.path.isfile(packageConfigFilePath) and os.path.isfile(lockFilePath)

    # 校验yaml中override的库，是否已在lock文件中存在且是相对路径源码引用
    def validate_lock_and_yaml_file(self, modulePath: str, depsKeys: list[str]) -> bool:
        lockPath = os.path.join(modulePath, "pubspec.lock")
        packageConfigFilePath = os.path.join(
            modulePath, ".dart_tool/package_config.json"
        )
        pathPackages: list = []
        jsonPackages: list = []
        if os.path.isfile(lockPath):
            with open(lockPath, "r", encoding="utf-8") as f:
                data = yaml.round_trip_load(f)
                packages: dict = data["packages"]
                for item in packages.keys():
                    if packages[item]["source"] == "path":
                        pathPackages.append(item)
        else:
            return False

        if os.path.isfile(packageConfigFilePath):
            with open(packageConfigFilePath, "r", encoding="utf-8") as readF:
                fileData = readF.read()
                dic: dict = json.loads(fileData)
                packages: list = dic["packages"]
                for item in packages:
                    if item["rootUri"].startswith("../../"):
                        jsonPackages.append(item["name"])
        else:
            return False

        # override的库一致，则不需要重新执行upgrade
        return sorted(depsKeys) == sorted(pathPackages) and sorted(depsKeys) == sorted(
            jsonPackages
        )
