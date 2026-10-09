from pathlib import Path
p=Path('outputs/보나센_원가계산기.html');s=p.read_text(encoding='utf-8')
def change(a,b):
 global s
 if a not in s: raise RuntimeError('Missing '+a[:100])
 s=s.replace(a,b)
change("return [...state.costOrder.map(i=>all[i]),all[2],all[11],all[12]];", "if(state.ledger.view==='actual'){all[9]=['広告'.replace('広告','광고·마케팅 월 전체 예산 (리뷰 포함)'),c.ad];return [...state.costOrder.filter(i=>i!==7&&i!==8).map(i=>all[i]),all[2],all[11],all[12]];}return [...state.costOrder.map(i=>all[i]),all[2],all[11],all[12]];")
change("costRows(c).slice(10)", "costRows(c).slice(-3)")
change("costRows(c).slice(0,10)", "costRows(c).slice(0,-3)")
change("${orderButtons('costOrder',i,state.costOrder.length)}", "${state.ledger.view==='actual'?'':orderButtons('costOrder',i,state.costOrder.length)}")
change("const before=r.price+r.shippingIncome-r.units*c.unit-r.price*r.fee/100-r.ship-r.pack,a=", "const before=state.ledger.view==='actual'&&c.sold?r.price+r.shippingIncome-r.units*(c.cogs+c.fee+c.ship+c.pack)/c.sold:r.price+r.shippingIncome-r.units*c.unit-r.price*r.fee/100-r.ship-r.pack,a=")
change('광고·관리비는 판매 제품 개수에 비례하여 배부합니다.', '일매출 기록 기준에서는 월 전체 제품·판매·광고·관리비 예산을 기준일까지 누적 판매된 제품 개수에 비례해 나누어 부담시킵니다. 판매계획 예측 기준에서는 입력 단가로 계산합니다.')
# Append reconciliation against frozen budgets to the basic input schedules.
needle="const summary=[...costRows(c).slice(-3)"
replacement="""if(state.ledger.view==='actual'){const rawAds=basis.ads.reduce((sum,r)=>sum+c.cost(r),0)+c.review,rawAdmin=basis.admin.reduce((sum,r)=>sum+c.cost(r),0);$('adsSummary').innerHTML+=`<tr><td colspan="5">월 확정예산 조정액</td><td class="num">${money(c.ad-rawAds)}</td><td></td></tr><tr class="result"><td colspan="5">월 전체 광고·마케팅 예산</td><td class="num">${money(c.ad)}</td><td></td></tr>`;$('adminSummary').innerHTML+=`<tr><td colspan="5">월 확정예산 조정액</td><td class="num">${money(c.admin-rawAdmin)}</td><td></td></tr><tr class="result"><td colspan="5">월 전체 제품 관리비 예산</td><td class="num">${money(c.admin)}</td><td></td></tr>`;}
const summary=[...costRows(c).slice(-3)"""
change(needle,replacement)
change("${money(c.ad)}</td><td></td></tr>`;}", "${money(sum+c.review)}</td><td></td></tr>`;}")
change("['적용 개월',state.months],['월 목표 매출',state.monthlyTarget],['기간 목표 매출',revenueTarget(state).target],['목표 매출 달성률',revenueTarget(state).ratio===null?'목표 미입력':pct(revenueTarget(state).ratio)]", "['적용 개월',basis.months],['계산 기준',state.ledger.view==='actual'?state.ledger.year+'년 '+(state.ledger.month?state.ledger.month+'월 '+state.ledger.day+'일까지 누계':'연간'):'판매계획 예측'],['월 목표 매출',basis.monthlyTarget],['기간 목표 매출',revenueTarget(basis).target],['목표 매출 달성률',revenueTarget(basis).ratio===null?'목표 미입력':pct(revenueTarget(basis).ratio)]")
change("operatingTotals(state).period", "operatingTotals(costBasis(state)).period")
change("operatingTotals(state).monthly", "operatingTotals(costBasis(state)).monthly")
s=s.replace("'広告'.replace('広告','광고·마케팅 월 전체 예산 (리뷰 포함)')", "'광고·마케팅 월 전체 예산 (리뷰 포함)'")
p.write_text(s,encoding='utf-8')
