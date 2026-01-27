# 03 — Feature Preparation for Supervised Learning

## 🎯 Mục tiêu chính

Notebook này đóng vai trò chuẩn bị dữ liệu **CHỈ** cho các mô hình **Supervised Learning** (Học có giám sát). Các bước chính bao gồm:

1.  **Lọc dữ liệu có nhãn:** Từ bộ dữ liệu semi-supervised, chỉ giữ lại những dòng có nhãn (`is_labeled == True`) trong tập TRAIN. Tập TEST được giữ nguyên.
2.  **Xây dựng Pipeline:** Tạo một pipeline tiền xử lý bằng `scikit-learn` để xử lý các loại dữ liệu khác nhau (số, phân loại).
3.  **Biến đổi dữ liệu:** Áp dụng pipeline lên dữ liệu để tạo ra các ma trận features sẵn sàng cho việc huấn luyện.
4.  **Lưu kết quả:** Lưu lại các ma trận features, target, tên features, và cả pipeline đã được huấn luyện.

---

## 📥 Đầu vào (Input)

| File | Mô tả |
| :--- | :--- |
| `data/processed/02_dataset_for_semi.parquet` | Bộ dữ liệu từ bước 02, chứa cả dữ liệu có nhãn và không nhãn. |

---

## 📤 Đầu ra (Output)

| File | Mô tả |
| :--- | :--- |
| `data/processed/03_features_for_classification.npz` | Ma trận features (`X_train`, `X_test`) và target (`y_train`, `y_test`) cho bài toán **phân loại** (`aqi_class`). |
| `data/processed/03_features_for_regression.npz` | Ma trận features (`X_train`, `X_test`) và target (`y_train`, `y_test`) cho bài toán **hồi quy** (dự đoán `pm25_24h`). |
| `data/processed/03_feature_names.json` | Danh sách tên các cột feature sau khi đã được biến đổi (ví dụ sau one-hot encoding). |
| `data/processed/03_pipeline.joblib` | Đối tượng pipeline của `scikit-learn` đã được `fit` trên tập TRAIN, sẵn sàng để `transform` dữ liệu mới. |

---

## 🔄 Quy trình xử lý

```
┌───────────────────────────────────────────────┐
│ 1. Load Data                                  │
│    pd.read_parquet(02_dataset_for_semi.parquet)│
└───────────────────────────────────────────────┘
                     |
                     ▼
┌───────────────────────────────────────────────┐
│ 2. Filter Labeled Data                        │
│    - Giữ lại toàn bộ tập TEST                 │
│    - Giữ lại dòng is_labeled == True trong TRAIN│
└───────────────────────────────────────────────┘
                     |
                     ▼
┌───────────────────────────────────────────────┐
│ 3. Build Preprocessing Pipeline               │
│    - Numeric: SimpleImputer(median)           │
│    - Categorical: SimpleImputer(most_frequent)│
│                   + OneHotEncoder             │
└───────────────────────────────────────────────┘
                     |
                     ▼
┌───────────────────────────────────────────────┐
│ 4. Fit & Transform Data                       │
│    pipeline.fit_transform(X_train)            │
│    pipeline.transform(X_test)                 │
└───────────────────────────────────────────────┘
                     |
                     ▼
┌───────────────────────────────────────────────┐
│ 5. Save Outputs                               │
│    → .npz, .json, .joblib                     │
└───────────────────────────────────────────────┘
```

---

## ⚠️ Lưu ý quan trọng: Loại bỏ Data Leakage

Trước khi huấn luyện pipeline, các cột sau sẽ bị **loại bỏ** khỏi tập features (`X`) để tránh rò rỉ dữ liệu (data leakage):
- `is_labeled`: Không còn cần thiết sau khi đã lọc.
- `PM2.5`: Giá trị PM2.5 tại thời điểm `t`.
- `pm25_24h`: Target của bài toán hồi quy, không thể dùng làm feature.
- `aqi_class`: Target của bài toán phân loại, không thể dùng làm feature.
- `datetime`: Thông tin đã được trích xuất ra các cột `year`, `month`, `hour`...

Mục tiêu là dự đoán chất lượng không khí dựa trên các **thuộc tính thời gian và các giá trị lag**, chứ không phải dựa vào chính giá trị PM2.5 tại thời điểm đó.

---

## 💡 Ý nghĩa trong dự án

Notebook này tạo ra một bộ dữ liệu "chuẩn" cho các mô hình Supervised Learning. Kết quả từ việc huấn luyện trên bộ dữ liệu này sẽ được dùng làm **đường cơ sở (baseline)**.

- **Baseline:** Là một thước đo hiệu suất tiêu chuẩn.
- **Mục đích so sánh:** Chúng ta sẽ so sánh kết quả của các mô hình Semi-supervised Learning (ở notebook 04, 05) với baseline này.
- **Câu hỏi cần trả lời:** "Liệu việc tận dụng thêm 95% dữ liệu không nhãn có thực sự giúp mô hình Semi-supervised vượt qua được baseline của mô hình Supervised (chỉ dùng 5% dữ liệu có nhãn) hay không?"

---

## 🔗 Notebooks liên quan

- **Trước đó:** [02_semi_dataset_preparation.md](./02_semi_dataset_preparation.md)
- **Tiếp theo:**
  - [06_classification_modelling.md](./06_classification_modelling.md)
  - `07_regression_modelling.ipynb`
