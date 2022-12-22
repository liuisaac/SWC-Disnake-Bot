from fpdf import FPDF
"""
https://pyfpdf.github.io/fpdf2/Tables.html
"""
PAGE_HEADERS = ("PARTS SIGN OUT SHEET", "(PLEASE PRINT)", "KIT #______")
PAGE_HEADER_SIZE = (14, 12, 13)
TABLE_COL_NAMES = ("Date", "Name", "Bin #", "Quantity of Parts", "Part Description", "S. Initial", "T. Initial")

class pdfgenerator:
    def __init__(self, TABLE_DATA):
        self.TABLE_DATA = TABLE_DATA
    def generate(self):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Helvetica", size=12)
        line_height = pdf.font_size * 2.5

        w = pdf.epw
        summ = w*2/17+w*4.25/17+w*1/17+w*1.75/17+w*4/17+w*2/17
        widtharray = (w*2/17, w*4.25/17, w*1/17, w*1.75/17, w*4/17, w*2/17, w-summ)

        col_width = pdf.epw / 4  # distribute content evenly
        def set_font_size(fsize):
            pdf.set_font("Helvetica", size=fsize)
        def render_table_header():
            # PAGE HEADER
            cnt = 0
            for header_name in PAGE_HEADERS:
                # headers
                # set_font_size(PAGE_HEADER_SIZE[cnt])
                pdf.cell(200, 10, txt=header_name, ln=1, align="C")
                cnt+=1
                print(header_name)
            
            set_font_size(12)

            # TABLE HEADER
            cnt = 0
            for col_name in TABLE_COL_NAMES:
                pdf.multi_cell(widtharray[cnt], line_height, col_name, border=1, new_x="RIGHT", new_y="TOP", max_line_height=pdf.font_size)
                cnt+=1
            pdf.ln(line_height)
            pdf.set_font(style="")  # disabling bold text

        render_table_header()

        set_font_size(8)
        for row in self.TABLE_DATA:
            if pdf.will_page_break(line_height):
                render_table_header()
            cnt = 0
            for datum in row:
                pdf.multi_cell(widtharray[cnt], line_height, datum, border=1, new_x="RIGHT", new_y="TOP", max_line_height=pdf.font_size)
                cnt+=1
            pdf.ln(line_height)

        pdf.output("converter//out.pdf")