import os
from .visualizer import draw_pie_chart, draw_line_chart, draw_bar_chart
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.backends.backend_pdf import PdfPages
import pandas as pd

# 소비 금액(지출 보고서) 정리
def generate_report(data, include_total=True, include_categories=True, include_monthly=True):
    report_lines = []
    report_lines.append("<지출 보고서>\n\n")
    
    if include_total:
        total_amount = data["금액"].sum()
        report_lines.append(f"총 소비 금액: {total_amount:,}원")
    
    if include_categories:
        if not data.empty and "카테고리" in data.columns:
            grouped_data = data.groupby("카테고리")["금액"].sum()
            report_lines.append("\n\n카테고리별 소비 금액:")
            total_amount = grouped_data.sum()
            for category, amount in grouped_data.items():
                percentage = (amount / total_amount) * 100
                report_lines.append(f"- {category}: {amount:,}원 ({percentage:.1f}%)")

    if include_monthly:
        if "날짜" in data.columns and not data["날짜"].isna().all():
            try:
                data["날짜"] = pd.to_datetime(data["날짜"], format="%Y%m%d", errors="coerce")
                data["월"] = data["날짜"].dt.to_period("M")
      
                monthly_totals = data.groupby("월")["금액"].sum()
                report_lines.append("\n\n월별 총 소비 금액:")
                for month, total in monthly_totals.items():
                    report_lines.append(f"- {month}: {total:,}원")
    
                report_lines.append("\n\n카테고리별 월별 소비 금액:")
                monthly_category_totals = data.groupby(["월", "카테고리"])["금액"].sum()
                for month in monthly_totals.index:
                    report_lines.append(f"- {month}:")
                    monthly_total = monthly_totals[month]
                    for category, total in monthly_category_totals.loc[month].items():
                        percentage = (total / monthly_total) * 100
                        report_lines.append(f"  {category}: {total:,}원 ({percentage:.1f}%)")
            except Exception as e:
                report_lines.append(f"\n날짜 처리 중 오류 발생: {e}")

    return "\n".join(report_lines)

# pdf 만들기
def save_report_to_pdf(data, report_text, selected_graphs, show_report=True, 
                       font_color="black", pdf_path="results/report.pdf"):

    os.makedirs(os.path.dirname(pdf_path), exist_ok=True)

    with PdfPages(pdf_path) as pdf:
        if show_report:
            fig, ax = plt.subplots(figsize=(8.5, 11))  
            ax.axis("off")

            line_count = len(report_text.split("\n"))
            if line_count < 30:
                font_size = 16
            elif line_count < 50:
                font_size = 14
            elif line_count < 80:
                font_size = 12
            else:
                font_size = 10

            ax.text(
                0.5,  
                0.5, 
                report_text,
                fontsize=font_size,
                color=font_color,
                va="center",
                ha="center", 
                wrap=True
            )
            pdf.savefig(fig)
            plt.close(fig)

        rows = 2
        cols = 2
        items_per_page = rows * cols
        current_index = 0

        while current_index < len(selected_graphs):
            fig = plt.figure(figsize=(10, 5 * rows))
            gs = GridSpec(rows, cols, figure=fig, height_ratios=[1] * rows, width_ratios=[1, 1])

            page_item_count = 0
            while current_index < len(selected_graphs) and page_item_count < items_per_page:
                graph_ax = fig.add_subplot(gs[page_item_count // cols, page_item_count % cols])
                if selected_graphs[current_index] == "pie":
                    draw_pie_chart(data, ax=graph_ax)
                elif selected_graphs[current_index] == "line":
                    draw_line_chart(data, ax=graph_ax)
                elif selected_graphs[current_index] == "bar":
                    draw_bar_chart(data, ax=graph_ax)
                current_index += 1
                page_item_count += 1

            for i in range(page_item_count, items_per_page):
                empty_ax = fig.add_subplot(gs[i // cols, i % cols])
                empty_ax.axis("off")

            plt.tight_layout(rect=[0, 0.03, 1, 0.95])
            pdf.savefig(fig)
            plt.close(fig)