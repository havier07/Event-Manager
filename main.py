import sys
import os
import json
import re
from datetime import datetime, timedelta
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QLineEdit, QPushButton, QStackedWidget, QMessageBox, 
    QComboBox, QScrollArea, QGridLayout, QDialog, QTextEdit, 
    QFileDialog, QDateEdit, QTimeEdit, QMenu, QFrame, QRadioButton, QButtonGroup,
    QCalendarWidget, QToolButton, QAbstractItemView, QSpinBox
)
from PySide6.QtCore import Qt, QSize, QDate, QTime, QTimer
from PySide6.QtGui import QPixmap, QIcon, QAction, QColor, QPainter, QPainterPath, QFont

DATA_FILE = "event_app_data.json"
LOGO_PATH = "Logo_PTIT.png"
THEME_COLOR = "#D32F2F"
THEME_HOVER = "#B71C1C"
TEXT_COLOR = "#333333"
BG_COLOR = "#F5F5F5"
CARD_BG = "#FFFFFF"
LINK_COLOR = "#1976D2"

STYLESHEET = f"""
    QWidget {{
        font-family: 'Segoe UI', sans-serif;
        font-size: 14px;
        color: {TEXT_COLOR};
    }}
    QMainWindow, QDialog {{
        background-color: {BG_COLOR};
    }}
    
    /* Input Styles */
    QLineEdit, QTextEdit, QComboBox, QDateEdit, QTimeEdit {{
        border: 1px solid #CCCCCC;
        border-radius: 6px;
        padding: 8px;
        background-color: {CARD_BG};
        color: {TEXT_COLOR};
        selection-background-color: {THEME_COLOR};
    }}
    QComboBox QAbstractItemView {{
        background-color: white;
        color: {TEXT_COLOR};
        selection-background-color: {THEME_COLOR};
        selection-color: white;
        border: 1px solid #CCCCCC;
        outline: none;
    }}
    QLineEdit:focus, QTextEdit:focus {{
        border: 1px solid {THEME_COLOR};
    }}
    
    /* --- CALENDAR --- */
    QCalendarWidget QAbstractItemView:enabled {{
        color: black;
        background-color: white;
        selection-background-color: {THEME_COLOR};
        selection-color: white;
    }}
    QCalendarWidget QAbstractItemView::item:hover {{
        border: 1px solid {THEME_COLOR};
        background-color: #FFEBEE;
        border-radius: 4px;
        color: black;
    }}
    
    QCalendarWidget QWidget {{
        alternate-background-color: #E0E0E0; 
    }}
    QCalendarWidget QWidget#qt_calendar_navigationbar {{
        background-color: {THEME_COLOR};
    }}
    QCalendarWidget QToolButton {{
        color: white;
        background-color: transparent;
        font-weight: bold;
        icon-size: 24px;
    }}
    QCalendarWidget QToolButton:hover {{
        background-color: {THEME_HOVER};
        border: 1px solid white;
    }}
    QCalendarWidget QMenu {{
        background-color: white;
        color: black;
        border: 1px solid #ccc;
    }}
    QCalendarWidget QMenu::item:selected {{
        background-color: #FFEBEE;
        color: black;
        border: 1px solid {THEME_COLOR};
    }}
    QCalendarWidget QSpinBox {{
        background-color: white;
        color: black;
        selection-background-color: {THEME_COLOR};
    }}
    
    /* --- STYLE RADIO BUTTON --- */
    QRadioButton {{
        spacing: 8px;
        color: {TEXT_COLOR};
    }}
    QRadioButton::indicator {{
        width: 16px;
        height: 16px;
        border-radius: 9px;
        border: 1px solid #999;
        background-color: white;
    }}
    QRadioButton::indicator:checked {{
        border: 1px solid {THEME_COLOR};
        background-color: {THEME_COLOR};
        image-position: center;
    }}
    QRadioButton::indicator:hover {{
        border-color: {THEME_COLOR};
    }}

    /* Button Styles */
    QPushButton {{
        border-radius: 6px;
        padding: 8px 16px;
        font-weight: bold;
        outline: none;
    }}
    QPushButton::menu-indicator {{ width: 0px; height: 0px; image: none; }}
    
    QPushButton.primary {{
        background-color: {THEME_COLOR};
        color: white;
        border: none;
    }}
    QPushButton.primary:hover {{
        background-color: {THEME_HOVER};
    }}
    
    QPushButton.secondary {{
        background-color: white;
        color: {THEME_COLOR};
        border: 1px solid {THEME_COLOR};
    }}
    QPushButton.secondary:hover {{
        background-color: #FFEBEE;
    }}

    /* Nút Quay Lại */
    QPushButton#BackBtn {{
        background-color: transparent;
        color: #555;
        border: 1px solid transparent;
        text-align: left;
    }}
    QPushButton#BackBtn:hover {{
        color: {THEME_COLOR};
        border: 1px solid {THEME_COLOR};
        background-color: #FFF5F5;
        border-radius: 5px;
    }}
    
    /* Links */
    QPushButton.link-blue {{
        background-color: transparent; color: {LINK_COLOR}; border: none; 
        text-align: center; padding: 5px; font-weight: normal;
    }}
    QPushButton.link-blue:hover {{ text-decoration: underline; }}

    QPushButton.link-red {{
        background-color: transparent; color: {THEME_COLOR}; border: none; 
        text-align: center; padding: 5px; font-weight: normal;
    }}
    QPushButton.link-red:hover {{ text-decoration: underline; }}

    QPushButton.link {{
        background-color: transparent; color: {THEME_COLOR}; border: none; 
        text-align: left; padding: 0;
    }}
    QPushButton.link:hover {{ text-decoration: underline; }}

    /* Typography */
    QLabel.title {{
        font-size: 26px; font-weight: bold; color: {THEME_COLOR}; margin-bottom: 10px;
    }}
    QLabel.header {{
        font-size: 18px; font-weight: bold; margin-top: 10px; margin-bottom: 5px;
    }}
    
    /* Cards */
    QFrame#Card {{
        background-color: {CARD_BG}; border-radius: 10px; border: 1px solid #E0E0E0;
    }}
    QFrame#Card:hover {{
        border: 1px solid {THEME_COLOR}; background-color: #FFFDFD;
    }}
    
    QScrollArea {{ border: none; background-color: transparent; }}
    QScrollArea > QWidget > QWidget {{ background-color: transparent; }}
    QFrame#Navbar {{ background-color: {THEME_COLOR}; border-bottom: 2px solid #B71C1C; }}
"""

def get_logo_pixmap(height=100):
    if os.path.exists(LOGO_PATH):
        pixmap = QPixmap(LOGO_PATH)
    else:
        pixmap = QPixmap(height, height)
        pixmap.fill(QColor(THEME_COLOR))
    return pixmap.scaledToHeight(height, Qt.SmoothTransformation)

