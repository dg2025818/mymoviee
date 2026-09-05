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

genre_counts = df['genre'].value_counts().reset_index()
genre_counts.columns = ['genre', 'count']

fig1 = px.pie(
    genre_counts,
    names='genre',
    values='count',
    hole=0.4,
    title="장르별 영화 편수 분포"
)

fig1.update_traces(
    textinfo='percent+label',
    hovertemplate="<b>장르:</b> %{label}<br><b>편수:</b> %{value}편<br><b>비율:</b> %{percent}"
)

st.plotly_chart(fig1, use_container_width=True)

st.markdown("> **💡 이 그래프로 알 수 있는 것:** 특정 주요 장르에 영화 개봉 편수가 집중되어 있는지, 혹은 다양한 장르로 고르게 분포되어 있는지 한눈에 파악할 수 있습니다.")

st.divider()

# -------------------------------------------------------------------
# 두 번째 그래프: 장르-영화 계층구조 트리맵 (칸 크기: total_audi)
# -------------------------------------------------------------------
st.subheader("2. 장르 및 영화별 총 관객 수 (트리맵)")

fig2 = px.treemap(
    df,
    path=[px.Constant("전체 장르"), 'genre', 'movieNm'],
    values='total_audi',
    color='genre',
    title="장르 및 영화별 총 관객 수 분포"
)

fig2.update_traces(
    hovertemplate="<b>영화명/장르:</b> %{label}<br><b>총 관객 수:</b> %{value:,}명"
)

st.plotly_chart(fig2, use_container_width=True)

st.markdown("> **💡 이 그래프로 알 수 있는 것:** 장르별 전체 관객 규모의 비중과 함께, 각 장르 내에서 어떤 영화가 총 관객 수를 주도했는지 한눈에 비교할 수 있습니다.")

st.divider()

# -------------------------------------------------------------------
# 세 번째 그래프: 총 관객 수 히스토그램
# -------------------------------------------------------------------
st.subheader("3. 총 관객 수(total_audi) 분포")

fig3 = px.histogram(
    df,
    x='total_audi',
    nbins=30,
    title="영화별 총 관객 수 분포 (히스토그램)",
    labels={'total_audi': '총 관객 수(명)'}
)

fig3.update_traces(
    hovertemplate="<b>관객 수 구간:</b> %{x}명<br><b>영화 수:</b> %{y}편"
)

st.plotly_chart(fig3, use_container_width=True)

top_movie = df.loc[df['total_audi'].idxmax()]
top_movie_name = top_movie['movieNm']
top_movie_audi = top_movie['total_audi']

st.markdown(f"> **💡 이 그래프로 알 수 있는 것:** 대부분의 영화는 관객 수가 적은 구간(하위 구간)에 밀집해 있으며, 상위 흥행작으로 갈수록 편수가 급격히 줄어드는 전형적인 비대칭 분포를 보입니다. 이 데이터에서 가장 관객이 많은 영화는 **'{top_movie_name}'**(총 {top_movie_audi:,}명)입니다.")

st.divider()

# -------------------------------------------------------------------
# 네 번째 그래프: 개봉일 스크린수 vs 총 관객 수 산점도
# -------------------------------------------------------------------
st.subheader("4. 개봉일 스크린수와 총 관객 수의 관계 (산점도)")

fig4 = px.scatter(
    df,
    x='first_scrn',
    y='total_audi',
    color='genre',
    hover_name='movieNm',
    title="개봉일 스크린수 대비 총 관객 수 분포",
    labels={
        'first_scrn': '개봉일 스크린수(개)',
        'total_audi': '총 관객 수(명)',
        'genre': '장르'
    }
)

fig4.update_traces(
    hovertemplate="<b>영화명:</b> %{hovertext}<br><b>개봉일 스크린수:</b> %{x:,}개<br><b>총 관객 수:</b> %{y:,}명"
)

st.plotly_chart(fig4, use_container_width=True)

st.markdown("> **💡 이 그래프로 알 수 있는 것:** 개봉일 스크린수가 많을수록 대체로 총 관객 수가 증가하는 양의 상관관계를 보이는지, 또는 스크린수가 적음에도 높은 관객 수를 기록한 흥행 이변작이 있는지 장르별 색상 구분을 통해 확인할 수 있습니다.")

st.divider()

