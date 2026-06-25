# -*- coding: utf-8 -*-
"""DB 시드 데이터 (단일 소스).
지역(도→시)·OTT·연예인·작품(원본 6 + 큐레이션)·장소·관계 매핑을 모두 이 파일에 둔다.

원칙:
- 한국 작품만 포함한다.
- CURATED_WORKS / 플랫폼·출연진 매핑은 '공식 실시간 순위'가 아니라 대표작 큐레이션이며,
  정확한 인기순위·스트리밍 제공처는 발표 전 1차 확인을 권장한다(주간 변동·권리 이동 가능).
- 2025~2026 방영작 등 확신이 낮은 항목은 넣지 않거나 주석으로 표시한다.
"""

# 전국 시·도 골격 (id, 한글명, 영문명). 데이터는 서울부터 채운다.
PROVINCES = [
    ("seoul",     "서울특별시",       "Seoul"),
    ("busan",     "부산광역시",       "Busan"),
    ("incheon",   "인천광역시",       "Incheon"),
    ("daegu",     "대구광역시",       "Daegu"),
    ("daejeon",   "대전광역시",       "Daejeon"),
    ("gwangju",   "광주광역시",       "Gwangju"),
    ("ulsan",     "울산광역시",       "Ulsan"),
    ("sejong",    "세종특별자치시",   "Sejong"),
    ("gyeonggi",  "경기도",           "Gyeonggi-do"),
    ("gangwon",   "강원특별자치도",   "Gangwon"),
    ("chungbuk",  "충청북도",         "Chungcheongbuk-do"),
    ("chungnam",  "충청남도",         "Chungcheongnam-do"),
    ("jeonbuk",   "전북특별자치도",   "Jeonbuk"),
    ("jeonnam",   "전라남도",         "Jeollanam-do"),
    ("gyeongbuk", "경상북도",         "Gyeongsangbuk-do"),
    ("gyeongnam", "경상남도",         "Gyeongsangnam-do"),
    ("jeju",      "제주특별자치도",   "Jeju"),
]

# 시/구 (id, province_id, 한글, 영문). 데이터가 있는 서울 구부터.
CITIES = [
    ("jongno",    "seoul", "종로구",   "Jongno-gu"),
    ("seocho",    "seoul", "서초구",   "Seocho-gu"),
    ("seodaemun", "seoul", "서대문구", "Seodaemun-gu"),
    ("gangdong",  "seoul", "강동구",   "Gangdong-gu"),
    ("gangseo",   "seoul", "강서구",   "Gangseo-gu"),
]

# 장소를 가진 원본 한국 작품 6편 (id, 제목ko, 제목en, 요약ko, 요약en)
BASE_WORKS = [
    ("tyrant_chef","폭군의 셰프","Bon Appétit, Your Majesty",
     "미슐랭 3스타 셰프 연지영이 조선으로 타임슬립해 폭군 이헌의 수라간에서 요리하는 판타지 로코 (tvN, 2025).",
     "A Michelin 3-star chef time-slips to Joseon and cooks in a tyrant king's royal kitchen. (tvN, 2025)"),
    ("true_education","참교육","Chamgyoyuk (True Education)",
     "무너진 교권을 지키는 ‘교권보호국’ 감독관 나화진의 이야기. 웹툰 원작 (넷플릭스, 2026).",
     "An inspector from a “Teachers' Rights Bureau” confronts a broken school system. (Netflix, 2026)"),
    ("goblin","도깨비","Goblin (Guardian)",
     "불멸의 도깨비 김신과 그를 볼 수 있는 소녀 지은탁의 판타지 로맨스 (tvN, 2016~2017).",
     "A fantasy romance between an immortal goblin and the girl who can see him. (tvN, 2016–2017)"),
    ("winter_sonata","겨울연가","Winter Sonata",
     "첫사랑의 기억을 둘러싼 멜로드라마. 한류를 세계에 알린 대표작 (KBS, 2002).",
     "A melodrama of first love — a landmark that spread the Korean Wave. (KBS, 2002)"),
    ("true_beauty","여신강림","True Beauty",
     "화장으로 콤플렉스를 감춘 소녀의 학원 로맨스. 동명 웹툰 원작 (tvN, 2020~2021).",
     "A school romance about a girl who hides her insecurities with makeup. (tvN, 2020–2021)"),
    ("red_sleeve","옷소매 붉은 끝동","The Red Sleeve",
     "자신의 삶을 지키려던 궁녀 성덕임과 정조의 궁중 멜로 (MBC, 2021~2022).",
     "A palace melodrama between court lady Seong Deok-im and King Jeongjo. (MBC, 2021–2022)"),
]


