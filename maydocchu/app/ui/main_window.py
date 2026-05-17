from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QListWidget, QListWidgetItem, QMessageBox, 
                             QLabel)
from PyQt6.QtCore import Qt
from app.logic.storage import Storage
from app.ui.editor_dialog import EditorDialog
from app.ui.prompter_window import PrompterWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Máy đọc chữ - Teleprompter")
        self.setMinimumSize(600, 550)
        
        self.storage = Storage()
        self.setup_ui()
        self.refresh_list()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Title
        title_label = QLabel("Danh sách kịch bản")
        title_label.setStyleSheet("font-size: 22px; font-weight: bold; color: #2c3e50; margin-bottom: 5px;")
        main_layout.addWidget(title_label)

        # List Widget
        self.list_widget = QListWidget()
        self.list_widget.setStyleSheet("""
            QListWidget { 
                font-size: 16px; 
                background-color: white; 
                border: 1px solid #ddd;
                border-radius: 4px;
            }
            QListWidget::item { 
                padding: 12px; 
                border-bottom: 1px solid #f0f0f0; 
            }
            QListWidget::item:selected { 
                background-color: #e8f4fd; 
                color: #2980b9; 
                font-weight: bold;
            }
        """)
        self.list_widget.itemDoubleClicked.connect(self.run_prompter)
        main_layout.addWidget(self.list_widget)

        # Bottom Buttons
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 10, 0, 0)
        
        self.add_btn = QPushButton("Thêm mới")
        self.edit_btn = QPushButton("Chỉnh sửa")
        self.delete_btn = QPushButton("Xóa")
        
        for btn in [self.add_btn, self.edit_btn, self.delete_btn]:
            btn.setStyleSheet("padding: 8px 15px; font-size: 14px;")
            button_layout.addWidget(btn)
            
        self.add_btn.clicked.connect(self.add_script)
        self.edit_btn.clicked.connect(self.edit_script)
        self.delete_btn.clicked.connect(self.delete_script)
        
        button_layout.addStretch()
        
        self.run_btn = QPushButton("CHẠY MÁY ĐỌC")
        self.run_btn.setStyleSheet("""
            background-color: #2ecc71; 
            color: white; 
            font-weight: bold; 
            padding: 12px 30px; 
            font-size: 18px;
            border-radius: 6px;
        """)
        self.run_btn.clicked.connect(self.run_prompter)
        button_layout.addWidget(self.run_btn)
        
        main_layout.addLayout(button_layout)

    def refresh_list(self):
        self.list_widget.clear()
        for script in self.storage.get_scripts():
            item = QListWidgetItem(script["title"])
            item.setData(Qt.ItemDataRole.UserRole, script)
            self.list_widget.addItem(item)

    def add_script(self):
        dialog = EditorDialog(self)
        if dialog.exec():
            title, content = dialog.get_data()
            if title:
                self.storage.add_script(title, content)
                self.refresh_list()

    def edit_script(self):
        current_item = self.list_widget.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng chọn kịch bản để sửa!")
            return
        
        script = current_item.data(Qt.ItemDataRole.UserRole)
        dialog = EditorDialog(self, script)
        if dialog.exec():
            title, content = dialog.get_data()
            self.storage.update_script(script["id"], title, content)
            self.refresh_list()

    def delete_script(self):
        current_item = self.list_widget.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng chọn kịch bản để xóa!")
            return
        
        script = current_item.data(Qt.ItemDataRole.UserRole)
        reply = QMessageBox.question(self, "Xác nhận", f"Bạn có chắc muốn xóa '{script['title']}'?",
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            self.storage.delete_script(script["id"])
            self.refresh_list()

    def run_prompter(self):
        current_item = self.list_widget.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng chọn kịch bản để chạy!")
            return
        
        script = current_item.data(Qt.ItemDataRole.UserRole)
        self.prompter = PrompterWindow(script)
        self.prompter.show()
