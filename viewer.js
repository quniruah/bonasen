let lastRevision=null,lastTemplate=null,loading=false,currentReport=null,frameReady=false,selectedDate=null,selectedProduct=null,viewSequence=0;
const reportFrame=document.getElementById('report');
function reportForSelectedDate(report){
 const portfolio=report.productViews;if(portfolio?.views){if(!selectedProduct||!Object.hasOwn(portfolio.views,selectedProduct))selectedProduct=portfolio.active;}const views=portfolio?.views?.[selectedProduct]||report.dateViews;if(!views||!Array.isArray(views.keys)||!Array.isArray(views.values)||views.year!==report.state?.ledger?.year||!views.dates)return report;
 const initial=report.state.ledger.year+'-'+String(report.state.ledger.month).padStart(2,'0')+'-'+String(report.state.ledger.day).padStart(2,'0');
 if(!selectedDate||!Object.hasOwn(views.dates,selectedDate))selectedDate=Object.hasOwn(views.dates,initial)?initial:views.maxDate;
 const refs=views.dates[selectedDate];if(!Array.isArray(refs)||refs.length!==views.keys.length)throw Error('날짜별 공개 결과 형식을 확인하세요.');
 const state=Object.fromEntries(views.keys.map((key,i)=>[key,JSON.parse(JSON.stringify(views.values[refs[i]]))])),months={};
 for(const date of Object.keys(views.dates))if(/^\d{4}-\d{2}-\d{2}$/.test(date)&&Number(date.slice(0,4))===views.year){const month=Number(date.slice(5,7));months[month]=Math.max(months[month]||0,Number(date.slice(8)));}
 state.publicDateChoices={year:views.year,months};if(portfolio?.products){state.publicProductChoices={products:portfolio.products};state.companyOverview=report.companyViews?.[selectedDate]||state.companyOverview;if(state.companyOverview){state.companyOverview=JSON.parse(JSON.stringify(state.companyOverview));state.companyOverview.target=0;for(const product of state.companyOverview.products){const pv=portfolio.views[product.id],refs=pv?.dates?.[selectedDate],li=pv?.keys?.indexOf('ledger'),ledger=refs&&li>=0?pv.values[refs[li]]:null;product.target=ledger?.years?.[ledger.year]?.targets?.[ledger.month-1]||0;state.companyOverview.target+=product.target;}}}return{schema:report.schema,publishedAt:report.publishedAt,state};
}
function sendCurrentReport(){if(frameReady&&currentReport?.schema==='bonasen-public-v2')reportFrame.contentWindow.postMessage({type:'BONASEN_REPORT',report:reportForSelectedDate(currentReport)},'*');}
window.addEventListener('message',event=>{if(event.source!==reportFrame.contentWindow)return;if(event.data?.type==='BONASEN_VIEW_READY'){frameReady=true;sendCurrentReport();}else if(event.data?.type==='BONASEN_SELECT_PRODUCT'){const id=event.data.productId;if(typeof id!=='string'||!currentReport?.productViews?.views||!Object.hasOwn(currentReport.productViews.views,id))return;selectedProduct=id;frameReady=false;reportFrame.src='admin.html?mode=viewer&v='+encodeURIComponent(lastTemplate||'current')+'&report='+lastRevision+'&view='+(++viewSequence);}else if(event.data?.type==='BONASEN_SELECT_DATE'){const date=event.data.date;if(typeof date!=='string'||!currentReport?.dateViews?.dates||!Object.hasOwn(currentReport.dateViews.dates,date))return;selectedDate=date;frameReady=false;reportFrame.src='admin.html?mode=viewer&v='+encodeURIComponent(lastTemplate||'current')+'&report='+lastRevision+'&view='+(++viewSequence);}});
async function refreshReport(){
 if(loading)return;loading=true;const status=document.getElementById('viewerStatus');
 try{
  const config=window.BONASEN_CONFIG;if(!config||!/^https:\/\/[a-z0-9-]+\.supabase\.co$/.test(config.supabaseUrl)||!config.publishableKey)throw Error('공개 서비스 연결 설정이 아직 필요합니다.');
  const response=await fetch(config.supabaseUrl+'/rest/v1/bonasen_public?id=eq.main&select=html,revision,updated_at',{headers:{apikey:config.publishableKey},cache:'no-store'});
  if(!response.ok)throw Error('공개 결과를 불러오지 못했습니다.');
  const rows=await response.json();if(!rows.length){status.textContent='관리자가 아직 결과를 공개하지 않았습니다.';return;}
  const saved=rows[0];let report=null;try{report=JSON.parse(saved.html);}catch{}
  if(report?.schema==='bonasen-public-v2'){
   const head=await fetch('admin.html',{method:'HEAD',cache:'no-cache'});if(!head.ok)throw Error('공통 화면을 불러오지 못했습니다.');
   const template=head.headers.get('etag')||head.headers.get('last-modified')||'current';currentReport=report;
   if(saved.revision!==lastRevision||template!==lastTemplate){frameReady=false;reportFrame.removeAttribute('srcdoc');reportFrame.src='admin.html?mode=viewer&v='+encodeURIComponent(template)+'&report='+saved.revision;lastTemplate=template;}
  }else if(saved.revision!==lastRevision){currentReport=null;reportFrame.removeAttribute('src');reportFrame.srcdoc=saved.html;}
  reportFrame.hidden=false;lastRevision=saved.revision;
  status.textContent='조회 전용 · 마지막 공개 '+new Date(saved.updated_at).toLocaleString('ko-KR',{timeZone:'Asia/Seoul'})+' · 30초마다 자동 갱신'+(report?.schema==='bonasen-public-v2'?'':' · 새 공통 화면 적용은 관리자에서 한 번 저장·공개해주세요.');
 }catch(error){status.textContent=error.message+(lastRevision!==null?' 마지막으로 불러온 결과를 표시합니다.':'');}finally{loading=false;}
}
refreshReport();setInterval(()=>{if(!document.hidden)refreshReport();},30000);
document.addEventListener('visibilitychange',()=>{if(!document.hidden)refreshReport();});
