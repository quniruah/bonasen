from pathlib import Path
p = Path('outputs/보나센_원가계산기.html')
s = p.read_text(encoding='utf-8')
changes = [
('광고·마케팅 총비용</small>', '광고·마케팅 기간 총비용</small>'),
('<em>선택한 항목과 기간 기준</em>', '<em id="adSplit">최초 1회 + 월 반복비 × 개월수</em>'),
('<h3>리뷰작업 부대비용</h3>', '<p class="notice" id="adSchedule"></p><h3>최초 1회 리뷰작업 비용</h3>'),
('> 리뷰작업 포함</label>', '> 이번 계산에 최초 리뷰비 포함</label>'),
('리뷰 건수 (1회)', '최초 리뷰 건수 (1회)'),
('<p id="reviewSummary" class="note"></p>', '<p id="reviewSummary" class="note"></p><p class="note">리뷰 작업비·수수료·배송비·기타비·제공 제품비는 최초 1회만 반영하며 개월수를 곱하지 않습니다. 작업 완료 후 이후 기간만 계산할 때는 위 체크를 해제하세요.</p>'),
('ad=s.ads.reduce((a,r)=>a+cost(r),0)+review,', "monthlyAd=s.ads.reduce((a,r)=>a+(r.enabled&&r.cycle==='monthly'?r.rate*r.qty:0),0),onceAd=s.ads.reduce((a,r)=>a+(r.enabled&&r.cycle==='once'?r.rate*r.qty:0),0),ad=monthlyAd*s.months+onceAd+review,"),
('reviewBase,reviewProduct,review,ad,admin,', 'reviewBase,reviewProduct,review,monthlyAd,onceAd,ad,admin,'),
("['광고·마케팅 (리뷰 포함)',c.ad]", "['최초 1회 리뷰작업',c.review],['기타 1회 광고비',c.onceAd],['월 반복 리워드·기타 광고비 (기간 합계)',c.monthlyAd*state.months]"),
("$('adTotal').textContent=money(c.ad)+' 원';", "$('adTotal').textContent=money(c.ad)+' 원';$('adSplit').textContent='최초·1회 '+money(c.review+c.onceAd)+'원 / 월 '+money(c.monthlyAd)+'원';$('adSchedule').textContent='월 반복 광고비 '+money(c.monthlyAd)+'원 × '+state.months+'개월 + 최초 리뷰 '+money(c.review)+'원 + 기타 1회 광고 '+money(c.onceAd)+'원 = 기간 광고·마케팅 총비용 '+money(c.ad)+'원';"),
('총원가 = 판매원가 + 판매수수료·배송·포장비 + 광고·리뷰비 + 관리비.', '광고·마케팅비 = 최초 리뷰비 + 기타 1회 광고비 + 월 리워드·기타 광고비 × 개월수.<br>총원가 = 판매원가 + 판매수수료·배송·포장비 + 광고·마케팅비 + 관리비.'),
]
for old,new in changes:
    if old not in s:
        raise RuntimeError('Missing expected source: '+old)
    s = s.replace(old,new)
p.write_text(s,encoding='utf-8')
print('Updated one-time review and monthly advertising breakdown')
