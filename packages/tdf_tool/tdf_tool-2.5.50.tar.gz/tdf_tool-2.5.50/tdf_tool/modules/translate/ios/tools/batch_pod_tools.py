import json
import os
from tdf_tool.tools.cmd import Cmd
from tdf_tool.tools.shell_dir import ShellDir
from tdf_tool.tools.cmd import Cmd
import json
from tdf_tool.tools.print import Print
from tdf_tool.modules.translate.file_util import FileUtil


class BatchPodModel:
    def __init__(self, name: str, branch: str, path: str):
        self.name = name
        self.branch = branch
        self.path = path
        self.source_files: set[str] = set()


class BatchPodTools:
    # 可以进行国际化的列表
    def batchPodList() -> list[BatchPodModel]:
        return BatchPodTools.batchPodListFrom("Podfile")

    def batchPodListFrom(file_path: str) -> list[BatchPodModel]:
        """获取可以进行国际化的列表

        Args:
            file_path (str): podfile的文件路径

        Returns:
            list[BatchPodModel]: 可以国际化的列表
        """
        os.environ["FLUTTER_IS_LOCAL"] = "false"
        os.environ["BATCH_IS_LOCAL"] = "true"
        podfile_json_str: str = Cmd.run("bundle exec pod ipc podfile-json " + file_path)
        podfile_json = json.loads(podfile_json_str)
        batch_pod_local = podfile_json["batch_pod_local"]
        pod_models = []
        for pod in batch_pod_local:
            pod_dic = batch_pod_local[pod][0]
            pod_model = BatchPodModel(
                pod,
                pod_dic["branch"],
                pod_dic["path"],
            )
            pod_models.append(pod_model)
        return pod_models

    # 获取 pod 的source_files
    def generate_pod_source_files(pods: list[BatchPodModel]):
        for pod in pods:
            podspec_path = ShellDir.findPodspec(pod.path)
            if isinstance(podspec_path, str):
                pod.source_files = BatchPodTools.get_source_files(podspec_path)
            else:
                Print.error(pod.path + "目录下没找到 podspec 文件")

    # path 为 podspec 所在的路径
    def get_source_files(podspec_path: str) -> set[str]:
        podspec_name = podspec_path.split("/")[-1]
        root_path = podspec_path.split("/" + podspec_name)[0]
        podspec_json_str: str = Cmd.run("pod ipc spec " + podspec_path)
        podspec_json: dict = json.loads(podspec_json_str)
        # 处理 root source_files
        root_source_paths: list[str] = podspec_json.get("source_files")
        if root_source_paths is None:
            root_source_paths = []
        elif isinstance(root_source_paths, str):
            root_source_paths = [root_source_paths]

        # 处理 sub source_files
        subspecs: list[dict] = podspec_json.get("subspecs")
        if subspecs is None:
            subspecs = []
        for subspec in subspecs:
            sub_source_files = subspec.get("source_files")
            if isinstance(sub_source_files, str):
                root_source_paths.append(sub_source_files)
            elif isinstance(sub_source_files, list):
                root_source_paths.extend(sub_source_files)

        # 获取 file_list
        root_source_paths_set: set[str] = set(root_source_paths)
        rb_file = FileUtil.generate_get_files_rb()
        ruby_cmd = ["ruby", rb_file]
        for source_path in root_source_paths_set:
            source_path = root_path + "/" + source_path
            ruby_cmd.append(source_path)
        file_list_str: str = Cmd.run(ruby_cmd, shell=False)
        file_list = file_list_str.split("\n")

        new_file_list: set[str] = set()
        for file in file_list:
            if os.path.isfile(file):
                new_file_list.add(file)

        return new_file_list
