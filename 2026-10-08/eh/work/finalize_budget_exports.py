from pathlib import Path
p=Path('outputs/보나센_원가계산기.html');s=p.read_text(encoding='utf-8')
s=s.replace('renderForecastSales(s);const totals=calculate(s);', 'renderForecastSales(s);const totals=calculate(costBasis(s));')
s=s.replace("<td class=\"note\">누계 자동 연동</td>", "<td class=\"note\">누계 자동 연동 ${s.sales.findIndex(v=>v.id===r.id)>=0?orderButtons('sales',s.sales.findIndex(v=>v.id===r.id),s.sales.length):''}</td>")
a=s.index("$('csv').onclick=");b=s.index("$('refreshMonthBudget').onclick=",a)
block=s[a:b]
block=block.replace('fixedTotals(state)', 'fixedTotals(basis)')
block=block.replace("[],['항목','기간 총액','판매 제품 개당']", "[],['월 전체 원가·지출예산','확정 금액'],...(state.ledger.view==='actual'?budgetKeys.map((k,i)=>[budgetNames[i],basis.monthCostBudget[k]]):[]),[],['항목','기간 총액','판매 제품 개당']")
block=block.replace('...state.sales.map(r=>', '...reportingSales(state).map(r=>')
block=block.replace('const b=r.price+r.shippingIncome-r.units*c.unit-r.price*r.fee/100-r.ship-r.pack;', "const b=state.ledger.view==='actual'&&c.sold?r.price+r.shippingIncome-r.units*(c.cogs+c.fee+c.ship+c.pack)/c.sold:r.price+r.shippingIncome-r.units*c.unit-r.price*r.fee/100-r.ship-r.pack;")
s=s[:a]+block+s[b:]
p.write_text(s,encoding='utf-8')
