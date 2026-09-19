p = 'index.html'
s = open(p, encoding='utf-8').read()
a = "  if(ios){txt.innerHTML="
b = "  new MutationObserver(function(){box.style.visibility=document.getElementById('menu').hidden?'hidden':''}).observe(document.getElementById('menu'),{attributes:true});\n" + a
assert s.count(a) == 1
s = s.replace(a, b, 1)
open(p, 'w', encoding='utf-8').write(s)
