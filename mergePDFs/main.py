import os
from PyPDF2 import PdfMerger

def merge_pdfs(source_folder, output_folder, output_filename):
    # Lấy danh sách file PDF trong thư mục source, sắp xếp theo tên
    pdf_files = sorted([f for f in os.listdir(source_folder) if f.lower().endswith('.pdf')])
    if not pdf_files:
        print("Không tìm thấy file PDF nào trong thư mục source.")
        return

    merger = PdfMerger()
    for pdf in pdf_files:
        pdf_path = os.path.join(source_folder, pdf)
        merger.append(pdf_path)
        print(f"Đã thêm: {pdf}")

    # Đảm bảo thư mục output tồn tại
    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, output_filename + '.pdf')
    merger.write(output_path)
    merger.close()
    print(f"Đã ghép xong! File lưu tại: {output_path}")

if __name__ == "__main__":
    output_name = input("Nhập tên file PDF output (không cần .pdf): ").strip()
    merge_pdfs('source', 'output', output_name)