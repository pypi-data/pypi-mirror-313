

# 用于 记录模块的依赖信息
import copy
from tdf_tool.tools.print import Print


class DepsRecord:
    def __init__(self, moduleName):
        self.moduleName = moduleName
        self.deps: list[str] = []

    def addDepsItemName(self, depsItemName: str):
        self.deps.append(depsItemName)


# 依赖分析工具类
class DepsAnalysisUtil:
    def __init__(self, recordList: list[DepsRecord]):
        self.recordList = copy.deepcopy(recordList) # 深拷贝

    # 分析依赖并以列表形式返回依赖顺序（倒叙，从下往上）
    def analysis(self) -> list[str]:
        sortModuleList = []
        while len(self.recordList) > 0:
            currentLen = len(self.recordList)
            for item in self.recordList:
                moduleName = item.moduleName
                if len(item.deps) == 0:
                    self.recordList.remove(item)
                    sortModuleList.append(moduleName)
                    for record in self.recordList:
                        if moduleName in record.deps:
                            record.deps.remove(moduleName)
                    break
            updateLen = len(self.recordList)
            # 如果当前次遍历，模块数量没有变化，那么只可能是循环引用
            if currentLen == updateLen:
                errorSortedList = sorted(self.recordList[:], key=lambda obj: len(obj.deps))
                first = errorSortedList[0]
                if len(first.deps) > 0:
                    Print.error("依赖存在循环引用  " + first.moduleName + " <=> " + first.deps[0])

        return sortModuleList
    

