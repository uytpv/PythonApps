from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                              QPushButton, QLabel, QSizePolicy)
from PyQt6.QtCore import Qt, QTimer, QPoint
from PyQt6.QtGui import QFont, QColor, QTransform, QPainter


# ──────────────────────────────────────────────
# Custom scroll-rendering label
# ──────────────────────────────────────────────
class ScrollLabel(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.setStyleSheet("color: white; background-color: black;")
        self.offset = 0
        self.mirror_h = False
        self.mirror_v = False

    def paintEvent(self, event):
        painter = QPainter(self)

        transform = QTransform()

        if self.mirror_h or self.mirror_v:
            cx = self.width() / 2
            cy = self.height() / 2
            transform.translate(cx, cy)
            transform.scale(-1 if self.mirror_h else 1, -1 if self.mirror_v else 1)
            transform.translate(-cx, -cy)

        transform.translate(0, -self.offset)
        painter.setTransform(transform)

        painter.setPen(QColor("white"))
        painter.setFont(self.font())

        draw_rect = self.rect()
        draw_rect.setHeight(200000)
        painter.drawText(draw_rect,
                         Qt.AlignmentFlag.AlignHCenter | Qt.TextFlag.TextWordWrap,
                         self.text())
        painter.end()


# ──────────────────────────────────────────────
# Spinner control: label + [−] value [+]
# with auto-repeat when button is held down
# ──────────────────────────────────────────────
class SpinControl(QWidget):
    """A compact numeric stepper with hold-to-repeat behaviour."""

    def __init__(self, label: str, value: int, min_val: int, max_val: int,
                 step: int = 1, parent=None):
        super().__init__(parent)
        self._value = value
        self._min = min_val
        self._max = max_val
        self._step = step

        # Timers for auto-repeat
        self._repeat_timer = QTimer(self)
        self._repeat_timer.setInterval(80)   # speed while holding
        self._repeat_dir = 0                 # +1 or -1

        # Initial delay before auto-repeat kicks in
        self._delay_timer = QTimer(self)
        self._delay_timer.setSingleShot(True)
        self._delay_timer.setInterval(400)   # 400 ms delay before repeating
        self._delay_timer.timeout.connect(self._start_repeat)

        self._repeat_timer.timeout.connect(self._do_repeat)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        self._lbl = QLabel(label)
        self._lbl.setStyleSheet("font-size: 17px; color: #aaa;")
        layout.addWidget(self._lbl)

        self._minus_btn = QPushButton("−")
        self._plus_btn  = QPushButton("+")
        self._val_lbl   = QLabel(str(self._value))

        btn_style = """
            QPushButton {
                background-color: #444;
                color: #ddd;
                border: 1px solid #666;
                border-radius: 6px;
                font-size: 22px;
                font-weight: bold;
                min-width: 42px;
                max-width: 42px;
                min-height: 42px;
                max-height: 42px;
                padding: 0px;
            }
            QPushButton:hover  { background-color: #555; color: white; }
            QPushButton:pressed { background-color: #222; }
        """
        val_style = """
            QLabel {
                font-size: 20px;
                font-weight: bold;
                color: white;
                min-width: 52px;
                max-width: 52px;
                qproperty-alignment: AlignCenter;
                background-color: #222;
                border: 1px solid #555;
                border-radius: 5px;
                padding: 4px 0px;
            }
        """
        self._minus_btn.setStyleSheet(btn_style)
        self._plus_btn.setStyleSheet(btn_style)
        self._val_lbl.setStyleSheet(val_style)

        layout.addWidget(self._minus_btn)
        layout.addWidget(self._val_lbl)
        layout.addWidget(self._plus_btn)

        # Click events (single tap)
        self._minus_btn.clicked.connect(lambda: self._change(-self._step))
        self._plus_btn.clicked.connect(lambda: self._change(+self._step))

        # Press / release for hold-to-repeat
        self._minus_btn.pressed.connect(lambda: self._on_press(-1))
        self._minus_btn.released.connect(self._on_release)
        self._plus_btn.pressed.connect(lambda: self._on_press(+1))
        self._plus_btn.released.connect(self._on_release)

        # Callback invoked when value changes
        self.on_value_changed = None   # set externally

    # ── value helpers ──────────────────────────
    @property
    def value(self) -> int:
        return self._value

    def _change(self, delta: int):
        new_val = max(self._min, min(self._max, self._value + delta))
        if new_val != self._value:
            self._value = new_val
            self._val_lbl.setText(str(self._value))
            if self.on_value_changed:
                self.on_value_changed(self._value)

    # ── hold-to-repeat logic ───────────────────
    def _on_press(self, direction: int):
        self._repeat_dir = direction
        self._delay_timer.start()

    def _on_release(self):
        self._delay_timer.stop()
        self._repeat_timer.stop()

    def _start_repeat(self):
        self._repeat_timer.start()

    def _do_repeat(self):
        self._change(self._repeat_dir * self._step)


# ──────────────────────────────────────────────
# Main prompter window
# ──────────────────────────────────────────────
class PrompterWindow(QWidget):
    def __init__(self, script):
        super().__init__()
        self.script = script
        self.scroll_speed = 1
        self.scroll_offset = 0
        self.is_scrolling = False

        self.setWindowTitle(f"Prompter - {script['title']}")
        self.setMinimumSize(800, 600)
        self.setStyleSheet("background-color: black;")

        self.setup_ui()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.scroll_text)
        self.timer.setInterval(20)   # 50 fps

    def setup_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # ── Text display ───────────────────────
        self.font_size = 40
        self.text_display = ScrollLabel(self.script['content'])
        self.text_display.setFont(QFont("Arial", self.font_size))
        self.layout.addWidget(self.text_display, 1)

        # ── Controls bar ───────────────────────
        self.controls = QWidget()
        self.controls.setStyleSheet("""
            QWidget {
                background-color: rgba(20, 20, 20, 230);
                color: #bbb;
                font-family: Arial;
                font-size: 18px;
            }
            QPushButton {
                background-color: #333;
                color: #bbb;
                border: 1px solid #555;
                border-radius: 8px;
                padding: 10px;
                min-height: 50px;
                min-width: 120px;
                font-size: 20px;
                font-weight: normal;
            }
            QPushButton:hover  { background-color: #444; color: white; border-color: #888; }
            QPushButton:pressed { background-color: #222; }
            QPushButton:checked {
                background-color: #555; color: white;
                border-color: #ccc; font-weight: bold;
            }
        """)

        control_layout = QHBoxLayout(self.controls)
        control_layout.setSpacing(22)
        control_layout.setContentsMargins(24, 16, 24, 16)

        # Play/Pause icon button
        play_btn_style = """
            QPushButton {
                background-color: #333;
                color: #ccc;
                border: 1px solid #555;
                border-radius: 8px;
                font-size: 26px;
                min-width: 58px;  max-width: 58px;
                min-height: 58px; max-height: 58px;
                padding: 0px;
            }
            QPushButton:hover  { background-color: #444; color: white; border-color: #888; }
            QPushButton:pressed { background-color: #222; }
        """
        self.play_btn = QPushButton("\u25B6")   # ▶
        self.play_btn.setToolTip("Bắt đầu")
        self.play_btn.setStyleSheet(play_btn_style)
        self.play_btn.clicked.connect(self.toggle_scrolling)
        control_layout.addWidget(self.play_btn)

        control_layout.addSpacing(10)

        # Speed spinner  (range 0–100, displayed as 0.0–10.0 internally)
        self._raw_speed = 5        # 0–100
        self.speed_spin = SpinControl("Tốc độ:", self._raw_speed, 0, 100, step=1)
        self.speed_spin.on_value_changed = self._on_speed_changed
        self._on_speed_changed(self._raw_speed)
        control_layout.addWidget(self.speed_spin)

        control_layout.addSpacing(10)

        # Font-size spinner
        self.font_spin = SpinControl("Cỡ chữ:", self.font_size, 10, 150, step=2)
        self.font_spin.on_value_changed = self._on_font_changed
        control_layout.addWidget(self.font_spin)

        control_layout.addStretch()

        # Mirror icon buttons — compact square
        icon_btn_style = """
            QPushButton {
                background-color: #333;
                color: #ccc;
                border: 1px solid #555;
                border-radius: 8px;
                font-size: 24px;
                min-width: 52px;  max-width: 52px;
                min-height: 52px; max-height: 52px;
                padding: 0px;
            }
            QPushButton:hover  { background-color: #444; color: white; border-color: #888; }
            QPushButton:pressed { background-color: #222; }
            QPushButton:checked {
                background-color: #1a6a9a;
                color: white;
                border-color: #4db3ff;
            }
        """

        self.mirror_h_btn = QPushButton("\u2194")   # ↔
        self.mirror_h_btn.setCheckable(True)
        self.mirror_h_btn.setToolTip("Lật ngang")
        self.mirror_h_btn.setStyleSheet(icon_btn_style)
        self.mirror_h_btn.toggled.connect(self.toggle_mirror_h)
        control_layout.addWidget(self.mirror_h_btn)

        self.mirror_v_btn = QPushButton("\u2195")   # ↕
        self.mirror_v_btn.setCheckable(True)
        self.mirror_v_btn.setToolTip("Lật dọc")
        self.mirror_v_btn.setStyleSheet(icon_btn_style)
        self.mirror_v_btn.toggled.connect(self.toggle_mirror_v)
        control_layout.addWidget(self.mirror_v_btn)

        self.layout.addWidget(self.controls)

    # ── event handlers ─────────────────────────
    def showEvent(self, event):
        super().showEvent(event)
        self.scroll_offset = -self.text_display.height()
        self.text_display.offset = self.scroll_offset
        self.text_display.update()

    def toggle_scrolling(self):
        self.is_scrolling = not self.is_scrolling
        if self.is_scrolling:
            self.timer.start()
            self.play_btn.setText("\u23F8")   # ⏸
            self.play_btn.setToolTip("Dừng")
        else:
            self.timer.stop()
            self.play_btn.setText("\u25B6")   # ▶
            self.play_btn.setToolTip("Tiếp tục")

    def scroll_text(self):
        self.scroll_offset += self.scroll_speed
        self.text_display.offset = self.scroll_offset
        self.text_display.update()

    def _on_speed_changed(self, value: int):
        self._raw_speed = value
        self.scroll_speed = value / 10.0

    def _on_font_changed(self, value: int):
        self.font_size = value
        self.text_display.setFont(QFont("Arial", self.font_size))
        self.text_display.update()

    def toggle_mirror_h(self, checked):
        self.text_display.mirror_h = checked
        self.text_display.update()

    def toggle_mirror_v(self, checked):
        self.text_display.mirror_v = checked
        self.text_display.update()

    def wheelEvent(self, event):
        delta = event.angleDelta().y()
        self.scroll_offset -= delta
        limit = -self.text_display.height()
        if self.scroll_offset < limit:
            self.scroll_offset = limit
        self.text_display.offset = self.scroll_offset
        self.text_display.update()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Space:
            self.toggle_scrolling()
        elif event.key() == Qt.Key.Key_Escape:
            self.close()
        elif event.key() == Qt.Key.Key_Up:
            self.speed_spin._change(+5)
        elif event.key() == Qt.Key.Key_Down:
            self.speed_spin._change(-5)
