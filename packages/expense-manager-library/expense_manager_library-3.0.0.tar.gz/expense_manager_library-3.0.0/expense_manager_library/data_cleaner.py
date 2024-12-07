import pandas as pd
import os

# 키워드와 카테고리 정의
CATEGORIES_KEYWORDS = {
    "식비": ["육앤샤", "배달", "푸드", "식당", "마라탕", "서브웨이", "파스타", "솥밥", "우동", "일백집", "고기", "밥", "회", "술", "맥주", "소주", "일식", "중식","양식", "한식", "짜장면", "짬뽕", "치킨", "샐러드", "떡볶이", "족발", "보쌈", "두루치기", "두루정", "용용선생", "분식", "도시락", "햄버거", "피자", "곱창", "소바", "샤브샤브", "팅수육", "국수", "면"],
    "카페/간식": ["스타벅스", "커피", "카페", "빵집", "뚜레쥬르", "베이커리", "투썸", "메가", "쥬시", "쥬씨", "스벅","성심당", "스타벅스", "cafe", "coffee","다방", "아이스크림", "배스킨라빈스", "과자", "케이크", "초코", "파이", "디저트", "젤라또"],
    "교통": ["버스", "바이크", "KTX", "지하철", "택시", "기차", "자전거", "킥보드", "우버", "카카오T", "티맵", "고속도로"],
    "편의점, 마트": ["CU", "세븐일레븐", "GS25", "마트", "편의점", "이마트24", "씨유", "지에스","홈플러스","이케아","IKEA", "다이소", "코스트코"],
    "쇼핑": ["에이블리", "쿠팡", "쇼핑", "서적", "무신사", "카카오선물하기", "지그재그", "옷", "백화점", "쇼핑", "아울렛","yes24","의류", "11번가", "G마켓", "temu"],
    "여가": ["CGV", "영화", "노래방", "PC방", "피씨방", "피시방","PC","아이센스리그","레드버튼", "여가", "시네마", "메가박스", "뮤지컬", "콘서트", "야구", "축구", "배구", "농구", "넷플릭스", "왓챠", "디즈니", "티빙", "웨이브", "게임", "플레이", "play"],
    "의료/건강": ["병원", "내과", "외과", "소아과", "치과", "한의원", "피부과", "산부인과", "정형외과", "비뇨기과", "신경과", "이비인후과", "안과", "정신과", "재활의학과", "가정의학과", "응급실", "약국", "의약품", "처방전", "약", "소염제", "연고", "건강보조제", "비타", "영양제", "오메가3", "프로바이오틱스", "홍삼", "피로회복제", "파스", "밴드", "해열제", "피트니스", "요가", "필라테스", "PT", "헬스", "마사지", "테라피", "건강검진", "혈압계", "체중계", "안마기", "운동기구"]
}

#사용자 지출 내역을 분류하여 결과 파일 저장.
def categorize_transactions(csv_path, results_dir="results"):
    
    
    # 데이터 읽기
    data = pd.read_csv(csv_path)
    data["거래처"] = data["거래처"].str.lower()
    
    # 키워드 매핑
    all_keywords = {keyword.lower(): category for category, keywords in CATEGORIES_KEYWORDS.items() for keyword in keywords}
    
    # 카테고리 분류
    def categorize(usages):
        result = []
        for usage in usages:
            categorized = "기타"  # 기본값
            for keyword, category in all_keywords.items():
                if keyword in usage:
                    categorized = category
                    break
            result.append(categorized)
        return result
    
    data["카테고리"] = categorize(data["거래처"])
    
    # 결과 디렉토리 생성
    os.makedirs(results_dir, exist_ok=True)
    output_path = os.path.join(results_dir, "classified_data.csv")
    
    # 결과 저장
    data.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(f"분류된 파일이 저장되었습니다: {output_path}")