def mask_image_circular(pixmap, size):
    if pixmap.isNull(): return pixmap
    scaled_pixmap = pixmap.scaled(size, size, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
    out_pixmap = QPixmap(size, size)
    out_pixmap.fill(Qt.transparent)
    painter = QPainter(out_pixmap)
    painter.setRenderHint(QPainter.Antialiasing)
    painter.setRenderHint(QPainter.SmoothPixmapTransform)
    path = QPainterPath()
    path.addEllipse(0, 0, size, size)
    painter.setClipPath(path)
    x = (size - scaled_pixmap.width()) // 2
    y = (size - scaled_pixmap.height()) // 2
    painter.drawPixmap(x, y, scaled_pixmap)
    painter.end()
    return out_pixmap

def is_valid_email(email):
    return re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email)

def is_valid_password(password):
    if not (8 <= len(password) <= 24): return False
    if not re.search(r"[a-z]", password): return False
    if not re.search(r"[A-Z]", password): return False
    if not re.search(r"\d", password): return False
    if not re.search(r"[@$!%*?&]", password): return False
    return True

class DataManager:
    def __init__(self):
        self.data = {"users": [], "events": [], "current_user": None}
        self.load_data()

    def load_data(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
            except: pass 
        self.save_data() 

    def save_data(self):
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

    def register_user(self, user_data):
        for u in self.data["users"]:
            if u["username"] == user_data["username"]: return False, "Tên đăng nhập đã tồn tại."
            if u["email"] == user_data["email"]: return False, "Email đã được sử dụng."
        user_data["id"] = str(datetime.now().timestamp())
        defaults = {"student_id": "", "class_name": "", "dob": "", "gender": "Nam", "address": "", "avatar": ""}
        user_data.update(defaults)
        self.data["users"].append(user_data)
        self.save_data()
        return True, "Đăng ký thành công!"

    def login(self, identifier, password):
        for u in self.data["users"]:
            if (u["username"] == identifier or u["email"] == identifier) and u["password"] == password:
                self.data["current_user"] = u
                self.save_data()
                return True, u
        return False, None

    def update_user(self, updated_data):
        if not self.data["current_user"]: return False
        for i, u in enumerate(self.data["users"]):
            if u["id"] == self.data["current_user"]["id"]:
                self.data["users"][i].update(updated_data)
                self.data["current_user"] = self.data["users"][i]
                self.save_data()
                return True
        return False

    def delete_account(self):
        if not self.data["current_user"]: return
        uid = self.data["current_user"]["id"]
        self.data["users"] = [u for u in self.data["users"] if u["id"] != uid]
        self.logout()

    def logout(self):
        self.data["current_user"] = None
        self.save_data()

    def add_event(self, event_data):
        event_data["id"] = str(datetime.now().timestamp())
        event_data["participants"] = []
        self.data["events"].append(event_data)
        self.save_data()

    def update_event(self, event_id, new_data):
        for i, e in enumerate(self.data["events"]):
            if e["id"] == event_id:
                new_data["participants"] = e["participants"]
                new_data["id"] = event_id
                self.data["events"][i] = new_data
                self.save_data()
                return True
        return False

    def delete_event(self, event_id):
        self.data["events"] = [e for e in self.data["events"] if e["id"] != event_id]
        self.save_data()

    def toggle_participation(self, event_id, user_id):
        for event in self.data["events"]:
            if event["id"] == event_id:
                if user_id in event["participants"]:
                    event["participants"].remove(user_id)
                    status = "removed"
                else:
                    event["participants"].append(user_id)
                    status = "added"
                self.save_data()
                return status, len(event["participants"])
        return None, 0

db = DataManager()

class EventCountdown(QLabel):
    def __init__(self, event_data, parent=None):
        super().__init__(parent)
        self.event_data = event_data
        self.setStyleSheet("font-weight: bold; font-size: 12px; margin-top: 5px;")
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
        self.update_time()

    def update_time(self):
        try:
            s_date = self.event_data.get("start_date", self.event_data.get("date"))
            e_date = self.event_data.get("end_date", s_date)
            s_time = self.event_data.get("start_time", "00:00")
            e_time = self.event_data.get("end_time", "23:59")
            
            fmt = "%d/%m/%Y %H:%M"
            try:
                start_dt = datetime.strptime(f"{s_date} {s_time}", fmt)
                end_dt = datetime.strptime(f"{e_date} {e_time}", fmt)
            except:
                self.setText(""); return

            now = datetime.now()
            if now < start_dt:
                delta = start_dt - now
                self.setStyleSheet("color: #E64A19; font-weight: bold; font-size: 12px; margin-top: 5px;")
                self.setText(f"🕒 Bắt đầu sau {self.format_delta(delta)}")
            elif start_dt <= now <= end_dt:
                delta = end_dt - now
                self.setStyleSheet("color: #388E3C; font-weight: bold; font-size: 12px; margin-top: 5px;")
                self.setText(f"⏳ Kết thúc sau {self.format_delta(delta)}")
            else:
                self.timer.stop()
                self.setStyleSheet("color: #757575; font-style: italic; font-size: 12px; margin-top: 5px;")
                self.setText("🏁 Đã kết thúc")
        except: self.setText("")

    def format_delta(self, delta):
        total = int(delta.total_seconds())
        d = total // 86400
        h = (total % 86400) // 3600
        m = (total % 3600) // 60
        s = total % 60
        if d > 0: return f"{d} ngày {h:02}:{m:02}:{s:02}"
        elif h > 0: return f"{h:02}:{m:02}:{s:02}"
        else: return f"{m:02}:{s:02}"

class StyledInput(QLineEdit):
    def __init__(self, placeholder, is_password=False):
        super().__init__()
        self.setPlaceholderText(placeholder)
        if is_password:
            self.setEchoMode(QLineEdit.Password)
            self.toggle_action = self.addAction(QIcon(), QLineEdit.TrailingPosition)
            self.toggle_action.triggered.connect(self.toggle_echo)
            self.update_icon(True)
    def toggle_echo(self):
        is_hidden = self.echoMode() == QLineEdit.Password
        self.setEchoMode(QLineEdit.Normal) if is_hidden else self.setEchoMode(QLineEdit.Password)
        self.update_icon(not is_hidden)
    def update_icon(self, is_hidden):
        icon_text = "👁️" if not is_hidden else "🔒"
        pix = QPixmap(24, 24)
        pix.fill(Qt.transparent)
        painter = QPainter(pix)
        painter.setPen(QColor("#777"))
        painter.drawText(pix.rect(), Qt.AlignCenter, icon_text)
        painter.end()
        self.toggle_action.setIcon(QIcon(pix))

class BaseScreen(QWidget):
    def __init__(self, nav_callback):
        super().__init__()
        self.nav = nav_callback
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setAlignment(Qt.AlignTop)

class AuthScreen(BaseScreen):
    def __init__(self, nav_callback, title_text):
        super().__init__(nav_callback)
        top_bar = QHBoxLayout()
        top_bar.setContentsMargins(10,10,10,0)
        btn_back = QPushButton("←")
        btn_back.setObjectName("BackBtn") 
        btn_back.setFixedSize(40, 40)
        btn_back.clicked.connect(lambda: self.nav("start"))
        top_bar.addWidget(btn_back)
        top_bar.addStretch()
        self.layout.addLayout(top_bar)
        
        self.content_layout = QVBoxLayout()
        self.content_layout.setSpacing(15)
        self.content_layout.setAlignment(Qt.AlignCenter)
        
        title_lbl = QLabel(title_text)
        title_lbl.setProperty("class", "title")
        title_lbl.setAlignment(Qt.AlignCenter)
        self.content_layout.addWidget(title_lbl)
        
        container = QFrame()
        container.setObjectName("Card") 
        container.setLayout(self.content_layout)
        container.setFixedWidth(420)
        self.content_layout.setContentsMargins(30, 30, 30, 30)

        wrapper = QHBoxLayout()
        wrapper.addStretch()
        wrapper.addWidget(container)
        wrapper.addStretch()
        self.layout.addLayout(wrapper)
        self.layout.addStretch()

class StartScreen(BaseScreen):
    def __init__(self, nav_callback):
        super().__init__(nav_callback)
        self.layout.setAlignment(Qt.AlignCenter)
        logo = QLabel()
        logo.setPixmap(get_logo_pixmap(180))
        logo.setAlignment(Qt.AlignCenter)
        title = QLabel("Quản Lý Sự Kiện - PTIT")
        title.setProperty("class", "title")
        title.setAlignment(Qt.AlignCenter)
        btn_container = QVBoxLayout()
        btn_container.setSpacing(15)
        btn_login = QPushButton("Đăng Nhập")
        btn_login.setProperty("class", "secondary")
        btn_login.setMinimumWidth(200)
        btn_login.clicked.connect(lambda: self.nav("login"))
        btn_register = QPushButton("Đăng Ký")
        btn_register.setProperty("class", "primary")
        btn_register.setMinimumWidth(200)
        btn_register.clicked.connect(lambda: self.nav("register"))
        btn_container.addWidget(btn_login)
        btn_container.addWidget(btn_register)
        self.layout.addWidget(logo)
        self.layout.addWidget(title)
        self.layout.addSpacing(40)
        self.layout.addLayout(btn_container)

class LoginScreen(AuthScreen):
    def __init__(self, nav_callback):
        super().__init__(nav_callback, "Đăng Nhập")
        self.txt_user = StyledInput("Tên đăng nhập / Email")
        self.txt_pass = StyledInput("Mật khẩu", is_password=True)
        btn_submit = QPushButton("Đăng Nhập")
        btn_submit.setProperty("class", "primary")
        btn_submit.clicked.connect(self.do_login)
        link_layout = QHBoxLayout()
        btn_forgot = QPushButton("Quên mật khẩu?")
        btn_forgot.setProperty("class", "link-blue")
        btn_forgot.clicked.connect(lambda: self.nav("forgot_pass"))
        btn_reg = QPushButton("Chưa có tài khoản? 'Đăng ký'")
        btn_reg.setProperty("class", "link-blue")
        btn_reg.clicked.connect(lambda: self.nav("register"))
        link_layout.addWidget(btn_forgot)
        link_layout.addStretch()
        link_layout.addWidget(btn_reg)
        self.content_layout.addWidget(self.txt_user)
        self.content_layout.addWidget(self.txt_pass)
        self.content_layout.addSpacing(10)
        self.content_layout.addWidget(btn_submit)
        self.content_layout.addLayout(link_layout)
    def do_login(self):
        user_id = self.txt_user.text().strip()
        pwd = self.txt_pass.text()
        success, acc = db.login(user_id, pwd)
        if success: self.nav("home")
        else: QMessageBox.warning(self, "Lỗi", "Sai tên đăng nhập hoặc mật khẩu!")

class RegisterScreen(AuthScreen):
    def __init__(self, nav_callback):
        super().__init__(nav_callback, "Đăng Ký Tài Khoản")
        self.txt_user = StyledInput("Tên Đăng Nhập")
        self.txt_name = StyledInput("Họ và Tên")
        self.txt_email = StyledInput("Email")
        self.cmb_role = QComboBox()
        self.cmb_role.addItems(["Sinh Viên", "Ban Tổ Chức"])
        self.txt_pass = StyledInput("Mật Khẩu", is_password=True)
        self.txt_confirm = StyledInput("Xác nhận mật khẩu", is_password=True)
        btn_submit = QPushButton("Tạo Tài Khoản")
        btn_submit.setProperty("class", "primary")
        btn_submit.clicked.connect(self.do_register)
        btn_login = QPushButton("Đã có tài khoản? 'Đăng Nhập'")
        btn_login.setProperty("class", "link-blue")
        btn_login.clicked.connect(lambda: self.nav("login"))
        self.content_layout.addWidget(self.txt_user)
        self.content_layout.addWidget(self.txt_name)
        self.content_layout.addWidget(self.txt_email)
        lbl_role = QLabel("Vai trò:")
        lbl_role.setStyleSheet("color: #555; font-weight: bold;")
        self.content_layout.addWidget(lbl_role)
        self.content_layout.addWidget(self.cmb_role)
        self.content_layout.addWidget(self.txt_pass)
        self.content_layout.addWidget(self.txt_confirm)
        self.content_layout.addSpacing(10)
        self.content_layout.addWidget(btn_submit)
        self.content_layout.addWidget(btn_login)
    def do_register(self):
        if not all([self.txt_user.text(), self.txt_name.text(), self.txt_email.text(), self.txt_pass.text(), self.txt_confirm.text()]):
            QMessageBox.warning(self, "Lỗi", "Vui lòng điền đầy đủ thông tin!")
            return
        if not is_valid_email(self.txt_email.text()):
            QMessageBox.warning(self, "Lỗi", "Email không hợp lệ!")
            return
        if not is_valid_password(self.txt_pass.text()):
            QMessageBox.warning(self, "Lỗi", "Mật khẩu không đủ mạnh.")
            return
        if self.txt_pass.text() != self.txt_confirm.text():
            QMessageBox.warning(self, "Lỗi", "Mật khẩu xác nhận không khớp!")
            return
        role = "admin" if self.cmb_role.currentText() == "Ban Tổ Chức" else "student"
        data = {
            "username": self.txt_user.text(),
            "full_name": self.txt_name.text(),
            "email": self.txt_email.text(),
            "role": role,
            "password": self.txt_pass.text()
        }
        success, msg = db.register_user(data)
        if success:
            QMessageBox.information(self, "Thành công", msg)
            self.nav("login")
        else:
            QMessageBox.warning(self, "Lỗi", msg)

class ForgotPasswordScreen(AuthScreen):
    def __init__(self, nav_callback):
        super().__init__(nav_callback, "Đặt Lại Mật Khẩu")
        self.txt_email = StyledInput("Nhập Email đăng ký")
        self.txt_new_pass = StyledInput("Mật khẩu mới", is_password=True)
        self.txt_confirm = StyledInput("Nhập lại mật khẩu mới", is_password=True)
        btn_submit = QPushButton("Xác Nhận")
        btn_submit.setProperty("class", "primary")
        btn_submit.clicked.connect(self.do_reset)
        self.content_layout.addWidget(self.txt_email)
        self.content_layout.addWidget(self.txt_new_pass)
        self.content_layout.addWidget(self.txt_confirm)
        self.content_layout.addWidget(btn_submit)
    def do_reset(self):
        email = self.txt_email.text().strip()
        pwd = self.txt_new_pass.text()
        confirm = self.txt_confirm.text()
        if not is_valid_email(email):
            QMessageBox.warning(self, "Lỗi", "Email không hợp lệ")
            return
        if pwd != confirm:
            QMessageBox.warning(self, "Lỗi", "Mật khẩu không khớp")
            return
        found = False
        for user in db.data["users"]:
            if user["email"] == email:
                user["password"] = pwd
                db.save_data()
                found = True
                break
        if found:
            QMessageBox.information(self, "Thành công", "Đổi mật khẩu thành công.")
            self.nav("login")
        else:
            QMessageBox.warning(self, "Lỗi", "Email không tồn tại.")

class EventDetailDialog(QDialog):
    def __init__(self, event, user, parent=None):
        super().__init__(parent)
        self.event_data = event # FIX TÊN BIẾN
        self.user = user
        self.setWindowTitle(event["title"])
        self.setMinimumSize(600, 700)
        self.setStyleSheet(STYLESHEET + """ QScrollArea { background-color: transparent; } """)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        content.setStyleSheet(f"background-color: {BG_COLOR};")
        v_content = QVBoxLayout(content)
        v_content.setSpacing(15)
        v_content.setContentsMargins(20, 20, 20, 20)

        lbl_poster = QLabel()
        lbl_poster.setFixedSize(500, 280)
        lbl_poster.setStyleSheet("background-color: #ddd; border: 1px solid #ccc; border-radius: 8px;")
        lbl_poster.setAlignment(Qt.AlignCenter)
        if os.path.exists(self.event_data.get("poster", "")):
            pix = QPixmap(self.event_data["poster"]).scaled(500, 280, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            lbl_poster.setPixmap(pix)
        else:
            lbl_poster.setText("")
        v_content.addWidget(lbl_poster, 0, Qt.AlignCenter)

        lbl_title = QLabel(self.event_data["title"])
        lbl_title.setStyleSheet(f"font-size: 22px; font-weight: bold; color: {THEME_COLOR};")
        lbl_title.setWordWrap(True)
        v_content.addWidget(lbl_title)

        info_frame = QFrame()
        info_frame.setStyleSheet("background-color: white; border-radius: 8px; padding: 10px;")
        grid = QGridLayout(info_frame)
        
        def add_info_row(row, label, val):
            lbl = QLabel(f"<b>{label}</b>")
            val_lbl = QLabel(val)
            val_lbl.setWordWrap(True)
            grid.addWidget(lbl, row, 0)
            grid.addWidget(val_lbl, row, 1)

        s_date = self.event_data.get("start_date", self.event_data.get("date", ""))
        e_date = self.event_data.get("end_date", "")
        date_str = s_date + (f" - {e_date}" if e_date and e_date != s_date else "")

        add_info_row(0, "Thời gian:", date_str)
        add_info_row(1, "Giờ:", f"{self.event_data.get('start_time','')} - {self.event_data.get('end_time','')}")
        add_info_row(2, "Địa điểm:", self.event_data["location"])
        
        max_p = self.event_data.get('max_participants', '∞')
        count = len(self.event_data['participants'])
        text_tham_gia = f"{count}/{max_p} sinh viên" if str(max_p).isdigit() else f"{count} sinh viên"
             
        grid.addWidget(QLabel("<b>Đã Tham Gia:</b>"), 3, 0)
        self.lbl_participants = QLabel(text_tham_gia)
        grid.addWidget(self.lbl_participants, 3, 1)
        
        add_info_row(4, "Phân loại:", self.event_data.get("tags", ""))
        v_content.addWidget(info_frame)

        v_content.addWidget(QLabel("<b>Mô tả:</b>"))
        lbl_desc = QLabel(self.event_data["description"])
        lbl_desc.setWordWrap(True)
        lbl_desc.setStyleSheet("color: #555;")
        v_content.addWidget(lbl_desc)
        
        v_content.addWidget(QLabel("<b>Nội dung chi tiết:</b>"))
        txt_content = QTextEdit()
        txt_content.setHtml(self.event_data["content"])
        txt_content.setReadOnly(True)
        txt_content.setMinimumHeight(150)
        txt_content.setStyleSheet("background-color: white;")
        v_content.addWidget(txt_content)

        v_content.addStretch()
        scroll.setWidget(content)
        layout.addWidget(scroll)

        btn_box = QHBoxLayout()
        is_expired = self.check_expired()
        
        if self.user["role"] == "admin":
            btn_edit = QPushButton("Chỉnh Sửa")
            btn_edit.setProperty("class", "secondary")
            btn_edit.clicked.connect(self.edit_event)
            btn_del = QPushButton("Xóa")
            btn_del.setStyleSheet("background-color: #D32F2F; color: white; border-radius: 5px; padding: 8px;")
            btn_del.clicked.connect(self.delete_event)
            btn_box.addWidget(btn_edit)
            btn_box.addWidget(btn_del)
        else:
            if not is_expired:
                self.btn_join = QPushButton()
                self.update_join_btn_state()
                self.btn_join.clicked.connect(self.toggle_join)
                btn_box.addWidget(self.btn_join)
        
        btn_ok = QPushButton("Đóng")
        btn_ok.clicked.connect(self.accept)
        btn_box.addWidget(btn_ok)
        layout.addLayout(btn_box)

    def check_expired(self):
        try:
            e_date_str = self.event_data.get("end_date", self.event_data.get("date"))
            return datetime.strptime(e_date_str, "%d/%m/%Y").date() < datetime.now().date()
        except: return True

    def update_join_btn_state(self):
        if db.data["current_user"]["id"] in self.event_data["participants"]:
            self.btn_join.setText("Hủy Tham Gia")
            self.btn_join.setProperty("class", "secondary")
        else:
            self.btn_join.setText("Tham Gia")
            self.btn_join.setProperty("class", "primary")

    def toggle_join(self):
        status, count = db.toggle_participation(self.event_data['id'], db.data["current_user"]["id"])
        if status:
            max_p = self.event_data.get('max_participants', '∞')
            self.lbl_participants.setText(f"{count}/{max_p} sinh viên" if str(max_p).isdigit() else f"{count} sinh viên")
            if status == "added": self.event_data["participants"].append(db.data["current_user"]["id"])
            else: self.event_data["participants"].remove(db.data["current_user"]["id"])
            self.update_join_btn_state()

    def edit_event(self): self.done(2)
    def delete_event(self):
        if QMessageBox.question(self, "Xác nhận", "Xóa sự kiện này?", QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
            db.delete_event(self.event_data['id'])
            self.done(3)

class EventWizard(QWidget):
    def __init__(self, nav_callback, event_data=None):
        super().__init__()
        self.nav = nav_callback
        self.edit_mode = event_data is not None
        self.event_id = event_data['id'] if self.edit_mode else None
        self.init_ui(event_data)

    def init_ui(self, event_data):
        layout = QVBoxLayout(self)
        header_text = "Chỉnh Sửa Sự Kiện" if self.edit_mode else "Tạo Sự Kiện Mới"
        lbl_header = QLabel(header_text)
        lbl_header.setProperty("class", "title")
        btn_back = QPushButton("← Quay Lại")
        btn_back.setObjectName("BackBtn")
        btn_back.clicked.connect(lambda: self.nav("manage_event"))
        
        header_layout = QHBoxLayout()
        header_layout.addWidget(btn_back)
        header_layout.addStretch()
        header_layout.addWidget(lbl_header)
        header_layout.addStretch()
        layout.addLayout(header_layout)

        form_scroll = QScrollArea()
        form_scroll.setWidgetResizable(True)
        form_content = QWidget()
        form_layout = QGridLayout(form_content)
        form_layout.setSpacing(10)
        
        self.inp_title = QLineEdit()
        self.inp_start_date = QDateEdit()
        self.inp_start_date.setCalendarPopup(True)
        self.inp_start_date.setDisplayFormat("dd/MM/yyyy")
        self.inp_start_date.setDate(QDate.currentDate())

        self.inp_end_date = QDateEdit()
        self.inp_end_date.setCalendarPopup(True)
        self.inp_end_date.setDisplayFormat("dd/MM/yyyy")
        self.inp_end_date.setDate(QDate.currentDate())
        
        self.inp_start_time = QTimeEdit()
        self.inp_start_time.setDisplayFormat("HH:mm")
        self.inp_end_time = QTimeEdit()
        self.inp_end_time.setDisplayFormat("HH:mm")
        
        self.inp_location = QLineEdit()
        self.inp_desc = QTextEdit()
        self.inp_desc.setMaximumHeight(60)
        self.inp_poster = QLineEdit()
        btn_poster = QPushButton("Chọn Ảnh")
        btn_poster.setProperty("class", "link-blue") 
        btn_poster.clicked.connect(self.choose_poster)
        self.inp_content = QTextEdit() 
        self.inp_tags = QLineEdit()
        self.inp_max = QLineEdit()
        self.inp_fee = QLineEdit("0")
        
        def add_row(row, label, widget):
            lbl = QLabel(label)
            lbl.setStyleSheet("font-weight: bold;")
            form_layout.addWidget(lbl, row, 0)
            if isinstance(widget, list):
                h = QHBoxLayout()
                for w in widget: h.addWidget(w)
                form_layout.addLayout(h, row, 1)
            else:
                form_layout.addWidget(widget, row, 1)

        add_row(0, "Tên Sự Kiện *:", self.inp_title)
        add_row(1, "Bắt đầu (Ngày - Giờ) *:", [self.inp_start_date, self.inp_start_time])
        add_row(2, "Kết thúc (Ngày - Giờ) *:", [self.inp_end_date, self.inp_end_time])
        add_row(3, "Địa điểm *:", self.inp_location)
        add_row(4, "Mô tả ngắn:", self.inp_desc)
        add_row(5, "Poster:", [self.inp_poster, btn_poster])
        add_row(6, "Nội dung (HTML) *:", self.inp_content)
        add_row(7, "Phân loại (Tags):", self.inp_tags)
        add_row(8, "Số lượng tối đa:", self.inp_max)
        add_row(9, "Lệ phí:", self.inp_fee)
        
        form_scroll.setWidget(form_content)
        layout.addWidget(form_scroll)
        
        btn_box = QHBoxLayout()
        btn_cancel = QPushButton("Hủy")
        btn_cancel.clicked.connect(lambda: self.nav("manage_event"))
        btn_save = QPushButton("Lưu Sự Kiện")
        btn_save.setProperty("class", "primary")
        btn_save.clicked.connect(self.save_event)
        
        btn_box.addStretch()
        btn_box.addWidget(btn_cancel)
        btn_box.addWidget(btn_save)
        layout.addLayout(btn_box)
        
        if self.edit_mode: self.load_data(event_data)

    def choose_poster(self):
        fname, _ = QFileDialog.getOpenFileName(self, "Chọn Poster", "", "Images (*.png *.jpg *.jpeg)")
        if fname: self.inp_poster.setText(fname)

    def load_data(self, data):
        self.inp_title.setText(data['title'])
        self.inp_start_date.setDate(QDate.fromString(data.get('start_date', data.get('date')), "dd/MM/yyyy"))
        self.inp_end_date.setDate(QDate.fromString(data.get('end_date', data.get('date')), "dd/MM/yyyy"))
        self.inp_start_time.setTime(QTime.fromString(data['start_time'], "HH:mm"))
        self.inp_end_time.setTime(QTime.fromString(data['end_time'], "HH:mm"))
        self.inp_location.setText(data['location'])
        self.inp_desc.setPlainText(data.get('description', ''))
        self.inp_poster.setText(data.get('poster', ''))
        self.inp_content.setHtml(data.get('content', '')) 
        self.inp_tags.setText(data.get('tags', ''))
        self.inp_max.setText(str(data.get('max_participants', '')))
        self.inp_fee.setText(str(data.get('fee', '')))

    def save_event(self):
        if not self.inp_title.text() or not self.inp_location.text() or not self.inp_content.toPlainText():
            QMessageBox.warning(self, "Thiếu thông tin", "Vui lòng điền các trường bắt buộc (*)")
            return
            
        data = {
            "title": self.inp_title.text(),
            "date": self.inp_start_date.date().toString("dd/MM/yyyy"),
            "start_date": self.inp_start_date.date().toString("dd/MM/yyyy"),
            "end_date": self.inp_end_date.date().toString("dd/MM/yyyy"),
            "start_time": self.inp_start_time.time().toString("HH:mm"),
            "end_time": self.inp_end_time.time().toString("HH:mm"),
            "location": self.inp_location.text(),
            "description": self.inp_desc.toPlainText(),
            "poster": self.inp_poster.text(),
            "content": self.inp_content.toHtml(),
            "tags": self.inp_tags.text(),
            "max_participants": self.inp_max.text(),
            "fee": self.inp_fee.text(),
        }
        
        if self.edit_mode: db.update_event(self.event_id, data)
        else: db.add_event(data)
        self.nav("manage_event")

class HomeScreen(BaseScreen):
    def __init__(self, navigator):
        super().__init__(navigator)
        self.navbar = self.create_navbar()
        self.layout.addWidget(self.navbar)
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(20, 20, 20, 20)
        self.scroll.setWidget(self.content_widget)
        self.layout.addWidget(self.scroll)

    def create_navbar(self):
        navbar = QFrame()
        navbar.setObjectName("Navbar")
        navbar.setFixedHeight(60)
        nav_layout = QHBoxLayout(navbar)
        nav_layout.setContentsMargins(20, 0, 20, 0)
        brand_layout = QHBoxLayout()

        small_logo = QLabel()
        small_logo.setFixedSize(45, 45)
        
        small_logo.setStyleSheet("""
            background-color: white; 
            border-radius: 20px; 
            padding: 4px;
        """)
        small_logo.setAlignment(Qt.AlignCenter)
        small_logo.setPixmap(get_logo_pixmap(28))

        title = QLabel("Quản Lý Sự Kiện - PTIT")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: white; margin-left: 5px;")
        brand_layout.addWidget(small_logo)
        brand_layout.addWidget(title)
        nav_layout.addLayout(brand_layout)
        nav_layout.addStretch()
        self.btn_avatar = QPushButton()
        self.btn_avatar.setFixedSize(40, 40)
        self.btn_avatar.setStyleSheet("""QPushButton {border-radius: 20px; background-color: white; border: 2px solid white; text-align: center; padding: 0px;}""")
        self.menu = QMenu()
        self.action_profile = self.menu.addAction("Thông Tin") 
        self.action_profile.triggered.connect(lambda: self.nav("profile"))
        self.menu.addSeparator()
        self.menu.addAction("Đăng Xuất", self.do_logout)
        self.menu.addAction("Thoát", QApplication.instance().quit)
        self.btn_avatar.setMenu(self.menu)
        nav_layout.addWidget(self.btn_avatar)
        return navbar

    def do_logout(self):
        db.logout()
        self.nav("start")

    def load_content(self):
        self.current_user = db.data.get("current_user")
        if not self.current_user: self.nav("start"); return
        
        role = self.current_user.get("role")
        self.action_profile.setText("Thông Tin Cá Nhân" if role == "admin" else "Thông Tin Sinh Viên")

        self.content_widget = QWidget()
        self.scroll.setWidget(self.content_widget)
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(20, 20, 20, 20)

        avatar_path = self.current_user.get("avatar", "")
        if os.path.exists(avatar_path):
            pix = mask_image_circular(QPixmap(avatar_path), 40)
            self.btn_avatar.setText("")  
            self.btn_avatar.setIcon(QIcon(pix))
            self.btn_avatar.setIconSize(QSize(36, 36))
        else:
            self.btn_avatar.setIcon(QIcon()) 
            self.btn_avatar.setText("👤")

        if role == "admin":
            btn_container = QHBoxLayout()
            
            btn_manage = QPushButton("⚙️ Quản Lý Sự Kiện")
            btn_manage.setProperty("class", "secondary")
            btn_manage.setCursor(Qt.PointingHandCursor)
            btn_manage.setFixedWidth(640)
            btn_manage.clicked.connect(lambda: self.nav("manage_event"))
            
            btn_container.addStretch()
            btn_container.addWidget(btn_manage)
            btn_container.addStretch()
            
            self.content_layout.addLayout(btn_container)

        self.render_event_section("Sự Kiện Đang Diễn Ra", "🟢", is_ongoing=True)
        self.render_event_section("Sự Kiện Đã Hết Hạn", "🔴", is_ongoing=False)
        self.content_layout.addStretch()

    def render_event_section(self, title, icon, is_ongoing):
        header = QLabel(f"{icon} {title}")
        header.setProperty("class", "header")
        self.content_layout.addWidget(header)
        events = db.data["events"]
        filtered = []
        now = datetime.now().date()
        for e in events:
            try:
                e_date = datetime.strptime(e.get("end_date", e.get("date")), "%d/%m/%Y").date()
                if (is_ongoing and e_date >= now) or (not is_ongoing and e_date < now): filtered.append(e)
            except: pass 
        
        if not filtered:
            lbl_empty = QLabel("Hiện chưa có sự kiện nào." if is_ongoing else "Không có sự kiện cũ.")
            lbl_empty.setStyleSheet("color: #777; font-style: italic; margin-left: 20px;")
            self.content_layout.addWidget(lbl_empty)
            return

        grid_widget = QWidget()
        grid = QGridLayout(grid_widget)
        grid.setSpacing(20)
        col = 0; row = 0; MAX_COL = 4
        for event in filtered:
            card = self.create_event_card(event)
            grid.addWidget(card, row, col)
            col += 1
            if col >= MAX_COL: col = 0; row += 1
        self.content_layout.addWidget(grid_widget)
        self.content_layout.addSpacing(20)

    def create_event_card(self, event):
        card = QFrame()
        card.setObjectName("Card")
        card.setFixedSize(230, 310)
        card.setCursor(Qt.PointingHandCursor)
        card.mousePressEvent = lambda ev: self.open_event_detail(event)

        vbox = QVBoxLayout(card)
        vbox.setContentsMargins(10,10,10,10)
        vbox.setSpacing(5)
        
        lbl_img = QLabel()
        lbl_img.setStyleSheet("background-color: #eee; border-radius: 6px;")
        lbl_img.setFixedSize(208, 140)
        lbl_img.setAlignment(Qt.AlignCenter)
        if os.path.exists(event.get("poster", "")):
            pix = QPixmap(event.get("poster")).scaled(208, 140, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
            lbl_img.setPixmap(pix)
        vbox.addWidget(lbl_img)

        lbl_name = QLabel(event["title"])
        lbl_name.setWordWrap(True)
        lbl_name.setStyleSheet("font-weight: bold; font-size: 15px; color: #333;")
        lbl_name.setAlignment(Qt.AlignTop)
        vbox.addWidget(lbl_name)
        
        s_date = event.get("start_date", event.get("date"))
        date_str = s_date + (f" - {event.get('end_date')}" if event.get('end_date') and event.get('end_date') != s_date else "")
        lbl_date = QLabel(f"📅 {date_str}")
        lbl_date.setStyleSheet("color: #666; font-size: 12px;")
        vbox.addWidget(lbl_date)

        if db.data["current_user"]["id"] in event["participants"]:
            lbl_joined = QLabel("✅ Đã tham gia")
            lbl_joined.setStyleSheet("color: #388E3C; font-weight: bold; font-size: 12px;")
            vbox.addWidget(lbl_joined)

        vbox.addWidget(EventCountdown(event))
        vbox.addStretch()
        return card

    def open_event_detail(self, event):
        user = db.data["current_user"]
        dialog = EventDetailDialog(event, user, self)
        res = dialog.exec()
        if res in [2, 3]: self.nav("manage_event")
        else: self.load_content()

class ProfileScreen(BaseScreen):
    def __init__(self, navigator):
        super().__init__(navigator)
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.content_widget = QWidget()
        self.scroll.setWidget(self.content_widget)
        self.layout.addWidget(self.scroll)
        
    def refresh_ui(self):
        user = db.data["current_user"]
        if not user: self.nav("start"); return
        
        self.content_widget = QWidget()
        self.scroll.setWidget(self.content_widget)
        
        main_layout = QHBoxLayout(self.content_widget)
        main_layout.setContentsMargins(40, 40, 40, 40)

        left_panel = QVBoxLayout()
        left_panel.setSpacing(10)
        btn_back = QPushButton("← Quay Lại")
        btn_back.setObjectName("BackBtn")
        btn_back.clicked.connect(lambda: self.nav("home"))
        left_panel.addWidget(btn_back)
        left_panel.addSpacing(10)

        self.lbl_avatar = QLabel()
        self.lbl_avatar.setFixedSize(150, 150)
        self.lbl_avatar.setStyleSheet(f"background-color: transparent; border: 3px solid {THEME_COLOR}; border-radius: 75px;")
        self.lbl_avatar.setAlignment(Qt.AlignCenter)
        self.update_avatar_display(user.get("avatar", ""))
        
        btn_change_avt = QPushButton("Thay Đổi Ảnh")
        btn_change_avt.setProperty("class", "link-blue") 
        btn_change_avt.clicked.connect(self.change_avatar)
        btn_remove_avt = QPushButton("Gỡ Ảnh")
        btn_remove_avt.setProperty("class", "link-red")
        btn_remove_avt.clicked.connect(self.remove_avatar)
        btn_del_acc = QPushButton("Xóa Tài Khoản")
        btn_del_acc.setStyleSheet("background-color: white; color: #D32F2F; border: 1px solid #D32F2F; margin-top: 20px;")
        btn_del_acc.clicked.connect(self.delete_account)

        left_panel.addWidget(self.lbl_avatar, 0, Qt.AlignCenter)
        left_panel.addWidget(btn_change_avt)
        left_panel.addWidget(btn_remove_avt)
        left_panel.addStretch()
        left_panel.addWidget(btn_del_acc)

        right_panel = QVBoxLayout()
        title_text = "Thông Tin Cá Nhân" if user.get("role") == "admin" else "Thông Tin Sinh Viên"
        header = QLabel(title_text)
        header.setProperty("class", "title")
        right_panel.addWidget(header)
        
        form_frame = QFrame()
        form_frame.setObjectName("Card")
        form = QGridLayout(form_frame)
        form.setSpacing(15)
        form.setContentsMargins(20,20,20,20)

        self.fields = {}
        def add_row(label, key, row_idx, is_readonly=False, widget=None):
            form.addWidget(QLabel(f"<b>{label}</b>"), row_idx, 0)
            if widget: 
                form.addWidget(widget, row_idx, 1)
            else: 
                inp = QLineEdit(user.get(key, ""))
                if is_readonly:
                    inp.setReadOnly(True)
                    inp.setStyleSheet("background-color: #eee; color: #555;")
                else:
                    inp.textChanged.connect(self.on_data_changed)
                form.addWidget(inp, row_idx, 1)
            if not widget: self.fields[key] = inp
            elif isinstance(widget, QLineEdit): self.fields[key] = widget

        add_row("Tên Đăng Nhập", "username", 0, True)
        add_row("Vai Trò", "role", 1, True)
        add_row("Họ và Tên", "full_name", 2)
        add_row("Mã Số Sinh Viên", "student_id", 3)
        add_row("Lớp", "class_name", 4)
        add_row("Email", "email", 5)
        
        dob_edit = QDateEdit()
        dob_edit.setCalendarPopup(True)
        dob_edit.setDisplayFormat("dd/MM/yyyy")
        if user.get("dob"):
            try: dob_edit.setDate(QDate.fromString(user["dob"], "dd/MM/yyyy"))
            except: pass
        dob_edit.dateChanged.connect(self.on_data_changed)
        add_row("Ngày Sinh", "dob", 6, widget=dob_edit)
        self.fields["dob"] = dob_edit

        radio_widget = QWidget()
        radio_layout = QHBoxLayout(radio_widget)
        radio_layout.setContentsMargins(0,0,0,0)
        self.rb_nam = QRadioButton("Nam")
        self.rb_nu = QRadioButton("Nữ")
        self.rb_group = QButtonGroup(radio_widget)
        self.rb_group.addButton(self.rb_nam)
        self.rb_group.addButton(self.rb_nu)
        gender = user.get("gender", "Nam")
        if gender == "Nữ": self.rb_nu.setChecked(True)
        else: self.rb_nam.setChecked(True)
        self.rb_nam.toggled.connect(self.on_data_changed)
        radio_layout.addWidget(self.rb_nam)
        radio_layout.addWidget(self.rb_nu)
        radio_layout.addStretch()
        add_row("Giới Tính", "gender", 7, widget=radio_widget)
        
        inp_addr = QLineEdit(user.get("address", ""))
        inp_addr.textChanged.connect(self.on_data_changed)
        add_row("Địa Chỉ", "address", 8, widget=inp_addr)
        self.fields["address"] = inp_addr 

        right_panel.addWidget(form_frame)
        self.btn_save = QPushButton("Lưu Thông Tin")
        self.btn_save.setProperty("class", "primary")
        self.btn_save.setVisible(False)
        self.btn_save.clicked.connect(self.save_info)
        right_panel.addWidget(self.btn_save)
        right_panel.addStretch()
        main_layout.addLayout(left_panel, 1)
        main_layout.addLayout(right_panel, 3)

    def update_avatar_display(self, path):
        if path and os.path.exists(path):
            pix = mask_image_circular(QPixmap(path), 150)
            self.lbl_avatar.setPixmap(pix)
        else:
            self.lbl_avatar.setPixmap(QPixmap())
            self.lbl_avatar.setText("Chưa có ảnh")
    
    def on_data_changed(self): self.btn_save.setVisible(True)
    def change_avatar(self):
        fname, _ = QFileDialog.getOpenFileName(self, "Chọn Ảnh Đại Diện", "", "Images (*.png *.jpg *.jpeg)")
        if fname:
            self.update_avatar_display(fname)
            self.fields["avatar_new_path"] = fname 
            self.on_data_changed()
    def remove_avatar(self):
        self.update_avatar_display("") 
        self.fields["avatar_new_path"] = "" 
        self.on_data_changed()

    def save_info(self):
        name = self.fields["full_name"].text().strip()
        email = self.fields["email"].text().strip()

        if not name:
            QMessageBox.warning(self, "Lỗi", "Họ và tên không được để trống!")
            self.fields["full_name"].setFocus()
            return

        if not is_valid_email(email):
            QMessageBox.warning(self, "Lỗi", "Email không hợp lệ!")
            self.fields["email"].setFocus()
            return

        user = db.data["current_user"]
        gender_val = "Nam" if self.rb_nam.isChecked() else "Nữ"
        data = {
            "full_name": self.fields["full_name"].text(),
            "student_id": self.fields["student_id"].text(),
            "class_name": self.fields["class_name"].text(),
            "email": self.fields["email"].text(),
            "address": self.fields["address"].text(),
            "dob": self.fields["dob"].date().toString("dd/MM/yyyy"),
            "gender": gender_val
        }
        if "avatar_new_path" in self.fields: data["avatar"] = self.fields["avatar_new_path"]
        db.update_user(data)
        QMessageBox.information(self, "Thành Công", "Đã lưu thông tin thành công!")
        self.btn_save.setVisible(False)

    def delete_account(self):
        if QMessageBox.question(self, "Xác Nhận", "Bạn có chắc muốn xóa tài khoản vĩnh viễn?", QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
            db.delete_account()
            self.nav("start")

class ManageEventScreen(BaseScreen):
    def __init__(self, navigator):
        super().__init__(navigator)
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(20, 20, 20, 20)
        self.scroll.setWidget(self.content_widget)
        self.layout.addWidget(self.scroll)

    def load_content(self):
        self.content_widget = QWidget()
        self.scroll.setWidget(self.content_widget)
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(20, 20, 20, 20)
            
        header_layout = QGridLayout()
        
        lbl_title = QLabel("Quản Lý Sự Kiện")
        lbl_title.setProperty("class", "title")
        lbl_title.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(lbl_title, 0, 0, Qt.AlignCenter)
        
        btn_back = QPushButton("← Quay về Trang Chủ")
        btn_back.setObjectName("BackBtn")
        btn_back.setCursor(Qt.PointingHandCursor)
        btn_back.clicked.connect(lambda: self.nav("home"))
        header_layout.addWidget(btn_back, 0, 0, Qt.AlignLeft)
        
        self.content_layout.addLayout(header_layout)
        self.content_layout.addSpacing(20)

        btn_create = QPushButton("+ TẠO SỰ KIỆN")
        btn_create.setProperty("class", "primary")
        btn_create.setMinimumHeight(45)
        btn_create.setCursor(Qt.PointingHandCursor)
        btn_create.clicked.connect(lambda: self.nav("create_event"))
        self.content_layout.addWidget(btn_create)
        self.content_layout.addSpacing(20)
        
        self.render_event_section("Sự Kiện Đang Diễn Ra", "🟢", is_ongoing=True)
        self.render_event_section("Sự Kiện Đã Hết Hạn", "🔴", is_ongoing=False)
        self.content_layout.addStretch()

    def render_event_section(self, title, icon, is_ongoing):
        header = QLabel(f"{icon} {title}")
        header.setProperty("class", "header")
        self.content_layout.addWidget(header)
        events = db.data["events"]
        filtered = []
        now = datetime.now().date()
        for e in events:
            try:
                e_date = datetime.strptime(e.get("end_date", e.get("date")), "%d/%m/%Y").date()
                if (is_ongoing and e_date >= now) or (not is_ongoing and e_date < now): filtered.append(e)
            except: pass 
        
        if not filtered:
            lbl_empty = QLabel("Hiện chưa có sự kiện nào.")
            lbl_empty.setStyleSheet("color: #777; font-style: italic; margin-left: 20px;")
            self.content_layout.addWidget(lbl_empty)
            return

        grid_widget = QWidget()
        grid = QGridLayout(grid_widget)
        grid.setSpacing(15)
        col = 0; row = 0; MAX_COL = 4
        for e in filtered:
            card = self.create_event_card(e)
            grid.addWidget(card, row, col)
            col += 1
            if col >= MAX_COL: col = 0; row += 1
        self.content_layout.addWidget(grid_widget)
        self.content_layout.addSpacing(30)

    def create_event_card(self, event):
        card = QFrame()
        card.setObjectName("Card")
        card.setFixedSize(230, 310)
        card.setCursor(Qt.PointingHandCursor)
        card.mousePressEvent = lambda ev: self.open_event_popup(event)

        vbox = QVBoxLayout(card)
        vbox.setContentsMargins(10,10,10,10)
        lbl_img = QLabel()
        lbl_img.setStyleSheet("background-color: #eee; border-radius: 6px;")
        lbl_img.setFixedSize(208, 140)
        lbl_img.setAlignment(Qt.AlignCenter)
        if os.path.exists(event.get("poster", "")):
            pix = QPixmap(event.get("poster")).scaled(208, 140, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
            lbl_img.setPixmap(pix)
        vbox.addWidget(lbl_img)

        lbl_name = QLabel(event["title"])
        lbl_name.setWordWrap(True)
        lbl_name.setStyleSheet("font-weight: bold; font-size: 15px; color: #333;")
        lbl_name.setAlignment(Qt.AlignTop)
        vbox.addWidget(lbl_name)
        
        s_date = event.get("start_date", event.get("date"))
        date_str = s_date + (f" - {event.get('end_date')}" if event.get('end_date') and event.get('end_date') != s_date else "")
        lbl_date = QLabel(f"📅 {date_str}")
        lbl_date.setStyleSheet("color: #666; font-size: 12px;")
        vbox.addWidget(lbl_date)
        vbox.addWidget(EventCountdown(event))
        vbox.addStretch()
        return card

    def open_event_popup(self, event):
        role = db.data["current_user"]["role"]
        dialog = EventDetailDialog(event, {"role": role}, self)
        res = dialog.exec()
        if res == 2: self.nav("edit_event", event)
        elif res == 3: self.load_content()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quản Lý Sự Kiện - PTIT")
        self.setMinimumSize(1024, 768)
        self.setStyleSheet(STYLESHEET)
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)
        self.screens = {}
        self.init_screens()
        if db.data.get("current_user"): self.navigate("home")
        else: self.navigate("start")

    def init_screens(self):
        self.screens["start"] = StartScreen(self.navigate)
        self.screens["login"] = LoginScreen(self.navigate)
        self.screens["register"] = RegisterScreen(self.navigate)
        self.screens["forgot_pass"] = ForgotPasswordScreen(self.navigate)
        self.screens["home"] = HomeScreen(self.navigate)
        self.screens["profile"] = ProfileScreen(self.navigate)
        self.screens["manage_event"] = ManageEventScreen(self.navigate)
        for s in self.screens.values(): self.stack.addWidget(s)

    def navigate(self, screen_name, data=None):
        self.setUpdatesEnabled(False) 
        try:
            if screen_name == "create_event":
                wiz = EventWizard(self.navigate)
                self.stack.addWidget(wiz)
                self.stack.setCurrentWidget(wiz)
            elif screen_name == "edit_event":
                wiz = EventWizard(self.navigate, data)
                self.stack.addWidget(wiz)
                self.stack.setCurrentWidget(wiz)
            elif screen_name in self.screens:
                if screen_name == "home": self.screens["home"].load_content()
                elif screen_name == "manage_event": self.screens["manage_event"].load_content()
                elif screen_name == "profile": self.screens["profile"].refresh_ui()
                self.stack.setCurrentWidget(self.screens[screen_name])
        finally:
            self.setUpdatesEnabled(True)

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    icon_path = resource_path(LOGO_PATH)
    window.setWindowIcon(QIcon(icon_path))
    window.show()
    sys.exit(app.exec())