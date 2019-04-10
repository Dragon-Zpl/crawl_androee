import os
from utils.init import PKGSTORE

if not os.path.exists(PKGSTORE):
    os.makedirs(PKGSTORE)