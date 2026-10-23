from datetime import datetime
from email.message import EmailMessage
import os
import smtplib
import ssl
from pathlib import Path

import requests
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request


BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

app = Flask(
    __name__
    ,static_folder=str(BASE_DIR / "public"),
    static_url_path=""
)

# ==================================================
# MENU
# Backend tự xác thực giá, không tin giá từ frontend
# ==================================================

MENU = {
    # Cà phê
    1: ("Hồ Sơ Đen", 35000),
    2: ("Lời Khai Ngọt Ngào", 40000),
    3: ("Lời Khai Nửa Thật", 40000),
    4: ("Dấu Vết Cuối Cùng", 45000),
    5: ("Nhân Chứng Câm Lặng", 45000),
    6: ("Kẻ Hai Mặt", 45000),

    # Trà sữa
    7: ("Lời Khai Ban Đầu", 45000),
    8: ("Bí Mật Hắc Ám", 45000),
    9: ("Mật Mã Hoa Hồng(Signature)", 55000),
    10: ("Lớp Mặt Nạ", 55000),
    11: ("Mắt Quỷ(Signature)", 55000),
    12: ("Cuộc Gọi Nặc Danh(Signature)", 55000),

    # Trà trái cây
    13: ("Án Mạng Hoàng Hôn", 50000),
    14: ("Hung Khí(Signature)", 55000),
    15: ("Chứng Cứ Ngoại Phạm(Signature)", 50000),
    16: ("Khẩu Cung", 50000),
    17: ("Dấu Vân Tay", 50000),
    18: ("Vùng Cấm(Signature)", 50000),

    # Soda
    19: ("Tang Chứng", 50000),
    20: ("Đồng Phạm", 50000),
    21: ("Manh Mối Giả", 50000),
    22: ("Nhân Chứng Đỏ", 50000),
    23: ("Hiện Trường Vụ Án", 50000),
    24: ("Kẻ Đứng Sau", 50000),
}

# ==================================================
# HÀM KIỂM TRA SỐ NGUYÊN
# ==================================================

def parse_integer(value):
    """Chấp nhận int hoặc chuỗi chữ số; loại bool, float, None và chuỗi sai."""

    if isinstance(value, bool):
        raise ValueError("Boolean không phải số nguyên hợp lệ.")

    if isinstance(value, int):
        return value

    if isinstance(value, str):
        value = value.strip()

        if value.isdecimal():
            return int(value)

    raise ValueError("Giá trị phải là số nguyên hợp lệ.")


# ==================================================
# GỬI ORDER ĐẾN GOOGLE APPS SCRIPT
#
# Payload tương thích với Code.gs:
# {
#   token,
#   order_type,
#   table,
#   items: [{name, quantity, price, subtotal}]
# }
#
# Apps Script trả về:
# {ok: true, message: "...", total: ...}
# Không sử dụng order_id nữa.
# ==================================================

def send_order_to_sheets(order_type, table, items):
    """Gửi một order; Apps Script sẽ ghi order thành một dòng."""

    url = os.getenv("GOOGLE_SCRIPT_URL", "").strip()
    token = os.getenv("ORDER_API_TOKEN", "").strip()

    if not url or not token:
        raise RuntimeError(
            "Thiếu GOOGLE_SCRIPT_URL hoặc ORDER_API_TOKEN trong .env."
        )

    payload = {
        "token": token,
        "order_type": order_type,
        "table": table,
        "items": [
            {
                "name": item["name"],
                "quantity": item["quantity"],
                "price": item["price"],
                "subtotal": item["subtotal"],
            }
            for item in items
        ],
    }

    response = requests.post(
        url,
        json=payload,
        timeout=30,
    )
    response.raise_for_status()

    try:
        result = response.json()
    except requests.exceptions.JSONDecodeError as exc:
        raise RuntimeError(
            "Google Apps Script trả về JSON không hợp lệ."
        ) from exc

    if not isinstance(result, dict) or result.get("ok") is not True:
        error = (
            result.get(
                "error",
                "Google Sheets không xác nhận đã lưu order."
            )
            if isinstance(result, dict)
            else "Phản hồi Google Sheets không hợp lệ."
        )

        raise RuntimeError(str(error))

    # Không kiểm tra order_id vì Code.gs mới không tạo mã hóa đơn.
    return result


# ==================================================
# GỬI EMAIL ORDER
#
# Thứ tự:
# Loại -> Bàn -> Đơn hàng -> Thành tiền
# ==================================================

def send_order_email(customer, table, items, total, order_type):
    host = os.getenv("SMTP_HOST", "smtp.gmail.com").strip()

    try:
        port = int(os.getenv("SMTP_PORT", "587"))
    except ValueError as exc:
        raise RuntimeError(
            "SMTP_PORT phải là số nguyên, ví dụ 587 hoặc 465."
        ) from exc

    username = os.getenv("SMTP_USER", "").strip()
    password = os.getenv("SMTP_PASSWORD", "").strip()
    recipient = os.getenv("ORDER_EMAIL_TO", "").strip()

    missing = [
        name
        for name, value in {
            "SMTP_USER": username,
            "SMTP_PASSWORD": password,
            "ORDER_EMAIL_TO": recipient,
        }.items()
        if not value
    ]

    if missing:
        raise RuntimeError(
            "Chưa cấu hình email: " + ", ".join(missing)
        )

    # Gom danh sách món, giữ số lượng cho từng món.
    item_lines = [
        f"- {item['name']} × {item['quantity']}"
        for item in items
    ]

    lines = [
        "ẨN KÝ CAFÉ — ORDER MỚI",
        "=" * 34,
        f"Loại: {order_type}",
        f"Bàn: {table}",
        "",
        "ĐƠN HÀNG",
        *item_lines,
        "",
        f"THÀNH TIỀN: {total:,}đ",
        "",
        f"Khách hàng: {customer}",
        (
            "Thời gian: "
            f"{datetime.now().astimezone().strftime('%d/%m/%Y %H:%M:%S %Z')}"
        ),
        "",
        "Email tự động từ website Ẩn Ký Café.",
    ]

    message = EmailMessage()
    message["Subject"] = (
        f"[Ẩn Ký Café] Order mới - {order_type} - {table}"
    )
    message["From"] = username
    message["To"] = recipient
    message.set_content("\n".join(lines))

    context = ssl.create_default_context()

    if port == 465:
        with smtplib.SMTP_SSL(
            host,
            port,
            context=context,
            timeout=20,
        ) as server:
            server.login(username, password)
            server.send_message(message)

    else:
        with smtplib.SMTP(
            host,
            port,
            timeout=20,
        ) as server:
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            server.login(username, password)
            server.send_message(message)


