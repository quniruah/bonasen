let lastRevision=null,lastTemplate=null,loading=false,currentReport=null,frameReady=false;
const reportFrame=document.getElementById('report');
function sendCurrentReport(){if(frameReady&&currentReport?.schema==='bonasen-public-v2')reportFrame.contentWindow.postMessage({type:'BONASEN_REPORT',report:currentReport},'*');}
window.addEventListener('message',event=>{if(event.source!==reportFrame.contentWindow)return;if(event.data?.type==='BONASEN_VIEW_READY'){frameReady=true;sendCurrentReport();}});
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
