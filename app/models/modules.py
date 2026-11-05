"""Module metadata: shared persistence model, distinct MVC views/controllers."""
MODULES = {
    "employees": {"name": "Hồ sơ nhân viên", "icon": "people", "description": "Hồ sơ, hợp đồng và quá trình công tác", "fields": ["Mã nhân viên", "Họ và tên", "Phòng ban", "Chức vụ", "Email", "Loại hợp đồng"]},
    "attendance": {"name": "Chấm công & tính công", "icon": "clock", "description": "Ca làm, tăng ca và tổng hợp công", "fields": ["Nhân viên", "Ngày công", "Ca làm", "Giờ vào / ra", "Tăng ca", "Ghi chú"]},
    "leave_requests": {"name": "Quản lý nghỉ phép", "icon": "calendar", "description": "Đơn nghỉ, phê duyệt và phép còn lại", "fields": ["Nhân viên", "Loại nghỉ", "Từ ngày", "Đến ngày", "Người duyệt", "Lý do"]},
    "recruitment": {"name": "Tuyển dụng", "icon": "briefcase", "description": "Tin tuyển dụng, ứng viên và phỏng vấn", "fields": ["Vị trí", "Ứng viên", "Email", "Ngày phỏng vấn", "Người phụ trách", "Đánh giá"]},
    "training": {"name": "Đào tạo & đánh giá", "icon": "book", "description": "Chương trình đào tạo, KPI và OKR", "fields": ["Chương trình", "Nhân viên", "Kỳ đánh giá", "Mục tiêu", "Kết quả", "Giảng viên"]},
    "payroll": {"name": "Lương & phúc lợi", "icon": "wallet", "description": "Bảng lương, phụ cấp và quyết toán", "fields": ["Nhân viên", "Kỳ lương", "Lương cơ bản", "Phụ cấp / thưởng", "Khấu trừ", "Trạng thái"]},
    "documents": {"name": "Hành chính & văn thư", "icon": "file", "description": "Công văn, quy chế, thông báo và tài sản", "fields": ["Tiêu đề", "Loại văn bản", "Số hiệu", "Ngày ban hành", "Đơn vị", "Tài sản cấp phát"]},
    "reports": {"name": "Báo cáo & thống kê", "icon": "chart", "description": "Báo cáo nhân sự, công, tuyển dụng và đào tạo", "fields": ["Tên báo cáo", "Loại báo cáo", "Kỳ báo cáo", "Người lập", "Ghi chú", "Trạng thái"]},
    "notifications": {"name": "Thông báo", "icon": "bell", "description": "Thông báo nội bộ và nhắc việc", "fields": ["Tiêu đề", "Đối tượng", "Nội dung", "Ngày gửi", "Kênh", "Trạng thái"]},
    "users": {"name": "Tài khoản & phân quyền", "icon": "settings", "description": "Vai trò, nhật ký hoạt động và cấu hình", "fields": ["Tên đăng nhập", "Họ và tên", "Vai trò", "Email", "Trạng thái", "Ghi chú"]},
}

STATUS_OPTIONS = ["Mới", "Đang xử lý", "Chờ duyệt", "Đã duyệt", "Hoàn tất", "Từ chối", "Đã hủy"]
