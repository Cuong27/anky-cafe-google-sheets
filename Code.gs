function doPost(e) {
  const lock = LockService.getScriptLock();
  let locked = false;

  try {
    if (!e || !e.postData || !e.postData.contents) {
      return jsonResponse({ ok: false, error: "Missing request body" });
    }

    const data = JSON.parse(e.postData.contents);
    const expectedToken = PropertiesService.getScriptProperties().getProperty("ORDER_API_TOKEN");
    if (!expectedToken || data.token !== expectedToken) {
      return jsonResponse({ ok: false, error: "Unauthorized" });
    }

    if (!Array.isArray(data.items) || data.items.length < 1 || data.items.length > 6) {
      return jsonResponse({ ok: false, error: "Invalid items" });
    }
    if (!["Take away", "Tại bàn"].includes(data.order_type)) {
      return jsonResponse({ ok: false, error: "Invalid order type" });
    }
    if (typeof data.table !== "string" || data.table.length > 20) {
      return jsonResponse({ ok: false, error: "Invalid table" });
    }

    const ss = SpreadsheetApp.getActiveSpreadsheet();
    const sheet = ss.getSheetByName("Orders");
    if (!sheet) throw new Error('Không tìm thấy trang tính "Orders".');

    const rows = data.items.map(item => {
      if (!item || typeof item.name !== "string" || item.name.length > 100) {
        throw new Error("Invalid product name");
      }
      if (!Number.isSafeInteger(item.quantity) || item.quantity < 1 || item.quantity > 50) {
        throw new Error("Invalid quantity");
      }
      if (!Number.isSafeInteger(item.price) || item.price < 0 ||
          !Number.isSafeInteger(item.subtotal) || item.subtotal !== item.price * item.quantity) {
        throw new Error("Invalid price or subtotal");
      }
      return [item.name, data.table, item.quantity, item.price, data.order_type, item.subtotal];
    });

    lock.waitLock(15000);
    locked = true;

    const props = PropertiesService.getScriptProperties();
    const lastNumber = Number(props.getProperty("LAST_ORDER_NUMBER") || "0");
    if (!Number.isSafeInteger(lastNumber) || lastNumber < 0) {
      throw new Error("LAST_ORDER_NUMBER không hợp lệ trong Script Properties.");
    }

    const nextNumber = lastNumber + 1;
    const orderId = "AK" + String(nextNumber).padStart(2, "0");
    const outputRows = rows.map(row => [orderId, ...row]);

    // Ghi các dòng của cùng một hóa đơn liền nhau.
    sheet.getRange(sheet.getLastRow() + 1, 1, outputRows.length, 7).setValues(outputRows);
    SpreadsheetApp.flush();
    props.setProperty("LAST_ORDER_NUMBER", String(nextNumber));

    return jsonResponse({ ok: true, order_id: orderId });
  } catch (err) {
    return jsonResponse({ ok: false, error: String(err && err.message ? err.message : err) });
  } finally {
    if (locked) lock.releaseLock();
  }
}

function jsonResponse(data) {
  return ContentService.createTextOutput(JSON.stringify(data))
    .setMimeType(ContentService.MimeType.JSON);
}
