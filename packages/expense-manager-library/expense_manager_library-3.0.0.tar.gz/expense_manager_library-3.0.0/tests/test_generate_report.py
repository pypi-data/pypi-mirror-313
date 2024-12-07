import unittest
import pandas as pd
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from expense_manager_library.report_generator import generate_report

class TestGenerateReport(unittest.TestCase):

    # 테스트용 데이터 
    def setUp(self):
        self.data = pd.DataFrame({
            "카테고리": ["교통", "쇼핑", "식비", "쇼핑"],
            "금액": [6000, 30000, 20000, 15000],
            "날짜": ["20241031", "20241031", "20241102", "20241105"]
        })
        self.output_dir = "results/"
        os.makedirs(self.output_dir, exist_ok=True)

    def tearDown(self):
        test_report_path = "results/test_report_all.txt"
        if os.path.exists(test_report_path):
            os.remove(test_report_path)

    def test_generate_report_include_all(self):
        report = generate_report(self.data, include_total=True, include_categories=True, include_monthly=True)
        self.assertIn("총 소비 금액: 71,000원", report)
        self.assertIn("쇼핑: 45,000원", report)
        self.assertIn("식비: 20,000원", report)
        self.assertIn("교통: 6,000원", report)
        self.assertIn("2024-10", report)
        self.assertIn("2024-11", report)
        output_path = os.path.join("results", "test_report_all.txt")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(report)

    def test_generate_report_only_total(self):
        report = generate_report(self.data, include_total=True, include_categories=False, include_monthly=False)
        self.assertIn("총 소비 금액: 71,000원", report)
        self.assertNotIn("쇼핑: 45,000원", report)
        self.assertNotIn("식비: 20,000원", report)
        self.assertNotIn("교통: 6,000원", report)

    def test_generate_report_only_categories(self):
        report = generate_report(self.data, include_total=False, include_categories=True, include_monthly=False)
        self.assertNotIn("총 소비 금액: 71,000원", report)
        self.assertIn("쇼핑: 45,000원 (63.4%)", report)
        self.assertIn("식비: 20,000원", report)
        self.assertIn("교통: 6,000원", report)

    def test_generate_report_empty_data(self):
        empty_data = pd.DataFrame(columns=["카테고리", "금액"])
        report = generate_report(empty_data, include_total=True, include_categories=True)
        self.assertIn("총 소비 금액: 0원", report)
        self.assertNotIn("월별 총 소비 금액", report)
        self.assertNotIn("카테고리별 소비 금액", report)

if __name__ == "__main__":
    unittest.main()
