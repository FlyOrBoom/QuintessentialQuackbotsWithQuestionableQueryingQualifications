import re

print(
''.join(list(map(
	lambda x:'\033[48:5:'+str(int(x)*255//99)+'m1',
        re.findall('..',str(703413075516325918))
)))
)
