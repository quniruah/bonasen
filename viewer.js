let lastRevision=null,loading=false;
async function refreshReport(){
  if(loading)return;loading=true;
  const status=document.getElementById('viewerStatus');
  try{
    const config=window.BONASEN_CONFIG;
    if(!config||!/^https:\/\/[a-z0-9-]+\.supabase\.co$/.test(config.supabaseUrl)||!config.publishableKey)throw Error('공개 서비스 연결 설정이 아직 필요합니다.');
    const response=await fetch(config.supabaseUrl+'/rest/v1/bonasen_public?id=eq.main&select=html,revision,updated_at',{headers:{apikey:config.publishableKey},cache:'no-store'});
    if(!response.ok)throw Error('공개 결과를 불러오지 못했습니다.');
    const rows=await response.json();
    if(!rows.length){status.textContent='관리자가 아직 결과를 공개하지 않았습니다.';return;}
    const report=rows[0];if(report.revision!==lastRevision){document.getElementById('report').srcdoc=report.html;document.getElementById('report').hidden=false;lastRevision=report.revision;}
    status.textContent='조회 전용 · 마지막 공개 '+new Date(report.updated_at).toLocaleString('ko-KR',{timeZone:'Asia/Seoul'})+' · 30초마다 자동 갱신';
  }catch(error){status.textContent=error.message+(lastRevision!==null?' 마지막으로 불러온 결과를 표시합니다.':'');}
  finally{loading=false;}
}
refreshReport();setInterval(()=>{if(!document.hidden)refreshReport();},30000);
document.addEventListener('visibilitychange',()=>{if(!document.hidden)refreshReport();});
