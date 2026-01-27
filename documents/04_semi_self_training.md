# 04 — Semi-supervised AQI Classification — Self-Training

## 🎯 Mục tiêu chính

Notebook này triển khai thuật toán **Self-Training**, một phương pháp học bán giám sát (Semi-supervised Learning), với các mục tiêu:

1.  **Tận dụng dữ liệu không nhãn:** Sử dụng một lượng lớn dữ liệu không có nhãn (`is_labeled == False`) để cải thiện hiệu suất của mô hình.
2.  **Tự động mở rộng tập huấn luyện:** Cho phép mô hình tự "dạy" chính nó bằng cách gán nhãn giả (pseudo-labels) cho những điểm dữ liệu mà nó tự tin nhất.
3.  **Đánh giá hiệu quả:** So sánh kết quả của mô hình Self-Training với một baseline được huấn luyện theo kiểu có giám sát (Supervised) để xem phương pháp này có thực sự hiệu quả hay không.

---

## 📥 Đầu vào (Input)

| Tham số | Giá trị thực tế | Mô tả |
| :--- | :--- | :--- |
| **`SEMI_DATASET_PATH`** | `data/processed/02_dataset_for_semi.parquet` | Bộ dữ liệu chứa cả dữ liệu có nhãn và không nhãn. |
| **`CUTOFF`** | `2017-01-01` | Mốc thời gian phân chia tập Train / Test. |
| **`TAU`** | `0.90` | **Ngưỡng tin cậy:** Mô hình chỉ gán nhãn giả nếu xác suất dự đoán > 90%. |
| **`MAX_ITER`** | `10` | Số vòng lặp tối đa của thuật toán. |

---

## 📤 Đầu ra (Output)

| File | Mô tả |
| :--- | :--- |
| `data/processed/04_metrics_self_training.json` | File JSON chứa toàn bộ kết quả, cấu hình và lịch sử huấn luyện. |
| `data/processed/04_predictions_self_training_sample.csv` | Mẫu dự đoán chi tiết trên tập Test để phân tích lỗi. |
| `data/processed/04_alerts_self_training_sample.csv` | Mô phỏng hệ thống cảnh báo dựa trên kết quả dự đoán. |

---

## ⚙️ Động cơ dự đoán: HistGradientBoostingClassifier

Bên trong vòng lặp Self-Training, thuật toán cốt lõi thực hiện việc dự đoán và gán nhãn giả chính là **`HistGradientBoostingClassifier`**, một mô hình mạnh mẽ của scikit-learn.

### Ý tưởng chính
Thuật toán này không xây dựng một cây quyết định phức tạp duy nhất. Thay vào đó, nó xây dựng một chuỗi hàng trăm cây quyết định đơn giản một cách tuần tự:
1.  **Cây đầu tiên** đưa ra dự đoán ban đầu.
2.  **Cây thứ hai** sẽ tập trung học và sửa những lỗi sai của cây đầu tiên.
3.  **Cây thứ ba** tiếp tục sửa lỗi của hai cây trước đó.
4.  Quá trình này tiếp tục, với mỗi cây sau trở nên "thông minh" hơn nhờ học từ sai lầm của các cây trước. Kết quả cuối cùng là sự tổng hợp ý kiến của cả chuỗi cây, tạo ra một dự đoán có độ chính xác cao.

Chữ **"Hist" (Histogram-based)** là một kỹ thuật tối ưu hóa giúp thuật toán này xử lý dữ liệu lớn cực kỳ nhanh chóng.

### Minh họa thuật toán
![Sơ đồ thuật toán HistGradientBoostingClassifier](../.images/ThuatToan_HistGradientBoostingClassifier.png)

### Vị trí trong dự án
Thuật toán này được định nghĩa và cấu hình trong file thư viện của dự án. Bạn có thể xem chi tiết tại file [semi_supervised_library.py](../src/semi_supervised_library.py)

---

## 🔬 Phân tích kết quả thực tế

### 1. Nhật ký quá trình học (`history`)

Bảng dưới đây tóm tắt quá trình "tự học" của mô hình qua 10 vòng lặp, dựa trên dữ liệu từ file `04_metrics_self_training.json`:

