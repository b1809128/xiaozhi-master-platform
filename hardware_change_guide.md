# Hướng Dẫn Cập Nhật Website Khi Thay Đổi Màn Hình Hoặc Thiết Bị Phần Cứng

Tài liệu này hướng dẫn cách cấu hình lại hệ thống Website Web Flasher khi bạn muốn bổ sung, thay thế màn hình hiển thị (Display), bộ vi xử lý (Chip MCU), hoặc mô-đun âm thanh (Audio Mic) mới.

Hệ thống Web Flasher được thiết kế theo dạng hướng dữ liệu (Data-driven). Khi có thay đổi phần cứng, bạn chỉ cần thực hiện theo 4 bước chuẩn hóa dưới đây:

---

## Quy Trình 4 Bước Cập Nhật Hệ Thống

### Bước 1: Chuẩn bị tệp nhị phân Firmware mới
1. Biên dịch firmware mới cho cấu hình phần cứng tương ứng (sử dụng hướng dẫn trong `firmware_build_guide.md`).
2. Sao chép tệp tin nhị phân ghép hoàn chỉnh (`merged-binary.bin`) vào thư mục `firmwares/` ở thư mục gốc của dự án Web Flasher.
3. Đặt tên tệp tin gợi nhớ và phân biệt, ví dụ:
   `fw_s3_oled1306_inmp441_0x0.bin` (nếu dùng màn hình mới là OLED SSD1306).

---

### Bước 2: Đăng ký cấu hình phần cứng vào `manifest.json`
Mở tệp [`manifest.json`](file:///Users/quochuy/QH_Code/IOT/xiaozhi-master-platform/manifest.json). Bổ sung một đối tượng cấu hình mới vào trong mảng `firmwares`. 

Ví dụ, nếu bạn thêm màn hình **SSD1306** kết nối với chip **ESP32-S3**:
```json
    {
      "chip": "ESP32-S3",
      "display": "SSD1306",
      "audio": "INMP441",
      "file": "fw_s3_oled1306_inmp441_0x0.bin",
      "description": "ESP32-S3 kết hợp màn hình OLED SSD1306 0.96 inch và Micro INMP441.",
      "pinout": {
        "display": {
          "SCL": "GPIO 12",
          "SDA": "GPIO 11",
          "RST": "GPIO 14"
        },
        "audio": {
          "I2S_WS": "GPIO 42",
          "I2S_SCK": "GPIO 2",
          "I2S_SD": "GPIO 41"
        }
      }
    }
```
*Lưu ý:* Trình duyệt sẽ tự động cập nhật danh sách Dropdown lựa chọn dựa trên sự xuất hiện của các trường `chip`, `display`, và `audio` mới khai báo ở đây.

---

### Bước 3: Định nghĩa tên hiển thị thân thiện trong Backend (`app.py`)
Mở tệp [`app.py`](file:///Users/quochuy/QH_Code/IOT/xiaozhi-master-platform/app.py), tìm đến hàm API `/api/hardware-options` (khoảng dòng 45-88). 

Thêm mã ánh xạ tên hiển thị thân thiện cho màn hình mới của bạn vào đối tượng `name_map` để người dùng dễ nhận biết trên giao diện web thay vì đọc mã driver thô:
```python
        name_map = {
            "ST7789": "ST7789 (1.54 inch)",
            "ILI9341": "ILI9341 (2.8 inch)",
            "GC9A01": "GC9A01 (Màn hình tròn)",
            "SSD1306": "OLED SSD1306 (0.96 inch)"  # <— Thêm dòng này để định nghĩa màn hình mới
        }
```

---

### Bước 4: Thiết lập hiển thị mô phỏng LCD trên giao diện (`flasher.js`)
Mở tệp [`static/js/flasher.js`](file:///Users/quochuy/QH_Code/IOT/xiaozhi-master-platform/static/js/flasher.js), tìm đến hàm `renderVisualPreview` (khoảng dòng 225-275).

Hàm này chịu trách nhiệm hiển thị khối mô phỏng màn hình LCD Simulator ở cột bên phải. Bạn cấu hình hình dạng (Tròn, Vuông, Chữ nhật) và icon mô phỏng cho driver màn hình mới:
```javascript
    // Xác định kiểu mô phỏng màn hình LCD
    let lcdClass = 'lcd-screen-square'; // Mặc định là khung vuông
    let lcdIcon = 'fa-tv';              // Mặc định là icon TV
    
    if (firmware.display === 'GC9A01') {
        lcdClass = 'lcd-screen-circle'; // Khung tròn
        lcdIcon = 'fa-compass';
    } else if (firmware.display === 'ILI9341') {
        lcdClass = 'lcd-screen-rect';   // Khung chữ nhật nằm ngang
        lcdIcon = 'fa-laptop-code';
    } else if (firmware.display === 'SSD1306') {
        lcdClass = 'lcd-screen-rect';   // Ví dụ màn hình OLED dạng chữ nhật dẹt
        lcdIcon = 'fa-mobile-screen';
    }
```

---

## Cơ Chế Tự Động Đồng Bộ Của Website

Nhờ kiến trúc đồng bộ dữ liệu thông minh giữa Backend và Frontend:
1. Khi có yêu cầu tải trang, Frontend gửi request tới API `/api/hardware-options` lấy danh sách phần cứng đã tổng hợp từ `manifest.json`.
2. Dropdown lựa chọn lập tức hiển thị thêm dòng chip/màn hình mới.
3. Khi người dùng click chọn cấu hình mới, API `/api/get-firmware-info` trả về đầy đủ đường dẫn file nạp, mô tả pinout GPIO đấu dây và hiển thị trực quan lên mô phỏng thiết bị tương ứng mà không cần phải viết lại giao diện web!