# 큐레이션 추가 작품 (장소는 아직 없음 — '동선 준비 중'으로 표시될 작품들).
# (id, 제목ko, 제목en, 요약ko, 요약en). 모두 2024년 이전 확실한 인기작 위주.
CURATED_WORKS = [
    # Netflix
    ("squid_game",     "오징어 게임",       "Squid Game",
     "거액의 상금을 건 의문의 서바이벌 게임에 참가한 사람들의 이야기 (넷플릭스, 2021).",
     "Players risk their lives in deadly children's games for a huge prize. (Netflix, 2021)"),
    ("the_glory",      "더 글로리",         "The Glory",
     "학교폭력 피해자가 가해자들에게 치밀하게 복수하는 드라마 (넷플릭스, 2022).",
     "A bullying survivor enacts a meticulous revenge. (Netflix, 2022)"),
    ("kingdom",        "킹덤",             "Kingdom",
     "조선을 배경으로 한 좀비 사극 스릴러 (넷플릭스, 2019).",
     "A zombie thriller set in Joseon-era Korea. (Netflix, 2019)"),
    ("sweet_home",     "스위트홈",         "Sweet Home",
     "괴물로 변해가는 세상에서 살아남으려는 사람들 (넷플릭스, 2020).",
     "Residents fight to survive as humans turn into monsters. (Netflix, 2020)"),
    ("dp",             "D.P.",            "D.P.",
     "탈영병을 잡는 군무 이탈 체포조의 이야기 (넷플릭스, 2021).",
     "A military unit hunts down army deserters. (Netflix, 2021)"),
    ("hellbound",      "지옥",             "Hellbound",
     "지옥행을 선고받는 초자연적 현상과 사회의 혼란 (넷플릭스, 2021).",
     "Supernatural beings condemn people to hell, shaking society. (Netflix, 2021)"),
    ("all_of_us_dead", "지금 우리 학교는",  "All of Us Are Dead",
     "좀비 사태가 벌어진 고등학교에서 살아남으려는 학생들 (넷플릭스, 2022).",
     "Students trapped in a school during a zombie outbreak. (Netflix, 2022)"),
    ("mask_girl",      "마스크걸",         "Mask Girl",
     "외모 콤플렉스를 가진 여성을 둘러싼 미스터리 스릴러 (넷플릭스, 2023).",
     "A mystery thriller around a woman with appearance complexes. (Netflix, 2023)"),
    ("celebrity",      "셀러브리티",       "Celebrity",
     "인플루언서 세계의 욕망과 이면을 그린 드라마 (넷플릭스, 2023).",
     "A drama exposing the glamour and dark side of influencers. (Netflix, 2023)"),
    # tvN (TVING)
    ("crash_landing",  "사랑의 불시착",     "Crash Landing on You",
     "사고로 북한에 불시착한 재벌 상속녀와 북한 장교의 로맨스 (tvN, 2019).",
     "An heiress crash-lands in North Korea and falls for an officer. (tvN, 2019)"),
    ("reply_1988",     "응답하라 1988",     "Reply 1988",
     "1988년 서울 쌍문동 골목, 다섯 가족의 따뜻한 이야기 (tvN, 2015).",
     "A warm tale of five families in a 1988 Seoul neighborhood. (tvN, 2015)"),
    ("hospital_playlist","슬기로운 의사생활", "Hospital Playlist",
     "의대 동기 다섯 의사의 일과 우정을 그린 드라마 (tvN, 2020).",
     "Five doctor friends balance work, life and friendship. (tvN, 2020)"),
    ("mr_sunshine",    "미스터 션샤인",     "Mr. Sunshine",
     "구한말을 배경으로 한 의병과 사랑의 대서사 (tvN, 2018).",
     "An epic of love and patriots in late-19th-century Korea. (tvN, 2018)"),
    ("vincenzo",       "빈센조",           "Vincenzo",
     "이탈리아 마피아 변호사가 한국에서 악당을 응징하는 이야기 (tvN, 2021).",
     "A mafia lawyer takes on villains in Korea. (tvN, 2021)"),
    ("twenty_five",    "스물다섯 스물하나",  "Twenty-Five Twenty-One",
     "IMF 시절 펜싱 소녀와 청년의 청춘 멜로 (tvN, 2022).",
     "A coming-of-age romance set during the IMF crisis era. (tvN, 2022)"),
    # KBS
    ("descendants_of_sun","태양의 후예",    "Descendants of the Sun",
     "군인과 의사의 사랑을 그린 멜로드라마 (KBS, 2016).",
     "A romance between a soldier and a doctor. (KBS, 2016)"),
    ("camellia",       "동백꽃 필 무렵",    "When the Camellia Blooms",
     "편견에 맞서 사는 싱글맘 동백과 순박한 경찰의 이야기 (KBS, 2019).",
     "A single mom and an earnest cop face down prejudice. (KBS, 2019)"),
    ("baker_king",     "제빵왕 김탁구",     "Baker King, Kim Takgu",
     "역경을 딛고 최고의 제빵사가 되는 김탁구의 성장기 (KBS, 2010).",
     "An underdog rises to become a master baker. (KBS, 2010)"),
    # MBC
    ("w_two_worlds",   "더블유",           "W: Two Worlds",
     "웹툰 속 세계와 현실을 오가는 판타지 로맨스 (MBC, 2016).",
     "A fantasy romance crossing between a webtoon world and reality. (MBC, 2016)"),
    ("dae_jang_geum",  "대장금",           "Dae Jang Geum",
     "수라간 궁녀에서 어의가 된 장금의 사극 (MBC, 2003).",
     "A palace cook rises to become the king's physician. (MBC, 2003)"),
    ("kill_me_heal_me","킬미 힐미",         "Kill Me, Heal Me",
     "다중인격을 가진 재벌 3세와 정신과 의사의 로맨스 (MBC, 2015).",
     "An heir with multiple personalities and his psychiatrist. (MBC, 2015)"),
    # Disney+
    ("moving",         "무빙",             "Moving",
     "초능력을 숨기고 사는 아이들과 부모 세대의 이야기 (디즈니+, 2023).",
     "Teens and parents hiding superpowers across generations. (Disney+, 2023)"),
    ("big_bet",        "카지노",           "Big Bet",
     "필리핀 카지노 세계에 뛰어든 한 남자의 인생 (디즈니+, 2022).",
     "One man's turbulent life in the Philippine casino world. (Disney+, 2022)"),
    ("connect",        "커넥트",           "Connect",
     "장기밀매 조직에서 탈출한 남자의 추격 스릴러 (디즈니+, 2022).",
     "A man who escaped organ traffickers hunts a killer. (Disney+, 2022)"),
    ("grid",           "그리드",           "Grid",
     "인류를 보호하는 미스터리한 방어막을 둘러싼 SF 스릴러 (디즈니+, 2022).",
     "An SF thriller around a mysterious shield protecting humanity. (Disney+, 2022)"),
    # TVING 오리지널
    ("yumi_cells",     "유미의 세포들",     "Yumi's Cells",
     "머릿속 세포들의 시점으로 그린 직장인 유미의 연애 (TVING, 2021).",
     "Office worker Yumi's love life told through her brain cells. (TVING, 2021)"),
    ("drink_now",      "술꾼도시여자들",     "Work Later, Drink Now",
     "술을 사랑하는 세 여성의 우정과 일상 (TVING, 2021).",
     "Three women who love drinking navigate life and friendship. (TVING, 2021)"),
]

