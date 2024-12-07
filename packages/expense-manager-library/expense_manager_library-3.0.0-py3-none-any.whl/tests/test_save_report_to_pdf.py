import unittest
import pandas as pd
import os
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from expense_manager_library.report_generator import save_report_to_pdf, generate_report

class TestSaveReportToPDF(unittest.TestCase):

    # 테스트용 데이터
    def setUp(self):
        self.data = pd.DataFrame({
            "카테고리": ["교통", "쇼핑", "식비", "쇼핑"],
            "금액": [6000, 30000, 20000, 15000],
            "날짜": ["20241031", "20241031", "20241102", "20241105"]
        })
        self.report_text = generate_report(self.data, include_total=True, include_categories=True, include_monthly=True)
        self.pdf_path = "results/test_report.pdf"
        os.makedirs(os.path.dirname(self.pdf_path), exist_ok=True)

    def tearDown(self):
        if os.path.exists(self.pdf_path):
            os.remove(self.pdf_path)

    def test_save_report_to_pdf(self):
        save_report_to_pdf(
            data=self.data,
            report_text=self.report_text,
            selected_graphs=["pie","line", "bar"],  
            show_report=True,  
            pdf_path=self.pdf_path
        )
        self.assertTrue(os.path.exists(self.pdf_path))
        self.assertTrue(os.path.getsize(self.pdf_path) > 0)

if __name__ == "__main__":
    unittest.main()  