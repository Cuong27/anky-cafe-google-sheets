from datetime import date, datetime, time
from email.message import EmailMessage
import os
import re
import smtplib
import ssl
from pathlib import Path
from zoneinfo import ZoneInfo

import requests
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request, send_from_directory

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

# On Vercel, the platform serves files in public/ directly.
# Locally, Flask serves the same files so URLs /css, /js and /img work at port 8000.
#if os.getenv("VERCEL"):
#    app = Flask(__name__, static_folder=None)
#else:
#    app = Flask(
#        __name__,
#        static_folder=str(BASE_DIR / "public"),
#       static_url_path="",
#    )

# Khai báo Flask app trực tiếp ở cấp cao nhất
app = Flask(__name__, static_folder=None)

@app.get("/css/<path:filename>")
def serve_css(filename):
    return send_from_directory(BASE_DIR / "public" / "css", filename)


@app.get("/js/<path:filename>")
def serve_js(filename):
    return send_from_directory(BASE_DIR / "public" / "js", filename)


@app.get("/img/<path:filename>")
def serve_img(filename):
    return send_from_directory(BASE_DIR / "public" / "img", filename)

VN_TZ = ZoneInfo("Asia/Ho_Chi_Minh")

# Prices and product names are validated server-side; never trust browser prices.
MENU = {
    1: ("Hồ Sơ Đen", 35000),
    2: ("Lời Khai Ngọt Ngào", 40000),
    3: ("Lời Khai Nửa Thật", 40000),
    4: ("Dấu Vết Cuối Cùng", 45000),
    5: ("Nhân Chứng Cảm Lặng", 45000),
    6: ("Kẻ Hai Mặt", 45000),
    7: ("Lời Khai Ban Đầu", 45000),
    8: ("Bí Mật Hắc Ám", 45000),
    9: ("Mật Mã Hoa Hồng", 55000),
    10: ("Lớp Mặt Nạ", 55000),
    11: ("Mắt Quỷ", 55000),
    12: ("Cuộc Gọi Nặc Danh", 55000),
    13: ("Án Mạng Hoàng Hôn", 50000),
    14: ("Hung Khí", 55000),
    15: ("Chứng Cứ Ngoại Phạm", 50000),
    16: ("Khẩu Cung", 50000),
    17: ("Dấu Vân Tay", 50000),
    18: ("Vùng Cấm", 50000),
    19: ("Tang Chứng", 50000),
    20: ("Đồng Phạm", 50000),
    21: ("Manh Mối Giả", 50000),
    22: ("Nhân Chứng Đỏ", 50000),
    23: ("Hiện Trường Vụ Án", 50000),
    24: ("Kẻ Đứng Sau", 50000),
}


def parse_integer(value):
    """Accept integers or digit-only strings; reject bools, floats and blanks."""
    if isinstance(value, bool):
        raise ValueError("Boolean không phải số nguyên hợp lệ.")
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        value = value.strip()
        if value.isdecimal():
            return int(value)
    raise ValueError("Giá trị phải là số nguyên hợp lệ.")


def smtp_settings():
    host = os.getenv("SMTP_HOST", "smtp.gmail.com").strip()
    try:
        port = int(os.getenv("SMTP_PORT", "587"))
    except ValueError as exc:
        raise RuntimeError("SMTP_PORT phải là số nguyên, ví dụ 587 hoặc 465.") from exc

    username = os.getenv("SMTP_USER", "").strip()
    # Gmail often displays App Passwords with spaces; strip spaces for SMTP login.
    password = re.sub(r"\s+", "", os.getenv("SMTP_PASSWORD", ""))
    recipient = os.getenv("ORDER_EMAIL_TO", "").strip()

    missing = [key for key, value in {
        "SMTP_USER": username,
        "SMTP_PASSWORD": password,
        "ORDER_EMAIL_TO": recipient,
    }.items() if not value]
    if missing:
        raise RuntimeError("Chưa cấu hình email: " + ", ".join(missing))
    if port not in (465, 587):
        raise RuntimeError("SMTP_PORT hiện chỉ hỗ trợ 465 hoặc 587.")

    return host, port, username, password, recipient


def send_email(message):
    host, port, username, password, _recipient = smtp_settings()
    context = ssl.create_default_context()

    if port == 465:
        with smtplib.SMTP_SSL(host, port, context=context, timeout=20) as server:
            server.login(username, password)
            server.send_message(message)
    else:
        with smtplib.SMTP(host, port, timeout=20) as server:
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            server.login(username, password)
            server.send_message(message)


