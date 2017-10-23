from urllib import parse

#这个是js的结果
# encodeURIComponent('中国')
# "%E4%B8%AD%E5%9B%BD"
jsRet='%E4%B8%AD%E5%9B%BD'
print(parse.unquote(jsRet))       #输出：中国
print(jsRet==parse.quote('中国'))  #输出：True

print(parse.quote('MTUwMjQyNDI4NA=='))
'MTUwMjQyODQ0NQ%3D%3D'
'MTUwMjQyNDU4Nw%3D%3D'
