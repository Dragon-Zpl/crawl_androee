import re
name = ['REKT High Octane Stunts [Mod: Unlocked + Money]']
if name and '[' in name:
    a = re.search(r'[\d\D]*\[', name[0]).group().replace(' [', "")
elif name:
    a = name[0]

print(a)