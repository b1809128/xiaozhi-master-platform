# Hướng Dẫn Sử Dụng Trình Nạp Firmware Xiaozhi ESP32 (Local)

Chào mừng bạn! Đây là công cụ nạp Firmware tùy biến cho mạch ESP32 (dựa trên repo `xiaozhi-esp32`) chạy trực tiếp trên máy tính cá nhân của bạn thông qua trình duyệt web. 

Hệ thống đã được **tinh gọn tối đa**: Lược bỏ hoàn toàn AI, cơ sở dữ liệu vector, LangChain và các dịch vụ phức tạp. Bạn chỉ cần chạy **một lệnh duy nhất** là website khởi chạy và sẵn sàng sử dụng ngay lập tức!

---

## 1. Hướng Dẫn Cho Hệ Điều Hành WINDOWS

Dành cho người mới bắt đầu, vui lòng thực hiện chính xác từng bước sau:

### Bước 1: Cài đặt Python (Nếu máy chưa có)
1. Truy cập trang web chính thức: [https://www.python.org/downloads/](https://www.python.org/downloads/)
2. Tải bản cài đặt Python mới nhất cho Windows.
3. Chạy file cài đặt vừa tải về. 
   > [!IMPORTANT]  
   > Bạn **BẮT BUỘC** phải tích chọn ô **"Add python.exe to PATH"** ở phía dưới cùng trước khi bấm **"Install Now"**. Nếu thiếu bước này, máy tính sẽ báo lỗi không nhận lệnh `python`.
4. Chờ quá trình cài đặt hoàn tất và bấm đóng.

### Bước 2: Mở cửa sổ Dòng lệnh (Command Prompt / CMD)
1. Nhấn phím **Windows** trên bàn phím (hoặc click vào nút Start).
2. Gõ chữ `cmd` rồi nhấn phím **Enter**.
3. Một cửa sổ màn hình màu đen (Command Prompt) sẽ hiện ra.
4. Chuyển thư mục làm việc về thư mục chứa mã nguồn này bằng cách gõ lệnh sau (thay đường dẫn bằng thư mục thực tế của bạn):
   ```cmd
   cd "Đường_Dẫn_Thư_Mục_Dự_Án"
   ```
   *(Ví dụ: `cd "C:\Users\Admin\Documents\xiaozhi-master-platform"`)*

### Bước 3: Cài đặt thư viện cần thiết
Tại cửa sổ CMD vừa mở, gõ lệnh sau và nhấn **Enter**:
```cmd
pip install -r requirements.txt
```
*(Chờ khoảng vài giây để hệ thống tải và cài đặt thư viện Flask).*

### Bước 4: Khởi chạy ứng dụng
Gõ lệnh sau và nhấn **Enter**:
```cmd
python app.py
```
Khi màn hình hiển thị dòng chữ `http://127.0.0.1:5001`, chúc mừng bạn đã khởi chạy thành công! Giữ nguyên cửa sổ này và chuyển sang **Mục 3** để sử dụng.

---

## 2. Hướng Dẫn Cho Hệ Điều Hành macOS (Macbook/iMac)

### Bước 1: Kiểm tra và cài đặt Python
macOS thường đi kèm sẵn Python3, hoặc bạn có thể tải bản cài đặt chuẩn:
1. Tải Python cho macOS tại: [https://www.python.org/downloads/mac-osx/](https://www.python.org/downloads/mac-osx/)
2. Chạy file cài đặt dạng `.pkg` vừa tải và bấm tiếp tục cho đến khi hoàn tất.

### Bước 2: Mở Terminal
1. Nhấn tổ hợp phím **Command ⌘ + Space** để mở thanh tìm kiếm Spotlight.
2. Gõ chữ `terminal` và nhấn **Enter**.
3. Di chuyển vào thư mục dự án bằng lệnh:
   ```bash
   cd "/đường/dẫn/thư/mục/dự/án"
   ```
   *(Mẹo: Bạn có thể gõ chữ `cd ` rồi kéo thả trực tiếp thư mục dự án từ Finder vào cửa sổ Terminal).*

### Bước 3: Cài đặt thư viện
Gõ lệnh sau và nhấn **Enter**:
```bash
pip3 install -r requirements.txt
```

### Bước 4: Khởi chạy ứng dụng
Gõ lệnh sau và nhấn **Enter**:
```bash
python3 app.py
```
Giữ nguyên cửa sổ Terminal này và chuyển sang **Mục 3** để bắt đầu nạp firmware.

---

## 3. Cách Sử Dụng Website Nạp Firmware

1. Mở trình duyệt Chrome, Edge, Brave hoặc bất kỳ trình duyệt nhân Chromium nào trên máy tính của bạn.
2. Nhập địa chỉ sau vào thanh URL: [http://localhost:5001](http://localhost:5001) hoặc [http://127.0.0.1:5001](http://127.0.0.1:5001)
3. Giao diện trang web nạp mạch chuyên nghiệp sẽ hiển thị.

### Các thao tác nạp:
*   **Tải Driver UART (Nếu máy tính chưa nhận cổng COM):** Ở góc trên bên phải, có nút tải driver `CH340` và `CP210x`. Nếu cắm cáp mà bấm "Kết nối" không thấy hiện cổng COM, hãy tải và cài đặt driver này rồi khởi động lại trình duyệt.
*   **TAB 1 - Cấu Hình Sẵn (Presets):** Click chọn một trong các Card có sẵn (ví dụ: *ESP32-S3 + ST7789 1.54 inch*). Hệ thống sẽ tự động cấu hình file `.bin` tương ứng và hiển thị sơ đồ nối dây GPIO trực quan.
*   **TAB 2 - Tùy Biến Linh Kiện (Matrix):** Tùy ý phối hợp các loại Chip -> Màn hình -> Micro. Hệ thống sẽ tự động tìm file `.bin` phù hợp nhất trong thư mục `firmwares/`.
*   **Quy trình nạp mạch:**
    1. Click **[Kết Nối Cổng COM]** và chọn thiết bị USB của bạn từ danh sách hiện ra.
    2. Tích chọn **Xóa toàn bộ Flash trước khi nạp** (nếu muốn làm sạch bộ nhớ cũ).
    3. Click nút **[⚡ Bắt Đầu Ghi & Nạp Firmware]**.
    4. Quá trình ghi sẽ chạy từ 0% đến 100% hiển thị trực tiếp trên Progress Bar và cửa sổ Terminal Log.
    5. Sau khi nạp xong, mạch sẽ tự động khởi động lại và bắt đầu chạy firmware mới.

---

## 4. Hướng Dẫn Sửa Lỗi Khi Nạp Mạch

### 1. Không tìm thấy cổng kết nối (Cổng COM)
*   **Nguyên nhân:** Dây cáp USB của bạn chỉ là loại cáp sạc điện thoại (không có lõi truyền dữ liệu), hoặc bạn chưa cài Driver CH340 / CP210x.
*   **Khắc phục:** Thay dây cáp USB khác (hỗ trợ truyền dữ liệu) và click cài đặt Driver ở góc phải màn hình.

### 2. Lỗi bắt tay thất bại (Handshake Timeout / Connecting...)
*   **Nguyên nhân:** Một số mạch ESP32 không tự động kích hoạt chế độ nạp chương trình (Bootloader mode).
*   **Khắc phục:** Nhấn và **giữ nguyên nút BOOT** (hoặc nút IO0) trên mạch ESP32 của bạn -> Click nút **[⚡ Bắt Đầu Ghi & Nạp Firmware]** trên web -> Khi màn hình Terminal bắt đầu chạy phần trăm nạp hoặc xuất hiện các dòng chấm `...`, bạn có thể thả tay ra khỏi nút BOOT.

### 3. Nạp thành công 100% nhưng thiết bị không chạy
*   **Nguyên nhân:** Nối sai chân GPIO của màn hình hoặc micro, hoặc nguồn cấp qua cổng USB của máy tính quá yếu.
*   **Khắc phục:** Xem kỹ sơ đồ chân tại khu vực **Sơ đồ chân (Pinout)** trên giao diện web để cắm lại dây cho chính xác. Thử cắm cổng USB ở phía sau thùng máy đối với PC để có dòng điện ổn định hơn.
# xiaozhi-master-platform
