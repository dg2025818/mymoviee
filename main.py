import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 페이지 기본 설정 및 제목 지정
st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 영화 데이터 그래프 도감 2 - 분포와 관계")
st.write("1년간 박스오피스 10위권에 든 영화 중, 해당 기간에 개봉한 216편의 분포와 관계를 시각화합니다.")

# 2. 데이터 불러오기 및 전처리 (캐싱 적용)
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"
    df = pd.read_csv(url)
    
    # genre 열 전처리: 세로막대 기호(|)로 분리되어 있는 경우 첫 번째 장르만 추출
    df['genre'] = df['genre'].astype(str).apply(lambda x: x.split('|')[0].strip())
    
    return df

df = load_data()

st.divider()

# -------------------------------------------------------------------
# 첫 번째 그래프: 장르별 영화 편수 (플롯리 도넛 그래프)
# -------------------------------------------------------------------
st.subheader("1. 장르별 영화 편수 비율")

# 장르별 영화 편수 집계
genre_counts = df['genre'].value_counts().reset_index()
genre_counts.columns = ['genre', 'count']

# Plotly 도넛 차트 생성
fig = px.pie(
    genre_counts,
    names='genre',
    values='count',
    hole=0.4, # 도넛 모양을 만드는 중앙 구멍 비율
    title="장르별 영화 편수 분포"
)

# 마우스 호버 시 편수(value)와 비율(percent) 및 장르명(label)이 명확히 표시되도록 설정
fig.update_traces(
    textinfo='percent+label',
    hovertemplate="<b>장르:</b> %{label}<br><b>편수:</b> %{value}편<br><b>비율:</b> %{percent}"
)

# 그래프 출력
st.plotly_chart(fig, use_container_width=True)

# 그래프 하단 설명 및 구역 분리
st.markdown("> **💡 이 그래프로 알 수 있는 것:** 특정 주요 장르에 영화 개봉 편수가 집중되어 있는지, 혹은 다양한 장르로 고르게 분포되어 있는지 한눈에 파악할 수 있습니다.")

st.divider()

# -------------------------------------------------------------------
# 추후 추가 시각화를 위한 영역 (예시 구조)
# -------------------------------------------------------------------
st.info("📌 추가적인 분포 및 관계 그래프가 들어갈 공간입니다.")
