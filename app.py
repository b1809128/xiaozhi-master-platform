import os
import json
from flask import Flask, render_template, jsonify, send_from_directory

app = Flask(__name__, static_folder='static', template_folder='templates')

# Default configuration to be generated if manifest.json is missing
DEFAULT_MANIFEST = {
  "firmwares": [
    {
      "name": "ESP32-S3 + ST7789 1.54 inch",
      "chip": "ESP32-S3",
      "display": "ST7789",
      "audio": "INMP441",
      "file": "fw_s3_st7789_inmp441_0x0.bin",
      "description": "Cấu hình chuẩn cho ESP32-S3 đi kèm màn hình ST7789 1.54 inch và Micro INMP441.",
      "pinout": {
        "display": {
          "SCL": "GPIO 12",
          "SDA": "GPIO 11",
          "CS": "GPIO 10",
          "DC": "GPIO 13",
          "RST": "GPIO 14"
        },
        "audio": {
          "I2S_WS": "GPIO 42",
          "I2S_SCK": "GPIO 2",
          "I2S_SD": "GPIO 41"
        }
      }
    },
    {
      "name": "ESP32-C3 Không Màn Hình",
      "chip": "ESP32-C3",
      "display": "None",
      "audio": "INMP441",
      "file": "fw_c3_none_inmp441_0x0.bin",
      "description": "Cấu hình siêu nhỏ gọn dùng chip ESP32-C3, không có màn hình và sử dụng Micro INMP441.",
      "pinout": {
        "display": {},
        "audio": {
          "I2S_WS": "GPIO 5",
          "I2S_SCK": "GPIO 1",
          "I2S_SD": "GPIO 4"
        }
      }
    },
    {
      "name": "ESP32-S3 Tròn GC9A01",
      "chip": "ESP32-S3",
      "display": "GC9A01",
      "audio": "MSM261",
      "file": "fw_s3_gc9a01_msm261_0x0.bin",
      "description": "Cấu hình cho bo mạch tròn dùng màn hình GC9A01 và Micro MSM261 (I2S).",
      "pinout": {
        "display": {
          "SCL": "GPIO 12",
          "SDA": "GPIO 11",
          "CS": "GPIO 10",
          "DC": "GPIO 13",
          "RST": "GPIO 14"
        },
        "audio": {
          "I2S_WS": "GPIO 42",
          "I2S_SCK": "GPIO 2",
          "I2S_SD": "GPIO 41"
        }
      }
    },
    {
      "name": "ESP32-S3 ILI9341 2.8 inch",
      "chip": "ESP32-S3",
      "display": "ILI9341",
      "audio": "INMP441",
      "file": "fw_s3_ili9341_inmp441_0x0.bin",
      "description": "Cấu hình màn hình lớn ILI9341 2.8 inch và Micro INMP441 trên nền chip ESP32-S3.",
      "pinout": {
        "display": {
          "SCL": "GPIO 12",
          "SDA": "GPIO 11",
          "CS": "GPIO 10",
          "DC": "GPIO 13",
          "RST": "GPIO 14"
        },
        "audio": {
          "I2S_WS": "GPIO 42",
          "I2S_SCK": "GPIO 2",
          "I2S_SD": "GPIO 41"
        }
      }
    },
    {
      "name": "ESP32-C3 + ST7789 1.54 inch",
      "chip": "ESP32-C3",
      "display": "ST7789",
      "audio": "INMP441",
      "file": "fw_c3_st7789_inmp441_0x0.bin",
      "description": "Cấu hình dùng chip ESP32-C3 với màn hình ST7789 1.54 inch và Micro INMP441.",
      "pinout": {
        "display": {
          "SCL": "GPIO 6",
          "SDA": "GPIO 7",
          "CS": "GPIO 10",
          "DC": "GPIO 2",
          "RST": "GPIO 3"
        },
        "audio": {
          "I2S_WS": "GPIO 5",
          "I2S_SCK": "GPIO 1",
          "I2S_SD": "GPIO 4"
        }
      }
    },
    {
      "name": "ESP32-S3 Không Màn Hình, Không Micro",
      "chip": "ESP32-S3",
      "display": "None",
      "audio": "None",
      "file": "fw_s3_none_none_0x0.bin",
      "description": "Cấu hình tối giản chỉ chạy chip ESP32-S3 core, không màn hình, không micro.",
      "pinout": {
        "display": {},
        "audio": {}
      }
    }
  ]
}

def init_workspace():
    """Tự động khởi tạo thư mục firmwares và file manifest.json nếu chưa tồn tại"""
    # 1. Tạo thư mục firmwares
    firmwares_dir = 'firmwares'
    if not os.path.exists(firmwares_dir):
        print(f"[*] Đang tạo thư mục: {firmwares_dir}")
        os.makedirs(firmwares_dir)
    
    # 2. Tạo file manifest.json
    manifest_path = 'manifest.json'
    if not os.path.exists(manifest_path):
        print(f"[*] Đang tạo file cấu hình mẫu: {manifest_path}")
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(DEFAULT_MANIFEST, f, indent=2, ensure_ascii=False)
    
    # 3. Tạo các file binary mẫu nếu chưa có
    try:
        with open(manifest_path, 'r', encoding='utf-8') as f:
            manifest_data = json.load(f)
    except Exception as e:
        print(f"[!] Không thể đọc {manifest_path}, dùng cấu hình mặc định. Lỗi: {e}")
        manifest_data = DEFAULT_MANIFEST

    for fw in manifest_data.get('firmwares', []):
        fw_file = fw.get('file')
        if fw_file:
            fw_path = os.path.join(firmwares_dir, fw_file)
            if not os.path.exists(fw_path):
                print(f"[*] Đang tạo file firmware mẫu: {fw_path}")
                # Tạo file binary dummy 1024 bytes (toàn số 0) để người dùng có thể test tải/nạp
                with open(fw_path, 'wb') as f:
                    f.write(b'\x00' * 1024)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/manifest')
def get_manifest():
    manifest_path = 'manifest.json'
    if os.path.exists(manifest_path):
        try:
            with open(manifest_path, 'r', encoding='utf-8') as f:
                return jsonify(json.load(f))
        except Exception as e:
            return jsonify({"error": f"Không thể đọc manifest.json: {str(e)}"}), 500
    return jsonify({"error": "Không tìm thấy file manifest.json"}), 404

@app.route('/firmwares/<path:filename>')
def download_firmware(filename):
    return send_from_directory('firmwares', filename, as_attachment=True)

if __name__ == '__main__':
    # Khởi tạo workspace
    init_workspace()
    
    port = int(os.environ.get('PORT', 5001))
    print(f"\n=======================================================")
    print(f"  Xiaozhi Flashing Platform đang chạy tại:")
    print(f"  --> http://127.0.0.1:{port}")
    print(f"  --> http://localhost:{port}")
    print(f"=======================================================\n")
    
    app.run(host='0.0.0.0', port=port, debug=True)
