# -*- coding: utf-8 -*-
"""
🧳✨ MBTI 여행지 추천기 ✨🧳
Streamlit Cloud 배포용 - 외부 라이브러리 없이 streamlit 표준 기능만 사용합니다.
"""

import random
import streamlit as st

# ────────────────────────────────────────────────────────────
# 페이지 설정
# ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MBTI 여행지 추천기",
    page_icon="🧳",
    layout="centered",
)

# ────────────────────────────────────────────────────────────
# 귀여운 스타일 (커스텀 CSS)
# ────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    /* 전체 배경 - 파스텔 그라데이션 */
    .stApp {
        background: linear-gradient(135deg, #ffe1ec 0%, #e5f0ff 50%, #fff5d6 100%);
    }

    /* 제목 카드 */
    .title-card {
        text-align: center;
        padding: 28px 20px;
        border-radius: 28px;
        background: rgba(255, 255, 255, 0.65);
        box-shadow: 0 8px 24px rgba(255, 170, 200, 0.35);
        margin-bottom: 8px;
    }
    .title-card h1 {
        font-size: 2.1rem;
        margin: 0;
        color: #ff6fa5;
        letter-spacing: -0.5px;
    }
    .title-card p {
        margin: 8px 0 0 0;
        color: #7a7a9d;
        font-size: 0.98rem;
    }

    /* 추천 결과 카드 */
    .result-card {
        background: rgba(255, 255, 255, 0.85);
        border-radius: 26px;
        padding: 26px 26px 22px 26px;
        box-shadow: 0 10px 30px rgba(150, 180, 255, 0.35);
        border: 3px dashed #ffc2d9;
        margin-top: 14px;
    }
    .result-emoji {
        font-size: 3.4rem;
        text-align: center;
        display: block;
        margin-bottom: 6px;
    }
    .result-place {
        text-align: center;
        font-size: 1.7rem;
        font-weight: 800;
        color: #ff6fa5;
        margin-bottom: 2px;
    }
    .result-country {
        text-align: center;
        color: #9a9ac0;
        font-size: 0.95rem;
        margin-bottom: 16px;
    }
    .result-desc {
        color: #55557a;
        font-size: 1.02rem;
        line-height: 1.7;
        text-align: center;
    }

    /* 키워드 뱃지 */
    .badge {
        display: inline-block;
        background: #fff0f6;
        color: #ff6fa5;
        border-radius: 999px;
        padding: 5px 14px;
        margin: 4px 4px;
        font-size: 0.86rem;
        font-weight: 700;
        border: 2px solid #ffd4e5;
    }

    /* 버튼 예쁘게 */
    .stButton > button {
        background: linear-gradient(90deg, #ff9ec4, #ffb0d6);
        color: white;
        border: none;
        border-radius: 999px;
        padding: 12px 28px;
        font-size: 1.05rem;
        font-weight: 800;
        box-shadow: 0 6px 16px rgba(255, 150, 190, 0.5);
        transition: transform 0.12s ease;
    }
    .stButton > button:hover {
        transform: scale(1.04);
        color: white;
    }

    /* 하단 문구 */
    .foot {
        text-align: center;
        color: #a8a8c8;
        font-size: 0.82rem;
        margin-top: 22px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ────────────────────────────────────────────────────────────
# MBTI별 여행지 데이터 (각 유형마다 여러 후보)
# ────────────────────────────────────────────────────────────
MBTI_DATA = {
    "INTJ": {
        "keywords": ["#조용한", "#역사탐방", "#효율여행"],
        "places": [
            ("체코 프라하", "🏰", "Czech Republic",
             "천 년의 건축과 이야기가 켜켜이 쌓인 도시예요. 계획대로 착착 둘러보며 사색하기 딱 좋아요!"),
            ("교토", "⛩️", "Japan",
             "고즈넉한 사찰과 정원을 거닐며 생각을 정리하기 좋은 곳. 계획형 당신의 완벽한 동선이 빛나요!"),
        ],
    },
    "INTP": {
        "keywords": ["#호기심", "#과학박물관", "#자유일정"],
        "places": [
            ("독일 베를린", "🔬", "Germany",
             "박물관 섬과 실험적인 문화가 가득한 도시. 궁금증 많은 당신이 마음껏 파고들 수 있어요!"),
            ("아이슬란드", "🌋", "Iceland",
             "화산과 오로라, 지구의 신비가 펼쳐지는 곳. 혼자 상상하고 탐구하기 완벽해요!"),
        ],
    },
    "ENTJ": {
        "keywords": ["#도시정복", "#야경", "#파워풀"],
        "places": [
            ("뉴욕", "🗽", "USA",
             "세상의 중심에서 에너지를 흡수하세요! 리더 기질의 당신에게 딱 맞는 스케일 큰 도시예요."),
            ("두바이", "🏙️", "UAE",
             "미래 도시의 위엄! 야망 넘치는 당신이 '나도 할 수 있어'를 외치게 되는 곳이에요."),
        ],
    },
    "ENTP": {
        "keywords": ["#즉흥", "#다채로움", "#새로운자극"],
        "places": [
            ("이스탄불", "🕌", "Turkey",
             "동양과 서양이 만나는 흥미진진한 도시! 토론과 발견을 즐기는 당신에게 최고예요."),
            ("멕시코시티", "🌮", "Mexico",
             "예술, 음식, 활기가 뒤섞인 자극의 도시. 새로운 아이디어가 마구 샘솟을 거예요!"),
        ],
    },
    "INFJ": {
        "keywords": ["#힐링", "#감성", "#의미있는여행"],
        "places": [
            ("교토 아라시야마", "🎋", "Japan",
             "대나무 숲 사이를 걸으며 마음을 정화해요. 깊이 있는 당신의 감수성이 채워지는 곳!"),
            ("스위스 인터라켄", "🏔️", "Switzerland",
             "고요한 호수와 웅장한 산 사이에서 내면과 대화하기 좋은 평화로운 여행지예요."),
        ],
    },
    "INFP": {
        "keywords": ["#몽글몽글", "#동화감성", "#꿈꾸는"],
        "places": [
            ("포르투갈 신트라", "🧚", "Portugal",
             "동화 속 같은 알록달록 궁전과 숲! 상상력 가득한 당신에게 꼭 맞는 꿈같은 마을이에요."),
            ("네덜란드 히트호른", "🛶", "Netherlands",
             "차 없이 배로만 다니는 물의 마을. 조용하고 사랑스러운 감성 여행에 완벽해요."),
        ],
    },
    "ENFJ": {
        "keywords": ["#사람들과함께", "#따뜻한", "#추억만들기"],
        "places": [
            ("스페인 바르셀로나", "🎨", "Spain",
             "가우디의 예술과 따뜻한 사람들! 함께하는 걸 좋아하는 당신에게 잊지 못할 추억을 선물해요."),
            ("이탈리아 로마", "🍝", "Italy",
             "골목마다 이야기가 있고 사람 냄새가 나는 도시. 정 많은 당신이 반할 곳이에요!"),
        ],
    },
    "ENFP": {
        "keywords": ["#설렘폭발", "#자유분방", "#인생샷"],
        "places": [
            ("발리", "🏝️", "Indonesia",
             "자유로운 영혼을 위한 낙원! 서핑, 요가, 감성 카페까지 반짝이는 순간이 가득해요."),
            ("모로코 마라케시", "🐫", "Morocco",
             "색색의 시장과 사막의 별밤! 모험을 사랑하는 당신의 심장이 콩닥콩닥 뛸 거예요."),
        ],
    },
    "ISTJ": {
        "keywords": ["#정석코스", "#클래식", "#안정감"],
        "places": [
            ("영국 런던", "🎡", "United Kingdom",
             "전통과 질서가 살아있는 도시. 계획적으로 명소를 차근차근 도는 데 최적이에요!"),
            ("오스트리아 빈", "🎻", "Austria",
             "클래식 음악과 격조 있는 건축의 도시. 신뢰감 있는 당신의 취향에 딱 맞아요."),
        ],
    },
    "ISFJ": {
        "keywords": ["#포근한", "#소도시", "#정겨운"],
        "places": [
            ("일본 오타루", "❄️", "Japan",
             "운하와 오르골, 따뜻한 감성이 가득한 소도시. 다정한 당신 마음처럼 포근한 곳이에요."),
            ("독일 로텐부르크", "🏘️", "Germany",
             "동화 같은 중세 마을에서 아늑한 시간을 보내세요. 세심한 당신에게 잘 어울려요!"),
        ],
    },
    "ESTJ": {
        "keywords": ["#알찬일정", "#랜드마크", "#효율만점"],
        "places": [
            ("싱가포르", "🌆", "Singapore",
             "깔끔하고 체계적인 도시! 시간 낭비 없이 알차게 즐기는 걸 좋아하는 당신에게 완벽해요."),
            ("미국 워싱턴 D.C.", "🏛️", "USA",
             "질서정연한 도시와 박물관들. 목표 지향적인 당신의 여행 스타일과 찰떡이에요!"),
        ],
    },
    "ESFJ": {
        "keywords": ["#함께먹방", "#인기명소", "#다같이"],
        "places": [
            ("태국 방콕", "🛺", "Thailand",
             "먹거리와 볼거리가 넘치는 활기찬 도시! 사람들과 왁자지껄 즐기기 최고예요."),
            ("베트남 다낭", "🏖️", "Vietnam",
             "바다, 맛집, 리조트까지! 모두가 만족하는 여행을 챙기는 당신에게 딱이에요."),
        ],
    },
    "ISTP": {
        "keywords": ["#액티비티", "#자연도전", "#혼자여유"],
        "places": [
            ("뉴질랜드 퀸스타운", "🪂", "New Zealand",
             "번지점프, 스카이다이빙의 성지! 직접 몸으로 부딪히는 걸 좋아하는 당신에게 짜릿해요."),
            ("네팔 히말라야", "🏔️", "Nepal",
             "묵묵히 산을 오르며 나만의 시간을 즐겨요. 담백한 모험가 당신에게 어울려요!"),
        ],
    },
    "ISFP": {
        "keywords": ["#감성사진", "#자연힐링", "#여유롭게"],
        "places": [
            ("그리스 산토리니", "🌊", "Greece",
             "새하얀 집과 파란 바다의 그림 같은 풍경! 아름다움에 예민한 당신이 흠뻑 빠질 거예요."),
            ("제주도", "🍊", "Korea",
             "돌담길과 바다, 감성 카페까지. 소소한 아름다움을 사랑하는 당신에게 포근한 곳!"),
        ],
    },
    "ESTP": {
        "keywords": ["#핫플", "#스릴", "#에너지"],
        "places": [
            ("라스베이거스", "🎰", "USA",
             "화려함과 스릴이 폭발하는 도시! 순간을 즐기는 당신의 에너지가 마음껏 터져요."),
            ("호주 골드코스트", "🏄", "Australia",
             "서핑과 테마파크, 신나는 액티비티 천국! 활동적인 당신에게 완벽한 놀이터예요."),
        ],
    },
    "ESFP": {
        "keywords": ["#축제", "#분위기폭발", "#인싸여행"],
        "places": [
            ("브라질 리우데자네이루", "🎉", "Brazil",
             "삼바와 축제, 흥의 도시! 분위기 메이커인 당신이 주인공이 되는 여행지예요."),
            ("스페인 이비자", "🎶", "Spain",
             "낮엔 해변, 밤엔 파티! 반짝이는 순간을 사랑하는 당신에게 최고의 무대예요."),
        ],
    },
}

# ────────────────────────────────────────────────────────────
# 상단 타이틀
# ────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="title-card">
        <h1>🧳✨ MBTI 여행지 추천기 ✨🧳</h1>
        <p>당신의 성격에 딱 맞는 여행지를 콕! 찍어드릴게요 💕</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")

# ────────────────────────────────────────────────────────────
# MBTI 선택
# ────────────────────────────────────────────────────────────
col1, col2 = st.columns([1, 1])
with col1:
    ei = st.radio("에너지 방향", ["E (외향)", "I (내향)"], horizontal=True)
    sn = st.radio("인식 기능", ["S (감각)", "N (직관)"], horizontal=True)
with col2:
    tf = st.radio("판단 기능", ["T (사고)", "F (감정)"], horizontal=True)
    jp = st.radio("생활 양식", ["J (계획)", "P (탐색)"], horizontal=True)

mbti = ei[0] + sn[0] + tf[0] + jp[0]

st.markdown(
    f"<p style='text-align:center; font-size:1.3rem; font-weight:800; color:#7a7ad0;'>"
    f"👉 당신의 MBTI: <span style='color:#ff6fa5;'>{mbti}</span></p>",
    unsafe_allow_html=True,
)

st.write("")

# ────────────────────────────────────────────────────────────
# 추천 버튼
# ────────────────────────────────────────────────────────────
btn_col = st.columns([1, 2, 1])
with btn_col[1]:
    go = st.button("🎁 여행지 추천받기 🎁", use_container_width=True)

if go:
    data = MBTI_DATA[mbti]
    place, emoji, country, desc = random.choice(data["places"])
    badges = "".join(f"<span class='badge'>{k}</span>" for k in data["keywords"])

    st.balloons()
    st.markdown(
        f"""
        <div class="result-card">
            <span class="result-emoji">{emoji}</span>
            <div class="result-place">{place}</div>
            <div class="result-country">📍 {country}</div>
            <div style="text-align:center; margin-bottom:14px;">{badges}</div>
            <div class="result-desc">{desc}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.caption("💡 버튼을 다시 누르면 같은 MBTI의 또 다른 여행지를 추천해드려요!")

# ────────────────────────────────────────────────────────────
# 하단
# ────────────────────────────────────────────────────────────
st.markdown(
    "<p class='foot'>made with 💗 · MBTI는 재미로 즐겨주세요!</p>",
    unsafe_allow_html=True,
)
