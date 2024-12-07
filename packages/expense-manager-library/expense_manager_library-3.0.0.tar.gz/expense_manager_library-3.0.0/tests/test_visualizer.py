import unittest
import pandas as pd
import os
import matplotlib.pyplot as plt
from expense_manager_library.visualizer import draw_pie_chart, draw_line_chart, draw_bar_chart

class TestVisualizer(unittest.TestCase):

    def setUp(self):
        self.data = pd.DataFrame({
            "카테고리": ["여가", "교통", "식비", "쇼핑"],
            "금액": [35000, 4000, 13000, 55000],
            "날짜": ["2024-10-29", "2024-11-02", "2024-11-02", "2024-11-03"]
        })
       
        self.data["날짜"] = self.data["날짜"].str.replace("-", "").astype(str)
        self.output_dir = "results/"
        os.makedirs(self.output_dir, exist_ok=True)

    def tearDown(self):
        if os.path.exists("results/test_bar_chart.png"):
            os.remove("results/test_bar_chart.png")
        if os.path.exists("results/test_line_chart.png"):
            os.remove("results/test_line_chart.png")
        if os.path.exists("results/test_pie_chart.png"):
            os.remove("results/test_pie_chart.png")

    def test_draw_pie_chart(self):
        fig, ax = plt.subplots()
        draw_pie_chart(self.data, ax=ax)
        self.assertIsNotNone(ax)
        plt.savefig(os.path.join(self.output_dir, "test_pie_chart.png"))

    def test_draw_line_chart(self):
        fig, ax = plt.subplots()
        draw_line_chart(self.data, ax=ax)
        self.assertIsNotNone(ax)
        plt.savefig(os.path.join(self.output_dir, "test_line_chart.png"))

    def test_draw_bar_chart(self):
        fig, ax = plt.subplots()
        draw_bar_chart(self.data, ax=ax)
        self.assertIsNotNone(ax)
        plt.savefig(os.path.join(self.output_dir, "test_bar_chart.png"))

if __name__ == "__main__":
    unittest.main()