def send_order_to_sheets(order_type, table, items):
    """Send an order to Apps Script; new Apps Script writes one row per order."""
    url = os.getenv("GOOGLE_SCRIPT_URL", "").strip()
    token = os.getenv("ORDER_API_TOKEN", "").strip()
    if not url or not token:
        raise RuntimeError("Thiếu GOOGLE_SCRIPT_URL hoặc ORDER_API_TOKEN trong Environment Variables.")

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

    response = requests.post(url, json=payload, timeout=25)
    response.raise_for_status()
    try:
        result = response.json()
    except requests.exceptions.JSONDecodeError as exc:
        raise RuntimeError("Google Apps Script trả về JSON không hợp lệ.") from exc

    if not isinstance(result, dict) or result.get("ok") is not True:
        error = (
            result.get("error", "Google Sheets không xác nhận đã lưu order.")
            if isinstance(result, dict)
            else "Phản hồi Google Sheets không hợp lệ."
        )
        raise RuntimeError(str(error))
    return result


def send_order_email(customer, table, items, total, order_type):
    _host, _port, username, _password, recipient = smtp_settings()
    lines = [
        "ẨN KÝ CAFÉ — ORDER MỚI",
        "=" * 34,
        f"Loại: {order_type}",
        f"Bàn: {table}",
        "",
        "ĐƠN HÀNG",
    ]
    lines.extend(f"- {item['name']} × {item['quantity']}" for item in items)
    lines.extend([
        "",
        f"THÀNH TIỀN: {total:,}đ",
        f"Khách hàng: {customer}",
        f"Thời gian nhận order: {datetime.now(VN_TZ).strftime('%d/%m/%Y %H:%M:%S %Z')}",
        "",
        "Email tự động từ website Ẩn Ký Café.",
    ])

    message = EmailMessage()
    message["Subject"] = f"[Ẩn Ký Café] Order mới - {order_type} - {table}"
    message["From"] = username
    message["To"] = recipient
    message.set_content("\n".join(lines))
    send_email(message)


def send_booking_email(customer, phone, booking_date, booking_time, case_no, case_title):
    """Email booking request to the cafe's ORDER_EMAIL_TO address."""
    _host, _port, username, _password, recipient = smtp_settings()
    lines = [
        "ẨN KÝ CAFÉ — YÊU CẦU ĐẶT LỊCH MỚI",
        "=" * 42,
        f"Hồ sơ: {case_no} — {case_title}",
        f"Tên người đặt: {customer}",
        f"Số điện thoại: {phone}",
        f"Ngày muốn đến: {booking_date.strftime('%d/%m/%Y')}",
        f"Giờ muốn đến: {booking_time.strftime('%H:%M')}",
        "",
        "Đây là yêu cầu đặt lịch từ website; nhân viên cần liên hệ khách để xác nhận.",
    ]

    message = EmailMessage()
    # Keep subject static to avoid putting untrusted form fields in mail headers.
    message["Subject"] = "[Ẩn Ký Café] Yêu cầu đặt lịch trải nghiệm mới"
    message["From"] = username
    message["To"] = recipient
    message.set_content("\n".join(lines))
    send_email(message)


@app.get("/")
def home():
    return render_template("index.html")


