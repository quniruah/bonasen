from pathlib import Path
p=Path('outputs/보나센_원가계산기.html');s=p.read_text(encoding='utf-8')
def change(a,b):
 global s
 if a not in s: raise RuntimeError('Missing '+a[:90])
 s=s.replace(a,b)
change('total=b.cogs+b.fee+b.ship+b.pack+b.ad+b.admin', 'total=c.cogs+b.fee+b.ship+b.pack+b.ad+b.admin')
change('cogs:b.cogs,fee:b.fee', 'cogs:c.cogs,fee:b.fee')
start=s.index('function renderMonthBudget(s)');end=s.index('\nfunction costBasis(s)',start)
s=s[:start]+'''function renderMonthBudget(s){const b=combinedMonthBudget(s),c=calculate(ledgerGraphState(s)),active=document.activeElement,typing=active&&active.dataset&&active.dataset.budgetKey!==undefined;$('monthBudgetBody').innerHTML=typing?$('monthBudgetBody').innerHTML:budgetKeys.map((k,i)=>k==='cogs'?`<tr><td>누적 판매 제품 제조원가 (자동 계산)<span class="daily-amount" id="manufacturingCostFormula"></span></td><td class="num" id="actualManufacturingCost"></td></tr>`:`<tr><td>${budgetNames[i]}</td><td class="num"><input type="number" min="0" step="any" value="${b[k]}" data-budget-key="${k}" aria-label="${budgetNames[i]} 월 예산" ${s.ledger.month?'':'readonly'}></td></tr>`).join('');$('actualManufacturingCost').textContent=money(c.cogs);$('manufacturingCostFormula').textContent='개당 '+money(c.unit)+'원 × 누적 판매 제품 '+money(c.sold)+'개';$('monthBudgetTotal').textContent=money(c.total+b.fixed);$('refreshMonthBudget').disabled=!s.ledger.month;}
''' +s[end:]
change('월 비용은 일매출과 별도로 미리 설정하고 고정합니다. 누적 판매수량이 늘어나도 이 비용은 자동 증가하지 않습니다. 처음에는 위쪽 원가·판매계획·광고·관리비 설정을 가져옵니다. 판매계획이 0이면 제품원가 예산은 총 생산비로 시작하므로 해당 월 부담액으로 조정하세요.', '제품 제조원가는 위쪽 개당 제조단가 × 누적 판매 제품수로 자동 계산합니다. 광고·관리·고정비 등 나머지 비용은 월 전체 예산으로 설정하고 유지합니다. 총 생산비를 판매수량으로 나누어 제조단가를 바꾸지 않습니다.')
change('월 전체 원가·지출예산</h3>', '판매 제품 원가와 월 지출예산</h3>')
change('월 전체 예산 (원)</th>', '금액 (원)</th>')
change('월 지출 총계 (원가 포함)', '누적 제품원가 + 월 지출예산 합계')
change('월 예산은 자동 저장됩니다. 이후 위쪽 기본단가 변경은 확정한 월 예산에 자동 반영되지 않습니다.', '제품 제조원가는 위쪽 단가와 일일 누적 판매수량에 연동됩니다. 나머지 월 예산은 자동 저장되며, 이후 기본설정 변경으로 자동 바뀌지 않습니다.')
change('일매출 기준의 비용은 미리 설정한 월 전체 원가·지출예산이며, 이익은 그 예산을 차감한 값입니다.', '일매출 기준의 제품 제조원가는 개당 제조단가 × 누적 판매수량이며, 나머지 비용은 설정한 월 지출예산입니다. 이익은 누적 매출에서 이 비용을 차감합니다.')
change('budgetKeys.map((k,i)=>[budgetNames[i],basis.monthCostBudget[k]])', "budgetKeys.map((k,i)=>[k==='cogs'?'누적 판매 제품 제조원가':budgetNames[i],k==='cogs'?c.cogs:basis.monthCostBudget[k]])")
change("!budgetKeys.includes(k)||el.value", "(!budgetKeys.includes(k)||k==='cogs')||el.value")
p.write_text(s,encoding='utf-8');print('Manufacturing cost now uses actual unit cost times cumulative units; all other monthly budgets preserved')