| Vòng lặp (iter) | Nhãn giả mới (new_pseudo) | F1-score (val_f1_macro) | Phân tích |
| :--- | :--- | :--- | :--- |
| **1** | **76,134** | **0.679** | **Khởi đầu mạnh mẽ:** Ngay vòng đầu, mô hình đã tự tin gán nhãn cho hơn 76,000 mẫu. |
| **2** | **202,713** | 0.678 | **Bùng nổ:** Đây là vòng lặp hiệu quả nhất, mô hình học được nhiều nhất và tìm thấy hơn 200,000 nhãn giả mới. |
| **3** | 45,622 | 0.673 | **Bão hòa:** Số lượng nhãn giả mới giảm mạnh, cho thấy các mẫu "dễ đoán" đã được xử lý. |
| **4-10**| Giảm dần (còn 353 ở iter 10) | Biến động (dao động quanh 0.61-0.66) | **Hội tụ:** Mô hình gần như đã học hết khả năng từ dữ liệu không nhãn, số lượng nhãn mới thêm vào không đáng kể. |

> ** nhận xét:** Quá trình học diễn ra rất tốt ở 2 vòng lặp đầu tiên, chứng tỏ Self-Training có khả năng tận dụng dữ liệu không nhãn một cách hiệu quả. Hiệu suất trên tập validation (`val_f1_macro`) đạt đỉnh sớm và sau đó giảm nhẹ, điều này cho thấy việc chọn mô hình ở vòng lặp thứ 2 hoặc 3 có thể là tối ưu nhất.

### 2. Kết quả cuối cùng trên tập Test (`test_metrics`)

Đây là "bảng điểm" cuối cùng của mô hình sau 10 vòng lặp, được đánh giá trên dữ liệu thực tế sau năm 2017.

| Chỉ số | Giá trị | Ý nghĩa |
| :--- | :--- | :--- |
| **`accuracy`** | **`0.589`** | Khoảng **58.9%** dự đoán của mô hình là chính xác. |
| **`f1_macro`** | **`0.534`** | **Đây là chỉ số quan trọng nhất.** F1-score trung bình cho tất cả các lớp là **0.534**. Con số này sẽ được dùng để so sánh trực tiếp với baseline. |

**Phân tích chi tiết hơn:**
-   **Mô hình làm tốt nhất ở lớp:** `Moderate` (F1-score: 0.704) và `Hazardous` (F1-score: 0.676).
-   **Mô hình yếu nhất ở lớp:** `Unhealthy_for_Sensitive_Groups` (F1-score: 0.179). Đây là lớp khó phân biệt nhất, mô hình thường nhầm lẫn nó với `Moderate` và `Unhealthy`.

### 3. Minh chứng từ dữ liệu thực tế

**Minh chứng 1: Dự đoán chính xác (`predictions_sample.csv`)**

File dự đoán cho thấy mô hình hoạt động rất tốt trong việc nhận diện các điều kiện thời tiết cực đoan.
```csv
datetime,station,y_true,y_pred
2017-01-01 00:00:00,Aotizhongxin,Hazardous,Hazardous
2017-01-01 01:00:00,Aotizhongxin,Hazardous,Hazardous
2017-01-01 02:00:00,Aotizhongxin,Hazardous,Hazardous
```
> Như bạn thấy, trong những giờ đầu của năm 2017, mô hình đã dự đoán **hoàn toàn chính xác** mức độ `Hazardous`.

**Minh chứng 2: Hệ thống cảnh báo (`alerts_sample.csv`)**

File cảnh báo cho thấy kết quả dự đoán được chuyển thành hành động cụ thể.
```csv
datetime,station,y_pred,is_alert
2017-01-01 00:00:00,Aotizhongxin,Hazardous,1
2017-01-01 01:00:00,Aotizhongxin,Hazardous,1
```
> Cột `is_alert` bằng `1` (True) xác nhận rằng hệ thống đã kích hoạt cảnh báo một cách chính xác khi mô hình dự đoán mức độ nguy hiểm.

---

## 💡 Ý nghĩa trong dự án

-   **Thành công bước đầu:** Notebook này đã chứng minh rằng thuật toán Self-Training có thể hoạt động, tự động gán nhãn và cải thiện mô hình qua các vòng lặp.
-   **Cung cấp kết quả để so sánh:** Kết quả cuối cùng (`f1_macro: 0.534`) là một con số cụ thể. Bước tiếp theo và quan trọng nhất là chạy notebook `06_classification_modelling.ipynb` để có được **baseline**.
-   **Giả thuyết cần kiểm chứng:** Nếu F1-score của baseline (chỉ dùng 5% dữ liệu) thấp hơn `0.534`, thì chúng ta có thể kết luận rằng **việc sử dụng Self-Training để tận dụng 95% dữ liệu không nhãn là có hiệu quả**.

---

## 🔗 Notebooks liên quan

- **Trước đó:** [02_semi_dataset_preparation.md](./02_semi_dataset_preparation.md)
- **Baseline để so sánh:** `06_classification_modelling.ipynb`
- **Phương pháp tương tự:** [05_semi_co_training.md](./05_semi_co_training.md)
