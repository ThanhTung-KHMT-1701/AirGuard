# AirGuard - Tính năng Dashboard tương tác

## 🎯 Tổng quan

Đã thêm 2 trang tương tác mới cho phép người dùng tùy chỉnh thông số và xem kết quả phân tích động từ dữ liệu đã có trong `data/processed/`.

## ✨ Tính năng đã thêm

### 1. 📊 Dashboard tương tác
**URL**: `/interactive-dashboard`

**Chức năng:**
- Cho phép người dùng chọn loại phân tích (Classification, Regression, Semi-supervised)
- Tùy chỉnh số lượng mẫu hiển thị
- Lọc metrics theo loại
- Tùy chỉnh độ chính xác hiển thị (số chữ số thập phân)

**Dữ liệu sử dụng:**
- `data/processed/06_metrics.json` - Metrics của Classification
- `data/processed/06_predictions_sample.csv` - Predictions của Classification
- `data/processed/07_regression_metrics.json` - Metrics của Regression
- `data/processed/07_regression_predictions_sample.csv` - Predictions của Regression
- `data/processed/04_metrics_self_training.json` - Metrics của Self-training
- `data/processed/05_metrics_co_training.json` - Metrics của Co-training
- `data/processed/04_predictions_self_training_sample.csv` - Predictions của Self-training

**Kết quả hiển thị:**
- ✅ Metrics cards với giá trị được format theo yêu cầu
- ✅ Bảng dữ liệu với số lượng dòng tùy chỉnh
- ✅ Thống kê tổng quan (tổng số mẫu, accuracy, sai số...)

### 2. ⚖️ So sánh mô hình nâng cao
**URL**: `/model-comparison`

**Chức năng:**
- Chọn nhiều mô hình để so sánh (checkbox)
- Chọn metric để so sánh (Accuracy, F1 Macro, F1 Weighted, Precision, Recall)
- Hiển thị kết quả dưới dạng bảng và biểu đồ

**Dữ liệu sử dụng:**
- Tất cả các file `*_metrics*.json` trong `data/processed/`

**Kết quả hiển thị:**
- ✅ Bảng xếp hạng với medals (🥇🥈🥉)
- ✅ Bar chart trực quan (HTML/CSS)
- ✅ Thống kê chi tiết: điểm cao nhất, thấp nhất, trung bình, chênh lệch
- ✅ Nhận xét tự động cho từng mô hình

## 🎨 Giao diện

### Đặc điểm thiết kế:
- ✅ Font-size tối thiểu: 1em
- ✅ Padding và margin hợp lý: 1em - 2em
- ✅ Color scheme:
  - Blue gradient: #1F62FF → #1FD2FF (buttons, headers)
  - Green: #1FFF2A (Dashboard button)
  - Orange: #FF9A1F (Compare button)
  - Background: #f8f9fa
- ✅ Responsive design
- ✅ Form inputs với styling đẹp mắt

## 📂 Files đã tạo/cập nhật

### Files mới:
1. `templates/interactive_dashboard.html` - Trang Dashboard tương tác
2. `templates/model_comparison.html` - Trang So sánh mô hình

### Files đã cập nhật:
1. `app.py` - Thêm 2 routes mới:
   - `/interactive-dashboard` (GET, POST)
   - `/model-comparison` (GET, POST)
   
2. `templates/base.html` - Thêm links vào navigation menu:
   - "📊 Dashboard tương tác" (highlighted với màu xanh lá)
   - "⚖️ So sánh mô hình nâng cao" (trong dropdown)

3. `templates/index.html` - Thêm quick links và hướng dẫn mới

4. `FLASK_README.md` - Cập nhật documentation

## 🚀 Cách sử dụng

### Dashboard tương tác:
1. Truy cập: http://localhost:5000/interactive-dashboard
2. Chọn các tham số mong muốn
3. Nhấn "Áp dụng và Xem kết quả"
4. Xem kết quả được hiển thị động

### So sánh mô hình:
1. Truy cập: http://localhost:5000/model-comparison
2. Tick chọn ít nhất 2 mô hình
3. Chọn metric để so sánh
4. Nhấn "So sánh các mô hình đã chọn"
5. Xem bảng xếp hạng và biểu đồ

## 💡 Ví dụ sử dụng

### Case 1: So sánh Classification vs Regression theo F1 Macro
```
1. Vào /model-comparison
2. Chọn: ☑ Classification Model, ☑ Regression Model
3. Metric: F1 Macro
4. Submit → Xem kết quả xếp hạng
```

### Case 2: Xem 50 dự đoán của Self-training
```
1. Vào /interactive-dashboard
2. Loại phân tích: Semi-supervised Learning
3. Số mẫu: 50
4. Submit → Xem 50 dòng dự đoán
```

### Case 3: So sánh Self-training vs Co-training
```
1. Vào /model-comparison
2. Chọn: ☑ Self-training, ☑ Co-training
3. Metric: Accuracy
4. Submit → Xem ai tốt hơn
```

## 🔧 Kỹ thuật triển khai

### Backend (Flask):
- Sử dụng POST method để nhận form data
- Load dữ liệu từ JSON/CSV dựa trên lựa chọn
- Tính toán summary statistics động
- Format số theo decimal_places

### Frontend (HTML/Jinja2):
- Form với select boxes và checkboxes
- Conditional rendering dựa trên params
- String formatting động: `{:.Xf}` format
- CSS bar chart tự vẽ bằng div + width %

### Data Flow:
```
User Input (Form)
    ↓
POST Request
    ↓
app.py (Process params)
    ↓
Load JSON/CSV from data/processed/
    ↓
Calculate stats
    ↓
Render template với data
    ↓
Display results
```

## ✅ Checklist hoàn thành

- [x] Trang Dashboard tương tác
- [x] Form tùy chỉnh thông số
- [x] Load dữ liệu từ processed files
- [x] Hiển thị metrics cards
- [x] Hiển thị bảng predictions
- [x] Tính toán summary statistics
- [x] Trang So sánh mô hình
- [x] Checkbox để chọn nhiều mô hình
- [x] Bảng xếp hạng với ranking
- [x] Bar chart visualization (HTML/CSS)
- [x] Thống kê chi tiết
- [x] Cập nhật navigation menu
- [x] Cập nhật trang chủ với quick links
- [x] Cập nhật documentation

## 🎓 Học được gì

### Skills áp dụng:
1. **Flask Forms**: POST method, request.form.get/getlist
2. **Dynamic Data Loading**: Load dữ liệu dựa trên user input
3. **Template Logic**: Jinja2 conditionals, loops, filters
4. **Data Processing**: Pandas operations, calculations
5. **CSS Visualization**: Tạo bar chart bằng HTML/CSS thuần
6. **UX Design**: Form design, responsive layout, color scheme

### Best Practices:
- ✅ Validation: Kiểm tra dữ liệu tồn tại trước khi load
- ✅ Default Values: Cung cấp giá trị mặc định cho form
- ✅ Error Handling: Hiển thị message khi chưa có data
- ✅ Code Organization: Tách logic rõ ràng
- ✅ Documentation: Comment đầy đủ

---

**Tác giả**: AirGuard Development Team  
**Ngày hoàn thành**: January 28, 2026  
**Version**: 2.0 (với Interactive Features)
