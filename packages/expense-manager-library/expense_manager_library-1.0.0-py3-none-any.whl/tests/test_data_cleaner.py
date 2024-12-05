import unittest
import os
import pandas as pd
from expense_manager_library.data_cleaner import categorize_transactions

class TestCategorizeTransactions(unittest.TestCase):
    def setUp(self):
        """테스트에 필요한 임시 데이터 생성"""
        self.input_csv = "test_input.csv"
        self.test_data = """날짜,거래처,금액
        20240404,스타벅스,4500
        20240405,육앤샤,12000
        20240406,버스,1250
        20240407,CU,3000
        """
        with open(self.input_csv, "w", encoding="utf-8") as f:
            f.write(self.test_data)
        
        self.results_dir = "test_results"
        self.expected_data = pd.DataFrame({
            "날짜": ["20240404", "20240405", "20240406", "20240407"],
            "거래처": ["스타벅스", "육앤샤", "버스", "CU"],
            "금액": [4500, 12000, 1250, 3000],
            "카테고리": ["카페/간식", "식비", "교통", "편의점, 마트"]
        })

    def tearDown(self):
        """테스트 후 파일 및 디렉토리 삭제"""
        if os.path.exists(self.input_csv):
            os.remove(self.input_csv)
        if os.path.exists(self.results_dir):
            for file in os.listdir(self.results_dir):
                os.remove(os.path.join(self.results_dir, file))
            os.rmdir(self.results_dir)

    def test_categorize_transactions(self):
        """categorize_transactions 함수 테스트"""
        categorize_transactions(self.input_csv, self.results_dir)
        output_csv = os.path.join(self.results_dir, "classified_data.csv")
        self.assertTrue(os.path.exists(output_csv), "결과 파일이 생성되지 않았습니다.")
        
        # 결과 데이터 로드
        result_data = pd.read_csv(output_csv)

        # 테스트 데이터에 날짜 추가
        self.expected_data["날짜"] = ["20240404", "20240405", "20240406", "20240407"]

        # 데이터 유형 변환: 날짜를 문자열로 통일
        result_data["날짜"] = result_data["날짜"].astype(str)
        self.expected_data["날짜"] = self.expected_data["날짜"].astype(str)

        # 공백 제거 및 소문자 변환
        result_data["거래처"] = result_data["거래처"].str.strip().str.lower()
        self.expected_data["거래처"] = self.expected_data["거래처"].str.strip().str.lower()

        # 열 순서 정렬
        result_data = result_data[["날짜", "거래처", "금액", "카테고리"]]
        self.expected_data = self.expected_data[["날짜", "거래처", "금액", "카테고리"]]
        
        # 비교
        pd.testing.assert_frame_equal(result_data, self.expected_data, check_like=True)






if __name__ == "__main__":
    unittest.main()
