import re

a = "/files/to_market/24359.php"

b = re.search('\d+',a)
print(b.group())