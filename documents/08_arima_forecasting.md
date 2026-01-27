# 08 — ARIMA Forecasting (Statistical Baseline)

## 🎯 Mục tiêu chính

Notebook này triển khai một hướng tiếp cận hoàn toàn khác để dự báo chất lượng không khí: mô hình **ARIMA**, một phương pháp **Thống kê cổ điển**.

Vai trò chính của nó là thiết lập một **baseline thứ hai cho bài toán hồi quy**, với các mục tiêu:
1.  **Dự báo chuỗi thời gian thuần túy:** Chỉ dựa vào các giá trị `pm25_24h` trong quá khứ để dự đoán các giá trị trong tương lai.
2.  **Không sử dụng features:** Khác với các mô hình Machine Learning, ARIMA không cần các features phụ trợ như nhiệt độ, hướng gió, hay thời gian.
3.  **Tạo một "đối thủ" cho Machine Learning:** Kết quả của ARIMA sẽ được so sánh trực tiếp với mô hình hồi quy `HistGradientBoostingRegressor` (từ notebook `07`) để xem phương pháp nào hiệu quả hơn.

---

## 📥 Đầu vào (Input)

| File | Mô tả |
| :--- | :--- |
| `data/processed/01_cleaned.parquet` | Dữ liệu đầu vào chính, từ đó sẽ trích xuất ra chuỗi thời gian `pm25_24h` của một trạm cụ thể (ví dụ: Aotizhongxin). |

---

## 📤 Đầu ra (Output)

| File | Mô tả |
| :--- | :--- |
| `data/processed/08_metrics_arima.json` | File JSON chứa các chỉ số lỗi của mô hình ARIMA, chủ yếu là `MSE` và `MAE`. |
| `images/08_arima_forecast.png` | Biểu đồ trực quan hóa kết quả dự báo, so sánh chuỗi thời gian thực tế và chuỗi dự báo của ARIMA. |
| `images/08_arima_diagnostics.png` | Các biểu đồ chẩn đoán để kiểm tra xem mô hình ARIMA có phù hợp với dữ liệu hay không. |

---

## 🔄 Quy trình xử lý

1.  **Chọn và chuẩn bị dữ liệu:** Chọn một trạm quan trắc duy nhất (ví dụ: `Aotizhongxin`) và tạo ra một chuỗi thời gian (time series) chỉ bao gồm cột `datetime` và `pm25_24h`.
2.  **Phân rã chuỗi thời gian (Decomposition):** Phân tích chuỗi thành các thành phần: Xu hướng (Trend), Tính mùa vụ (Seasonality), và Phần dư (Residuals) để hiểu rõ hơn về dữ liệu.
3.  **Kiểm tra tính dừng (Stationarity Test):** Sử dụng kiểm định ADF để xác định xem chuỗi có "tính dừng" hay không. Nếu không, thực hiện phép sai phân (differencing) để làm cho chuỗi dừng.
4.  **Tìm tham số (p, d, q):** Sử dụng biểu đồ ACF và PACF để xác định các tham số tối ưu cho mô hình ARIMA.
5.  **Huấn luyện (Fit) mô hình:** Huấn luyện mô hình SARIMA (Seasonal ARIMA) trên dữ liệu train.
6.  **Dự báo và đánh giá:** Thực hiện dự báo trên tập test và tính toán các chỉ số lỗi.

---

## 💡 Ý nghĩa và mối liên hệ

-   **Baseline Thống kê:** ARIMA cung cấp một thước đo hiệu suất từ một phương pháp đã được kiểm chứng và sử dụng rộng rãi trong nhiều thập kỷ. Nó giúp trả lời câu hỏi: "Liệu các mô hình Machine Learning phức tạp có thực sự tốt hơn các phương pháp thống kê cổ điển hay không?".
-   **Đối thủ trực tiếp của Hồi quy ML:** Kết quả `MSE` từ notebook này sẽ được **so sánh trực tiếp** với `MSE` từ notebook `07`.
    -   Nếu `MSE` của `07` thấp hơn, điều đó có nghĩa là việc sử dụng thêm các features (nhiệt độ, gió, lag...) giúp cải thiện đáng kể độ chính xác.
    -   Nếu `MSE` của `08` thấp hơn, điều đó cho thấy các quy luật nội tại của chuỗi thời gian đã đủ mạnh để dự báo mà không cần features ngoài.

---

## 🔗 Notebooks liên quan

- **Trước đó:** [01_preprocessing_and_eda.md](./01_preprocessing_and_eda.md)
- **So sánh với:** [07_regression_modelling.md](./07_regression_modelling.md)
- **Tổng hợp kết quả:** [09_semi_supervised_report.md](./09_semi_supervised_report.md)
