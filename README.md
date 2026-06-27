# passport_management_system
```text
passport_management_system/
|-- db_scripts/                   (Thư mục chứa các kịch bản SQL khởi tạo và thiết lập bảo mật Oracle)
|   |-- 01_init_tables.sql        (Khởi tạo schema, các bảng dữ liệu nền tảng và phân quyền cơ bản)
|   |-- 02_insert_data_and_proc.sql (Thêm dữ liệu mẫu cho danh mục và Procedure nộp hồ sơ đăng ký)
|   |-- 03_xt_roles_users.sql     (Tạo Database User và cấp quyền thao tác cho bộ phận Xác thực)
|   |-- 04_xd_vpd_policy.sql      (Thiết lập chính sách VPD/RLS chặn xem dữ liệu dân cư đối với bộ phận Xét duyệt)
|   |-- 05_lt_masking_policy.sql  (Thiết lập chính sách che giấu dữ liệu Column Masking bảo vệ thông tin cá nhân cho Lưu trữ)
|   |-- 06_gs_audit_policy.sql    (Thiết lập Unified Auditing ghi nhật ký thao tác dữ liệu phục vụ bộ phận Giám sát)
|   |-- 07_mac_ols_policy.sql    (Thiết lập level, compartment, group và tạo user, gán nhãn thủ công cho mock_data)
|   |-- 08_proc_tao_tai_khoan.sql    (Proc gán label tự động khi có user mới được tạo)
|   
|-- app/                          (Thư mục chứa mã nguồn ứng dụng web giao diện Python Streamlit)
|   |-- main.py                   (Tệp chạy chính, quản lý cấu hình trang, điều hướng và kiểm soát trạng thái đăng nhập)
|   |-- config.py                 (Tệp lưu trữ các tham số hệ thống và cấu hình kết nối CSDL)
|   |
|   |-- dal/                      (Data Access Layer: Lớp giao tiếp trực tiếp với cơ sở dữ liệu Oracle)
|   |   |-- db_connection.py      (Hàm khởi tạo kết nối CSDL động theo Database User tương ứng với từng role)
|   |   |-- user_dal.py           (Xử lý các truy vấn và procedure liên quan đến chức năng đăng ký, đăng nhập)
|   |   |-- xt_dal.py             (Xử lý lệnh SQL truy xuất và cập nhật dữ liệu của luồng Xác thực)
|   |   |-- xd_dal.py             (Xử lý lệnh SQL truy xuất dữ liệu của luồng Xét duyệt)
|   |   |-- lt_dal.py             (Xử lý lệnh SQL gọi procedure lưu trữ của luồng Lưu trữ)
|   |   |-- gs_dal.py             (Xử lý lệnh SQL đọc dữ liệu nhật ký hệ thống của luồng Giám sát)
|   |
|   |-- bll/                      (Business Logic Layer: Lớp xử lý logic nghiệp vụ trung gian)
|   |   |-- auth_bll.py           (Xử lý logic xác thực tài khoản và kiểm tra tính hợp lệ của dữ liệu form nộp vào)
|   |   |-- xt_bll.py             (Nhận dữ liệu từ UI, gọi DAL và xử lý điều kiện chuyển trạng thái xác thực)
|   |   |-- xd_bll.py             (Nhận dữ liệu từ UI, đối chiếu quy định và xử lý điều kiện xét duyệt hồ sơ)
|   |   |-- lt_bll.py             (Nhận dữ liệu từ UI và gọi DAL xử lý chuyển trạng thái lưu trữ)
|   |   |-- gs_bll.py             (Định dạng và xử lý dữ liệu log trước khi trả về cho UI hiển thị)
|   |
|   |-- ui/                       (Presentation Layer: Lớp giao diện người dùng, sử dụng Passive MVP)
|   |   |-- login_view.py         (Giao diện form đăng nhập dành cho cán bộ xử lý)
|   |   |-- register_view.py      (Giao diện tờ khai đăng ký cấp hộ chiếu trực tuyến cho công dân)
|   |   |-- xt_view.py            (Màn hình thao tác và bảng điều khiển của bộ phận Xác thực)
|   |   |-- xd_view.py            (Màn hình thao tác và bảng điều khiển của bộ phận Xét duyệt)
|   |   |-- lt_view.py            (Màn hình thao tác và bảng điều khiển của bộ phận Lưu trữ)
|   |   |-- gs_view.py            (Màn hình xem nhật ký hệ thống của bộ phận Giám sát)
|
|-- file_storage/                 (Thư mục lưu trữ vật lý các tệp đính kèm do người dùng tải lên như ảnh thẻ, giấy tờ)
|-- docker-compose.yml            (Tệp cấu hình môi trường Docker để khởi chạy đồng thời Oracle DB và Web App)
```
