from pathlib import Path
p=Path('outputs/보나센_원가계산기.html');s=p.read_text(encoding='utf-8')
def change(old,new):
 global s
 if old not in s: raise RuntimeError('Missing '+old[:100])
 s=s.replace(old,new)
change('<p class="note" id="fixedSummary"></p>', '<p class="note" id="fixedSummary"></p><div class="two"><div class="card"><small>고정비 차감 후 기간 운영 순이익</small><strong id="operatingProfit">—</strong><em>기간 비교이익 − 기간 고정비</em></div><div class="card"><small id="monthlyProfitLabel">월 운영 순이익</small><strong id="monthlyProfit">—</strong><em id="operatingNote">부가세 정산·법인세 반영 전</em></div></div>')
change('사업 운영비를 별도로 확인하는 표입니다.', '아래 운영 순이익에서는 고정비를 차감합니다. 여러 달 선택 시 월평균 순이익을 표시합니다.')
change('월 고정비 표의 금액은 제품 원가와 모든 비교이익에서 제외하며 별도 비용으로만 표시합니다.', '월 고정비는 제품 원가·묶음별 비교이익에서 제외합니다. 기간 운영 순이익 = 기간 비교이익 − 월 고정비 × 개월수. 월평균 운영 순이익 = 기간 운영 순이익 ÷ 개월수. 부가세 정산·법인세 반영 전이며 월별 실제 손익은 기간별로 따로 입력해 확인하세요.')
change("version:1,period:'',", "version:1,costOrder:Array.from({length:13},(_,i)=>i),period:'',")
change('if(v&&v.version===1&&v.fixed===undefined)v.fixed=d.fixed;', 'if(v&&v.version===1&&v.fixed===undefined)v.fixed=d.fixed;if(v&&v.version===1&&v.costOrder===undefined)v.costOrder=d.costOrder;')
change("throw Error('고정비는 0 이상의 숫자로 입력하세요.');return v;", "throw Error('고정비는 0 이상의 숫자로 입력하세요.');if(!Array.isArray(v.costOrder)||v.costOrder.length!==13||new Set(v.costOrder).size!==13||v.costOrder.some(i=>!Number.isInteger(i)||i<0||i>12))throw Error('원가표 순서 형식 오류');return v;")
change("function input(value,k,group,i,extra='')", """function operatingTotals(s){const c=calculate(s),f=fixedTotals(s),period=c.profit-f.period;return{period,monthly:period/s.months};}
function moveRow(s,group,index,direction){if(!['sales','ads','admin','fixed','costOrder'].includes(group)||!Number.isInteger(index)||![1,-1].includes(direction))return false;const rows=s[group],next=index+direction;if(index<0||index>=rows.length||next<0||next>=rows.length)return false;[rows[index],rows[next]]=[rows[next],rows[index]];return true;}
function orderButtons(group,i,length){return `<span class="order-controls"><button data-move="${group}" data-index="${i}" data-direction="-1" ${i===0?'disabled':''} aria-label="항목 위로 이동">↑</button> <button data-move="${group}" data-index="${i}" data-direction="1" ${i===length-1?'disabled':''} aria-label="항목 아래로 이동">↓</button></span>`;}
function input(value,k,group,i,extra='')""")
change('<td><button data-remove="sales"', '<td>${orderButtons(\'sales\',i,state.sales.length)} <button data-remove="sales"')
change('<td><button data-remove="${group}"', '<td>${orderButtons(group,i,state[group].length)} <button data-remove="${group}"')
change('<td><button data-remove="fixed"', '<td>${orderButtons(\'fixed\',i,state.fixed.length)} <button data-remove="fixed"')
change("['비교이익',c.profit]];}", "['비교이익',c.profit]].filter((r,i)=>i>=0).map((r,i,all)=>all[state.costOrder[i]]);}")
change(".filter((r,i)=>i>=0).map((r,i,all)", ".map((r,i,all)")
change('costRows(c).map(([n,v])=>`<tr><td>${n}</td>', 'costRows(c).map(([n,v],i)=>`<tr><td>${n} ${orderButtons(\'costOrder\',i,state.costOrder.length)}</td>')
change("$('bundles').innerHTML=state.sales.map(r=>", "$('bundles').innerHTML=state.sales.map((r,i)=>")
change('<tr><td>${r.units}개 구성</td>', '<tr><td>${r.units}개 구성 ${orderButtons(\'sales\',i,state.sales.length)}</td>')
change("$('fixedSummary').textContent='입력값을 확인하세요.';", "$('fixedSummary').textContent='입력값을 확인하세요.';$('operatingProfit').textContent='—';$('monthlyProfit').textContent='—';")
change("const fixed=fixedTotals(state);", "const fixed=fixedTotals(state),operating=operatingTotals(state);$('operatingProfit').textContent=money(operating.period)+' 원';$('monthlyProfit').textContent=money(operating.monthly)+' 원';$('operatingProfit').className=operating.period<0?'negative':'positive';$('monthlyProfit').className=operating.monthly<0?'negative':'positive';$('monthlyProfitLabel').textContent=state.months===1?'월 운영 순이익':'월평균 운영 순이익';$('operatingNote').textContent=(state.months>1?'기간 순이익 ÷ '+state.months+'개월 · ':'')+'부가세 정산·법인세 반영 전';")
change("document.addEventListener('click',e=>{const b=e.target.closest('[data-remove]');", "document.addEventListener('click',e=>{const m=e.target.closest('[data-move]');if(m){if(moveRow(state,m.dataset.move,Number(m.dataset.index),Number(m.dataset.direction)))render();return;}const b=e.target.closest('[data-remove]');")
change("['고정비 합계',fixedTotals(state).monthly,fixedTotals(state).period],", "['고정비 합계',fixedTotals(state).monthly,fixedTotals(state).period],['고정비 차감 후 기간 운영 순이익','',operatingTotals(state).period],[state.months===1?'월 운영 순이익':'월평균 운영 순이익',operatingTotals(state).monthly,''],")
change('button.primary{', 'button:disabled{opacity:.35;cursor:default}.order-controls{display:inline-flex;gap:3px;margin-left:6px}.order-controls button{padding:5px 9px}button.primary{')
change('입력값은 이 브라우저의 이 파일에 자동 저장됩니다.', '각 표의 ↑·↓ 버튼으로 항목 순서를 변경할 수 있습니다. 입력값과 항목 순서는 이 브라우저의 이 파일에 자동 저장됩니다.')
p.write_text(s,encoding='utf-8');print('Updated all item tables: reordering and separate fixed-cost-adjusted operating profit')
