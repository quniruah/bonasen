from pathlib import Path
p=Path('outputs/보나센_원가계산기.html');s=p.read_text(encoding='utf-8')
def change(old,new):
 global s
 if old not in s: raise RuntimeError('Missing '+old[:100])
 s=s.replace(old,new)
for old,new in [('기간 총 비교이익','기간 이익 (고정비 차감 전)'),('고정비 차감 후 기간 운영 순이익','기간 이익 (고정비 차감 후)'),('건당 최종 비교이익','건당 이익 (고정비 차감 전)'),('월평균 운영 순이익','월평균 이익 (고정비 차감 후)'),('월 운영 순이익','월 이익 (고정비 차감 후)'),('기간 운영 순이익','기간 이익 (고정비 차감 후)'),('기간 순이익','기간 이익 (고정비 차감 후)'),('비교이익','고정비 차감 전 이익'),('운영 순이익','고정비 차감 후 이익'),('월평균 순이익','월평균 이익')]:
 s=s.replace(old,new)
change('tfoot{font-weight:700}', 'tfoot{font-weight:700}tfoot td{background:#e7f0f7;border-bottom:1px solid #c3d5e4}tfoot tr:first-child td{border-top:3px solid #416987}tfoot tr.result td{background:#d9eef1;font-size:16px}tfoot tr.final-result td{background:#143d58;color:white;font-size:17px}tfoot .negative{color:#b53928!important}tfoot .positive{color:#08747a!important}tfoot tr.final-result .negative{color:#ffc7b8!important}tfoot tr.final-result .positive{color:#b9f0e7!important}.result-label{font-size:12px;font-weight:600;display:block;margin-bottom:3px;color:inherit}')
for id in ['sales','ads','admin','bundles']:
 change(f'<tbody id="{id}"></tbody>',f'<tbody id="{id}"></tbody><tfoot id="{id}Summary"></tfoot>')
change('<tbody id="costs"></tbody>', '<tbody id="costs"></tbody><tfoot id="costSummary"></tfoot>')
change("costOrder:Array.from({length:13},(_,i)=>i)","costOrder:[0,1,3,4,5,6,7,8,9,10]")
change('if(v&&v.version===1&&v.costOrder===undefined)v.costOrder=d.costOrder;', 'if(v&&v.version===1&&v.costOrder===undefined)v.costOrder=d.costOrder;if(v&&Array.isArray(v.costOrder)&&v.costOrder.length===13)v.costOrder=v.costOrder.filter(i=>![2,11,12].includes(i));')
change('v.costOrder.length!==13||new Set(v.costOrder).size!==13||v.costOrder.some(i=>!Number.isInteger(i)||i<0||i>12)', 'v.costOrder.length!==10||new Set(v.costOrder).size!==10||v.costOrder.some(i=>!d.costOrder.includes(i))')
start=s.index('function costRows(c)');end=s.index('\nfunction update()',start)
s=s[:start]+'''function costRows(c){const all=[['제품 매출',c.revenue],['고객 부담 배송비 수입',c.shippingIncome],['매출 총계',c.income],['판매 제품 제조원가',c.cogs],['판매수수료',c.fee],['배송비',c.ship],['포장비',c.pack],['최초 1회 리뷰작업',c.review],['기타 1회 광고비',c.onceAd],['월 리워드·기타 광고비 (기간 합계)',c.monthlyAd*state.months],['제품 관리비',c.admin],['비용 총계 (고정비 제외)',c.total],['고정비 차감 전 이익',c.profit]];return [...state.costOrder.map(i=>all[i]),all[2],all[11],all[12]];}
function renderTotals(c){const f=fixedTotals(state),op=operatingTotals(state);$('salesSummary').innerHTML=`<tr><td colspan="2">판매계획 총계</td><td class="num">${money(c.orders)}건</td><td colspan="5">제품 ${money(c.sold)}개 · 제품 매출 ${money(c.revenue)}원 · 배송비 수입 ${money(c.shippingIncome)}원</td></tr>`;for(const g of ['ads','admin']){const sum=state[g].reduce((a,r)=>a+c.cost(r),0);$(g+'Summary').innerHTML=`<tr><td colspan="5">${g==='ads'?'리워드·기타 광고비 합계 (리뷰 제외)':'제품 관리비 합계'}</td><td class="num">${money(sum)}</td><td></td></tr>`;if(g==='ads')$('adsSummary').innerHTML+=`<tr><td colspan="5">최초 1회 리뷰비</td><td class="num">${money(c.review)}</td><td></td></tr><tr class="result"><td colspan="5">광고·마케팅 총계 (리뷰 포함)</td><td class="num">${money(c.ad)}</td><td></td></tr>`;}
const summary=[...costRows(c).slice(10).map(([name,value],i)=>[name,value,c.sold?value/c.sold:null,i===2?'result':'']),['월 고정비 (기간 합계)',f.period,null,''],['고정비 차감 후 이익',op.period,null,'final-result']];$('costSummary').innerHTML=summary.map(([name,value,unit,cls])=>`<tr class="${cls}"><td>${cls?'<span class="result-label">계산 결과</span>':''}${name}</td><td class="num ${value<0?'negative':cls?'positive':''}">${money(value)}</td><td class="num">${money(unit)}</td></tr>`).join('');$('bundlesSummary').innerHTML=`<tr class="result"><td colspan="7">기간 이익 총계 (고정비 차감 전)</td><td class="num ${c.profit<0?'negative':'positive'}">${c.sold?money(c.profit):'—'}</td></tr>`;}
''' +s[end:]
change('costRows(c).map(([n,v],i)=>`<tr>', 'costRows(c).slice(0,10).map(([n,v],i)=>`<tr>')
change("const segments=[c.cogs", "renderTotals(c);const segments=[c.cogs")
change("$('costs').innerHTML='';$('bundles').innerHTML='';", "$('costs').innerHTML='';$('bundles').innerHTML='';for(const id of ['salesSummary','adsSummary','adminSummary','bundlesSummary','costSummary'])$(id).innerHTML='';")
change('<h2>6. 원가표와 손익</h2>', '<h2>6. 원가표와 손익</h2><p class="notice"><b>고정비 차감 전 이익</b> = 매출 총계 − 제품·판매·광고·관리비.<br><b>고정비 차감 후 이익</b> = 위 이익 − 임대료·전기료 등 고정비. 모든 이익은 부가세 정산·법인세 반영 전입니다.</p>')
change('각 표의 ↑·↓ 버튼으로 항목 순서를 변경할 수 있습니다.', '각 표의 ↑·↓ 버튼으로 상세 항목 순서를 변경할 수 있습니다. 합계·계산 결과 행은 표 하단에 고정됩니다.')
change('입력값 백업</button>', '입력값 백업</button>')
p.write_text(s,encoding='utf-8');print('Clear profit labels, pinned summary footers, highlighted result rows; previous order preserved for details')