# -------------------------------------------------------------------
# 다섯 번째 그래프: 영화 10편 이상 주요 장르별 총 관객 수 박스플롯
# -------------------------------------------------------------------
st.subheader("5. 주요 장르별 총 관객 수 분포 (박스플롯)")

# 1. 영화가 10편 이상인 장르만 필터링
genre_counts_series = df['genre'].value_counts()
major_genres = genre_counts_series[genre_counts_series >= 10].index.tolist()
df_major_genres = df[df['genre'].isin(major_genres)]

# 2. 박스플롯 생성
fig5 = px.box(
    df_major_genres,
    x='genre',
    y='total_audi',
    color='genre',
    points="outliers",       # 상자 밖의 이상치(Outlier) 점 표시
    hover_name='movieNm',    # 점 마우스 호버 시 영화명 표시
    title="영화 10편 이상 주요 장르별 총 관객 수 분포 비교",
    labels={
        'genre': '장르',
        'total_audi': '총 관객 수(명)'
    }
)

# 호버 툴팁 서식 지정
fig5.update_traces(
    hovertemplate="<b>영화명:</b> %{hovertext}<br><b>총 관객 수:</b> %{y:,}명"
)

st.plotly_chart(fig5, use_container_width=True)

st.markdown("> **💡 이 그래프로 알 수 있는 것:** 주요 장르별 관객 수의 중간값과 분포 범위(변동성)를 비교할 수 있으며, 상자 위쪽 밖으로 튀어나온 이상치 점을 통해 해당 장르 내에서 대흥행을 거둔 시그니처 작품을 식별할 수 있습니다.")

st.divider()

# -------------------------------------------------------------------
# 여섯 번째 그래프: 개봉일 스크린수 vs 총 관객 수 vs 첫 주 관객 (버블 그래프)
# -------------------------------------------------------------------
st.subheader("6. 스크린수, 총 관객 수, 첫 주 관객 수의 관계 (버블 그래프)")

fig6 = px.scatter(
    df,
    x='first_scrn',
    y='total_audi',
    size='first_week_audi',  # 버블 크기: 개봉 첫 주 관객 수
    color='genre',
    hover_name='movieNm',
    title="개봉일 스크린수 대비 총 관객 수 및 첫 주 관객 수 분포",
    labels={
        'first_scrn': '개봉일 스크린수(개)',
        'total_audi': '총 관객 수(명)',
        'first_week_audi': '첫 주 관객 수(명)',
        'genre': '장르'
    },
    size_max=60
)

fig6.update_traces(
    hovertemplate="<b>영화명:</b> %{hovertext}<br><b>개봉일 스크린수:</b> %{x:,}개<br><b>첫 주 관객 수:</b> %{marker.size:,}명<br><b>총 관객 수:</b> %{y:,}명"
)

st.plotly_chart(fig6, use_container_width=True)

st.markdown("> **💡 이 그래프로 알 수 있는 것:** 네 번째 산점도 정보에 더해 버블의 크기(개봉 첫 주 관객)를 통해 초기 흥행 폭발력을 시각적으로 비교할 수 있습니다. 스크린수가 적어도 버블이 크다면 입소문을 통한 초기 선전, 스크린수가 많아도 버블이 작다면 기대 이하의 초기 성적을 의미할 수 있습니다.")

st.divider()

# -------------------------------------------------------------------
# 일곱 번째 그래프: 제작 국가별-장르별 영화 편수 선버스트 차트
# -------------------------------------------------------------------
st.subheader("7. 제작 국가 및 장르별 영화 편수 (선버스트 그래프)")

# 선버스트 그래프 생성 (계층 구조: 제작 국가 -> 장르)
fig7 = px.sunburst(
    df,
    path=['nation', 'genre'],
    title="제작 국가 및 장르별 영화 편수 분포",
    color='nation'
)

# 호버 툴팁 및 라벨 서식 설정 (영화 편수 및 비율 표시)
fig7.update_traces(
    hovertemplate="<b>구분:</b> %{label}<br><b>영화 편수:</b> %{value}편<br><b>상위 계층 대비 비율:</b> %{percentParent:.1%}"
)

st.plotly_chart(fig7, use_container_width=True)

st.markdown("> **💡 이 그래프로 알 수 있는 것:** 제작 국가별 전체 개봉 영화 편수의 비중과, 각 국가 내에서 주로 어떤 장르의 영화가 수입/제작되어 개봉했는지 계층적 구조로 한눈에 파악할 수 있습니다.")

st.divider()
