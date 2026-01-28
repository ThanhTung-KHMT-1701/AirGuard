# AirGuard: Beijing Air Quality Monitoring & Prediction System

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE.txt)
[![Status](https://img.shields.io/badge/Status-Active-success.svg)]()

**AirGuard** là một hệ thống end-to-end pipeline phân tích và dự báo chất lượng không khí tại Bắc Kinh (Beijing), sử dụng dữ liệu từ 12 trạm quan trắc. Dự án tập trung vào ba mục tiêu chính:

1. 🎯 **Dự báo PM2.5** - Regression & ARIMA time series forecasting
2. 🚨 **Phân loại AQI** - Multi-class classification cho 6 levels (Good → Hazardous)
3. 🤖 **Semi-supervised Learning** - Cải thiện model khi thiếu labeled data

---

## 📋 Mục lục

- [Tổng quan dự án](#-tổng-quan-dự-án)
  - [Key insights](#-key-insights)
  - [Kết quả chính](#-kết-quả-chính)
- [Cấu trúc dự án](#-cấu-trúc-dự-án)
- [Dataset](#-dataset)
- [Cài đặt môi trường](#-cài-đặt-môi-trường)
- [Pipeline notebooks](#-pipeline-notebooks)
- [Kết quả chi tiết](#-kết-quả-chi-tiết)
  - [1. Classification baseline](#1-classification-baseline-supervised-learning)
  - [2. Regression PM2.5](#2-regression-pm25-prediction)
  - [3. ARIMA forecasting](#3-arima-time-series-forecasting)
  - [4. Semi-supervised methods](#4-semi-supervised-learning-comparison)
- [Documentation](#-documentation)
- [Chạy pipeline](#-chạy-pipeline)
- [Bài học và insights](#-bài-học-và-insights)
- [Tác giả](#-tác-giả)
- [License](#-license)

---

## 🌟 Tổng quan dự án

### 🔑 Key Insights

Sau khi thử nghiệm toàn diện với **6 phương pháp machine learning** (1 supervised baseline + 5 semi-supervised), chúng tôi rút ra những insights quan trọng sau:

#### 1. Semi-supervised Learning hiệu quả với labeled data ít

| Method | F1-Macro | Improvement vs Baseline | Use Case |
|--------|----------|------------------------|----------|
| **Supervised Baseline** | 0.472 | - | Baseline reference |
| **Self-Training** | 0.680 | **+44.1%** | ✅ General purpose, scalable |
| **Co-Training** | 0.710 | **+50.4%** | ✅ Best với 2 independent views |
| **Label Propagation** | 0.860* | **+82.2%** | ✅ Small data, binary only |
| **Label Spreading** | 0.870* | **+84.3%** | ✅ Best accuracy, binary only |
| **Dynamic Threshold** | 0.685 | **+45.1%** | ✅ Best cho imbalanced data |

\*Graph-based methods sử dụng binary classification (Healthy vs Unhealthy)

#### 2. Model confidence ảnh hưởng lớn đến SSL performance

**Phát hiện quan trọng**:
- HistGradientBoostingClassifier có xu hướng **rất tự tin** (mean confidence ~0.95) trên dữ liệu AQI
- ~62% unlabeled samples có confidence ≥ 0.9
- → Hyperparameter tuning cần phù hợp với confidence distribution

![Confidence Distribution](images/13_DEBUG_confidence_distribution.png)

*Hình 1: Phân bố confidence scores cho thấy model rất tự tin (mean=0.95)*

#### 3. Class imbalance cần chiến lược đặc biệt

**Vấn đề**:
- Baseline supervised: F1=0.0 cho class "Good" (hoàn toàn fail)
- Fixed threshold self-training: Thiên lệch về lớp phổ biến (Moderate, Unhealthy)

**Giải pháp**:
- **Dynamic Threshold** (FlexMatch approach): +15.4% recall cho class "Hazardous"
- Class-specific threshold: τ_c = max(τ_base, p_model(c) / p_data(c))

![Dynamic Threshold Comparison](images/13_01_f1_macro_comparison.png)

*Hình 2: Dynamic Threshold cải thiện F1-macro và recall cho lớp hiếm*

#### 4. Graph-based SSL: Accuracy cao nhưng không scalable

**Ưu điểm**:
- Accuracy cao nhất: F1-macro = 0.87 (+84% vs baseline)
- Không cần iterative training
- Theoretical guarantees (convex optimization)

**Hạn chế**:
- Memory intensive: O(n²) similarity matrix
- Chỉ áp dụng được cho binary classification (với dataset này)
- Không scale với >100K samples

#### 5. Trade-offs quan trọng

```
Accuracy ↔ Scalability ↔ Memory ↔ Training Time
```

- **Label Spreading**: Best accuracy, worst scalability
- **Co-Training**: Best label efficiency, 2× training time
- **Self-Training**: Best balance cho production
- **Dynamic Threshold**: Best cho imbalanced & health-critical use case

### 📊 Kết quả chính

#### Classification Performance (Multi-class: 6 AQI levels)

![Method Comparison](images/14_01_f1_macro_comparison.png)

*Hình 3: So sánh F1-macro của 6 phương pháp*

| Metric | Baseline | Self-Training | Co-Training | Dynamic Threshold |
|--------|----------|---------------|-------------|-------------------|
| **Accuracy** | 0.602 | 0.614 | 0.639 | 0.617 |
| **F1-Macro** | 0.472 | 0.680 | 0.710 | 0.685 |
| **Recall (Hazardous)** | 0.54 | 0.60 | 0.65 | **0.70** |
| **Training Time** | 1× | 10× | 20× | 10× |

#### Regression Performance (PM2.5 Prediction)

| Metric | Value | Interpretation |
|--------|-------|----------------|
| **RMSE** | 25.33 μg/m³ | Sai số trung bình ~25 units |
| **MAE** | 12.32 μg/m³ | Sai số tuyệt đối ~12 units |
| **SMAPE** | 23.84% | Sai số phần trăm ~24% |
| **R²** | 0.949 | Model giải thích 94.9% variance |

![Actual vs Predicted PM2.5](images/07_actual_vs_predicted.png)

*Hình 4: PM2.5 thực tế vs dự đoán cho thấy R²=0.949*

#### ARIMA Forecasting (Single Station)

| Metric | Value | Note |
|--------|-------|------|
| **RMSE** | ~28 μg/m³ | Comparable với regression |
| **Forecast Horizon** | 168 hours (7 days) | Weekly ahead prediction |
| **Seasonal Pattern** | Detected | Hourly & daily cycles |

![ARIMA Forecast](images/08_forecast_vs_actual.png)

*Hình 5: ARIMA forecast 7 ngày với confidence intervals*

---

## 🗂️ Cấu trúc dự án

- Nguồn: **Beijing Multi‑Site Air Quality** (12 stations, dữ liệu theo giờ).
- Repo hỗ trợ 2 cách nạp dữ liệu trong notebook `preprocessing_and_eda.ipynb`:
  - **(Khuyến nghị cho lớp học)** dùng file ZIP local:
    - đặt file vào `data/raw/PRSA2017_Data_20130301-20170228.zip`
    - set `USE_UCIMLREPO=False`
  - dùng `ucimlrepo` (nếu notebook có hỗ trợ trong code): set `USE_UCIMLREPO=True`

> Lưu ý “leakage”: **không dùng trực tiếp `PM2.5` / `pm25_24h` trong feature đầu vào cho mô hình phân lớp AQI**.

---

## 2) Cấu trúc thư mục

```
air_quality_timeseries_with_semi/
├─ data/
│  ├─ raw/                # ZIP dữ liệu gốc
│  └─ processed/          # parquet + metrics + predictions + alerts
├─ notebooks/
│  ├─ preprocessing_and_eda.ipynb
│  ├─ feature_preparation.ipynb
│  ├─ classification_modelling.ipynb
│  ├─ regression_modelling.ipynb
│  ├─ arima_forecasting.ipynb
│  ├─ semi_dataset_preparation.ipynb          
│  ├─ semi_self_training.ipynb                
│  ├─ semi_co_training.ipynb                  
│  ├─ semi_supervised_report.ipynb            
│  └─ runs/                                   # output notebooks khi chạy papermill
├─ src/
│  ├─ classification_library.py
│  ├─ regression_library.py
│  ├─ timeseries_library.py
│  └─ semi_supervised_library.py              
├─ run_papermill.py
├─ requirements.txt
└─ README.md
```

---

## 3) Cài đặt môi trường

### 3.1 Tạo môi trường (Conda) và kernel cho Papermill
Repo mặc định chạy papermill với kernel tên **`beijing_env`** (xem `run_papermill.py`).

```bash
conda create -n beijing_env python=3.11 -y
conda activate beijing_env
pip install -r requirements.txt

# đăng ký kernel để Papermill gọi được
python -m ipykernel install --user --name beijing_env --display-name "beijing_env"
```

### 3.2 Kiểm tra nhanh
```bash
python -c "import pandas, sklearn, papermill; print('OK')"
```

---

## 4) Chạy pipeline (Papermill)

Chạy toàn bộ pipeline:

```bash
python run_papermill.py
```

Kết quả:
- Notebook chạy xong sẽ nằm ở `notebooks/runs/*_run.ipynb`
- Artefacts nằm ở `data/processed/` (metrics, predictions, alerts, parquet)

---

## 5) Mô tả pipeline notebooks (Notebook‑per‑task)

| Thứ tự | Notebook | Mục tiêu | Output chính |
|---:|---|---|---|
| 01 | `preprocessing_and_eda.ipynb` | đọc dữ liệu, làm sạch, tạo time features cơ bản | `data/processed/cleaned.parquet` |
| 02 | `semi_dataset_preparation.ipynb` | **giữ dữ liệu chưa nhãn + giả lập thiếu nhãn (train‑only)** | `data/processed/dataset_for_semi.parquet` |
| 03 | `feature_preparation.ipynb` | tạo dataset supervised cho phân lớp | `data/processed/dataset_for_clf.parquet` |
| 04 | `semi_self_training.ipynb` | **Self‑Training** cho AQI classification | `metrics_self_training.json`, `alerts_self_training_sample.csv` |
| 05 | `semi_co_training.ipynb` | **Co‑Training (2 views)** cho AQI classification | `metrics_co_training.json`, `alerts_co_training_sample.csv` |
| 06 | `classification_modelling.ipynb` | baseline supervised classification | `metrics.json`, `predictions_sample.csv` |
| 07 | `regression_modelling.ipynb` | dự báo PM2.5 (regression) | `regression_metrics.json`, `regressor.joblib` |
| 08 | `arima_forecasting.ipynb` | ARIMA forecasting cho 1 trạm | `arima_pm25_*` |
| 09 | `semi_supervised_report.ipynb` | **Storytelling report**: so sánh baseline vs semi + alert theo trạm | notebook report chạy trong `notebooks/runs/` |

---

## 6) Thư viện OOP (src/)

### 6.1 `src/classification_library.py`
- `time_split(df, cutoff)`: chia train/test theo thời gian
- `train_classifier(train_df, test_df, target_col='aqi_class')` → trả về `{model, metrics, pred_df}`
- Guard leakage: loại cột như `PM2.5`, `pm25_24h`, `datetime` khỏi features.

### 6.2 `src/semi_supervised_library.py` 
- `mask_labels_time_aware(...)`: giả lập thiếu nhãn **chỉ trong TRAIN**
- `SelfTrainingAQIClassifier`: vòng lặp pseudo‑label theo ngưỡng `tau`
- `CoTrainingAQIClassifier`: co‑training 2 views + late‑fusion
- `add_alert_columns(...)`: tạo `is_alert` theo ngưỡng mức AQI (vd từ `"Unhealthy"`)

---

## 7) MINI PROJECT: Semi‑Supervised AQI + Alerts theo trạm

### 7.1 Mục tiêu
Xây dựng hệ thống:
- dự đoán `aqi_class` cho từng timestamp/trạm
- sinh **cảnh báo** theo trạm (`is_alert`)
- khi **thiếu nhãn AQI** (hoặc nhãn không chuẩn), dùng **Self‑Training** và **Co‑Training** để cải thiện chất lượng.

### 7.2 Thiết kế thí nghiệm (bắt buộc)
1) **Baseline supervised**  
   - Chạy `classification_modelling.ipynb`  
   - Lấy `accuracy`, `f1_macro` từ `data/processed/metrics.json`

2) **Giả lập thiếu nhãn (train‑only)**  
   - Chạy `semi_dataset_preparation.ipynb` với:
     - `LABEL_MISSING_FRACTION ∈ {0.7, 0.9, 0.95, 0.98}`

3) **Self‑Training**  
   - Chạy `semi_self_training.ipynb` với:
     - `TAU ∈ {0.8, 0.9, 0.95}`
   - Phân tích: vòng lặp nào bắt đầu “bão hoà”, số pseudo‑labels tăng/giảm ra sao.

4) **Co‑Training**  
   - Chạy `semi_co_training.ipynb` với `TAU` giống Self‑Training
   - Bắt buộc thử 2 chế độ:
     - **Auto split views** (để `VIEW1_COLS=None`, `VIEW2_COLS=None`)
     - **Manual views**: tự thiết kế 2 views và giải thích vì sao hợp lý.


## 8) Chạy nhanh từng notebook (không dùng Papermill)
Bạn có thể mở Jupyter và chạy tuần tự từng notebook theo thứ tự ở mục (5).

---

## 9) Author
Project được thực hiện bởi:
Trang Le

## 10) License
MIT — sử dụng tự do cho nghiên cứu, học thuật và ứng dụng nội bộ.
