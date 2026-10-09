from pathlib import Path
p=Path('outputs/보나센_원가계산기.html');s=p.read_text(encoding='utf-8')
s=s.replace('<div id="dashMix"', '<progress id="dashProgress" max="100" value="0" style="width:100%;height:16px;accent-color:#21b1bf;margin-top:16px" aria-label="월 매출목표 달성률"></progress><div id="dashMix"')
s=s.replace('<h2>6. 원가표와 손익</h2>', '<h3>누적 원가와 세트별 손익</h3>')
s=s.replace('<div class="notice" id="expectedRevenueHeadline"></div>', '<div class="notice" id="expectedRevenueHeadline"></div><button id="useExpectedTarget">예상매출을 월 목표로 적용</button>')
s=s.replace("$('dashRate').textContent=pct(g.ratio);", "$('dashRate').textContent=pct(g.ratio);$('dashProgress').value=g.ratio===null?0:Math.min(100,g.ratio*100);$('dashProgress').setAttribute('aria-valuetext',g.ratio===null?'목표 미입력':pct(g.ratio));")
s=s.replace("$('expectedRevenueHeadline').textContent=", "$('useExpectedTarget').disabled=!s.ledger.month;$('expectedRevenueHeadline').textContent=")
marker='function renderDashboard(s)'
functions="""function syncSelectedBudget(keys){if(!state.ledger.month)return;const source=initialMonthBudget(state,state.ledger.month),selected=monthlyBudget(state,state.ledger.month);for(const key of keys)selected[key]=source[key];}
"""
s=s.replace(marker,functions+marker)
s=s.replace("state.sales[index][key]=value;}render();", "state.sales[index][key]=value;}if(key==='monthlyOrders')syncSelectedBudget(['fee','ship','pack']);else if(key==='price'||key==='fee')syncSelectedBudget(['fee']);else if(key==='ship'||key==='pack')syncSelectedBudget([key]);render();")
s=s.replace("r[k]=el.type==='checkbox'?el.checked:k==='name'||k==='cycle'?el.value:Number(el.value);update();", "r[k]=el.type==='checkbox'?el.checked:k==='name'||k==='cycle'?el.value:Number(el.value);if(el.dataset.group==='ads')syncSelectedBudget(['ad']);if(el.dataset.group==='admin')syncSelectedBudget(['admin']);if(el.dataset.group==='fixed')syncSelectedBudget(['fixed']);update();")
s=s.replace("$('vendor').value='custom';}update();", "$('vendor').value='custom';}if(el.id.startsWith('review'))syncSelectedBudget(['ad']);update();")
s=s.replace("$('ledgerDay').onchange=", "$('useExpectedTarget').onclick=()=>{if(!state.ledger.month)return;const plan=calculate({...state,monthCostBudget:undefined,months:1,sales:state.sales.map(r=>({...r,orders:r.orders/state.months}))});ensureLedgerYear(state).targets[state.ledger.month-1]=plan.income;update();};$('ledgerDay').onchange=")
s=s.replace('再設定', '재설정')
# Labels explain that the primary tables now update the selected monthly budget.
s=s.replace('이후 기본설정 변경으로 자동 바뀌지 않습니다.', '일매출 입력으로 바뀌지 않습니다. 광고·관리비·고정비 표의 금액을 수정하면 선택한 월 예산에 반영됩니다.')
p.write_text(s,encoding='utf-8')
print('Dashboard progress, forecast-to-goal action, selected-month cost updates and concise detail labels completed')
