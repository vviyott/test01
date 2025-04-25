import plotly.express as px
import plotly
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 한글 폰트 설정 부분 완전히 제거
# 대신 Streamlit의 마크다운/HTML을 사용하여 한글 제목 표시

try:
    # 상대 경로로 파일 읽기 시도
    money = pd.read_csv("money_data7.csv")
except FileNotFoundError:
    # 파일이 없는 경우 사용자에게 알림
    st.error("money_data7.csv 파일을 찾을 수 없습니다. 파일이 저장소의 메인 디렉토리에 있는지 확인하세요.")
    st.stop()  # 앱 실행 중단

# 년도 선택 박스 넣기
option = st.selectbox(
    '년도를 선택하세요',
    ('2020', '2021', '2022'))

option2 = int(option)

st.write('선택한 년도:', option)

# 해당 년도의 데이터만 필터링
filtered_money = money[money['A_YEAR'] == option2]

# 데이터가 비어있는지 확인
if filtered_money.empty:
    st.warning(f"{option}년도의 데이터가 없습니다.")
    st.stop()

fig, ax = plt.subplots(2, 2, figsize=(12, 8))

# 미국 금리 월별 라인 그래프 그리기
plt.subplot(221)
plt.plot(list(filtered_money['A_MONTH']), list(filtered_money['A_RATE']), color='red', marker='o')
plt.xticks(tuple(filtered_money['A_MONTH']))
# 한글 제목 대신 영어 또는 ASCII 문자 사용
plt.title('US Interest Rate')

# 한국 금리 월별 라인 그래프 그리기
plt.subplot(222)
plt.plot(list(filtered_money['A_MONTH']), list(filtered_money['K_RATE']), color='blue', marker='o')
plt.xticks(tuple(filtered_money['A_MONTH']))
plt.title('Korea Interest Rate')

# 한국 코스피 지수 월별 라인 그래프 그리기
plt.subplot(223)
plt.plot(list(filtered_money['A_MONTH']), list(filtered_money['KOSPI']), color='green', marker='o')
plt.xticks(tuple(filtered_money['A_MONTH']))
plt.title('KOSPI Index')

# 한국 집값 월별 라인 그래프 그리기기
plt.subplot(224)
plt.plot(list(filtered_money['A_MONTH']), list(filtered_money['HOUSE_PRICE']), color='yellow', marker='o')
plt.xticks(tuple(filtered_money['A_MONTH']))
plt.title('House Price')

# 그래프 표시
st.pyplot(fig)

# Streamlit 마크다운을 통해 한글 제목 별도 표시
st.markdown("""
## 차트 설명
* **왼쪽 상단**: 미국금리
* **오른쪽 상단**: 한국금리
* **왼쪽 하단**: 코스피 지수
* **오른쪽 하단**: 집값
""")