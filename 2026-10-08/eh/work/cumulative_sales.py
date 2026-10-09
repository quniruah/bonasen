from pathlib import Path
p=Path('outputs/보나센_원가계산기.html');s=p.read_text(encoding='utf-8')
def change(a,b):
 global s
 if a not in s: raise RuntimeError('Missing '+a[:100])
 s=s.replace(a,b)
change('<label>선택일 매출목표 (원)', '<label hidden>선택일 매출목표 (원)')
change('<label>일 목표 설정', '<label hidden>일 목표 설정')
change('<label>확인할 날짜', '<label>월 누계 기준일')
change('선택한 날짜의 일매출과 일 목표로 달성률을 계산합니다. 일 목표 기본값은 월 목표 ÷ 해당 월의 날짜 수이며 날짜별로 수정할 수 있습니다. 일 목표를 수정해도 월 목표는 유지됩니다.', '월 1일부터 기준일까지 입력된 누적 매출을 월 전체 목표와 비교합니다. 기준일 이후에 입력된 매출은 누계 그래프와 위쪽 원가·손익에서 제외됩니다.')
change('월 탭의 매출·목표 막대는 선택일 기준이며, 비용·이익 막대는 월 누계 기준입니다.', '월 탭의 매출 막대는 기준일까지의 누적 매출, 목표 막대는 월 전체 목표입니다. 월 광고·관리·고정비는 그대로 유지합니다.')
change('<th class="num">일 목표</th><th class="num">일 달성률</th>', '<th class="num">월 누적 매출</th><th class="num">월 목표 달성률</th>')
change("const g=dailyRevenueTarget(s,date);$('dailyGoal-'+date).textContent=g.target>0||Object.hasOwn(y.dailyTargets,date)?money(g.target):'—';$('dailyRate-'+date).textContent=g.recorded?pct(g.ratio):'미입력';", "const g=cumulativeRevenueTarget(s,date);$('dailyGoal-'+date).textContent=money(g.actual);$('dailyRate-'+date).textContent=pct(g.ratio);")
change("sales:ledgerItems(s,month)", "sales:cumulativeLedgerItems(s)")
change('function ledgerColumns(s)', '''function cumulativeLedgerItems(s,date=s.ledger.month?selectedLedgerDate(s):null){return ledgerItems(s,s.ledger.month).filter(r=>!date||r.date<=date);}
function cumulativeRevenueTarget(s,date=selectedLedgerDate(s)){const month=Number(date.slice(5,7)),y=ensureLedgerYear(s),actual=dailyTotals(ledgerItems(s,month).filter(r=>r.date<=date)).income,target=y.targets[month-1];return{date,actual,target,ratio:target>0?actual/target:null,remaining:target>0?Math.max(0,target-actual):null,recorded:ledgerItems(s,month).some(r=>r.date<=date)};}
function costBasis(s){return s.ledger.view==='actual'?ledgerGraphState(s):s;}
function reportingSales(s){if(s.ledger.view!=='actual')return s.sales;const groups=new Map();for(const r of cumulativeLedgerItems(s)){const key=[r.id,r.units,r.price,r.fee,r.ship,r.pack,r.shippingIncome].join('|');if(!groups.has(key))groups.set(key,{...r,orders:0});groups.get(key).orders+=r.orders;}const list=[...groups.values()];for(const r of s.sales)if(!list.some(v=>v.id===r.id))list.push({...r,orders:0});list.sort((a,b)=>{const ai=s.sales.findIndex(r=>r.id===a.id),bi=s.sales.findIndex(r=>r.id===b.id);return (ai<0?9999:ai)-(bi<0?9999:bi);});return list;}
function renderSalesReport(s){if(s.ledger.view!=='actual')return;const rows=reportingSales(s);$('sales').innerHTML=rows.map(r=>`<tr>${['units','price','orders','fee','ship','pack','shippingIncome'].map(k=>`<td class="num">${money(r[k])}${k==='units'?'개':k==='orders'?'세트':''}</td>`).join('')}<td class="note">누계 자동 연동</td></tr>`).join('');$('salesModeNote').textContent=s.ledger.year+'년 '+(s.ledger.month?s.ledger.month+'월 1일~'+Math.min(s.ledger.day,daysInMonth(s.ledger.year,s.ledger.month))+'일':'연간')+' 일매출 누계 기준입니다. 판매단가가 바뀐 기록은 단가별로 나누어 표시합니다. 판매가·배송비 설정 또는 예측 주문수를 수정하려면 그래프 기준을 판매계획 예측으로 변경하세요.';}
function ledgerColumns(s)''')
change('<h2>2. 묶음별 판매계획과 배송·판매비</h2>', '<h2>2. 묶음별 판매수량과 배송·판매비</h2><p id="salesModeNote" class="notice"></p>')
change('goal=dailyMode?dailyRevenueTarget(s)', 'goal=dailyMode?cumulativeRevenueTarget(s)')
change("label:'선택일 매출목표'", "label:'월 전체 매출목표'")
change("label:'선택일 매출'", "label:'기준일까지 월 누적 매출'")
change("dailyMode&&!goal.recorded?'선택일 매출이 미입력입니다. 일 목표 '+money(goal.target)+'원 · 날짜별 판매 세트수를 입력하세요.':", '')
change("dailyMode?'일 매출':'목표 매출'", "dailyMode?'월 누적 매출':'목표 매출'")
change("dailyMode?'선택일 목표':'기간 목표'", "dailyMode?'월 전체 목표':'기간 목표'")
change("goal.date+' · 매출·목표는 선택일 기준 / 비용·이익은 해당 월 누계 기준'", "goal.date+'까지 월 누적 매출 · 목표는 월 전체 목표 / 광고·관리·고정비는 월 비용 유지'")
change('function update(){let c;try{validate(state);c=calculate(state);', 'function update(){let c,basis;try{validate(state);basis=costBasis(state);c=calculate(basis);')
start=s.index('function update()');end=s.index("\ndocument.addEventListener('input'",start)
block=s[start:end]
block=block.replace('fixedTotals(state)','fixedTotals(basis)').replace('operatingTotals(state)','operatingTotals(basis)').replace('state.months','basis.months').replace('state.reviewEnabled?','basis.reviewEnabled?')
block=block.replace('state.sales.map((r,i)=>','reportingSales(state).map((r,i)=>')
block=block.replace("${orderButtons('sales',i,state.sales.length)}", "${state.ledger.view==='actual'?'':orderButtons('sales',i,state.sales.length)}")
block=block.replace("renderTotals(c);renderChart(state);", "renderTotals(c,basis);renderSalesReport(state);renderChart(state);")
block=block.replace("for(const group of ['ads','admin'])state[group].forEach((r,i)=>$(`${group}-${i}`).textContent=money(c.cost(r)));", "for(const group of ['ads','admin'])basis[group].forEach((r,i)=>$(`${group}-${i}`).textContent=money(c.cost(r)));if(state.ledger.view==='plan')$('salesModeNote').textContent='판매계획 예측 기준입니다. 판매 주문수를 직접 수정할 수 있습니다.';")
s=s[:start]+block+s[end:]
change('function renderTotals(c){const f=fixedTotals(state),op=operatingTotals(state);', 'function renderTotals(c,basis=costBasis(state)){const f=fixedTotals(basis),op=operatingTotals(basis);')
change('state[g].reduce((a,r)=>a+c.cost(r),0)', 'basis[g].reduce((a,r)=>a+c.cost(r),0)')
change("c.monthlyAd*state.months", "c.monthlyAd*costBasis(state).months")
change("const c=calculate(state),rows=[['보나센 원가표'", "const basis=costBasis(state),c=calculate(basis),rows=[['보나센 원가표'")
# Original current sales are preserved as the independent forecast; actual sales are derived from the ledger.
change("render();\n</script>", "render();\n</script>")
change("$('ledgerView').onchange=()=>{state.ledger.view=$('ledgerView').value;update();}", "$('ledgerView').onchange=()=>{state.ledger.view=$('ledgerView').value;render();}")
change("['날짜','일 목표 매출','일 실제 매출','일 달성률']", "['날짜','월 전체 목표','当日 매출'.replace('当日','일'),'월 누적 매출','월 목표 달성률']")
change("g=dailyRevenueTarget(state,date);return[date,g.target,g.recorded?g.actual:'미입력',g.recorded?(g.ratio===null?'목표 미입력':pct(g.ratio)):'미입력'];", "day=dailyRevenueTarget(state,date),g=cumulativeRevenueTarget(state,date);return[date,g.target,day.recorded?day.actual:'미입력',g.actual,g.ratio===null?'목표 미입력':pct(g.ratio)];")
s=s.replace("'当日 매출'.replace('当日','일')", "'일 매출'")
p.write_text(s,encoding='utf-8');print('Month-to-date revenue vs full monthly target; same cumulative quantities and historical sales prices feed upper costing and profits')
