# 01 — Preprocessing & EDA (Beijing Multi-Site Air Quality)

## 🎯 Mục tiêu chính

Notebook này thực hiện các bước **tiền xử lý dữ liệu** và **phân tích khám phá dữ liệu (EDA)** cho bộ dữ liệu chất lượng không khí Beijing Multi-Site, bao gồm:

1. **Tải dữ liệu** từ UCI Repository hoặc file ZIP local
2. **Làm sạch dữ liệu** (xử lý missing values, chuẩn hóa)
3. **Tạo nhãn phân lớp AQI** dựa trên PM2.5 trung bình 24h
4. **Tạo đặc trưng thời gian** (hour, day, month, etc.)
5. **Tạo đặc trưng lag** để phục vụ dự đoán chuỗi thời gian

---

## 📥 Đầu vào (Input)

| Tham số | Giá trị mặc định | Mô tả |
|---------|------------------|-------|
| `USE_UCIMLREPO` | `False` | Nếu `True`: tải từ UCI Repository (cần internet). Nếu `False`: dùng file local |
| `RAW_ZIP_PATH` | `data/raw/PRSA2017_Data_20130301-20170228.zip` | Đường dẫn file ZIP chứa dữ liệu thô |
| `LAG_HOURS` | `[1, 3, 24]` | Danh sách các khoảng thời gian lag (giờ) để tạo features |

**Dữ liệu thô:** 12 file CSV từ 12 trạm quan trắc tại Beijing (2013-2017), bao gồm:
- Aotizhongxin, Changping, Dingling, Dongsi, Guanyuan, Gucheng
- Huairou, Nongzhanguan, Shunyi, Tiantan, Wanliu, Wanshouxigong

---

## 📤 Đầu ra (Output)

| File | Mô tả |
|------|-------|
| `data/processed/01_cleaned.parquet` | **Dataset chính** đã làm sạch và có đầy đủ features |
| `data/processed/01_raw_data_sample.csv` | Mẫu 100 dòng dữ liệu thô |
| `data/processed/01_cleaned_data_sample.csv` | Mẫu 100 dòng dữ liệu đã làm sạch |
| `data/processed/01_missing_rate.csv` | Tỷ lệ missing của từng cột |
| `data/processed/01_class_distribution.csv` | Phân bố các lớp AQI |
| `images/01_class_distribution.png` | Biểu đồ phân bố lớp AQI |

---

## 🔄 Quy trình xử lý

```
┌─────────────────────────────────────────────────────────────────┐
│  1. Load Data                                                    │
│     load_beijing_air_quality() → df_raw                         │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  2. Clean Data                                                   │
│     clean_air_quality_df() → Xử lý missing, chuẩn hóa           │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  3. Create AQI Labels                                            │
│     add_pm25_24h_and_label() → Tính PM2.5 24h mean → aqi_class  │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  4. Add Time Features                                            │
│     add_time_features() → hour, day, month, weekday, etc.       │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  5. Add Lag Features                                             │
│     add_lag_features() → PM2.5_lag_1h, lag_3h, lag_24h          │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  6. Save Output                                                  │
│     → 01_cleaned.parquet                                        │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📊 Cột dữ liệu chính

| Cột | Mô tả |
|-----|-------|
| `datetime` | Timestamp của quan trắc |
| `station` | Tên trạm quan trắc |
| `PM2.5` | Nồng độ PM2.5 (µg/m³) |
| `pm25_24h` | PM2.5 trung bình 24 giờ gần nhất |
| `aqi_class` | Nhãn phân lớp AQI (Good, Moderate, Unhealthy, etc.) |
| `hour`, `day`, `month`, `weekday` | Đặc trưng thời gian |
| `PM2.5_lag_1h`, `PM2.5_lag_3h`, `PM2.5_lag_24h` | Giá trị PM2.5 ở các thời điểm trước |

---

## 🏷️ Tiêu chí phân loại chất lượng không khí (AQI Class)

Nhãn `aqi_class` được tính dựa trên **PM2.5 trung bình 24 giờ** (µg/m³) theo tiêu chuẩn US EPA:

| Mức độ (AQI Class) | PM2.5 (µg/m³) | Ý nghĩa | Màu sắc |
|--------------------|---------------|---------|---------|
| **Good** | 0.0 – 9.0 | Chất lượng không khí tốt | 🟢 Xanh lá |
| **Moderate** | 9.1 – 35.4 | Chất lượng không khí trung bình | 🟡 Vàng |
| **Unhealthy_for_Sensitive_Groups** | 35.5 – 55.4 | Không tốt cho nhóm nhạy cảm (trẻ em, người già, người có bệnh hô hấp) | 🟠 Cam |
| **Unhealthy** | 55.5 – 125.4 | Không tốt cho sức khỏe | 🔴 Đỏ |
| **Very_Unhealthy** | 125.5 – 225.4 | Rất không tốt cho sức khỏe | 🟣 Tím |
| **Hazardous** | > 225.4 | Nguy hại - Cảnh báo khẩn cấp | 🟤 Nâu đỏ |

**Hình minh họa:**

![Tiêu chí phân loại chất lượng không khí](../.images/TieuChiPhanLoaiChatLuongKhongKhi.png)

**Mã nguồn tham khảo:** [src/classification_library.py](../src/classification_library.py) - hàm `pm25_to_aqi_class()`

```python
# PM2.5 breakpoints (µg/m³)
bins = [-np.inf, 9.0, 35.4, 55.4, 125.4, 225.4, np.inf]
AQI_CLASSES = ["Good", "Moderate", "Unhealthy_for_Sensitive_Groups", 
               "Unhealthy", "Very_Unhealthy", "Hazardous"]
```

---

## 💡 Ý nghĩa trong dự án

Notebook này là **bước đầu tiên và quan trọng nhất** trong pipeline xử lý dữ liệu:

- **Output `01_cleaned.parquet`** là đầu vào cho tất cả các notebooks tiếp theo
- **Nhãn `aqi_class`** được sử dụng cho các bài toán Classification và Semi-supervised Learning
- **Lag features** được sử dụng cho các bài toán Time Series và Regression

---

## 🔗 Notebooks liên quan

- **Tiếp theo:** [02_semi_dataset_preparation.md](02_semi_dataset_preparation.md) - Chuẩn bị dữ liệu cho Semi-supervised Learning
