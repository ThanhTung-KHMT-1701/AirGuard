# 09 — Semi-supervised Learning Report

## 🎯 Mục tiêu chính

Đây là notebook **cuối cùng và quan trọng nhất** của luồng thí nghiệm. Nó đóng vai trò là một **báo cáo tổng kết**, nơi tất cả các kết quả từ các phương pháp khác nhau được hội tụ, so sánh và trực quan hóa.

Mục tiêu chính của notebook này là:
1.  **Tổng hợp kết quả:** Tải và hợp nhất các file metrics (`.json`) từ các notebook `04` (Self-Training), `05` (Co-Training), và `06` (Supervised Baseline).
2.  **Trực quan hóa so sánh:** Tạo ra các bảng và biểu đồ rõ ràng để so sánh hiệu suất (chủ yếu là `f1_macro`) giữa các phương pháp.
3.  **Rút ra kết luận:** Dựa trên các bằng chứng từ dữ liệu, đưa ra kết luận cuối cùng cho câu hỏi nghiên cứu của dự án:
    > "Liệu các phương pháp học bán giám sát có thực sự cải thiện hiệu suất dự báo chất lượng không khí khi đối mặt với tình trạng thiếu nhãn hay không? Và nếu có, phương pháp nào là tốt nhất?"

---

## 📥 Đầu vào (Input)

Notebook này không xử lý dữ liệu thô, mà "tiêu thụ" kết quả của các notebook khác.

| File | Được tạo ra từ | Mô tả |
| :--- | :--- | :--- |
| `data/processed/06_metrics_classification.json` | Notebook `06` | **Baseline:** Kết quả của mô hình Supervised. |
| `data/processed/04_metrics_self_training.json` | Notebook `04` | Kết quả của mô hình Self-Training. |
| `data/processed/05_metrics_co_training.json` | Notebook `05` | Kết quả của mô hình Co-Training. |

---

## 📤 Đầu ra (Output)

Đầu ra của notebook này không phải là file dữ liệu, mà là các **phân tích và trực quan hóa** được hiển thị trực tiếp trong notebook.

| Loại đầu ra | Mô tả |
| :--- | :--- |
| **Bảng so sánh tổng hợp** | Một DataFrame hiển thị các chỉ số chính (`accuracy`, `f1_macro`) của cả ba phương pháp để dễ dàng so sánh. |
| **Biểu đồ cột so sánh F1-score** | Một biểu đồ cột, trực quan hóa `f1_macro` của từng phương pháp, giúp làm nổi bật phương pháp nào là tốt nhất. |
| **Biểu đồ so sánh F1-score theo từng lớp** | Biểu đồ chi tiết hơn, so sánh hiệu suất của từng phương pháp trên mỗi lớp AQI (`Good`, `Moderate`...). Điều này giúp tìm ra điểm mạnh, điểm yếu của từng mô hình. |
| **Kết luận cuối cùng** | Một đoạn văn bản tổng kết lại toàn bộ kết quả và trả lời câu hỏi nghiên cứu. |

---

## 🔬 Phân tích và kết luận (Dựa trên kết quả thực tế)

Notebook này sẽ tự động hóa việc tạo ra các phân tích sau:

### 1. Bảng so sánh hiệu suất tổng thể

| Phương pháp | f1_macro (trên Test Set) | So với Baseline |
| :--- | :--- | :--- |
| **Supervised (Baseline)** | 0.472 | - |
| **Self-Training** | **0.534** | **+13.1%** |
| **Co-Training** | 0.404 | -14.4% |

### 2. Biểu đồ so sánh

Biểu đồ sẽ trực quan hóa bảng trên, cho thấy cột **Self-Training** cao hơn đáng kể so với hai cột còn lại, khẳng định đây là phương pháp chiến thắng.

### 3. Kết luận của dự án

Dựa trên tất cả các bằng chứng, notebook này sẽ giúp bạn rút ra kết luận cuối cùng:
> Trong khuôn khổ của dự án này, với bộ dữ liệu và cấu hình đã cho, phương pháp **Self-Training đã chứng tỏ được hiệu quả vượt trội**. Nó đã thành công trong việc tận dụng một lượng lớn dữ liệu không nhãn để cải thiện đáng kể hiệu suất so với mô hình Supervised Baseline. Ngược lại, phương pháp Co-Training với cách chia "view" tự động đã không mang lại hiệu quả như kỳ vọng.

---

## 🔗 Notebooks liên quan

Notebook này là điểm đến cuối cùng của luồng phân tích phân loại.

- **Nguồn dữ liệu từ:** [04_semi_self_training.md](./04_semi_self_training.md), [05_semi_co_training.md](./05_semi_co_training.md), [06_classification_modelling.md](./06_classification_modelling.md)
- **Các nhánh song song:** [07_regression_modelling.md](./07_regression_modelling.md), [08_arima_forecasting.md](./08_arima_forecasting.md)
