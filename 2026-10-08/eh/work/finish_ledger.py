from pathlib import Path
p=Path('outputs/보나센_원가계산기.html');s=p.read_text(encoding='utf-8')
s=s.replace('현재 입력값을 지우고 참고표 값으로 초기화할까요?', '현재 입력값과 모든 연도의 일매출 기록을 지우고 초기화할까요? 기록을 보관하려면 먼저 입력값 백업을 저장하세요.')
s=s.replace('다른 컴퓨터로 이동할 때는 ‘입력값 백업’ 파일을 가져오세요.', '연간 일매출 기록과 월별 목표도 함께 저장됩니다. 정기적으로 ‘입력값 백업’을 보관하고, 다른 컴퓨터로 이동할 때 해당 백업 파일을 가져오세요.')
p.write_text(s,encoding='utf-8')
