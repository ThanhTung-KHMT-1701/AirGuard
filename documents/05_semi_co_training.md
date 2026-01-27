# 05 — Semi-supervised AQI Classification — Co-Training

## 🎯 Mục tiêu chính

Notebook này triển khai thuật toán **Co-Training**, một phương pháp học bán giám sát tinh vi hơn Self-Training. Các mục tiêu chính bao gồm:

1.  **Tận dụng "Đa góc nhìn" (Multi-view):** Chia bộ features thành hai "góc nhìn" riêng biệt và huấn luyện hai mô hình độc lập trên mỗi góc nhìn.
2.  **Học hỏi lẫn nhau:** Cho phép hai mô hình tự "dạy" cho nhau bằng cách trao đổi các nhãn giả (pseudo-labels) mà chúng tự tin nhất.
3.  **Đánh giá và so sánh:** So sánh hiệu quả của Co-Training với Self-Training và baseline Supervised để xác định phương pháp tiếp cận tốt nhất.

---

## 📥 Đầu vào (Input)

| Tham số | Giá trị thực tế | Mô tả |
| :--- | :--- | :--- |
| **`SEMI_DATASET_PATH`** | `data/processed/02_dataset_for_semi.parquet` | Bộ dữ liệu chứa cả dữ liệu có nhãn và không có nhãn. |
| **`CUTOFF`** | `2017-01-01` | Mốc thời gian phân chia tập Train / Test. |
| **`TAU`** | `0.90` | Ngưỡng tin cậy để một mô hình đề xuất nhãn giả. |
| **`MAX_NEW_PER_ITER`** | `500` | Giới hạn số lượng nhãn giả mới được thêm vào mỗi vòng lặp. |
| **`VIEW1_COLS`, `VIEW2_COLS`**| `None` | **Tự động phân chia features** thành 2 "góc nhìn". |

---

## 📤 Đầu ra (Output)

| File | Mô tả |
| :--- | :--- |
| `data/processed/05_metrics_co_training.json` | File JSON chứa toàn bộ kết quả, cấu hình, và lịch sử huấn luyện. |
| `data/processed/05_predictions_co_training_sample.csv` | Mẫu dự đoán chi tiết trên tập Test. |
| `data/processed/05_alerts_co_training_sample.csv` | Mô phỏng hệ thống cảnh báo dựa trên kết quả. |

---

## 🔄 Quy trình xử lý

1.  **Phân chia Features:** Dữ liệu features được tự động chia thành 2 "góc nhìn" (View 1 và View 2).
    *   **View 1 (Cảm biến & Lag):** Gồm 42 cột như `PM10`, `SO2`, `TEMP_lag1`...
    *   **View 2 (Bối cảnh & Thời gian):** Gồm 10 cột như `station`, `wd`, `hour`, `month`...
2.  **Huấn luyện ban đầu:** Huấn luyện `Mô hình 1` trên `View 1` và `Mô hình 2` trên `View 2`, chỉ sử dụng 5% dữ liệu có nhãn.
3.  **Dạy lẫn nhau (Lặp lại 10 lần):**
    *   Cả hai mô hình cùng dự đoán trên dữ liệu không nhãn.
    *   Chúng trao đổi tối đa 500 nhãn giả tin cậy nhất cho nhau.
    *   Hai mô hình được huấn luyện lại trên tập dữ liệu mới, lớn hơn.
4.  **Dự đoán cuối cùng:** Kết quả trên tập Test được tổng hợp từ dự đoán của cả hai mô hình.

---

## ⚙️ Cơ chế phân chia "View" tự động

Khi `VIEW1_COLS` và `VIEW2_COLS` được để là `None`, chương trình sẽ tự động chia các features thành 2 "góc nhìn" dựa vào một bộ quy tắc được định nghĩa sẵn.

### Quy tắc phân chia
Hàm `make_default_views` trong thư viện sẽ thực hiện việc này:
1.  **Xác định View 2 (Bối cảnh & Thời gian):** Chương trình tìm tất cả các cột có tên chứa các từ khóa như: `"station"`, `"wd"`, `"hour_"`, `"dow"`, `"month"`, `"year"`. Đây được coi là các feature về bối cảnh.
2.  **Xác định View 1 (Cảm biến & Lag):** View 1 được định nghĩa là tất cả các cột features còn lại không thuộc View 2. Đây chủ yếu là các giá trị đo lường từ cảm biến và các giá trị lag.

### Vị trí trong dự án
Bạn có thể xem chi tiết logic của hàm này tại file : [semi_supervised_library.py](../src/semi_supervised_library.py)

![FeaturesToViews](../.images/CoTraining_FeaturesToViews.png)

