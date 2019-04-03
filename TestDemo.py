import hashlib
import os
import shutil

from helper import Helper




def _download_obb(obbname, basic_dir, apk_details, pkgname):
    md5_pkgname = hashlib.md5((pkgname).encode('utf-8')).hexdigest()
    apk_path = basic_dir + md5_pkgname + ".apk"
    app_path = basic_dir + md5_pkgname + "/"
    obb_path_temp = app_path + obbname
    if os.path.exists(basic_dir + obbname):
        os.system("rm {}".format(basic_dir + obbname))
    shutil.move(obb_path_temp, basic_dir)
    obbpath = basic_dir + obbname
    tpkpath = _compose_tpk(apk_details, apk_path, obbpath, basic_dir, pkgname)
    os.system("rm -rf {}".format(app_path))

def _compose_tpk(self, apk_details, apkpath, obbpath, basic_dir, pkgname):
    dict_tpk = Helper.configinfo(apk_details, apkpath)
    Helper.build_tpk(basic_dir, obbpath, pkgname, dict_tpk)
    md5_pkgname = hashlib.md5((pkgname).encode('utf-8')).hexdigest()
    tpkpath = basic_dir + md5_pkgname + ".tpk"
    return tpkpath