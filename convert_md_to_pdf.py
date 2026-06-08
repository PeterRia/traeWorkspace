#!/usr/bin/env python3
"""Markdown to PDF converter using markdown + fpdf2"""

from fpdf import FPDF
import re
import os


class MarkdownPDF(FPDF):
    def __init__(self):
        super().__init__()
        # 尝试加载中文字体
        heifi_path = 'C:/Windows/Fonts/simhei.ttf'
        simsun_path = 'C:/Windows/Fonts/simsun.ttc'
        
        font_loaded = False
        if os.path.exists(heifi_path):
            self.add_font('CustomSimHei', '', heifi_path)
            self.add_font('CustomSimHei', 'B', heifi_path)
            font_loaded = True
        
        if not font_loaded and os.path.exists(simsun_path):
            self.add_font('CustomSimHei', '', simsun_path)
            self.add_font('CustomSimHei', 'B', simsun_path)
            font_loaded = True
            
        if not font_loaded:
            raise FileNotFoundError("未找到中文字体文件")
        
        self.set_font('CustomSimHei', size=11)
        self.set_auto_page_break(auto=True, margin=20)
        self.set_margins(20, 20, 20)

    def _render_line(self, text, size=11, style='', fill=False):
        """渲染一行文本，自动处理加粗"""
        self.set_font('SimHei', size=size, style=style)
        self.multi_cell(0, size * 0.6, text.strip())

    def add_markdown(self, md_text):
        """解析 Markdown 文本并渲染为 PDF"""
        # 替换所有 SimHei 为 CustomSimHei
        lines = md_text.split('\n')
        i = 0
        page_break_needed = False

        while i < len(lines):
            line = lines[i]
            stripped = line.strip()

            # 跳过空行
            if not stripped:
                self.ln(2)
                i += 1
                continue

            # 分隔线
            if stripped == '---':
                self.ln(4)
                i += 1
                continue

            # 一级标题
            if stripped.startswith('# '):
                if page_break_needed:
                    self.ln(3)
                self.ln(6)
                self.set_font('CustomSimHei', size=20, style='B')
                self.set_text_color(30, 30, 30)
                self.multi_cell(0, 12, stripped[2:].strip())
                self.ln(8)
                page_break_needed = True
                i += 1
                continue

            # 二级标题
            if stripped.startswith('## '):
                if page_break_needed:
                    self.ln(3)
                self.ln(5)
                self.set_font('CustomSimHei', size=16, style='B')
                self.set_text_color(30, 30, 30)
                self.multi_cell(0, 10, stripped[3:].strip())
                self.ln(4)
                page_break_needed = True
                i += 1
                continue

            # 三级标题
            if stripped.startswith('### '):
                if page_break_needed:
                    self.ln(2)
                self.set_font('CustomSimHei', size=13, style='B')
                self.set_text_color(50, 50, 50)
                self.multi_cell(0, 8, stripped[4:].strip())
                self.ln(3)
                i += 1
                continue

            # 引用块 (带警告图标)
            if stripped.startswith('> ⚠️'):
                self.set_font('CustomSimHei', size=10, style='B')
                self.set_fill_color(255, 248, 230)
                self.set_text_color(200, 100, 0)
                self.multi_cell(0, 7, stripped, border=0, fill=True)
                self.ln(5)
                i += 1
                continue

            # 引用块 (普通引用)
            if stripped.startswith('> '):
                self.set_font('CustomSimHei', size=10)
                self.set_fill_color(245, 245, 245)
                self.set_text_color(80, 80, 80)
                text = stripped[2:]
                text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
                self.multi_cell(0, 7, text, border=0, fill=True)
                self.ln(5)
                i += 1
                continue

            # 普通链接行
            if stripped.startswith('['):
                match = re.match(r'\[(.+?)\]\((.+?)\)', stripped)
                if match:
                    self.set_font('CustomSimHei', size=10, style='U')
                    self.set_text_color(0, 100, 200)
                    self.multi_cell(0, 7, match.group(1))
                    self.ln(2)
                    i += 1
                    continue

            # 表格检测
            if '|' in stripped and i + 1 < len(lines) and '---' in lines[i + 1]:
                self._render_table(lines, i)
                i += 3
                while i < len(lines) and '|' in lines[i]:
                    i += 1
                self.ln(5)
                continue

            # 图片标记 (跳过，PDF不显示图片)
            if stripped.startswith('!['):
                i += 1
                continue

            # 列表项
            if stripped.startswith('- '):
                self.set_font('CustomSimHei', size=11)
                self.set_text_color(40, 40, 40)
                text = stripped[2:]
                avail = self.w - 40 - 6
                self.set_font('CustomSimHei', size=11)
                self.cell(6, 7, '• ')
                self.cell(avail, 7, text)
                self.ln()
                i += 1
                continue

            # 普通文本行 - 处理加粗
            if '**' in stripped:
                parts = re.split(r'(\*\*(.+?)\*\*)', stripped)
                for part in parts:
                    if part.startswith('**') and part.endswith('**'):
                        self.set_font('CustomSimHei', size=11, style='B')
                        self.cell(0, 7, part[2:-2])
                    elif part:
                        self.set_font('CustomSimHei', size=11)
                        self.cell(0, 7, part)
                self.ln()
            else:
                self.set_font('CustomSimHei', size=11)
                self.set_text_color(40, 40, 40)
                self.cell(0, 7, stripped)
                self.ln()

            page_break_needed = True
            i += 1

    def _render_table(self, lines, start_idx):
        """渲染 Markdown 表格"""
        headers = [h.strip() for h in lines[start_idx].split('|') if h.strip()]
        data_rows = []
        for j in range(start_idx + 2, len(lines)):
            if '|' not in lines[j]:
                break
            row = [cell.strip() for cell in lines[j].split('|') if cell.strip()]
            if row:
                data_rows.append(row)

        if not headers:
            return

        max_cols = max(len(headers), *(len(row) for row in data_rows))
        table_width = self.w - 40
        col_width = table_width / max_cols

        self.set_font('CustomSimHei', size=10, style='B')
        self.set_fill_color(60, 60, 60)
        self.set_text_color(255, 255, 255)
        for header in headers:
            self.cell(col_width, 8, header, border=1, fill=True, align='C')
        self.ln()

        self.set_font('CustomSimHei', size=10)
        self.set_text_color(40, 40, 40)
        fill = False
        for row in data_rows:
            while len(row) < len(headers):
                row.append('')
            for cell in row:
                self.cell(col_width, 7, cell, border=1, fill=fill)
            self.ln()
            fill = not fill

    def header(self):
        if self.page_no() > 1:
            self.set_font('CustomSimHei', size=9)
            self.set_text_color(150, 150, 150)
            self.cell(0, 10, 'Agnes AI API Key 获取与配置教程', 0, 0, 'L')
            self.ln(15)

    def footer(self):
        self.set_y(-15)
        self.set_font('CustomSimHei', size=9)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', 0, 0, 'C')


def convert_md_to_pdf(md_path, pdf_path):
    """将 Markdown 文件转换为 PDF"""
    with open(md_path, 'r', encoding='utf-8') as f:
        md_text = f.read()

    pdf = MarkdownPDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.add_markdown(md_text)
    pdf.output(pdf_path)
    print(f"✓ PDF 已成功生成: {pdf_path}")


if __name__ == '__main__':
    md_file = r'f:\python\TreaWorkSpace\免费的模型API获取\tuto.md'
    pdf_file = r'f:\python\TreaWorkSpace\免费的模型API获取\tuto.pdf'
    convert_md_to_pdf(md_file, pdf_file)
