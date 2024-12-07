
import os
from ruamel import yaml

from tdf_tool.tools.print import Print

# yaml 文件操作
class YamlFileUtils:
    yamlFileName = "pubspec.yaml"
    dependenciesNode = "dependencies"
    dependencyOverridesNode = "dependency_overrides"

    def __init__(self, path):
        self.yamlPath = os.path.join(path, YamlFileUtils.yamlFileName)

    def readOverrideDepsKeys(self) -> list[str]:
        with open(self.yamlPath, encoding="utf-8") as f:
            doc = yaml.round_trip_load(f)
            node = YamlFileUtils.dependencyOverridesNode
            if isinstance(doc, dict) and doc.__contains__(node) and isinstance(doc[node], dict):
                return list(dict(doc[node]).keys())        
        return []
    
    def writeOverrideDeps(self, moduleList: list[str], isShell: bool = True):
        with open(self.yamlPath, encoding="utf-8") as f:
            doc = yaml.round_trip_load(f)
            node = YamlFileUtils.dependencyOverridesNode
            if isinstance(doc, dict):
                if doc.__contains__(node) and doc[node] is not None:
                    doc[node] = None
            
            # 重写依赖
            overrideDict = dict()
            for item in moduleList:
                if isShell:
                    overrideDict[item] = {"path": "../.tdf_flutter/{0}/".format(item)}
                else:
                    overrideDict[item] = {"path": "../{0}/".format(item)}
            if len(moduleList) > 0:
                doc[node] = overrideDict

            with open(self.yamlPath, "w+", encoding="utf-8") as reW:
                yaml.round_trip_dump(
                    doc,
                    reW,
                    default_flow_style=False,
                    encoding="utf-8",
                    allow_unicode=True,
                )
                reW.close()
    
    def writeOverrideDepsByDict(self, deps: list[dict], isShell: bool = True):
        with open(self.yamlPath, encoding="utf-8") as f:
            doc = yaml.round_trip_load(f)
            node = YamlFileUtils.dependencyOverridesNode
            if isinstance(doc, dict):
                if doc.__contains__(node) and doc[node] is not None:
                    doc[node] = None
            
            # 重写依赖
            overrideDict = {}
            for item in deps:
                key = list(item.keys())[0]
                overrideDict[key] = item[key]
            if len(deps) > 0:
                doc[node] = overrideDict

            with open(self.yamlPath, "w+", encoding="utf-8") as reW:
                yaml.round_trip_dump(
                    doc,
                    reW,
                    default_flow_style=False,
                    encoding="utf-8",
                    allow_unicode=True,
                )
                reW.close()