# OTT만 노출(타깃=외국인은 OTT로 시청). 원 방송사(tvN·KBS·MBC 등)는 노출하지 않고,
# 작품을 '공개된 OTT'로 매핑한다. kind는 모두 ott.
PLATFORMS = [
    ("netflix", "넷플릭스", "Netflix", "ott"),
    ("tving",   "티빙",     "TVING",   "ott"),
    ("disney",  "디즈니+",  "Disney+", "ott"),
    ("wavve",   "웨이브",   "Wavve",   "ott"),
]

# 작품 → 공개 OTT. '제작사 계열 → 대표 OTT'로 결정적 매핑.
#   CJ ENM(tvN 등) → 티빙 / 지상파(KBS·MBC·SBS) → 웨이브 / 넷플릭스·디즈니 오리지널 → 각자.
# (해외에선 일부 작품을 넷플릭스로도 볼 수 있으나 국가별로 달라 검증 어려움 — 발표 전 확인 권장)
WORK_PLATFORM = {
    # 장소 보유 6편 (원 채널 → OTT)
    "tyrant_chef":    ["tving"],    # tvN → 티빙
    "true_education": ["netflix"],
    "goblin":         ["tving"],    # tvN → 티빙
    "winter_sonata":  ["wavve"],    # KBS → 웨이브
    "true_beauty":    ["tving"],    # tvN → 티빙
    "red_sleeve":     ["wavve"],    # MBC → 웨이브
    # Netflix 오리지널
    "squid_game": ["netflix"], "the_glory": ["netflix"], "kingdom": ["netflix"],
    "sweet_home": ["netflix"], "dp": ["netflix"], "hellbound": ["netflix"],
    "all_of_us_dead": ["netflix"], "mask_girl": ["netflix"], "celebrity": ["netflix"],
    # tvN → 티빙
    "crash_landing": ["tving"], "reply_1988": ["tving"], "hospital_playlist": ["tving"],
    "mr_sunshine": ["tving"], "vincenzo": ["tving"], "twenty_five": ["tving"],
    # 지상파 → 웨이브
    "descendants_of_sun": ["wavve"], "camellia": ["wavve"], "baker_king": ["wavve"],
    "w_two_worlds": ["wavve"], "dae_jang_geum": ["wavve"], "kill_me_heal_me": ["wavve"],
    # Disney+
    "moving": ["disney"], "big_bet": ["disney"], "connect": ["disney"], "grid": ["disney"],
    # TVING 오리지널
    "yumi_cells": ["tving"], "drink_now": ["tving"],
}

# 연예인 (id, 한글, 영문, 종류). kind: actor | idol
PERSONS = [
    ("gongyoo",    "공유",   "Gong Yoo",      "actor"),
    ("kimgoeun",   "김고은", "Kim Go-eun",    "actor"),
    ("leedongwook","이동욱", "Lee Dong-wook", "actor"),
    ("baeyongjoon","배용준", "Bae Yong-joon", "actor"),
    ("choijiwoo",  "최지우", "Choi Ji-woo",   "actor"),
    ("moongayoung","문가영", "Moon Ga-young", "actor"),
    ("chaeunwoo",  "차은우", "Cha Eun-woo",   "idol"),   # 아스트로
    ("leejunho",   "이준호", "Lee Jun-ho",    "idol"),   # 2PM
    ("leeseyoung", "이세영", "Lee Se-young",  "actor"),
    ("yoona",      "임윤아", "YoonA",         "idol"),   # 소녀시대
    ("leechaemin", "이채민", "Lee Chae-min",  "actor"),
    # 큐레이션 작품 주연(고확신)
    ("leejungjae", "이정재", "Lee Jung-jae",  "actor"),
    ("songhyekyo", "송혜교", "Song Hye-kyo",  "actor"),
    ("songjoongki","송중기", "Song Joong-ki", "actor"),
    ("hyunbin",    "현빈",   "Hyun Bin",      "actor"),
    ("sonyejin",   "손예진", "Son Ye-jin",    "actor"),
    ("chojungseok","조정석", "Cho Jung-seok", "actor"),
    ("leebyunghun","이병헌", "Lee Byung-hun", "actor"),
    ("kimtaeri",   "김태리", "Kim Tae-ri",    "actor"),
    ("namjoohyuk", "남주혁", "Nam Joo-hyuk",  "actor"),
    ("leesungmin", "이성민", "Lee Sung-min",  "actor"),
    ("hanhyojoo",  "한효주", "Han Hyo-joo",   "actor"),
    ("leejongsuk", "이종석", "Lee Jong-suk",  "actor"),
    ("leeyoungae", "이영애", "Lee Young-ae",  "actor"),
    ("jisung",     "지성",   "Ji Sung",       "actor"),
]

