from html.parser import HTMLParser
from html import escape
from pathlib import Path
class Node:
 def __init__(self,tag=None,attrs=(),text=''):self.tag=tag;self.attrs=dict(attrs);self.children=[];self.parent=None;self.text=text
 def add(self,n):
  if n.parent:n.parent.children.remove(n)
  n.parent=self;self.children.append(n);return n
 def remove(self):
  if self.parent:self.parent.children.remove(self);self.parent=None
 def html(self):
  if not self.tag:return self.text
  a=''.join(' '+k+('="'+escape(v,quote=True)+'"' if v is not None else '') for k,v in self.attrs.items())
  if self.tag in void:return '<'+self.tag+a+'>'
  return '<'+self.tag+a+'>'+''.join(n.html() for n in self.children)+'</'+self.tag+'>'
 def find(self,test):
  if test(self):return self
  for n in self.children:
   found=n.find(test)
   if found:return found
 def plain(self):return self.text if not self.tag else ''.join(n.plain() for n in self.children)
void={'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}
class Parser(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=False);self.root=Node('root');self.stack=[self.root]
 def handle_starttag(self,t,a):
  n=self.stack[-1].add(Node(t,a))
  if t not in void:self.stack.append(n)
 def handle_endtag(self,t):
  for i in range(len(self.stack)-1,0,-1):
   if self.stack[i].tag==t:self.stack=self.stack[:i];break
 def handle_data(self,d):self.stack[-1].add(Node(text=d))
 def handle_entityref(self,n):self.handle_data('&'+n+';')
 def handle_charref(self,n):self.handle_data('&#'+n+';')
def fragment(text):
 q=Parser();q.feed(text);return q.root.children[:]
def append(n,html):
 for c in fragment(html):n.add(c)
def replace_text(n,text):n.children=[];n.add(Node(text=text))
p=Path('outputs/보나센_원가계산기.html');old=p.read_text(encoding='utf-8');q=Parser();q.feed(old);root=q.root
get=lambda id:root.find(lambda n:n.attrs.get('id')==id)
main=root.find(lambda n:n.tag=='main');sections=[n for n in main.children if n.tag=='section']
criteria,product,sales,ads,admin,fixed,costs,journal,notes=sections
for n,text in [(product,'1. 제품원가표'),(ads,'2. 광고·마케팅 비용'),(fixed,'3. 월 관리비·고정경비'),(journal,'4. 월 예상매출과 일일 누계 달성현황')]:replace_text(n.find(lambda c:c.tag=='h2'),text)
toolbar=main.find(lambda n:n.attrs.get('class')=='toolbar');status=get('status');warnings=get('warnings')
dashboard=Node('section',[('class','dashboard'),('aria-labelledby','dashboardTitle')])
append(dashboard,'<h2 id="dashboardTitle">보나센 매출 대시보드</h2><div class="grid" id="dashboardControls"></div>')
controls=dashboard.find(lambda n:n.attrs.get('id')=='dashboardControls')
for id in ['ledgerYear','ledgerDay']:controls.add(get(id).parent)
append(controls,'<label>선택 월 목표 매출 (원)<input id="dashboardTarget" type="number" min="0" step="any"></label><div class="note" style="align-self:center" id="dashboardPeriod"></div>')
dashboard.add(get('monthTabs'))
append(dashboard,'<div class="cards dashboard-cards"><div class="card"><small>월 목표 매출</small><strong id="dashGoal">—</strong></div><div class="card"><small>기준일까지 누적 매출</small><strong id="dashRevenue">—</strong></div><div class="card"><small>목표 달성률</small><strong id="dashRate">—</strong></div><div class="card"><small>목표까지 남은 매출</small><strong id="dashRemaining">—</strong></div><div class="card"><small>누적 판매량</small><strong id="dashSets">—</strong><em id="dashUnits"></em></div><div class="card"><small>고정비 차감 후 이익</small><strong id="profit">—</strong><em id="margin"></em></div></div><div id="dashMix" class="legend"></div><p class="note">매출은 월 1일부터 기준일까지 누계, 목표는 월 전체 목표입니다. 제조원가는 개당 단가 × 누적 판매 제품수로 계산하며 나머지 월 경비는 예산을 적용합니다.</p>')
# Retain one authoritative input per setting; old fields needed for older backups stay hidden.
hidden=Node('div',[('hidden',None),('id','legacyFields')]);main.add(hidden)
for id in ['period','months']:
 hidden.add(get(id).parent)
criteria.find(lambda n:n.tag=='h2').remove()
for n in criteria.children[:]:product.add(n)
criteria.remove()
oldcards=get('unit').parent.parent
for id in ['unit','adTotal','cash','operatingProfit','monthlyProfit','monthlyProfitLabel','operatingNote','fixedSummary','forecastUnitCost','forecastMonths','forecastFullCost','monthlyTarget','ledgerView','ledgerTarget','ledgerDailyTarget','resetDailyTarget']:
 n=get(id)
 if n:hidden.add(n)
oldcards.remove()
product.add(Node('div',[('class','notice'),('id','manufacturingUnitHeadline')]))
sales.attrs['hidden']=None;hidden.add(sales)
# Ads: recurring spend is primary; review settings are one-time advanced detail.
reviewHeading=ads.find(lambda n:n.tag=='h3')
if reviewHeading:
 idx=ads.children.index(reviewHeading);review=Node('details');append(review,'<summary>리뷰작업 비용 (1회성)</summary>')
 for n in ads.children[idx:]:review.add(n)
 ads.add(review)
get('adSchedule').attrs['class']='note'
# Fixed expenses have one section, with administration and cost budget grouped below.
for n in fixed.children[:]:
 if n.tag=='div' and n.attrs.get('class')=='two':n.remove()
for n in admin.children[:]:
 if n.tag=='h2':replace_text(n,'제품 관리비');n.tag='h3'
 fixed.add(n)
append(fixed,'<h3>선택 월 경비 합계</h3>')
budget=get('monthBudgetBody')
while budget.tag!='section':budget=budget.parent
replace_text(budget.find(lambda n:n.tag=='h3'),'월 경비 예산 확인·조정')
budgetDetails=Node('details');append(budgetDetails,'<summary>월 경비 예산 확인·조정</summary>');budgetDetails.add(budget);fixed.add(budgetDetails)
append(fixed,'<div class="notice" id="fixedExpenseHeadline"></div>')
# Remove startup-oriented notices and duplicated control grids in the journal.
journalGrid=journal.find(lambda n:n.attrs.get('class')=='grid')
for id in ['ledgerOnceYear','ledgerOnceMonth']:
 n=get(id)
 if n:
  d=ads.find(lambda n:n.tag=='details');d.add(n.parent)
if journalGrid:journalGrid.remove()
forecast=get('forecastSales')
while forecast.tag!='details':forecast=forecast.parent
forecast.find(lambda n:n.tag=='summary').remove()
for n in forecast.children[:]:
 if n.tag=='div' and n.attrs.get('class')=='grid':n.remove()
 if n.tag=='p' and n.attrs.get('class')=='note':replace_text(n,'세트별 월 예상 판매수량과 판매가·배송비를 설정합니다. 일매출 실적은 아래에서 별도로 기록하며 예측 수량을 덮어쓰지 않습니다.')
forecast.tag='div'
append(journal,'<div id="predictionMount"></div>')
mount=get('predictionMount');append(mount,'<h3>세트별 월 예상매출</h3>');mount.add(forecast)
append(mount,'<div class="notice" id="expectedRevenueHeadline"></div>')
for n in list(journal.children):
 if n is mount:journal.children.remove(n);journal.children.insert(1,n)
panel=get('ledgerPanel')
annual=Node('details');append(annual,'<summary>월별·연간 매출 요약</summary>')
heading=panel.find(lambda n:n.tag=='h3' and n.plain()=='월별 매출 요약')
annual.add(heading);annualTable=get('annualSummary')
while annualTable.tag!='div':annualTable=annualTable.parent
annual.add(annualTable);panel.add(annual)
detail=Node('details');append(detail,'<summary>누적 원가·세트별 이익 상세</summary>');detail.add(costs);journal.add(detail)
# Leave source definitions as a compact single details block.
notes=sections[-1];notes.tag='section'
footer=main.find(lambda n:n.tag=='footer')
for n in main.children:n.parent=None
main.children=[]
for n in [toolbar,status,dashboard,warnings,product,ads,fixed,journal,notes,hidden,footer]:main.add(n)
style=root.find(lambda n:n.tag=='style');style.children[0].text+='\n.dashboard{background:#102e49;color:white;border-color:#102e49}.dashboard h2{font-size:24px}.dashboard .note,.dashboard label{color:#d6e4ed}.dashboard .card{color:#17283b}.dashboard-cards{grid-template-columns:repeat(3,1fr)}.dashboard .legend{margin-top:18px;color:#d6e4ed}.dashboard .month-tabs button{border-color:#7690a3}.dashboard input,.dashboard select{color:#17283b}.dashboard .card strong{font-size:27px}.dashboard details{color:#17283b}h3{margin-top:22px}details{margin:16px 0;padding:14px;border:1px solid #dbe4ed;border-radius:8px}details summary{font-size:15px}#predictionMount{margin-top:20px}@media(max-width:750px){.dashboard-cards{grid-template-columns:repeat(2,1fr)}}@media(max-width:480px){.dashboard-cards{grid-template-columns:1fr}}@media print{.dashboard{background:white;color:#17283b}.dashboard label,.dashboard .note{color:#52677b}}\n'
script=root.find(lambda n:n.tag=='script');js=script.children[0].text
js=js.replace("function renderChart(s){renderLedger(s);", "function renderChart(s){renderDashboard(s);renderLedger(s);")
js=js.replace("function input(value,k,group,i,extra=", '''function renderDashboard(s){const basis=costBasis(s),c=calculate(basis),g=revenueTarget(basis),net=operatingTotals(basis).period;$('dashGoal').textContent=money(g.target)+' 원';$('dashRevenue').textContent=money(g.actual)+' 원';$('dashRate').textContent=pct(g.ratio);$('dashRemaining').textContent=g.remaining===null?'목표를 입력하세요':money(g.remaining)+' 원';$('dashSets').textContent=money(c.orders)+' 세트';$('dashUnits').textContent='제품 '+money(c.sold)+'개';$('dashboardTarget').disabled=!s.ledger.month;$('dashboardTarget').value=s.ledger.month?ensureLedgerYear(s).targets[s.ledger.month-1]:g.target;$('dashboardPeriod').textContent=s.ledger.year+'년 '+(s.ledger.month?s.ledger.month+'월 '+s.ledger.day+'일까지 누계':'연간 누계');const rows=reportingSales(s),mix=new Map();for(const r of rows)mix.set(r.units,(mix.get(r.units)||0)+r.orders);$('dashMix').innerHTML=[...mix].map(([units,orders])=>`<span>${units}개 묶음 ${money(orders)}세트</span>`).join('');$('manufacturingUnitHeadline').textContent='개당 제조원가 '+money(c.unit)+'원 · 누적 판매 '+money(c.sold)+'개 · 판매 제품 제조원가 '+money(c.cogs)+'원';const b=combinedMonthBudget(s);$('fixedExpenseHeadline').textContent='월 제품 관리비 '+money(b.admin)+'원 + 월 고정비 '+money(b.fixed)+'원 = 총 고정경비 '+money(b.admin+b.fixed)+'원';const plan=calculate({...s,monthCostBudget:undefined,months:1,sales:s.sales.map(r=>({...r,orders:r.orders/s.months}))});$('expectedRevenueHeadline').textContent='월 예상 판매 '+money(plan.orders)+'세트 / 제품 '+money(plan.sold)+'개 · 월 예상매출 '+money(plan.income)+'원';}
function input(value,k,group,i,extra=''')
js=js.replace("const el=e.target;if(el.dataset.budgetKey", "const el=e.target;if(el.id==='dashboardTarget'){const n=Number(el.value);if(el.value!==''&&Number.isFinite(n)&&n>=0&&state.ledger.month){ensureLedgerYear(state).targets[state.ledger.month-1]=n;update();}return;}if(el.dataset.budgetKey")
js=js.replace("render();\n</script>","render();\n</script>")
js=js.replace("\nrender();\n", "\nstate.ledger.view='actual';render();\n")
script.children[0].text=js
p.write_text('<!doctype html>\n'+''.join(n.html() for n in root.children),encoding='utf-8')
print('Reorganized into dashboard, product costs, advertising, fixed overhead, and set-based forecasts/daily cumulative sales; preserved existing data model')
