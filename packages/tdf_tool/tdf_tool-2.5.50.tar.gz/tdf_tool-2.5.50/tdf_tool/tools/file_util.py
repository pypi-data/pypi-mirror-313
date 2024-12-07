from tdf_tool.tools.generator import DefaultGenerator


# tl 命令写文件专用类
class TLFileUtil:
    def __init__(self, file_path: str, generator_name: str = 'default generator'):
        self.__file_path = file_path
        self.__generator = generator_name
        self.fw = open(self.__file_path, "w+")
        self.defaultDesc()

    # 默认描述
    def defaultDesc(self):
        self.fw.write(DefaultGenerator.defaultTitleDesc(self.__generator))

    def write(self, content: str):
        self.fw.write(content)

    def close(self):
        self.fw.close()
