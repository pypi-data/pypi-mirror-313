from ruamel import yaml


class TranslateEnable:
    """
    翻译的开关：通过 .gitlab-ci.yml 文件检测当前库是否需要翻译
    """

    def __init__(self, file_path: str):
        # 读取 .gitlab-ci.yml 内容
        with open(file_path, encoding="utf-8") as f:
            self.gitlab_ci = yaml.round_trip_load(f)
            f.close()
        try:
            # 获取 .gitlab-ci.yml 文件中 translate_enable 的值
            self.no_translate = self.gitlab_ci["variables"]["NO_TRANSLATE"] == 1
        except KeyError:
            self.no_translate = False
