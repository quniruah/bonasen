from pathlib import Path
p=Path('outputs/보나센_원가계산기.html');s=p.read_text(encoding='utf-8')
s=s.replace('일 목표 기본값은 월 목표 ÷ 해당 월의 날짜 수이며 날짜별로 수정할 수 있습니다.', '일 목표 기본값은 월 목표 ÷ 해당 월의 날짜 수이며 날짜별로 수정할 수 있습니다. 일 목표를 수정해도 월 목표는 유지됩니다.')
a=s.index('function exportLedgerCsv()')
b=s.index('})];download',a)
s=s[:b]+s[b:].replace("})];download", "}),[],['날짜','일 목표 매출','일 실제 매출','일 달성률'],...Array.from({length:12},(_,m)=>Array.from({length:daysInMonth(year,m+1)},(_,d)=>{const date=year+'-'+String(m+1).padStart(2,'0')+'-'+String(d+1).padStart(2,'0'),g=dailyRevenueTarget(state,date);return[date,g.target,g.recorded?g.actual:'미입력',g.recorded?(g.ratio===null?'목표 미입력':pct(g.ratio)):'미입력'];})).flat()];download",1)
p.write_text(s,encoding='utf-8')
