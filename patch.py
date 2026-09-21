import io,subprocess,hashlib
SHA='371661f5f0323cf481bd5bc44bda655683beb928'
subprocess.run(['git','fetch','--depth','1','origin',SHA],check=True)
data=subprocess.run(['git','show',SHA+':index.html'],check=True,capture_output=True).stdout
if hashlib.sha256(data).hexdigest()[:16]!='74a4bdd9abaf5801':
    raise SystemExit('unexpected index.html from '+SHA)
open('index.html','wb').write(data)
w=io.open('sw.js',encoding='utf-8').read().replace("const CACHE = 'smena-v5';","const CACHE = 'smena-v6';",1)
io.open('sw.js','w',encoding='utf-8').write(w)
print('OK rolled back to v7 rules, cache v6')
