import json
import os

class Storage:
    def __init__(self, filename="scripts.json"):
        self.filename = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), filename)
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
