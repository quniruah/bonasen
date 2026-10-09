from pathlib import Path
p=Path('outputs/보나센_원가계산기.html')
s=p.read_text(encoding='utf-8')
a=s.index('function update()')
b=s.index('const goal=revenueTarget(s);',a)
e=s.index("$('chartPeriod').textContent='';",b)
s=s[:b]+s[e:]
p.write_text(s,encoding='utf-8')
