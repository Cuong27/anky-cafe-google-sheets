# Ẩn Ký Café — Flask + Google Sheets + email

## 1. Chuẩn bị Google Sheets
1. Tạo Google Sheet, tạo tab tên `Orders`.
2. Dòng đầu tiên của tab `Orders` đặt đúng 7 tiêu đề:
   `Mã hóa đơn | Đơn hàng | Bàn | Số lượng | Tiền mỗi món | Loại | Thành tiền`
3. Trong Extensions → Apps Script, dán nội dung `Code.gs`.
4. Apps Script → Project Settings → Script Properties, thêm:
   - `ORDER_API_TOKEN`: chuỗi bí mật mạnh.
   - `LAST_ORDER_NUMBER`: `0` nếu bắt đầu từ `AK01`; nếu đã có hóa đơn thì đặt số cuối cùng đã dùng.
5. Deploy → New deployment → Web app. Execute as: Me. Chọn quyền truy cập cho phép Flask gọi endpoint (thường là Anyone nếu endpoint công khai); token bí mật trong request dùng để xác thực ứng dụng. Sao chép URL `/exec`.

## 2. Cấu hình Flask
```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
```
Sửa `.env`: `GOOGLE_SCRIPT_URL`, `ORDER_API_TOKEN` và thông tin SMTP. Với Gmail, bật xác minh 2 bước và tạo App Password. Không commit `.env` lên Git.

## 3. Chạy
```bash
python app.py
```
Mở http://127.0.0.1:5000.

## 4. Định dạng dữ liệu frontend
POST `/api/orders` gửi JSON dạng:
```json
{
  "customer_name": "Minh",
  "table_number": "02",
  "order_type": "Tại bàn",
  "items": [
    {"product_id": 1, "quantity": 2},
    {"product_id": 6, "quantity": 1}
  ]
}
```
`order_type` chỉ nhận `Take away` hoặc `Tại bàn`. Backend xác định giá từ `MENU`; không gửi giá từ trình duyệt.

## Ghi chú vận hành
- Mỗi món trong một hóa đơn được ghi thành một dòng, chung mã hóa đơn.
- Mã hóa đơn được cấp trong Apps Script với lock để tránh hai request đồng thời nhận cùng số.
- Nếu request timeout sau khi Google Sheets đã ghi thành công, khách có thể không nhận được phản hồi dù đơn đã ghi. Bản demo chưa có idempotency key để tự khử đơn trùng; khi dùng thực tế nên bổ sung cơ chế này.
- Email là bước sau khi ghi Sheet. Nếu email thất bại, API vẫn trả trạng thái đơn đã ghi cùng `email_sent: false`.
- Chỉ dùng Flask `debug=True` trên máy local, không triển khai debug server công khai.


## Menu hiện tại

Menu gồm 24 món thuộc 4 nhóm: Cà phê, Trà sữa, Trà trái cây và Soda. Tên và giá được khai báo ở `static/js/app.js` (hiển thị) và `app.py` (xác thực giá phía server). Khi đổi tên/giá món, cần cập nhật cả hai nơi và giữ cùng `id` sản phẩm.
