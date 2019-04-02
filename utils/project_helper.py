import hashlib
import socket

import yaml


class ProjectHepler:
    with open('./config/config.yaml', 'r') as fr:
        config_file = yaml.load(fr)
    ip_config = config_file["ip_config"]

    @classmethod
    def get_ip(cls):
        s = None
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
        finally:
            s.close()
        return ip

    @classmethod
    def get_del_ip(cls):
        return "http://" + cls.get_ip() + ":5000"

    @classmethod
    def get_download_ip(cls, myhost):
        try:
            download_host = cls.ip_config["ip_to_host"][myhost]
        except:
            download_host = cls.get_ip()
        return download_host

    @classmethod
    def get_basic_path(cls, myhost):
        try:
            path = cls.ip_config["ip_to_filePath"][myhost]
        except:
            path = "./"
        return path

    @classmethod
    def Filemd5(cls, filepath):
        fp = open(filepath, 'rb')
        md5_obj = hashlib.md5()
        while True:
            tmp = fp.read(8096)
            if not tmp:
                break
            md5_obj.update(tmp)
        hash_code = md5_obj.hexdigest()
        fp.close()
        md5 = str(hash_code).lower()
        return md5


if __name__ == '__main__':
    print(ProjectHepler.get_ip())
