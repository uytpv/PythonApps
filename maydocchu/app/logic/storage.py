import json
import os
import sys
import shutil

class Storage:
    def __init__(self, filename="scripts.json"):
        # 1. Xác định đường dẫn file mặc định đi kèm (bundled)
        default_bundled_path = None
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            # Nếu chạy từ exe của PyInstaller, file đi kèm được giải nén vào thư mục tạm _MEIPASS
            default_bundled_path = os.path.join(sys._MEIPASS, filename)
        else:
            # Nếu chạy từ mã nguồn Python
            default_bundled_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), filename)

        # 2. Xác định thư mục lưu trữ ngoài (persistent)
        if getattr(sys, 'frozen', False):
            # Lưu cùng thư mục với file .exe (để người dùng dễ quản lý, copy)
            base_dir = os.path.dirname(sys.executable)
        else:
            # Lưu ở thư mục gốc của dự án khi chạy dev
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

        # 3. Kiểm tra xem thư mục có quyền ghi hay không (ví dụ: chạy trong C:\Program Files)
        try:
            test_file = os.path.join(base_dir, '.write_test')
            with open(test_file, 'w') as f:
                f.write('test')
            os.remove(test_file)
        except (IOError, OSError):
            # Nếu không có quyền ghi, fallback về AppData/Roaming/MayDocChu
            appdata_dir = os.path.join(os.environ.get('APPDATA', os.path.expanduser('~')), 'MayDocChu')
            os.makedirs(appdata_dir, exist_ok=True)
            base_dir = appdata_dir

        self.filename = os.path.join(base_dir, filename)

        # 4. Sao chép file kịch bản mặc định sang nơi lưu trữ ngoài nếu chưa tồn tại
        if not os.path.exists(self.filename) and default_bundled_path and os.path.exists(default_bundled_path):
            try:
                shutil.copy2(default_bundled_path, self.filename)
            except Exception as e:
                print(f"Error copying default scripts: {e}")

        self.scripts = self._load_scripts()

    def _load_scripts(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading scripts: {e}")
                return []
        return []

    def save_scripts(self):
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(self.scripts, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Error saving scripts: {e}")

    def add_script(self, title, content):
        script_id = len(self.scripts) + 1
        new_script = {
            "id": script_id,
            "title": title,
            "content": content
        }
        self.scripts.append(new_script)
        self.save_scripts()
        return new_script

    def update_script(self, script_id, title, content):
        for script in self.scripts:
            if script["id"] == script_id:
                script["title"] = title
                script["content"] = content
                self.save_scripts()
                return True
        return False

    def delete_script(self, script_id):
        self.scripts = [s for s in self.scripts if s["id"] != script_id]
        self.save_scripts()

    def get_scripts(self):
        return self.scripts
