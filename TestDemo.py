a = 'FR LEGENDS [Mod Money]'

import re


b = re.search("\[[\d\D]+?\]",a)
print(b.group().replace('[','').replace(']',''))