---

## 🔬 Phân tích kết quả thực tế

### 1. Nhật ký quá trình học (`history`)

Quá trình học của Co-Training diễn ra rất **ổn định và có kiểm soát**.

| Vòng lặp (iter) | Nhãn giả mới (new_pseudo) | F1-score (val_f1_macro) | Phân tích |
| :--- | :--- | :--- | :--- |
| **1-10** | **500** (không đổi) | **~0.64 - 0.67** | **Học tập đều đặn:** Do bị giới hạn, mỗi vòng lặp thuật toán chỉ thêm đúng 500 nhãn giả. Quá trình học diễn ra từ từ, không có sự "bùng nổ" như Self-Training. Hiệu suất trên tập validation đạt đỉnh **0.674** ở vòng 2 và khá ổn định sau đó. |

### 2. Kết quả cuối cùng và so sánh (`test_metrics`)

Đây là "bảng điểm" cuối cùng của Co-Training, so sánh trực tiếp với Self-Training.

| Chỉ số | Co-Training (Hiện tại) | Self-Training (Trước đó) | Nhận xét |
| :--- | :--- | :--- | :--- |
| **`accuracy`** | `0.534` | `0.589` | 🔻 Thấp hơn |
| **`f1_macro`** | **`0.404`** | **`0.534`** | **🔻 Kém hiệu quả hơn đáng kể** |

> **Kết luận:** Với cấu hình mặc định, **Self-Training là phương pháp vượt trội hơn**.

### 3. Phân tích sâu hơn với Ma trận nhầm lẫn (`confusion_matrix`)

Ma trận nhầm lẫn từ file `metrics.json` đã chỉ ra **lý do chính** khiến Co-Training hoạt động kém hiệu quả:

```
Labels: [Good, Moderate, Unhealthy_SG, Unhealthy, V.Unhealthy, Hazardous]
...
[  38,    980,          0,         14,            0,           0  ]  <-- Actual is Good
...
[   0,   1489,         50,        608,           19,           0  ]  <-- Actual is Unhealthy_SG
...
```
-   **Thiên vị nghiêm trọng:** Mô hình có xu hướng dự đoán rất nhiều về `Moderate`.
-   **Minh chứng:** Khi thực tế là `Good`, có tới **980 lần** mô hình dự đoán nhầm thành `Moderate`. Tương tự, khi thực tế là `Unhealthy_for_Sensitive_Groups`, có tới **1489 lần** mô hình cũng dự đoán là `Moderate`.
-   **Hậu quả:** Mô hình gần như "mù" với các lớp `Good` và `Unhealthy_for_Sensitive_Groups`, dẫn đến F1-score tổng thể (`f1_macro`) bị kéo xuống rất thấp.

### 4. Minh chứng từ dữ liệu thực tế

Mặc dù hiệu suất tổng thể không cao, mô hình vẫn hoạt động tốt trong các tình huống cụ thể.

**Dự đoán chính xác các mức độ cực đoan (`predictions_sample.csv`):**
```csv
datetime,station,y_true,y_pred
2017-01-01 00:00:00,Aotizhongxin,Hazardous,Hazardous
2017-01-01 01:00:00,Aotizhongxin,Hazardous,Hazardous
```
> Giống như Self-Training, Co-Training nhận diện rất tốt các mức độ nguy hiểm cao nhất.

---

## 💡 Ý nghĩa trong dự án

-   **Một kết quả giá trị:** Thí nghiệm đã cho thấy Co-Training, mặc dù là một thuật toán tinh vi, nhưng không phải lúc nào cũng tốt hơn. Trong trường hợp này, việc **chia features thành 2 view có thể đã làm mất đi sự tương quan quan trọng**, khiến các mô hình hoạt động kém hiệu quả.
-   **Bài học kinh nghiệm:** Sự thành công của Co-Training phụ thuộc rất nhiều vào việc **lựa chọn "góc nhìn" (views)**. Có thể một cách phân chia khác (ví dụ: tự tay chọn các cột) sẽ cho kết quả tốt hơn.
-   **Hoàn thiện báo cáo:** Kết quả này cung cấp một sự so sánh rất giá trị cho báo cáo cuối cùng (`09_semi_supervised_report.ipynb`), cho thấy Self-Training là lựa chọn tốt hơn cho bộ dữ liệu này.

---

## 🔗 Notebooks liên quan

- **Trước đó:** [04_semi_self_training.md](./04_semi_self_training.md)
- **Baseline để so sánh:** `06_classification_modelling.ipynb`
- **Tổng hợp kết quả:** [09_semi_supervised_report.md](./09_semi_supervised_report.md)
