# AirGuard - Hướng dẫn sử dụng giao diện Flask

## Giới thiệu

Ứng dụng web Flask này cung cấp giao diện trực quan để khám phá kết quả phân tích chất lượng không khí của dự án AirGuard.

## Cài đặt

### 0. Kích hoạt môi trường conda (quan trọng!)

```bash
conda activate KhaiPhaDuLieu
```

### 1. Cài đặt các thư viện cần thiết

```bash
pip install -r requirements.txt
```

### 2. Cấu trúc thư mục

Đảm bảo rằng các thư mục sau tồn tại với đầy đủ dữ liệu:
- `images/` - Chứa các file ảnh biểu đồ (.png)
- `data/processed/` - Chứa các file dữ liệu đầu ra (.csv, .json)
- `templates/` - Chứa các file HTML template
- `static/` - Chứa các file CSS

## Chạy ứng dụng

### Phương pháp 1: Sử dụng script tự động (Khuyến nghị)

```bash
run_flask.bat
```

Script này sẽ tự động:
- Kích hoạt môi trường conda KhaiPhaDuLieu
- Kiểm tra và cài đặt dependencies nếu cần
- Chạy ứng dụng Flask

### Phương pháp 2: Chạy thủ công

```bash
# Kích hoạt môi trường
conda activate KhaiPhaDuLieu

# Chạy ứng dụng
python app.py
```

### Phương pháp 3: Chạy trực tiếp

```bash
python app.py
```

### Phương pháp 2: Chạy với Flask CLI

```bash
# Windows
set FLASK_APP=app.py
set FLASK_ENV=development
flask run

# Linux/Mac
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

Sau khi chạy, mở trình duyệt và truy cập:
- **URL**: http://localhost:5000
- **Hoặc**: http://127.0.0.1:5000

## Các tính năng tương tác mới 🆕

### 1. Dashboard tương tác (`/interactive-dashboard`)
Cho phép người dùng tùy chỉnh các thông số và xem kết quả trực quan:

**Các tùy chọn:**
- **Loại phân tích**: Classification, Regression, hoặc Semi-supervised Learning
- **Số mẫu hiển thị**: 10, 20, 50, 100 hoặc tất cả
- **Metric hiển thị**: Lọc theo loại metric (Accuracy, F1, Precision, Recall)
- **Số chữ số thập phân**: 2, 3, hoặc 4 chữ số

**Kết quả hiển thị:**
- Các chỉ số đánh giá dưới dạng cards
- Bảng dữ liệu dự đoán với số lượng mẫu tùy chỉnh
- Thống kê tổng quan

### 2. So sánh mô hình nâng cao (`/model-comparison`)
So sánh hiệu suất giữa nhiều mô hình khác nhau:

**Các tùy chọn:**
- **Chọn mô hình**: Classification, Regression, Self-training, Co-training
- **Metric so sánh**: Accuracy, F1 Macro, F1 Weighted, Precision, Recall

**Kết quả hiển thị:**
- Bảng xếp hạng các mô hình
- Biểu đồ bar chart so sánh trực quan
- Thống kê chi tiết (điểm cao nhất, thấp nhất, trung bình, chênh lệch)
- Nhận xét tự động cho từng mô hình

## Cấu trúc giao diện

### Trang chủ (/)
Tổng quan về dự án AirGuard, mục tiêu và cấu trúc.

### Tiền xử lý & Phân tích
- **01. Tiền xử lý và EDA** (`/preprocessing-eda`)
  - Tỷ lệ giá trị thiếu
  - Phân bố các lớp chất lượng không khí
  - Mẫu dữ liệu gốc và sau khi làm sạch

- **02. Chuẩn bị dữ liệu Semi-supervised** (`/semi-dataset`)
  - Tạo tập labeled và unlabeled
  - Mẫu dữ liệu cho Semi-supervised Learning

- **03. Chuẩn bị đặc trưng** (`/feature-preparation`)
  - Danh sách đặc trưng
  - Dữ liệu sau khi feature engineering

### Semi-supervised Learning
- **04. Self-training** (`/self-training`)
  - Kết quả đánh giá metrics
  - Quá trình Self-training dynamics
  - Mẫu dự đoán và cảnh báo

- **05. Co-training** (`/co-training`)
  - Kết quả đánh giá metrics
  - Quá trình Co-training dynamics
  - Mẫu dự đoán và cảnh báo

- **09. Báo cáo Semi-supervised** (`/semi-supervised-report`)
  - So sánh Supervised vs Semi-supervised
  - Phân tích chi tiết Self-training và Co-training
  - Timeline và top alerts

### Mô hình
- **06. Phân loại** (`/classification`)
  - Kết quả đánh giá
  - Ma trận nhầm lẫn
  - Báo cáo phân loại chi tiết

- **07. Hồi quy** (`/regression`)
  - Metrics đánh giá (MAE, MSE, RMSE, R²)
  - Actual vs Predicted
  - Phân bố target

- **08. Dự báo ARIMA** (`/arima-forecasting`)
  - Chuỗi thời gian gốc
  - ACF và PACF plots
  - Forecast vs Actual
  - Hourly seasonality

### Câu hỏi & So sánh
- **10. Câu hỏi 01** (`/question-01`)
  - So sánh các thuật toán phân loại

- **11. Câu hỏi 02** (`/question-02`)
  - Phân tích tham số Co-training

- **12. Câu hỏi 03** (`/question-03`)
  - So sánh Graph-based methods

- **13. Câu hỏi 04** (`/question-04`)
  - Phân tích lớp hiếm (rare classes)

- **14. Baseline và So sánh** (`/baseline-comparison`)
  - So sánh tổng thể
  - Performance vs Cost
  - Improvement percentage

## Tính năng

### 1. Navigation Menu
- Menu dropdown phân nhóm theo chức năng
- Sticky navigation luôn hiển thị khi cuộn trang
- Responsive design cho mobile và tablet

### 2. Hiển thị dữ liệu
- **Biểu đồ**: Tự động load từ thư mục `images/`
- **Bảng CSV**: Hiển thị dạng HTML table với pagination
- **Metrics JSON**: Hiển thị dạng card layout

### 3. Styling
- Font-size tối thiểu: 1em (16px)
- Padding và margin hợp lý cho tất cả các phần tử
- Color scheme theo yêu cầu:
  - Blue tones: #1F62FF, #1FD2FF
  - Red: #FF351F
  - Green: #1FFF2A
  - Orange: #FF9A1F
  - Yellow: #FFDA1F

### 4. Responsive Design
- Tự động điều chỉnh layout cho màn hình nhỏ
- Grid layout linh hoạt
- Mobile-friendly navigation

## Cấu trúc file

```
AirGuard/
├── app.py                          # Flask application chính
├── requirements.txt                # Dependencies
├── FLASK_README.md                 # File này
├── templates/                      # HTML templates
│   ├── base.html                   # Base template với nav & footer
│   ├── index.html                  # Trang chủ
│   ├── 01_preprocessing_eda.html
│   ├── 02_semi_dataset.html
│   ├── 03_feature_preparation.html
│   ├── 04_self_training.html
│   ├── 05_co_training.html
│   ├── 06_classification.html
│   ├── 07_regression.html
│   ├── 08_arima_forecasting.html
│   ├── 09_semi_supervised_report.html
│   ├── 10_question_01.html
│   ├── 11_question_02.html
│   ├── 12_question_03.html
│   ├── 13_question_04.html
│   └── 14_baseline_comparison.html
├── static/                         # Static files
│   └── style.css                   # Custom CSS
├── images/                         # Biểu đồ output
│   └── *.png
└── data/processed/                 # Dữ liệu output
    ├── *.csv
    └── *.json
