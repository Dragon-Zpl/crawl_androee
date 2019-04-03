import re

a = """
('#images_while').load('/index.php?m=files&f=images_while&id=8525&youtube=9uXNn1AKon0" ')
"""

b = re.findall(r"load[\d\D]+?\" \'\)",a)[0].replace("load('","").replace("\" ')","")

print(b)