# 작품 → 출연 연예인.
WORK_PERSON = {
    # 장소 보유 6편
    "goblin":        ["gongyoo", "kimgoeun", "leedongwook"],
    "winter_sonata": ["baeyongjoon", "choijiwoo"],
    "true_beauty":   ["moongayoung", "chaeunwoo"],
    "red_sleeve":    ["leejunho", "leeseyoung"],
    "tyrant_chef":   ["yoona", "leechaemin"],   # 2025작 — 발표 전 확인 권장
    "true_education":[],
    # 큐레이션
    "squid_game":         ["leejungjae"],
    "the_glory":          ["songhyekyo"],
    "crash_landing":      ["hyunbin", "sonyejin"],
    "hospital_playlist":  ["chojungseok"],
    "mr_sunshine":        ["leebyunghun", "kimtaeri"],
    "twenty_five":        ["kimtaeri", "namjoohyuk"],
    "descendants_of_sun": ["songjoongki", "songhyekyo"],
    "vincenzo":           ["songjoongki"],
    "moving":             ["leesungmin", "hanhyojoo"],
    "w_two_worlds":       ["leejongsuk"],
    "big_bet":            ["leejongsuk"],
    "dae_jang_geum":      ["leeyoungae"],
    "kill_me_heal_me":    ["jisung"],
}

# 작품 인기순(수동 큐레이션, 클수록 위. '공식 순위' 아님 — 정렬용).
POPULARITY = {
    # 장소 보유 6편
    "goblin": 96, "winter_sonata": 70, "true_beauty": 78,
    "red_sleeve": 80, "tyrant_chef": 74, "true_education": 60,
    # Netflix
    "squid_game": 100, "the_glory": 95, "kingdom": 88, "sweet_home": 84,
    "dp": 86, "hellbound": 82, "all_of_us_dead": 85, "mask_girl": 79, "celebrity": 72,
    # tvN/TVING
    "crash_landing": 97, "reply_1988": 92, "hospital_playlist": 90,
    "mr_sunshine": 89, "vincenzo": 87, "twenty_five": 83,
    # KBS
    "descendants_of_sun": 91, "camellia": 81, "baker_king": 68,
    # MBC
    "w_two_worlds": 77, "dae_jang_geum": 88, "kill_me_heal_me": 73,
    # Disney+
    "moving": 93, "big_bet": 76, "connect": 66, "grid": 62,
    # TVING
    "yumi_cells": 75, "drink_now": 71,
}


