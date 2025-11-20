# PTIT Event Management System 📅

Ứng dụng Desktop quản lý sự kiện dành cho sinh viên và ban tổ chức trường PTIT. Được xây dựng bằng **Python** và thư viện giao diện **PySide6 (Qt)**.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![PySide6](https://img.shields.io/badge/GUI-PySide6-green.svg)
![Status](https://img.shields.io/badge/Status-Completed-red.svg)

## 📖 Giới Thiệu

Dự án này là một giải pháp phần mềm giúp quản lý các hoạt động, sự kiện trong trường đại học. Ứng dụng cho phép Ban tổ chức tạo và quản lý sự kiện, trong khi Sinh viên có thể xem thông tin và đăng ký tham gia.

Giao diện được thiết kế hiện đại, sử dụng tông màu đỏ chủ đạo của PTIT (`#D32F2F`), tối ưu trải nghiệm người dùng với các hiệu ứng hover, bo tròn và bố cục responsive.

## ✨ Tính Năng Chính

### 1. Hệ Thống Tài Khoản & Phân Quyền
* **Đăng ký/Đăng nhập:** Xác thực người dùng, kiểm tra định dạng email và độ mạnh mật khẩu.
* **Quên mật khẩu:** Tính năng khôi phục mật khẩu cơ bản.
* **Phân quyền:**
    * **Sinh viên:** Xem sự kiện, đăng ký/hủy tham gia, chỉnh sửa hồ sơ cá nhân.
    * **Ban Tổ Chức (Admin):** Toàn quyền quản lý sự kiện (Thêm, Sửa, Xóa), xem danh sách người tham gia.

### 2. Quản Lý Sự Kiện (Event Management)
* **Hiển thị:** Danh sách sự kiện được chia thành "Đang diễn ra" và "Đã hết hạn" dựa trên thời gian thực.
* **Bộ đếm ngược (Countdown):**
    * Hiển thị thời gian còn lại đến khi bắt đầu (🕒 Màu cam).
    * Hiển thị thời gian còn lại đến khi kết thúc (⏳ Màu xanh).
* **Chi tiết sự kiện:** Hỗ trợ nội dung HTML, ảnh poster, thời gian bắt đầu/kết thúc, địa điểm và số lượng người tham gia.
* **CRUD:** Ban tổ chức có thể Tạo mới, Chỉnh sửa và Xóa sự kiện (kể cả sự kiện đã hết hạn).

### 3. Hồ Sơ Cá Nhân (User Profile)
* **Avatar:** Hỗ trợ tải ảnh đại diện, tự động cắt hình tròn, có tính năng "Gỡ ảnh" về mặc định.
* **Thông tin:** Cập nhật họ tên, mã sinh viên, lớp, ngày sinh (Date picker), giới tính (Radio button), địa chỉ.
* **Bảo mật:** Tùy chọn xóa tài khoản vĩnh viễn.

### 4. Giao Diện & Trải Nghiệm (UI/UX)
* **Theme:** Màu đỏ PTIT (`#D32F2F`) kết hợp nền trắng/xám nhạt sạch sẽ.
* **Responsive:** Giao diện tự co giãn, căn giữa tiêu đề thông minh.
* **Double Buffering:** Xử lý mượt mà khi chuyển trang, không bị chập chờn (flickering).
* **Visual Cues:** Hiệu ứng viền đỏ khi hover vào lịch, nút bấm, và các thành phần tương tác.

## 🛠️ Cài Đặt & Chạy Ứng Dụng

# Cách 1:
Có thể tải, giải nén và khởi chạy trực tiếp file `EventManager.exe` tại [đây](https://drive.google.com/drive/folders/1V9vb3JM3ksyquWqbaOrOCAanGORHlhA3?hl=vi)

# Cách 2:
### Yêu cầu hệ thống
* Python 3.8 trở lên.

### Bước 1: Cài đặt thư viện
Mở terminal/command prompt và chạy lệnh sau để cài đặt `PySide6` và chương trình:

```bash
pip install PySide6

git clone https://github.com/havier07/Event-Manager.git

cd Event-Manager

python main.py
```

### Bước 2: Chuẩn bị tài nguyên

Đảm bảo bạn có file logo (tùy chọn) đặt cùng thư mục với file code:

Logo_PTIT.png: Ảnh logo trường (nếu không có, ứng dụng sẽ tự tạo placeholder).

### Bước 3: Chạy ứng dụng

```bash
python main.py
```

## 📂 Cấu Trúc Dự Án

```Plaintext
Event-Manager/
│
├── main.py                # Mã nguồn chính của chương trình
├── event_app_data.json    # Cơ sở dữ liệu (Tự động tạo khi chạy lần đầu)
├── Logo_PTIT.png          # Logo hiển thị trên giao diện (Cần thêm vào)
└── README.md              # Tài liệu hướng dẫn
```

## ⚙️ Công Nghệ Sử Dụng
Ngôn ngữ: Python.

Framework GUI: PySide6 (Qt for Python).

Database: JSON (Lưu trữ cục bộ đơn giản, không cần cài đặt SQL).

Libraries: sys, os, json, re, datetime.