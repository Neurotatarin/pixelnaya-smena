import io
p='sw.js'
s=io.open(p,encoding='utf-8').read().replace("smena-v4","smena-v5",1)
io.open(p,'w',encoding='utf-8').write(s)
print('OK cache bumped')
