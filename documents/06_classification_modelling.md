# Tài liệu: 06 - Xây dựng mô hình phân loại (Baseline)

## 🎯 Mục tiêu

Notebook này giữ một vai trò cực kỳ quan trọng: **thiết lập một đường cơ sở (Baseline) về hiệu suất cho bài toán phân loại AQI.**

Chúng ta sẽ huấn luyện và đánh giá một mô hình học có giám sát tiêu chuẩn (`HistGradientBoostingClassifier`) chỉ trên một phần nhỏ dữ liệu có nhãn (tương đương 5% của tập huấn luyện).

Mục đích là để trả lời câu hỏi:
> "Với lượng dữ liệu có nhãn hạn chế, hiệu suất tốt nhất mà một mô hình tiêu chuẩn có thể đạt được là bao nhiêu?"

Kết quả này sẽ trở thành **thước đo tiêu chuẩn** để so sánh và khẳng định giá trị của các phương pháp học bán giám sát được thử nghiệm ở các bước khác.

---

## 🔬 Phân tích kết quả

### 1. Hiệu suất tổng thể: Baseline đã được xác định!

Các chỉ số hiệu suất tổng thể trên tập kiểm tra (TEST) đã thiết lập một cột mốc rõ ràng.

| Chỉ số         | Giá trị     | Ý nghĩa                                                                 |
| :------------- | :---------- | :---------------------------------------------------------------------- |
| `Accuracy`     | 0.602       | Khoảng 60.2% dự đoán của mô hình là chính xác.                          |
| **`f1_macro`** | **0.472**   | **Đây là Baseline!** F1-score trung bình, xét đến sự mất cân bằng, là 0.472. |

`f1_macro` là chỉ số quan trọng hơn vì nó đánh giá khả năng của mô hình trên tất cả các lớp một cách công bằng, không bị ảnh hưởng bởi số lượng mẫu của mỗi lớp.

### 2. Phân tích sâu với ma trận nhầm lẫn

Ma trận nhầm lẫn cho chúng ta thấy chi tiết về các loại lỗi mà mô hình đang mắc phải.

![Ma trận nhầm lẫn của mô hình Baseline](../images/06_confusion_matrix.png)
*Hình 1: Trực quan hóa ma trận nhầm lẫn. Các ô trên đường chéo chính thể hiện số lượng dự đoán đúng.*

- **Điểm mạnh**: Mô hình hoạt động rất tốt với các lớp đa số như `Moderate` (4173 dự đoán đúng) và `Unhealthy for Sensitive Groups` (3663 dự đoán đúng). Đây là lý do tại sao `Accuracy` tương đối cao.
- **Điểm yếu chí mạng**:
    - **Hoàn toàn "bỏ lỡ" lớp `Good`**: Hàng đầu tiên của ma trận cho thấy, trong số 1032 mẫu thực sự là `Good`, không có mẫu nào được dự đoán đúng (số 0 ở ô đầu tiên). Thay vào đó, mô hình đã nhầm lẫn gần như toàn bộ (1012 mẫu) sang lớp `Moderate`.
    - **Nhầm lẫn giữa các lớp liền kề**: Có sự nhầm lẫn đáng kể giữa các lớp có mức độ ô nhiễm gần nhau, ví dụ `Unhealthy` và `Very Unhealthy`.

### 3. Báo cáo phân loại chi tiết (`Classification Report`)

Bảng báo cáo này cung cấp cái nhìn chi tiết về hiệu suất trên từng lớp riêng biệt.

| Lớp                              | precision | recall | **f1-score** | support |
| :------------------------------- | :-------- | :----- | :----------- | :------ |
| Good                             | 0.00      | 0.00   | **0.00**     | 1032    |
| Moderate                         | 0.57      | 0.77   | 0.66         | 5422    |
| Unhealthy_for_Sensitive_Groups   | 0.62      | 0.81   | 0.70         | 4539    |
| Unhealthy                        | 0.59      | 0.52   | 0.55         | 3060    |
| Very_Unhealthy                   | 0.55      | 0.42   | 0.48         | 1083    |
| Hazardous                        | 0.71      | 0.23   | 0.35         | 344     |

- **Phân tích**:
    - `f1-score` của lớp `Good` là **0.0**, xác nhận lại rằng mô hình hoàn toàn thất bại với lớp này.
    - `recall` của lớp `Hazardous` rất thấp (0.23), nghĩa là mô hình chỉ phát hiện được 23% các trường hợp thực sự nguy hiểm. Đây là một rủi ro lớn trong ứng dụng thực tế.
    - Các lớp ở giữa (`Moderate`, `Unhealthy_...`) có F1-score tốt hơn nhiều, phản ánh sự mất cân bằng trong dữ liệu huấn luyện.

---

## 💾 Kết quả đầu ra

| Tệp                                           | Mô tả                                                                                                        |
| :-------------------------------------------- | :----------------------------------------------------------------------------------------------------------- |
| `data/processed/06_metrics.json`              | File JSON chứa các chỉ số hiệu suất tổng thể (Accuracy, F1-macro) trên tập kiểm tra.                          |
| `data/processed/06_classification_report.csv` | Bảng báo cáo phân loại chi tiết, cung cấp Precision, Recall, và F1-score cho từng lớp AQI.                      |
| `data/processed/06_predictions_sample.csv`    | Một mẫu các dự đoán trên tập kiểm tra, giúp so sánh trực tiếp giữa giá trị thực tế (`y_true`) và dự đoán (`y_pred`). |

---

## 💡 Kết luận

- Notebook này đã thành công trong việc thiết lập một **baseline định lượng được (f1_macro: 0.472)**.
- Phân tích chi tiết đã chỉ ra rõ ràng điểm yếu của mô hình baseline: nó hoạt động tốt trên các lớp phổ biến nhưng lại **hoàn toàn thất bại trên các lớp thiểu số quan trọng**.
- Kết quả này tạo ra một tiền đề vững chắc để chứng minh giá trị của các kỹ thuật học bán giám sát: liệu chúng có thể cải thiện được những điểm yếu này bằng cách học từ dữ liệu không nhãn hay không.
- **So sánh với:** [04_semi_self_training.md](./04_semi_self_training.md), [05_semi_co_training.md](./05_semi_co_training.md)
- **Tổng hợp kết quả:** [09_semi_supervised_report.md](./09_semi_supervised_report.md)
