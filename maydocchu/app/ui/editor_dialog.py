from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLineEdit, QTextEdit, QPushButton, QLabel

class EditorDialog(QDialog):
    def __init__(self, parent=None, script=None):
        super().__init__(parent)
        self.script = script
        self.setWindowTitle("Chỉnh sửa kịch bản" if script else "Thêm kịch bản mới")
        self.setMinimumSize(600, 400)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Tiêu đề:"))
        self.title_input = QLineEdit()
        if self.script:
            self.title_input.setText(self.script.get("title", ""))
        layout.addWidget(self.title_input)

        layout.addWidget(QLabel("Nội dung:"))
        self.content_input = QTextEdit()
        if self.script:
            self.content_input.setPlainText(self.script.get("content", ""))
        layout.addWidget(self.content_input)

        button_layout = QHBoxLayout()
        self.save_btn = QPushButton("Lưu")
        self.save_btn.clicked.connect(self.accept)
        self.cancel_btn = QPushButton("Hủy")
        self.cancel_btn.clicked.connect(self.reject)

        button_layout.addStretch()
        button_layout.addWidget(self.save_btn)
        button_layout.addWidget(self.cancel_btn)
        layout.addLayout(button_layout)

    def get_data(self):
        return self.title_input.text(), self.content_input.toPlainText()
