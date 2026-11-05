# HCNS Manager

Ứng dụng quản lý Hành chính – Nhân sự viết bằng Flask theo cấu trúc MVC.

## Chạy cục bộ

1. Tạo môi trường ảo và cài thư viện trong `requirements.txt`.
2. Sao chép `.env.example` thành `.env`, đặt `DB_ENGINE=sqlite` để chạy cục bộ.
3. Chạy `flask --app main run --debug`.

Lần đầu chạy, mở `/setup` để tạo tài khoản administrator đầu tiên (mật khẩu tối thiểu 12 ký tự). Administrator tạo tài khoản và gán vai trò tại **Tài khoản người dùng**.

Ứng dụng khởi tạo các bảng còn thiếu khi khởi động. SQLite lưu dữ liệu trong `instance/hcns_manager.db`.

## Kết nối SQL Server

Cài ODBC Driver 18 for SQL Server và `pyodbc`, sau đó cấu hình:

```dotenv
DB_ENGINE=sqlserver
DB_SERVER=192.168.1.69\QA-204
DB_NAME=HCNS_Manager
DB_ODBC_DRIVER=ODBC Driver 18 for SQL Server
```

Để dùng Windows Authentication, để trống `DB_USER` và `DB_PASSWORD`. Nếu dùng SQL Authentication, đặt hai biến này bên ngoài mã nguồn. Tài khoản kết nối cần quyền đọc/ghi và tạo/cập nhật bảng trong database.

## Cấu trúc MVC

- `app/models/`: kết nối database, metadata nghiệp vụ và audit log.
- `app/modules/<module>/model.py`: truy cập dữ liệu nghiệp vụ của module.
- `app/modules/<module>/controller.py`: route và điều phối yêu cầu của module.
- `app/templates/modules/<module>/`: giao diện riêng của module; các phần dùng chung nằm trong `app/templates/modules/_index.html`.
- `app/controllers/`: dashboard và nhật ký hệ thống.
- `app/static/`: CSS responsive và JavaScript tương tác.

Các module dữ liệu có danh sách, tìm kiếm, lọc trạng thái, thêm/sửa/xóa và xuất CSV. Quản lý phòng họp có danh mục mẫu, đặt lịch, phát hiện trùng khung giờ, duyệt/từ chối/hủy. Đây là nền tảng MVC dùng bộ trường dữ liệu chung; các quy trình tính lương, đồng bộ thiết bị chấm công, thông báo thời gian thực và sao lưu cần được tích hợp theo quy trình thực tế của công ty.

## Vai trò truy cập

- `administrator`: truy cập dashboard, toàn bộ phân hệ, duyệt phòng họp và quản lý tài khoản.
- Người dùng khác: chỉ truy cập đơn nghỉ phép của chính mình và dữ liệu chấm công gán theo tài khoản. Chỉ được tạo đơn nghỉ; trạng thái do administrator quản lý.
- `to_truong`, `to_pho`, `truong_phong`, `pho_phong`, `ban_giam_doc`: được xem lịch và yêu cầu đặt phòng. Mọi yêu cầu mới có trạng thái chờ administrator duyệt; thời gian chồng lấn với lịch chưa hủy/bị từ chối bị từ chối ngay khi gửi.
