c = "https://www.androeed.ru"
a = "/index.php?m=' +ur+ 'f=images_while&id=24492&youtube=oxO1XF2Lyfg"

b = a.split('&')
print(b[-1])
print(b[-2])
print(c+"/index.php?m=files&f=images_while&"+b[-2]+"&"+b[-1])