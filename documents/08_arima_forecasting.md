# Tài liệu: 08 - Dự báo chuỗi thời gian với ARIMA

## 🎯 Mục tiêu

Notebook này khám phá một cách tiếp cận hoàn toàn khác để dự báo nồng độ PM2.5: sử dụng mô hình **ARIMA (AutoRegressive Integrated Moving Average)**, một phương pháp thống kê kinh điển được thiết kế chuyên biệt cho dữ liệu chuỗi thời gian.

Mục tiêu chính là:
1.  **Xây dựng mô hình dự báo thuần túy**: Chỉ dựa vào các giá trị trong quá khứ của chính chuỗi dữ liệu PM2.5 để dự đoán tương lai, mà không cần đến các đặc trưng ngoại sinh (như nhiệt độ, gió, v.v.).
2.  **Thiết lập Baseline thống kê**: Tạo ra một thước đo hiệu suất từ một phương pháp cổ điển để so sánh với cách tiếp cận dựa trên Machine Learning (từ notebook 07).

---

## 🔬 Quy trình phân tích chuỗi thời gian

### 1. Phân rã chuỗi thời gian (Time Series Decomposition)

Bước đầu tiên là "nhìn sâu" vào bên trong dữ liệu để hiểu các thành phần cấu tạo nên nó.

![Phân rã chuỗi thời gian](../images/08_rolling_statistics.png)
*Hình 1: Phân rã chuỗi PM2.5 thành các thành phần: Xu hướng (Trend), Mùa vụ (Seasonality), và Phần dư (Residual).*

- **Xu hướng (Trend)**: Cho thấy xu hướng dài hạn của nồng độ PM2.5. Có thể thấy một sự cải thiện nhẹ (giảm dần) về chất lượng không khí qua các năm.
- **Mùa vụ (Seasonality)**: Cho thấy các chu kỳ lặp lại hàng năm. Nồng độ PM2.5 có xu hướng tăng cao vào các tháng mùa đông và giảm vào mùa hè.
- **Phần dư (Residual)**: Là những biến động ngẫu nhiên sau khi đã loại bỏ xu hướng và tính mùa vụ.

### 2. Kiểm tra tính dừng và xác định tham số ARIMA

- **Tính dừng (Stationarity)**: Một chuỗi thời gian được gọi là "dừng" nếu các đặc tính thống kê của nó (như trung bình, phương sai) không thay đổi theo thời gian. Hầu hết các mô hình chuỗi thời gian, bao gồm cả ARIMA, đều yêu cầu dữ liệu phải có tính dừng. Chúng tôi sử dụng các phép kiểm định thống kê (ADF test) và phép sai phân (differencing) để đạt được điều này.
- **Xác định tham số (p, d, q)**:
    - **p (AutoRegressive - Tự hồi quy)**: Số lượng quan sát quá khứ được sử dụng để dự đoán.
    - **d (Integrated - Tích hợp)**: Số lần thực hiện phép sai phân.
    - **q (Moving Average - Trung bình trượt)**: Số lượng lỗi dự báo trong quá khứ được sử dụng.
    Chúng tôi sử dụng biểu đồ Tự tương quan (ACF) và Tự tương quan riêng phần (PACF) để lựa chọn các tham số này một cách hợp lý.

![Biểu đồ ACF và PACF](../images/08_acf_plot.png)
*Hình 2: Biểu đồ ACF được sử dụng để xác định tham số q.*

![Biểu đồ ACF và PACF](../images/08_pacf_plot.png)
*Hình 3: Biểu đồ PACF được sử dụng để xác định tham số p.*

### 3. Huấn luyện và Dự báo

Sau khi xác định được các tham số, mô hình SARIMA (Seasonal ARIMA, một phiên bản mở rộng có xử lý tính mùa vụ) được huấn luyện trên dữ liệu trước năm 2017 và sau đó được sử dụng để dự báo cho giai đoạn sau đó.

---

## 📊 Phân tích kết quả

### 1. Trực quan hóa kết quả dự báo

![Dự báo vs. Thực tế](../images/08_forecast_vs_actual.png)
*Hình 4: So sánh giữa chuỗi giá trị PM2.5 thực tế (màu xanh) và chuỗi dự báo của mô hình ARIMA (màu đỏ).*

- **Phân tích**: Mô hình ARIMA đã nắm bắt được xu hướng chung và tính mùa vụ của dữ liệu. Tuy nhiên, có thể thấy rõ rằng dự báo của ARIMA **kém linh hoạt** hơn so với thực tế. Nó không thể dự báo được các **đỉnh nhọn và biến động đột ngột**, vốn là đặc tính quan trọng của dữ liệu ô nhiễm không khí.

### 2. So sánh hiệu suất với Mô hình Hồi quy Machine Learning

| Phương pháp                            | **RMSE**      | **MAE**     | Nhận xét                                                                                                                          |
| :-------------------------------------- | :------------ | :---------- | :-------------------------------------------------------------------------------------------------------------------------------- |
| **Hồi quy ML (Notebook 07)**            | **30.14**     | **19.46**   | **Vượt trội hơn hẳn.**                                                                                                            |
| **ARIMA (Thống kê)**                    | 104.10        | 77.69       | Sai số cao hơn đáng kể (cao hơn 3-4 lần).                                                                                         |

- **Kết luận**: **Mô hình hồi quy dựa trên Machine Learning cho kết quả chính xác hơn đáng kể.**
- **Lý do**: Mô hình Machine Learning có khả năng học hỏi từ một tập hợp các **đặc trưng ngoại sinh** phong phú (nhiệt độ, áp suất, tốc độ gió, hướng gió, thời gian, v.v.). Những thông tin bổ sung này cung cấp ngữ cảnh quan trọng, giúp mô hình hiểu rõ hơn về các yếu tố gây ra sự thay đổi của nồng độ PM2.5, điều mà mô hình ARIMA thuần túy (chỉ nhìn vào lịch sử của chính nó) không thể làm được.

---

## 💾 Kết quả đầu ra

| Tệp                                           | Mô tả                                                                                                        |
| :-------------------------------------------- | :----------------------------------------------------------------------------------------------------------- |
| `data/processed/08_arima_pm25_summary.json`   | File JSON chứa các chỉ số hiệu suất (RMSE, MAE) và các tham số (p,d,q) của mô hình ARIMA đã được huấn luyện.   |
| `data/processed/08_arima_pm25_predictions.csv`| Bảng dữ liệu chứa các giá trị dự báo chi tiết cùng với khoảng tin cậy.                                        |

---

## 💡 Bài học rút ra

- ARIMA là một công cụ mạnh mẽ để hiểu và mô hình hóa các thành phần của chuỗi thời gian, nhưng có thể không phải là lựa chọn tốt nhất cho các chuỗi dữ liệu phức tạp, bị ảnh hưởng bởi nhiều yếu tố bên ngoài.
- Đối với bài toán dự báo chất lượng không khí, việc kết hợp thêm các đặc trưng liên quan (thời tiết, thời gian) thông qua các mô hình Machine Learning đã được chứng minh là mang lại hiệu quả vượt trội.
