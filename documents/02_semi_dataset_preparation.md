# 02 — Semi-supervised Dataset Preparation

## 🎯 Mục tiêu chính

Notebook này chuẩn bị bộ dữ liệu cho **Semi-supervised Learning** (Học bán giám sát), với 2 nhiệm vụ:

1. **Giữ lại dữ liệu chưa có nhãn AQI** (`aqi_class = NaN`) để dùng cho các thuật toán self-training/co-training
2. **Giả lập tình huống thiếu nhãn** trong tập TRAIN theo phương pháp time-aware (có ý thức về thời gian)

---

## 📥 Đầu vào (Input)

| Tham số | Giá trị mặc định | Mô tả |
|---------|------------------|-------|
| `CLEANED_PATH` | `data/processed/01_cleaned.parquet` | File dữ liệu đã được làm sạch từ bước 01 |
| `CUTOFF` | `2017-01-01` | Ngày phân chia TRAIN/TEST (trước cutoff = TRAIN, sau = TEST) |
| `LABEL_MISSING_FRACTION` | `0.95` | **95% dữ liệu TRAIN bị ẩn nhãn**, chỉ 5% có nhãn |
| `RANDOM_STATE` | `42` | Seed để tái tạo kết quả |

---

## 📤 Đầu ra (Output)

| File | Mô tả |
|------|-------|
| `data/processed/02_dataset_for_semi.parquet` | **Dataset chính** cho semi-supervised learning |
| `data/processed/02_dataset_for_semi_sample.csv` | Mẫu 500 dòng đầu tiên (để xem nhanh) |

---

## 🔄 Quy trình xử lý

```
┌─────────────────────────────────────────────────────────────────┐
│  1. Load Cleaned Data                                            │
│     pd.read_parquet(01_cleaned.parquet)                         │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  2. Configure Semi-supervised Settings                           │
│     SemiDataConfig(cutoff, random_state)                        │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  3. Mask Labels (Time-aware)                                     │
│     mask_labels_time_aware(df, cfg, missing_fraction=0.95)      │
│     - TRAIN (before cutoff): Che 95% nhãn                       │
│     - TEST (after cutoff): Giữ nguyên 100% nhãn                 │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  4. Add is_labeled Column                                        │
│     is_labeled = True nếu có nhãn, False nếu bị che             │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  5. Save Output                                                  │
│     → 02_dataset_for_semi.parquet                               │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📊 Cột dữ liệu quan trọng được thêm

| Cột | Kiểu | Mô tả |
|-----|------|-------|
| `is_labeled` | `bool` | `True` nếu dòng có nhãn, `False` nếu nhãn bị che (masked) |

---

## 📈 Thống kê kỳ vọng

Với `LABEL_MISSING_FRACTION = 0.95`:

| Tập dữ liệu | Tỷ lệ có nhãn | Mô tả |
|-------------|---------------|-------|
| **TRAIN** (before 2017-01-01) | ~5% | Chỉ 5% dữ liệu có nhãn để huấn luyện |
| **TEST** (after 2017-01-01) | 100% | Toàn bộ dữ liệu test có nhãn để đánh giá |

---

## 💡 Ý nghĩa trong dự án

Notebook này tạo điều kiện để thử nghiệm các thuật toán **Semi-supervised Learning**:

### Tại sao cần giả lập thiếu nhãn?

Trong thực tế, việc gán nhãn chất lượng không khí (AQI class) đòi hỏi:
- Chuyên gia môi trường đánh giá
- Chi phí và thời gian đáng kể

Do đó, thường chỉ có **một phần nhỏ dữ liệu được gán nhãn**, phần còn lại không có nhãn.

### Semi-supervised Learning giải quyết vấn đề gì?

Các thuật toán semi-supervised sẽ:
1. **Học từ 5% dữ liệu có nhãn** (labeled data)
2. **Tận dụng 95% dữ liệu không nhãn** (unlabeled data) để cải thiện mô hình
3. **Tự động gán nhãn** cho dữ liệu chưa có nhãn (pseudo-labeling)

---

## 🔗 Notebooks liên quan

- **Trước đó:** [01_preprocessing_and_eda.md](./01_preprocessing_and_eda.md) - Tiền xử lý và EDA
- **Tiếp theo (nhánh Supervised):** [03_feature_preparation.md](./03_feature_preparation.md) - Chuẩn bị features cho Supervised Learning
- **Tiếp theo (nhánh Semi-supervised):** 
  - [04_semi_self_training.md](./04_semi_self_training.md) - Self-training algorithm
  - `05_semi_co_training.ipynb` - Co-training algorithm