# ==================================================
# TRANG CHỦ
# ==================================================

@app.get("/")
def home():
    return render_template("index.html")


# ==================================================
# API TẠO ORDER
# ==================================================

@app.post("/api/orders")
def create_order():
    payload = request.get_json(silent=True)

    if not isinstance(payload, dict):
        return jsonify(
            error="Dữ liệu order không hợp lệ."
        ), 400

    # Kiểm tra giỏ hàng.
    raw_items = payload.get("items")

    if not isinstance(raw_items, list) or not raw_items:
        return jsonify(
            error="Giỏ hàng đang trống."
        ), 400

    if len(raw_items) > len(MENU):
        return jsonify(
            error="Giỏ hàng có quá nhiều loại sản phẩm."
        ), 400

    # Kiểm tra loại order.
    order_type = payload.get("order_type")

    if order_type not in ("Take away", "Tại bàn"):
        return jsonify(
            error="Loại đơn phải là Take away hoặc Tại bàn."
        ), 400

    # Kiểm tra tên khách.
    customer = payload.get("customer_name", "")

    if not isinstance(customer, str):
        return jsonify(
            error="Tên khách hàng không hợp lệ."
        ), 400

    customer = customer.strip()[:60] or "Khách tại quán"

    # Kiểm tra bàn.
    raw_table = payload.get("table_number", "")

    if (
        not isinstance(raw_table, (str, int))
        or isinstance(raw_table, bool)
    ):
        return jsonify(
            error="Thông tin bàn không hợp lệ."
        ), 400

    table = str(raw_table).strip()[:20]

    if order_type == "Tại bàn":
        if not table:
            return jsonify(
                error="Vui lòng nhập số bàn."
            ), 400
    else:
        table = "Mang đi"

    # Xác thực món và số lượng ở backend.
    clean_items = []
    total = 0
    seen = set()

    for item in raw_items:
        if not isinstance(item, dict):
            return jsonify(
                error="Dữ liệu sản phẩm không hợp lệ."
            ), 400

        raw_product_id = item.get("product_id")
        raw_quantity = item.get("quantity")

        try:
            product_id = parse_integer(raw_product_id)
            quantity = parse_integer(raw_quantity)

        except (TypeError, ValueError, OverflowError):
            return jsonify(
                error="Mã món hoặc số lượng phải là số nguyên hợp lệ."
            ), 400

        if (
            product_id not in MENU
            or quantity < 1
            or quantity > 50
            or product_id in seen
        ):
            return jsonify(
                error="Món hoặc số lượng không hợp lệ."
            ), 400

        seen.add(product_id)

        name, price = MENU[product_id]
        subtotal = price * quantity
        total += subtotal

        clean_items.append({
            "product_id": product_id,
            "name": name,
            "price": price,
            "quantity": quantity,
            "subtotal": subtotal,
        })

    # --------------------------------------------------
    # BƯỚC 1: GHI GOOGLE SHEETS TRƯỚC
    # --------------------------------------------------

    try:
        send_order_to_sheets(
            order_type,
            table,
            clean_items,
        )

    except (
        OSError,
        requests.RequestException,
        RuntimeError,
        ValueError,
    ):
        app.logger.exception(
            "Không ghi được order vào Google Sheets."
        )

        return jsonify(
            error=(
                "Chưa xác nhận được order trên Google Sheets. "
                "Vui lòng kiểm tra với nhân viên trước khi thử lại."
            )
        ), 503

    # --------------------------------------------------
    # BƯỚC 2: GỬI EMAIL SAU KHI SHEET XÁC NHẬN THÀNH CÔNG
    # --------------------------------------------------

    email_sent = True

    try:
        send_order_email(
            customer,
            table,
            clean_items,
            total,
            order_type,
        )

    except (
        OSError,
        smtplib.SMTPException,
        RuntimeError,
        ValueError,
    ):
        email_sent = False

        app.logger.exception(
            "Order bàn %s đã lưu Sheet nhưng gửi email thất bại.",
            table,
        )

    # --------------------------------------------------
    # BƯỚC 3: TRẢ KẾT QUẢ VỀ FRONTEND
    #
    # Không trả order_id vì Apps Script không tạo mã nữa.
    # --------------------------------------------------

    return jsonify(
        total=total,
        status="Đã ghi Google Sheets",
        email_sent=email_sent,
    ), 201


# ==================================================
# CHẠY FLASK LOCAL
# ==================================================

if __name__ == "__main__":
    # Chỉ dùng debug trên máy phát triển local.
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True,
    )