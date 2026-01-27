# 07 — Regression Modelling (Supervised Baseline)

## 🎯 Mục tiêu chính

Notebook này triển khai một hướng tiếp cận song song cho bài toán dự báo chất lượng không khí: **Hồi quy (Regression)**.

Vai trò chính của nó là thiết lập một **baseline cho bài toán hồi quy**, với mục tiêu:
> Dự đoán trực tiếp **giá trị số** của `pm25_24h` (ví dụ: 15.2, 58.7), thay vì dự đoán nhãn phân loại (`aqi_class`).

Kết quả từ notebook này sẽ được dùng để:
1.  Đánh giá hiệu suất của một mô hình Supervised Learning tiêu chuẩn cho bài toán hồi quy.
2.  So sánh hiệu quả giữa phương pháp Machine Learning (trong notebook này) và phương pháp Thống kê cổ điển (ARIMA trong notebook `08`).

---

## 📥 Đầu vào (Input)

| Tham số | Giá trị thực tế | Mô tả |
| :--- | :--- | :--- |
| **`FEATURES_PATH`** | `data/processed/03_features_for_regression.npz` | **Dữ liệu chính:** File chứa các ma trận features và target (`pm25_24h`) đã được xử lý. |
| **`REGRESSOR`** | `hgboost` | Chỉ định mô hình sử dụng là `HistGradientBoostingRegressor`. |

---

## 📤 Đầu ra (Output)

| File | Mô tả |
| :--- | :--- |
| `data/processed/07_metrics_regression.json` | File JSON chứa "bảng điểm" của mô hình hồi quy, với các chỉ số như `MSE`, `MAE`, `R²`. |
| `data/processed/07_predictions_regression_sample.csv` | Mẫu dự đoán chi tiết trên tập Test, so sánh giá trị `pm25_24h` thực tế (`y_true`) và giá trị dự đoán (`y_pred`). |
| `images/07_regression_predictions.png` | Biểu đồ trực quan hóa, so sánh đường đi của giá trị thực tế và giá trị dự đoán theo thời gian. |

---

## 🔬 Phân tích kết quả (Dựa trên kết quả mẫu nếu có)

*Do chưa có kết quả chạy thực tế, phần này sẽ mô tả cách phân tích khi bạn đã chạy xong notebook.*

### 1. Phân tích các chỉ số (`07_metrics_regression.json`)

-   **`mse` (Mean Squared Error - Sai số bình phương trung bình):** Càng gần 0 càng tốt. Chỉ số này "trừng phạt" các lỗi lớn nặng hơn.
-   **`mae` (Mean Absolute Error - Sai số tuyệt đối trung bình):** Càng gần 0 càng tốt. Cho biết trung bình, dự đoán của mô hình lệch khỏi giá trị thực tế bao nhiêu µg/m³.
-   **`r2` (R-squared - Hệ số xác định):** Càng gần 1 càng tốt. Cho biết mô hình giải thích được bao nhiêu phần trăm sự biến thiên của dữ liệu. Ví dụ, `R² = 0.75` nghĩa là mô hình giải thích được 75% sự thay đổi của `pm25_24h`.

### 2. Phân tích biểu đồ (`07_regression_predictions.png`)

Biểu đồ sẽ vẽ hai đường:
-   **Đường giá trị thực tế (`y_true`):** Thường có màu xanh.
-   **Đường giá trị dự đoán (`y_pred`):** Thường có màu đỏ.

> **Đánh giá:** Hai đường này càng **chồng khít** lên nhau, mô hình dự đoán càng chính xác. Nếu đường màu đỏ có thể "bắt chước" được các đỉnh và đáy của đường màu xanh, điều đó cho thấy mô hình hoạt động tốt trong việc dự báo các biến động mạnh của ô nhiễm.

---

## 💡 Ý nghĩa và mối liên hệ

-   **Baseline cho Hồi quy:** Notebook này thiết lập một thước đo hiệu suất tiêu chuẩn cho bất kỳ mô hình hồi quy nào khác trong tương lai.
-   **Đối thủ của ARIMA:** Kết quả `MSE` từ notebook này sẽ được **so sánh trực tiếp** với kết quả `MSE` của mô hình ARIMA (trong notebook `08`) để xác định phương pháp nào dự báo chuỗi thời gian tốt hơn: Machine Learning hay Thống kê cổ điển.
-   **Cung cấp góc nhìn khác:** So với các mô hình phân loại (`04`, `05`, `06`), mô hình này cung cấp dự đoán chi tiết hơn (con số cụ thể), hữu ích cho các chuyên gia phân tích môi trường.

---

## 🔗 Notebooks liên quan

- **Trước đó:** [03_feature_preparation.md](./03_feature_preparation.md)
- **So sánh với:** [08_arima_forecasting.md](./08_arima_forecasting.md)
- **Tổng hợp kết quả:** [09_semi_supervised_report.md](./09_semi_supervised_report.md)
