# Hướng Dẫn Cấu Hình, Biên Dịch Và Tạo File Bin Nạp Firmware Xiaozhi

Tài liệu này hướng dẫn chi tiết các bước thiết lập môi trường phát triển ESP-IDF, cách cấu hình bo mạch và thực hiện biên dịch mã nguồn thành một tệp tin nhị phân đơn nhất (Single Merged Binary) sẵn sàng để nạp trực tiếp qua trình duyệt web.

---

## 1. Yêu Cầu Chuẩn Bị & Môi Trường

Mã nguồn firmware Xiaozhi nằm trong thư mục `xiaozhi-esp32/` được xây dựng dựa trên bộ SDK chính thức **ESP-IDF** của Espressif.

### A. Tải và cài đặt ESP-IDF
- **Phiên bản khuyến nghị:** **ESP-IDF v6.0.2** (hoặc các phiên bản thuộc nhánh `v6.0.x`).
- **Lưu ý:** Không nên dùng các bản quá cũ hoặc các bản thử nghiệm không tương thích.
- Cài đặt theo hướng dẫn chính thức từ trang chủ Espressif hoặc qua Tiện ích mở rộng (Extension) của VS Code / Cursor.

### B. Thiết lập biến môi trường (Environment Setup)
Mỗi lần mở một Terminal mới để làm việc, bạn cần kích hoạt môi trường ESP-IDF bằng các lệnh tương ứng:
- **macOS / Linux:**
  ```bash
  . $IDF_PATH/export.sh
  ```
- **Windows (Command Prompt):**
  ```cmd
  %IDF_PATH%\export.bat
  ```
- **Windows (PowerShell):**
  ```powershell
  . $env:IDF_PATH/export.ps1
  ```

---

## 2. Kiểm Tra Các Cấu Hình Hỗ Trợ

Chuyển thư mục làm việc của Terminal vào thư mục chứa firmware:
```bash
cd xiaozhi-esp32
```

Sử dụng script `build.py` trong thư mục `scripts/` để truy vấn thông tin:

1. **Xem danh sách bo mạch & biến thể màn hình được hỗ trợ:**
   ```bash
   python3 scripts/build.py --list-boards
   ```
2. **Xem danh sách ngôn ngữ hỗ trợ:**
   ```bash
   python3 scripts/build.py --list-languages
   ```
3. **Xem các mô hình nhận diện từ thức tỉnh (Wake-word) khả dụng:**
   ```bash
   python3 scripts/build.py --list-wake-words
   ```

---

## 3. Lệnh Biên Dịch & Ghép Tệp Tin Nhị Phân (Merge Bin)

Dự án ESP-IDF khi biên dịch mặc định sẽ xuất ra nhiều file `.bin` riêng biệt (gồm `bootloader.bin`, `partition-table.bin`, và ứng dụng `app.bin`) nằm ở các địa chỉ nhớ khác nhau. 

Script `build.py` sẽ tự động thực thi các bước cấu hình SDKConfig, gọi trình biên dịch, sau đó chạy tính năng **merge-bin** để ghép tất cả thành một tệp duy nhất để nạp tại địa chỉ **`0x0`**.

### Cú pháp lệnh biên dịch:
```bash
python3 scripts/build.py <board_type> --name "<variant_name>" [--language <locale>] [--wake-word <wake_word>] [--zip]
```

### Giải thích tham số:
- `<board_type>`: Thư mục chứa cấu hình bo mạch (ví dụ: `s3nx`, `s3mini`, `c3mini`... xem trong danh sách `--list-boards`).
- `--name "<variant_name>"`: Tên biến thể cấu hình (ví dụ: `"ESP32 S3Nx"`, `"ESP32-C3 Super Mini"`).
- `--language` (tùy chọn): Mã ngôn ngữ hệ thống phát ra loa, ví dụ: `vi-VN` (tiếng Việt), `en-US` (tiếng Anh).
- `--wake-word` (tùy chọn): Mô hình từ thức tỉnh offline, ví dụ: `wn9_jarvis_tts` hoặc `disabled` (tắt wake word).
- `--zip` (tùy chọn): Tự động tạo tệp nén `.zip` chứa file nhị phân hoàn chỉnh lưu vào thư mục `releases/`.

---

## 4. Ví Dụ Cụ Thể

### Ví dụ 1: Biên dịch cho mạch ESP32-S3 dòng S3Nx (tiếng Việt, từ thức tỉnh Jarvis, xuất file zip)
```bash
python3 scripts/build.py s3nx --name "ESP32 S3Nx" --language vi-VN --wake-word wn9_jarvis_tts --zip
```

### Ví dụ 2: Biên dịch cho mạch ESP32-C3 Super Mini
```bash
python3 scripts/build.py c3mini --name "ESP32-C3 Super Mini" --language vi-VN --wake-word disabled --zip
```

---

## 5. Kết Quả Đầu Ra & Đưa Lên Web Flasher

Khi quá trình biên dịch chạy thành công:
1. File nhị phân dạng ghép đơn nhất sẽ được tạo ra tại đường dẫn:
   `xiaozhi-esp32/build/merged-binary.bin`
2. Nếu có cờ `--zip`, một file phân phối đóng gói sẽ xuất hiện tại:
   `xiaozhi-esp32/releases/v<version>_<name>.zip`
3. **Cập nhật lên Web Flasher nội bộ của bạn:**
   - Copy file `merged-binary.bin` đã biên dịch xong.
   - Đổi tên file cho rõ ràng (ví dụ: `fw_s3_st7789_inmp441_0x0.bin`).
   - Di chuyển file này vào thư mục `firmwares/` của dự án Web Flasher (`xiaozhi-master-platform`).
   - Mở file [`manifest.json`](file:///Users/quochuy/QH_Code/IOT/xiaozhi-master-platform/manifest.json) ở thư mục gốc của Web Flasher và khai báo cấu hình bo mạch tương ứng cùng tên file để hệ thống nhận diện trên giao diện web.
