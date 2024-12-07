import hashlib
import zipfile
import requests
from tdf_tool.modules.translate.tools.translate_tool import LanguageType
from tdf_tool.tools.print import Print


class I18nRequest:
    _secret = "BoivJgAlmBUO05yoxD6RU/SZ/nhLvpXT40v2ceqKJ1s="
    _common_parameter = {
        "s_net": "1",
        "s_did": "cf14ac482d044ded40a8e8f936fe7dfb",
        "app_key": "200006",
        "s_os": "android",
        "s_eid": "99229474",
        "s_osv": "31",
        "format": "json",
        "s_sc": "1440*3007",
        "s_br": "M2011K2C",
        "s_apv": "6.1.40",
        "appKey": "100001",
    }

    def __init__(
        self, host: str, file_name: str, unzip_dir: str, lang_prefix: LanguageType
    ):
        self.host = host
        self.file_name = file_name
        self.unzip_dir = unzip_dir
        self.lang_prefix = lang_prefix

    def start(self):
        # host = "10.1.26.41:8080"
        query_url = self._generate_query_url(self._common_parameter)
        post_params = {"lang_prefix": self.lang_prefix.str(), "type": "MAI"}
        self._common_parameter.update(post_params)

        sign = self._sign(self._common_parameter)
        url = f"{self.host}/boss/v1/export_multi_content_by_type_and_lang?{query_url}&sign={sign}"
        response = requests.post(
            url=url,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data=post_params,
        )
        result = response.text
        Print.str(result)
        json = eval(result)
        if json["code"] != 1:
            Print.error(f"请求失败：{json}")
        download_url = json["data"]
        if len(download_url) <= 0:
            return
        r = requests.get(download_url)
        with open(self.file_name, "wb") as f:
            f.write(r.content)
            f.close()
        self._unzip_file(self.file_name, self.unzip_dir)

    def _sign(self, parameters):
        sorted_keys = sorted(parameters.keys())
        string_builder = ""
        for key in sorted_keys:
            if key in ["appKey", "format", "sign", "method", "timestamp"]:
                continue
            string_builder += f"{key}{self._common_parameter[key]}"
        return hashlib.md5(
            f"{string_builder}{self._secret}".encode(encoding="utf-8")
        ).hexdigest()

    def _generate_query_url(self, parameters):
        string_builder = ""
        for key, _ in parameters.items():
            string_builder += f"{key}={parameters[key]}&"
        return string_builder[0 : len(string_builder) - 1]

    def _unzip_file(self, zip_src, dst_dir):
        r = zipfile.is_zipfile(zip_src)
        if r:
            fz = zipfile.ZipFile(zip_src, "r")
            for file in fz.namelist():
                fz.extract(file, dst_dir)
        else:
            Print.error("This is not zip")
