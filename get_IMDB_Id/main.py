import re

def extract_imdb_ids_from_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Tìm tất cả các ID IMDB (dạng ttxxxxxxx) bằng regex
        imdb_ids = sorted(set(re.findall(r'tt\d{7,8}', content)))  # Loại bỏ trùng lặp và sắp xếp
        print("Các ID tìm thấy:", imdb_ids)
        # Ghi các ID vào file imdbids.txt
        with open('imdbids.txt', 'w', encoding='utf-8') as file:
            for imdb_id in imdb_ids:
                file.write(f"'{imdb_id}',\n")

        print(f"Đã trích xuất {len(imdb_ids)} ID IMDB duy nhất và lưu vào file imdbids.txt.")
    except Exception as e:
        print(f"Đã xảy ra lỗi: {e}")

if __name__ == "__main__":
    file_path = 'page_source.html'  # Đường dẫn đến file HTML đã lưu
    extract_imdb_ids_from_file(file_path)