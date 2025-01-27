import os
import PyPDF2
import win32com.client as win32


def convert_pdf_to_docx(pdf_path, docx_path):
    # Tạo đường dẫn tuyệt đối cho tệp đầu ra
    docx_abs_path = os.path.abspath(docx_path)

    # Tạo đối tượng COM của Word
    word = win32.gencache.EnsureDispatch('Word.Application')

    try:
        # Mở tệp PDF trong Word
        doc = word.Documents.Open(pdf_path)

        # Lưu tệp PDF dưới dạng định dạng tài liệu Word
        doc.SaveAs2(docx_abs_path, FileFormat=16)

        # Đóng tài liệu và Word
        doc.Close()
        word.Quit()

        print(
            f"Chuyển đổi tệp PDF {pdf_path} sang tệp Word {docx_path} thành công!")
    except Exception as e:
        print(f"Lỗi khi chuyển đổi tệp PDF sang tệp Word: {e}")


pdf_path = "c:\\Users\\UY\\Downloads\\Than So Hoc\\ZFL.pdf"
docx_path = "c:\\Users\\UY\\Downloads\\Than So Hoc\\ZFL.docx"

convert_pdf_to_docx(pdf_path, docx_path)