# 장소(원본 7 + 검증된 서울 촬영지 7). city=시/구, sort=동선 내 정렬, links=(작품, 해설ko, 해설en).
# 촬영지 출처: 서울시 미디어허브/나무위키 등 공개자료. 일부는 커뮤니티 기반(stop_ko에 '검토' 표기).
PLACES = [
    {"place_id":"sojubang","city":"jongno","sort":1,
     "name_ko":"경복궁 소주방(수라간 권역)","name_en":"Sojubang Royal Kitchen, Gyeongbokgung",
     "area_ko":"서울 종로구 사직로 161, 경복궁 내","area_en":"Inside Gyeongbokgung, Jongno-gu, Seoul",
     "map_query":"경복궁","stop_ko":"세계관 원형","stop_en":"World-setting model",
     "visit_ko":"경복궁 입장 시 상시 관람 (수라간 시식 체험은 비정기)","visit_en":"Viewable with palace entry (tasting program seasonal)",
     "theme_ko":"궁중음식·한정식, (시즌) 수라간 시식공감, 한복 입고 경복궁","theme_en":"Royal court cuisine, (seasonal) Suragan tasting, hanbok for free entry",
     "story_ko":"조선 왕의 수라(식사)를 마련하던 궁궐 부엌입니다. 내소주방(일상식)·외소주방(잔치)·생물방(다과)으로 나뉘었고, 대령숙수가 일했으며 왕은 하루 다섯 번(영조실록) 식사해 저녁은 12첩 반상이었습니다. 1915년 헐렸다가 2011~2015년 복원됐습니다.",
     "story_en":"The palace kitchen for the Joseon king's meals. It had three parts (everyday, banquet, snacks); a male chef called daeryeong-suksu worked here, and the king ate five times a day with a famous 12-dish dinner. Demolished in 1915, restored in 2011–2015.",
     "links":[("tyrant_chef",
       "드라마에서 연지영이 일하던 그 수라간 — 실제 모델이 바로 여기 경복궁 소주방이에요. 요리 경합은 상상이지만, 이 부엌에서 매일 임금의 수라가 차려졌다는 건 실제랍니다.",
       "The royal kitchen where Yeon Ji-yeong worked — its real model is right here. The cooking battles are fiction, but the king's daily meals were truly made in this kitchen.")]},

    {"place_id":"gyeonghoeru","city":"jongno","sort":2,
     "name_ko":"경복궁 경회루","name_en":"Gyeonghoeru Pavilion, Gyeongbokgung",
     "area_ko":"서울 종로구 경복궁 내, 서쪽 연못 위 누각","area_en":"Pavilion on the pond, west of Gyeongbokgung, Seoul",
     "map_query":"경복궁 경회루","stop_ko":"세계관 원형","stop_en":"World-setting model",
     "visit_ko":"외부 상시 관람 / 2층 내부는 봄·가을 사전예약 특별관람","visit_en":"Exterior anytime; 2nd floor by seasonal reservation",
     "theme_ko":"(시즌) 경회루 2층 특별관람, 경복궁 야간개장·별빛야행, 한복 사진","theme_en":"(Seasonal) 2nd-floor tour, night opening / Starlight Tour, hanbok photos",
     "story_ko":"경복궁 서쪽 연못 위 2층 누각으로, 나라의 경사·외국 사신 접대·왕실 잔치의 공식 연회장이었습니다. 태종 12년(1412) 크게 짓고 임진왜란 소실 뒤 1867년 중건, 1985년 국보 제224호로 지정됐습니다.",
     "story_en":"A two-story pavilion on the pond, the royal banquet hall for state celebrations and envoy receptions. Greatly rebuilt in 1412, reconstructed in 1867, and designated National Treasure No. 224 in 1985.",
     "links":[("tyrant_chef",
       "드라마 속 화려한 궁중 연회와 요리 경합 — 그런 잔치가 실제로 펼쳐지던 왕실 최고의 연회장이에요. 연못 위에 떠 있는 듯한 이 누각에서 궁중 잔치의 무대를 마주하게 됩니다.",
       "The lavish court banquets in the drama really took place here, the royal family's grandest banquet hall. By this pavilion floating on its pond, you face the real stage of those feasts.")]},

    {"place_id":"ungyeong","city":"jongno","sort":3,
     "name_ko":"운경고택","name_en":"Ungyeong Old House",
     "area_ko":"서울 종로구 인왕산로 7 (사직동)","area_en":"7 Inwangsan-ro, Jongno-gu, Seoul",
     "map_query":"서울 종로구 인왕산로 7","stop_ko":"세계관 연결 (검토)","stop_en":"World-setting link (under review)",
     "visit_ko":"사전 예약제 · 입장료 1만원 · 11~17시 · 월·화 휴관","visit_en":"Reservation · 10,000 won · 11:00–17:00 · closed Mon/Tue",
     "theme_ko":"한복 대여 후 사직단·서촌 골목 산책, 서촌 한옥 전통찻집","theme_en":"Hanbok walk around Sajikdan and Seochon, hanok teahouse",
     "story_ko":"인왕산·사직단을 내려다보는 전통 서울식 한옥입니다. 조선 ‘도정궁’ 터로 전해지며(선조 생부 덕흥대원군과 연결), 광복 후 운경 이재형이 1953년부터 거주, 2019년 공개됐습니다.",
     "story_en":"A traditional Seoul hanok overlooking Mt. Inwangsan. Said to stand on the former “Dojeonggung” site tied to King Seonjo's birth father; later home to Lee Jae-hyung from 1953, open to the public since 2019.",
     "links":[("tyrant_chef",
       "이 한옥의 ‘터’엔 조선 왕실 이야기가 깔려 있어요. 옛 도정궁 자리라, ‘폭군의 셰프’가 그린 궁중 세계를 실제 왕실과 닿은 이 땅에서 떠올려볼 수 있죠. (※촬영지 여부는 공식 미확인.)",
       "This hanok stands on ground tied to the Joseon royal family — the old Dojeonggung site. So you can picture the drama's royal world here. (Filming here is not officially confirmed.)")]},

    {"place_id":"jungang_hs","city":"jongno","sort":4,
     "name_ko":"서울 중앙고등학교","name_en":"Jungang High School, Gyedong",
     "area_ko":"서울 종로구 계동 (북촌, 안국역 인근)","area_en":"Gyedong, Jongno-gu (Bukchon, near Anguk Stn.)",
     "map_query":"서울중앙고등학교","stop_ko":"실제 촬영지","stop_en":"Filming site",
     "visit_ko":"운영 중인 학교 — 평일 출입 제한, 외부 관람 위주, 방문 전 확인","visit_en":"A working school — weekday entry restricted; view the exterior",
     "theme_ko":"북촌한옥마을·계동길 산책, K-드라마 성지 둘러보기","theme_en":"Stroll Bukchon and Gyedong-gil, K-drama pilgrimage spots",
     "story_ko":"1917년 계동에 세운 사립학교로, 본관·동관·서관이 각각 국가 사적(제281·282·283호)입니다. 1934년 화재 후 건축가 박동진이 고딕풍 석조로 재건해 한국 근대학교 건축의 대표작으로 꼽힙니다.",
     "story_en":"A private school founded in Gyedong in 1917; its three halls are National Historic Sites (Nos. 281–283). After a 1934 fire it was rebuilt in Gothic-style stone by architect Bak Dong-jin — a landmark of modern Korean school architecture.",
     "links":[
       ("true_education","넷플릭스 ‘참교육’ 속 ‘진원고등학교’ 장면(9~10화)을 촬영한 곳이에요. 무너진 학교를 다루는 드라마지만, 정작 이 건물은 한 세기 가까이 학생을 길러 온 진짜 학교랍니다.",
        "Filmed as “Jinwon High” in the Netflix drama Chamgyoyuk (eps 9–10). The show is about a broken school, yet this building has raised students for nearly a century."),
       ("goblin","‘도깨비’에서 지은탁(김고은)이 다니던 고등학교가 바로 여기예요. 도깨비를 부르던 그 학창시절 무대죠.",
        "This is the high school Ji Eun-tak attends in “Goblin” — the very campus of those school-day scenes."),
       ("winter_sonata","한류 1세대 ‘겨울연가’ 속 준상·유진의 학창시절을 촬영한 곳이에요. 일본을 비롯해 아시아 팬들이 찾던 성지죠.",
        "A filming spot for the school days in “Winter Sonata,” the first-generation Korean Wave hit — long a pilgrimage site for Asian fans."),
       ("true_beauty","웹툰 원작 ‘여신강림’ 속 학교 장면도 이 고풍스러운 교사에서 찍었어요.",
        "The school scenes of the webtoon-based “True Beauty” were also shot at this elegant old campus.")]},

    {"place_id":"bukchon","city":"jongno","sort":5,
     "name_ko":"북촌한옥마을","name_en":"Bukchon Hanok Village",
     "area_ko":"서울 종로구 계동·가회동 일대 (안국역 인근)","area_en":"Gyedong/Gahoe-dong, Jongno-gu (near Anguk Stn.)",
     "map_query":"북촌한옥마을","stop_ko":"실제 촬영지","stop_en":"Filming site",
     "visit_ko":"상시 개방 (주민 거주지 — 정숙 관람)","visit_en":"Open anytime (a residential area — please keep quiet)",
     "theme_ko":"한복 입고 한옥 골목 산책, 전통 공방·찻집","theme_en":"Hanbok stroll through hanok alleys, craft workshops and teahouses",
     "story_ko":"경복궁·창덕궁·종묘 사이 언덕에 조선시대 양반 가옥이 밀집한 전통 한옥 지구입니다. 지금의 한옥 골목은 주로 1930년대에 형성됐고, ‘살아있는 거리 박물관’으로 불립니다. 좁은 골목과 기와지붕 덕에 수많은 드라마·화보의 배경이 됩니다.",
     "story_en":"A district of densely packed traditional hanok between the palaces and Jongmyo. Today's hanok clusters largely took shape in the 1930s, and it's often called a living street museum. Its alleys and tiled roofs are a backdrop for countless dramas.",
     "links":[("goblin",
       "‘도깨비’에서 김신과 은탁이 거닐던 북촌 골목 — 특히 가회동 31번지 일대가 유명해요. 한옥 담장을 따라 걷는 그 데이트 장면의 배경이죠. 세트가 아니라 사람이 실제로 사는 동네라, 골목 자체가 살아있는 무대랍니다.",
       "The Bukchon alleys where Kim Shin and Eun-tak walk in “Goblin” — the Gahoe-dong 31 area is especially famous. Not a film set but a living neighborhood, so the lanes themselves are the stage.")]},

    {"place_id":"changdeok_huwon","city":"jongno","sort":6,
     "name_ko":"창덕궁 후원","name_en":"Changdeokgung Secret Garden (Huwon)",
     "area_ko":"서울 종로구 율곡로 99, 창덕궁 뒤편","area_en":"99 Yulgok-ro, behind Changdeokgung, Jongno-gu",
     "map_query":"창덕궁 후원","stop_ko":"실제 촬영지·궁궐","stop_en":"Filming site · palace",
     "visit_ko":"후원은 제한관람 — 해설사 동반, 선착순 예약, 회차당 인원 제한","visit_en":"Rear garden: guided limited tours only — reserve ahead, capped size",
     "theme_ko":"해설사 동반 후원 산책, 한복 입고 경복궁·창덕궁 ‘두 궁’ 함께 관람","theme_en":"Guided garden walk, hanbok for a two-palaces day",
     "story_ko":"1405년 태종 때 처음 지은 궁궐로 유네스코 세계유산(1997)입니다. 경복궁이 웅장한 정궁이라면 창덕궁은 아늑한 궁궐로, 그 뒤편 ‘후원(비원)’은 자연 지형을 살려 연못과 정자를 배치한 한국 전통 조경의 백미입니다. 후원은 해설사 동반 제한관람으로만 들어갈 수 있습니다.",
     "story_en":"A palace first built in 1405, a UNESCO World Heritage Site (1997). Its rear garden (Huwon/Biwon) is a masterpiece of Korean landscaping, with ponds and pavilions set into the natural terrain, accessible only by guided, limited tours.",
     "links":[("red_sleeve",
       "‘옷소매 붉은 끝동’에서 궁녀 성덕임이 연못가를 뛰어다니던 장면, 영조와 이산(정조)의 낚시 장면을 바로 이 후원 ‘부용지’에서 찍었어요. 드라마 속 조용한 궁중의 순간들이 펼쳐진 실제 무대랍니다.",
       "In “The Red Sleeve,” court lady Seong Deok-im runs by the pond, and the kings fish — all filmed here at the Buyongji pond. It's the real stage behind the drama's quiet royal moments.")]},

    {"place_id":"gwangjang","city":"jongno","sort":7,
     "name_ko":"광장시장","name_en":"Gwangjang Market",
     "area_ko":"서울 종로구 창경궁로 88 (종로5가)","area_en":"88 Changgyeonggung-ro, Jongno-gu (Jongno 5-ga)",
     "map_query":"광장시장","stop_ko":"실제 촬영지·먹거리","stop_en":"Filming site · food",
     "visit_ko":"상시 개방 (점포 영업시간 상이, 식사 시간대 혼잡)","visit_en":"Open daily (stall hours vary; busy at mealtimes)",
     "theme_ko":"마약김밥·육회·빈대떡 맛보기, 손칼국수 골목, 청계천 산책","theme_en":"Try mayak gimbap, yukhoe, bindaetteok; the hand-cut noodle alley; stroll Cheonggyecheon",
     "story_ko":"1905년 무렵 ‘배오개 시장’에서 출발한 서울의 대표 전통시장으로, 100년이 넘었습니다. 빈대떡·마약김밥·육회·칼국수 같은 길거리 음식으로 유명해, 외국인 미식 여행자들이 몰리는 명소입니다.",
     "story_en":"One of Seoul's oldest markets, rooted in the early-1900s Baeogae market — over a century old. Famous for street foods, it's a magnet for foreign foodies.",
     "links":[]},

    {"place_id":"sewoon","city":"jongno","sort":9,
     "name_ko":"세운상가 (세운청계상가)","name_en":"Sewoon Sangga",
     "area_ko":"서울 종로구 청계천로 159","area_en":"159 Cheonggyecheon-ro, Jongno-gu, Seoul",
     "map_query":"세운상가","stop_ko":"실제 촬영지","stop_en":"Filming site",
     "visit_ko":"상시 개방 (상가 영업시간 상이)","visit_en":"Open daily (shop hours vary)",
     "theme_ko":"세운옥상 전망, 청계천·을지로 골목 탐방","theme_en":"Rooftop view, Cheonggyecheon & Euljiro alleys",
     "story_ko":"1968년 지은 국내 최초의 주상복합·종합 전자상가로, 건축가 김수근이 설계했습니다. 지금도 작은 가게들이 영업하며 청계·대림상가와 이어집니다.",
     "story_en":"Korea's first mixed-use electronics arcade (1968), designed by Kim Swoo-geun; small shops still operate, linked to the Cheonggye and Daerim arcades.",
     "links":[("vincenzo",
       "‘빈센조’ 속 ‘금가프라자’가 바로 이 세운상가예요. 빈센조와 금가프라자 식구들이 얽히던 낡고 정겨운 상가 건물이 실제 이곳입니다.",
       "The “Geumga Plaza” in Vincenzo is this very Sewoon Sangga — the worn, characterful arcade where Vincenzo and its tenants tangle.")]},

    {"place_id":"yangjae_stn","city":"seocho","sort":10,
     "name_ko":"양재시민의숲역","name_en":"Yangjae Citizens' Forest Stn.",
     "area_ko":"서울 서초구 (신분당선)","area_en":"Seocho-gu, Seoul (Sinbundang Line)",
     "map_query":"양재시민의숲역","stop_ko":"실제 촬영지","stop_en":"Filming site",
     "visit_ko":"지하철역 — 상시","visit_en":"Subway station — anytime",
     "theme_ko":"양재시민의숲 산책, 매헌 윤봉길의사기념관","theme_en":"Yangjae Citizens' Forest walk, Maeheon memorial",
     "story_ko":"신분당선 지하철역으로, 일대에 양재시민의숲이 넓게 펼쳐져 있습니다.",
     "story_en":"A Sinbundang Line subway station beside the leafy Yangjae Citizens' Forest.",
     "links":[("squid_game",
       "‘오징어 게임’의 시작을 알린 딱지치기 장면 — 기훈이 정체불명의 남자에게 딱지치기를 권유받던 지하철 승강장이 이곳으로 소개됐어요. (※서울시 미디어허브 기준)",
       "The ddakji (paper-flip) scene that opens Squid Game — the platform where Gi-hun is recruited is featured here. (per Seoul city media)")]},

    {"place_id":"pagoda_baduk","city":"jongno","sort":11,
     "name_ko":"파고다기원 (종로3가)","name_en":"Pagoda Baduk Club (Jongno 3-ga)",
     "area_ko":"서울 종로구 종로3가","area_en":"Jongno 3-ga, Jongno-gu, Seoul",
     "map_query":"파고다기원","stop_ko":"실제 촬영지","stop_en":"Filming site",
     "visit_ko":"기원 영업시간 확인 후 방문","visit_en":"Check the baduk club's hours",
     "theme_ko":"탑골공원·종로3가, 익선동 한옥거리","theme_en":"Tapgol Park & Jongno 3-ga, Ikseon-dong hanok street",
     "story_ko":"종로3가의 오래된 바둑 기원으로, 어르신들이 모여 바둑을 두는 서울의 옛 정취가 남은 곳입니다.",
     "story_en":"An old baduk (Go) club in Jongno 3-ga, keeping the city's old-time atmosphere.",
     "links":[("the_glory",
       "‘더 글로리’에서 문동은이 하도영에게 접근하려 바둑을 두던 기원이 이곳으로 알려져 있어요. 복수극의 결정적 인연이 시작되는 장면의 배경이죠.",
       "The baduk club where Moon Dong-eun approaches Ha Do-yeong in The Glory — where a pivotal tie in her revenge begins.")]},

    {"place_id":"unhyeon_yanggwan","city":"jongno","sort":8,
     "name_ko":"운현궁 양관 (도깨비 집)","name_en":"Unhyeongung Yanggwan",
     "area_ko":"서울 종로구 (덕성여대 종로캠퍼스 내)","area_en":"Inside Duksung Women's Univ. Jongno campus, Seoul",
     "map_query":"운현궁 양관","stop_ko":"실제 촬영지","stop_en":"Filming site",
     "visit_ko":"대학 캠퍼스 내 — 외관 위주 관람, 방문 전 확인","visit_en":"On a university campus — exterior viewing; check first",
     "theme_ko":"운현궁·삼일대로, 인사동·익선동","theme_en":"Unhyeongung, Insa-dong, Ikseon-dong",
     "story_ko":"1912년경 지은 서양식 건물로 일본인 건축가 가타야마 도쿠마가 설계했습니다. 아치형 구조와 베란다, 대한제국 황실의 이화 문양이 남아 있고 현재 덕성여대 종로캠퍼스 안에 있습니다.",
     "story_en":"A Western-style building from c.1912 designed by Katayama Tokuma — arches, verandas and Korean Empire plum-blossom emblems; now inside Duksung Women's University's Jongno campus.",
     "links":[("goblin",
       "‘도깨비’에서 김신(공유)이 살던 저택의 외관이 바로 이 운현궁 양관이에요. 불멸의 도깨비가 머물던 고풍스러운 집의 실제 모습이죠.",
       "The exterior of Kim Shin's mansion in Goblin is this very Unhyeongung Yanggwan — the real face of the immortal goblin's elegant home.")]},

    {"place_id":"chungjeong_apt","city":"seodaemun","sort":12,
     "name_ko":"충정아파트 (스위트홈 ‘그린홈’)","name_en":"Chungjeong Apartments (Sweet Home)",
     "area_ko":"서울 서대문구 충정로 30","area_en":"30 Chungjeong-ro, Seodaemun-gu, Seoul",
     "map_query":"충정아파트","stop_ko":"실제 촬영지","stop_en":"Filming site",
     "visit_ko":"주민 거주 건물 — 외관만 관람, 정숙","visit_en":"A residential building — exterior only, please be quiet",
     "theme_ko":"충정로·서대문 일대, 경교장","theme_en":"Chungjeong-ro & Seodaemun area, Gyeonggyojang",
     "story_ko":"1930년 무렵 지어진 한국에서 가장 오래된 아파트 중 하나로, 서울시 미래유산으로 지정됐습니다.",
     "story_en":"One of Korea's oldest apartment buildings (c.1930), designated a Seoul Future Heritage site.",
     "links":[("sweet_home",
       "‘스위트홈’의 무대 ‘그린홈’ 외관이 바로 이 충정아파트예요. 괴물과 맞서던 낡은 아파트의 음산한 분위기가 실제 이 오래된 건물에서 나왔죠.",
       "The “Green Home” of Sweet Home is this Chungjeong Apartments — the eerie old block where residents face monsters.")]},

    {"place_id":"ewha_seoul_hosp","city":"gangseo","sort":13,
     "name_ko":"이대서울병원 (‘율제병원’)","name_en":"Ewha Womans Univ. Seoul Hospital",
     "area_ko":"서울 강서구 마곡","area_en":"Magok, Gangseo-gu, Seoul",
     "map_query":"이대서울병원","stop_ko":"실제 촬영지","stop_en":"Filming site",
     "visit_ko":"운영 중인 병원 — 로비 등 공용공간 위주, 진료 방해 금지","visit_en":"A working hospital — public areas only; do not disturb care",
     "theme_ko":"마곡·서울식물원 일대","theme_en":"Magok area & Seoul Botanic Park",
     "story_ko":"서울 강서구 마곡에 있는 대형 종합병원으로 2019년 개원했습니다.",
     "story_en":"A large general hospital in Magok, Gangseo-gu, opened in 2019.",
     "links":[("hospital_playlist",
       "‘슬기로운 의사생활’ 속 ‘율제병원’ 로비·정원 장면을 이곳 이대서울병원에서 찍었어요. 다섯 의사의 일상이 펼쳐지던 병원의 실제 모습이죠.",
       "The lobby and garden of “Yulje Hospital” in Hospital Playlist were filmed here — the real face of the five doctors' workplace.")]},

    {"place_id":"jeongwon_hs","city":"gangdong","sort":14,
     "name_ko":"정원고등학교 (무빙) — 상일여고","name_en":"“Jeongwon High” (Moving) — Sangil Girls' HS",
     "area_ko":"서울 강동구 상일동","area_en":"Sangil-dong, Gangdong-gu, Seoul",
     "map_query":"상일여자고등학교","stop_ko":"실제 촬영지 (검토)","stop_en":"Filming site (under review)",
     "visit_ko":"운영 중인 학교 — 외부 관람 위주, 방문 전 확인","visit_en":"A working school — view exterior; check first",
     "theme_ko":"고덕·상일동 일대 산책","theme_en":"Stroll around Godeok / Sangil-dong",
     "story_ko":"강동구 상일동의 고등학교로, 디즈니+ ‘무빙’ 속 ‘정원고등학교’ 배경으로 알려져 있습니다.",
     "story_en":"A high school in Sangil-dong, reported as the model for “Jeongwon High” in Disney+'s Moving.",
     "links":[("moving",
       "초능력을 숨긴 아이들이 다니던 ‘정원고’ — 극 중 지도에 표시된 위치가 이 학교로 알려져 있어요. (※커뮤니티 기반 — 발표 전 확인 권장)",
       "“Jeongwon High,” where the kids hiding superpowers attend — reported from an in-show map. (Community-sourced; verify before the demo.)")]},
]

# 기존 장소에 작품 추가 연결: (place_id, work_id, story_ko, story_en)
EXTRA_PLACE_WORK = [
    ("changdeok_huwon", "kingdom",
     "넷플릭스 ‘킹덤’도 이 창덕궁 일대(후원 관람정 등)에서 사극 장면을 촬영했어요. 조선 궁궐을 배경으로 한 좀비 사극의 무대가 실제 이 궁이었죠.",
     "Netflix's Kingdom also filmed palace scenes around Changdeokgung (incl. the Gwallamjeong pavilion in the rear garden) — the real stage of its Joseon zombie saga."),
]
