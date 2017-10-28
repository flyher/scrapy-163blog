

import re
# str='http://dwmahonggang.blog.163.com/?fromBlogger'
# pattern = re.compile(r'http://(.+)\.blog\.163.com')
# print pattern.search(str).group(1)
str="http://dwmahonggang.blog.163.com/blog/static/16545562220167192445857/"
a=re.compile('\d+')
print a.findall(str)[1][:9]