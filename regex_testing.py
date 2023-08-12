import re

string = "hello"

p = re.compile("hel*")

print(p.match(string).group())
