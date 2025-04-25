import streamlit as st
import openai
import random

# 페이지 설정
st.set_page_config(page_title="부동산 데이터 분석 챗봇", page_icon="🏠")

# OpenAI API 키 설정 (실제 사용시 환경 변수나 secrets 이용 권장)
# openai.api_key = "your-api-key-here"
# 실습 환경에서는 다음과 같이 사이드바에서 입력 받을 수 있음
api_key = st.sidebar.text_input("OpenAI API 키를 입력하세요", type="password")
if api_key:
    openai.api_key = api_key

# 페이지 제목
st.title("🏠 부동산 데이터 분석 챗봇")
st.write("네이버 블로그에서 수집한 부동산 데이터에 대해 질문해보세요.")

# 가상의 부동산 데이터 (실제로는 벡터 데이터베이스에서 가져옴)
property_data = [
    "강남 아파트 가격이 3개월 연속 하락세를 보이고 있습니다. 많은 블로거들이 금리 인상의 영향이라고 분석하고 있습니다.",
    "경기도 지역 아파트는 전월 대비 2.5% 하락했으며, 매수자들의 관망세가 계속되고 있습니다.",
    "30대 블로거들은 대출 규제와 금리 인상으로 내집 마련이 더 어려워졌다고 호소하고 있습니다.",
    "부동산 전문가들은 현재 시장 상황을 '조정기'로 보고 있으며, 1-2년간 조정이 계속될 것으로 전망합니다.",
    "40-50대 블로거들은 투자용 부동산의 가치 하락과 임대 수익률 감소에 대한 우려를 표하고 있습니다."
]

# 간단한 키워드 검색 함수 (실제로는 벡터 유사도 검색 사용)
def search_property_data(query):
    relevant_data = []
    query_keywords = query.lower().split()

    for data in property_data:
        for keyword in query_keywords:
            if keyword in data.lower():
                relevant_data.append(data)
                break

    return relevant_data if relevant_data else ["관련 데이터를 찾을 수 없습니다."]

# ChatGPT API를 활용한 응답 생성 함수
def get_chatgpt_response(query, context):
    if not openai.api_key:
        return "OpenAI API 키가 설정되지 않았습니다. 사이드바에서 API 키를 입력해주세요."

    try:
        # 프롬프트 준비
        prompt = f"""
        다음은 네이버 블로그에서 수집한 부동산 관련 데이터입니다:
        {' '.join(context)}

        이 정보를 바탕으로 다음 질문에 답변해주세요: {query}
        """

        # API 호출
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "당신은 부동산 데이터 분석 전문가입니다."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.7
        )

        return response.choices[0].message.content
    except Exception as e:
        return f"죄송합니다, 오류가 발생했습니다: {str(e)}"

# API 키가 없을 경우 간단한 응답 함수 (데모용)
def get_simple_response(query, context):
    if "가격" in query.lower():
        return f"블로그 데이터 분석 결과, 최근 아파트 가격은 하락세를 보이고 있습니다. {context[0]}"
    elif "30대" in query.lower() or "젊은" in query.lower():
        return f"30대 블로거들의 의견을 살펴보면, 대출 규제와 금리 인상으로 내집 마련이 더 어려워졌다고 호소하고 있습니다."
    elif "전망" in query.lower() or "앞으로" in query.lower():
        return f"부동산 시장 전망에 대해서는, 전문가들이 1-2년간의 조정기를 예상하고 있습니다."
    else:
        return f"분석 결과: {context[0]}"

# 챗봇 응답 생성 함수
def chat_response(question):
    # 관련 데이터 검색
    relevant_data = search_property_data(question)

    # ChatGPT API 키가 있으면 API 사용, 없으면 간단한 응답
    if openai.api_key:
        return get_chatgpt_response(question, relevant_data)
    else:
        return get_simple_response(question, relevant_data)

# 세션 상태 초기화
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 이전 대화 내용 표시
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력 받기
if prompt := st.chat_input("질문을 입력하세요 (예: 최근 아파트 가격 변화 추세는 어떤가요?)"):
    # 사용자 메시지 표시
    with st.chat_message("user"):
        st.markdown(prompt)

    # 사용자 메시지 저장
    st.session_state.chat_history.append({"role": "user", "content": prompt})

    # 응답 생성
    with st.spinner("답변 생성 중..."):
        response = chat_response(prompt)

    # 응답 메시지 표시
    with st.chat_message("assistant"):
        st.markdown(response)

    # 응답 메시지 저장
    st.session_state.chat_history.append({"role": "assistant", "content": response})

# 예시 질문
st.sidebar.header("예시 질문")
example_questions = [
    "최근 아파트 가격 변화에 대한 사람들의 생각이 어떤가요?",
    "30대들은 부동산 시장에 대해 어떻게 생각하나요?",
    "부동산 시장 앞으로 어떻게 될까요?",
    "경기도 지역 아파트 가격은 어떻게 변했나요?"
]

for question in example_questions:
    if st.sidebar.button(question):
        # 사용자 메시지 표시 및 저장
        with st.chat_message("user"):
            st.markdown(question)
        st.session_state.chat_history.append({"role": "user", "content": question})

        # 응답 생성
        with st.spinner("답변 생성 중..."):
            response = chat_response(question)

        # 응답 메시지 표시 및 저장
        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.chat_history.append({"role": "assistant", "content": response})

        # 페이지 새로고침
        st.rerun()

# 대화 기록 초기화 버튼
if st.sidebar.button("대화 기록 초기화"):
    st.session_state.chat_history = []
    st.rerun()

# 데이터 확인 섹션
with st.sidebar.expander("부동산 데이터 확인"):
    st.write("현재 분석에 사용 중인 데이터:")
    for idx, data in enumerate(property_data):
        st.write(f"{idx+1}. {data}")