```

## Customization

### Thay đổi Port
Mặc định ứng dụng chạy trên port 5000. Để thay đổi, chỉnh sửa trong `app.py`:

```python
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)  # Thay đổi port ở đây
```

### Thêm trang mới
1. Tạo route mới trong `app.py`:
```python
@app.route('/new-page')
def new_page():
    data = {
        # Load dữ liệu
    }
    return render_template('new_page.html', data=data)
```

2. Tạo template mới `templates/new_page.html`:
```html
{% extends "base.html" %}
{% block title %}Trang mới{% endblock %}
{% block content %}
    <!-- Nội dung trang -->
{% endblock %}
```

3. Thêm link vào navigation trong `templates/base.html`

### Thay đổi màu sắc
Chỉnh sửa các biến CSS trong `static/style.css`:

```css
:root {
    --primary-blue: #1F62FF;
    --secondary-blue: #1FD2FF;
    /* ... */
}
```

## Troubleshooting

### Lỗi: "Template not found"
- Kiểm tra xem thư mục `templates/` có đầy đủ file không
- Đảm bảo tên file template khớp với tên trong `render_template()`

### Lỗi: "Image not found" (404)
- Kiểm tra xem file ảnh có tồn tại trong thư mục `images/` không
- Đảm bảo tên file trong code khớp với tên file thực tế

### Lỗi: "Cannot load CSV/JSON"
- Kiểm tra đường dẫn file trong `data/processed/`
- Đảm bảo file không bị corrupt

### Ứng dụng chạy chậm
- Giảm số lượng dòng hiển thị trong bảng (tham số `nrows`)
- Optimize kích thước ảnh
- Sử dụng production server (gunicorn, uWSGI) thay vì Flask development server

## Production Deployment

Để deploy lên production, không nên dùng Flask development server. Sử dụng:

### Option 1: Gunicorn (Linux/Mac)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Option 2: Waitress (Windows)
```bash
pip install waitress
waitress-serve --host=0.0.0.0 --port=5000 app:app
```

## Liên hệ & Hỗ trợ

Nếu có vấn đề hoặc câu hỏi, vui lòng tạo issue trong repository hoặc liên hệ team phát triển.

---

**© 2026 AirGuard Project - Hệ thống giám sát chất lượng không khí**