@app.post("/api/orders")
def create_order():
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return jsonify(error="Dữ liệu order không hợp lệ."), 400

    raw_items = payload.get("items")
    if not isinstance(raw_items, list) or not raw_items:
        return jsonify(error="Giỏ hàng đang trống."), 400
    if len(raw_items) > len(MENU):
        return jsonify(error="Giỏ hàng có quá nhiều loại sản phẩm."), 400

    order_type = payload.get("order_type")
    if order_type not in ("Take away", "Tại bàn"):
        return jsonify(error="Loại đơn phải là Take away hoặc Tại bàn."), 400

    customer = payload.get("customer_name", "")
    if not isinstance(customer, str):
        return jsonify(error="Tên khách hàng không hợp lệ."), 400
    customer = customer.strip()[:60] or "Khách tại quán"

    raw_table = payload.get("table_number", "")
    if not isinstance(raw_table, (str, int)) or isinstance(raw_table, bool):
        return jsonify(error="Thông tin bàn không hợp lệ."), 400
    table = str(raw_table).strip()[:20]
    if order_type == "Tại bàn" and not table:
        return jsonify(error="Vui lòng nhập số bàn."), 400
    if order_type == "Take away":
        table = "Mang đi"

    clean_items = []
    total = 0
    seen = set()

    for item in raw_items:
        if not isinstance(item, dict):
            return jsonify(error="Dữ liệu sản phẩm không hợp lệ."), 400
        try:
            product_id = parse_integer(item.get("product_id"))
            quantity = parse_integer(item.get("quantity"))
        except (TypeError, ValueError, OverflowError):
            return jsonify(error="Mã món hoặc số lượng phải là số nguyên hợp lệ."), 400

        if product_id not in MENU or quantity < 1 or quantity > 50 or product_id in seen:
            return jsonify(error="Món hoặc số lượng không hợp lệ."), 400

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

    # Save to Sheets first. Email is sent only when Apps Script confirms the write.
    try:
        send_order_to_sheets(order_type, table, clean_items)
    except (OSError, requests.RequestException, RuntimeError, ValueError):
        app.logger.exception("Không ghi được order vào Google Sheets")
        return jsonify(
            error="Chưa xác nhận được order trên Google Sheets. Vui lòng liên hệ nhân viên trước khi thử lại."
        ), 503

    email_sent = True
    try:
        send_order_email(customer, table, clean_items, total, order_type)
    except (OSError, smtplib.SMTPException, RuntimeError, ValueError):
        email_sent = False
        app.logger.exception("Order bàn %s đã lưu Sheet nhưng gửi email thất bại", table)

    return jsonify(
        total=total,
        status="Đã ghi Google Sheets",
        email_sent=email_sent,
    ), 201


@app.post("/api/bookings")
def create_booking():
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return jsonify(error="Dữ liệu đặt lịch không hợp lệ."), 400

    customer = payload.get("customer_name")
    phone = payload.get("phone")
    booking_date_raw = payload.get("booking_date")
    booking_time_raw = payload.get("booking_time")
    case_no = payload.get("case_no")
    case_title = payload.get("case_title")

    if not isinstance(customer, str) or not customer.strip():
        return jsonify(error="Vui lòng nhập tên người đặt."), 400
    customer = customer.strip()
    if len(customer) > 80:
        return jsonify(error="Tên người đặt không được quá 80 ký tự."), 400
    if any(ord(ch) < 32 for ch in customer):
        return jsonify(error="Tên người đặt chứa ký tự không hợp lệ."), 400

    if not isinstance(phone, str):
        return jsonify(error="Vui lòng nhập số điện thoại."), 400
    phone = phone.strip()
    if not re.fullmatch(r"[0-9+().\-\s]{8,24}", phone) or sum(ch.isdigit() for ch in phone) < 8:
        return jsonify(error="Số điện thoại chưa hợp lệ."), 400

    if not isinstance(booking_date_raw, str) or not isinstance(booking_time_raw, str):
        return jsonify(error="Vui lòng chọn ngày và giờ đến."), 400
    try:
        booking_date = date.fromisoformat(booking_date_raw)
        booking_time = time.fromisoformat(booking_time_raw)
    except ValueError:
        return jsonify(error="Ngày hoặc giờ không đúng định dạng."), 400

    requested_at = datetime.combine(booking_date, booking_time, tzinfo=VN_TZ)
    if requested_at <= datetime.now(VN_TZ):
        return jsonify(error="Ngày và giờ đặt lịch phải ở trong tương lai."), 400

    if not isinstance(case_no, str) or not re.fullmatch(r"[A-Za-z0-9—-]{1,20}", case_no.strip()):
        return jsonify(error="Thông tin hồ sơ không hợp lệ."), 400
    if not isinstance(case_title, str) or not case_title.strip() or len(case_title.strip()) > 120:
        return jsonify(error="Tên hồ sơ không hợp lệ."), 400

    try:
        send_booking_email(
            customer=customer,
            phone=phone,
            booking_date=booking_date,
            booking_time=booking_time,
            case_no=case_no.strip(),
            case_title=case_title.strip(),
        )
    except (OSError, smtplib.SMTPException, RuntimeError, ValueError):
        app.logger.exception("Không gửi được email yêu cầu đặt lịch")
        return jsonify(
            error="Chưa gửi được yêu cầu đặt lịch. Vui lòng thử lại hoặc liên hệ trực tiếp với quán."
        ), 503

    app.logger.info("Đã gửi email yêu cầu đặt lịch cho hồ sơ %s", case_no)
    return jsonify(
        ok=True,
        message="Đã gửi yêu cầu đặt lịch. Nhân viên sẽ liên hệ để xác nhận.",
    ), 201


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
