# Tài liệu: 03 - Chuẩn bị đặc trưng cho học có giám sát

## 🎯 Mục tiêu

Notebook này đóng vai trò then chốt trong việc chuẩn bị dữ liệu đầu vào (đặc trưng) cho các mô hình **học có giám sát (Supervised Learning)**. Mục tiêu không chỉ là biến đổi dữ liệu, mà còn là xây dựng một `pipeline` tiền xử lý mạnh mẽ, đảm bảo tính nhất quán và ngăn chặn rò rỉ dữ liệu.

---

## 🔑 Nguyên tắc cốt lõi: Tạo Baseline để so sánh

Kết quả từ các mô hình được huấn luyện trên dữ liệu do notebook này tạo ra sẽ đóng vai trò là **đường cơ sở (baseline)**. Đây là một cột mốc hiệu suất quan trọng, giúp chúng ta trả lời câu hỏi:

> "Liệu các mô hình học bán giám sát, với việc tận dụng thêm 95% dữ liệu không nhãn, có thực sự vượt trội hơn một mô hình học có giám sát chỉ được huấn luyện trên 5% dữ liệu có nhãn hay không?"

Để có một baseline công bằng, chúng ta chỉ sử dụng phần dữ liệu có nhãn (`is_labeled == True`) từ tập huấn luyện đã tạo ở bước trước.

---

## 🔄 Quy trình xây dựng Pipeline tiền xử lý

Chúng tôi sử dụng `ColumnTransformer` của scikit-learn để xây dựng một pipeline xử lý riêng biệt cho từng loại đặc trưng, sau đó kết hợp chúng lại.

### 1. Xác định và Phân loại Đặc trưng

- **Đặc trưng số (Numeric Features)**: Các cột có giá trị liên tục như nhiệt độ, áp suất, tốc độ gió, và các giá trị trễ (lag) của PM2.5.
- **Đặc trưng phân loại (Categorical Features)**: Các cột có giá trị rời rạc như `station`, `weekday`, `month`.
- **Các cột cần loại bỏ**:
    - `is_labeled`: Không còn ý nghĩa sau khi đã lọc dữ liệu có nhãn.
    - `PM2.5`, `pm25_24h`, `aqi_class`: Đây là các biến mục tiêu (target) hoặc có liên quan trực tiếp đến target, đưa vào làm đặc trưng sẽ gây ra **rò rỉ dữ liệu (data leakage)**.
    - `datetime`: Đã được trích xuất thành các đặc trưng thời gian chi tiết hơn.

### 2. Xây dựng Pipeline cho từng loại dữ liệu

- **Đối với đặc trưng số**:
    1.  `SimpleImputer(strategy='median')`: Điền các giá trị thiếu bằng giá trị trung vị của cột. Trung vị được ưu tiên hơn trung bình vì nó ít bị ảnh hưởng bởi các giá trị ngoại lai (outliers).
- **Đối với đặc trưng phân loại**:
    1.  `SimpleImputer(strategy='most_frequent')`: Điền các giá trị thiếu bằng giá trị xuất hiện nhiều nhất trong cột.
    2.  `OneHotEncoder(handle_unknown='ignore')`: Chuyển đổi các cột phân loại thành các cột nhị phân (0/1). `handle_unknown='ignore'` giúp pipeline không bị lỗi nếu gặp một danh mục mới trong tập kiểm tra mà chưa từng thấy trong tập huấn luyện.

### 3. Huấn luyện (Fit) và Biến đổi (Transform)

- Pipeline được **huấn luyện (fit) chỉ trên tập huấn luyện (TRAIN)**. Quá trình này giúp pipeline "học" các tham số thống kê (ví dụ: giá trị trung vị, các danh mục phổ biến) từ dữ liệu huấn luyện.
- Sau đó, pipeline được dùng để **biến đổi (transform) cho cả tập huấn luyện và tập kiểm tra (TEST)**. Việc áp dụng cùng một pipeline đã được huấn luyện lên cả hai tập đảm bảo rằng dữ liệu được xử lý một cách nhất quán.

---

## 💾 Kết quả đầu ra

| Tệp                                           | Mô tả                                                                                                                              |
| --------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| `data/processed/03_dataset_for_clf.parquet`   | Dữ liệu đã qua xử lý, sẵn sàng cho các mô hình **phân loại**.                                                                      |
| `data/processed/03_feature_list.csv`          | Danh sách tên của các đặc trưng sau khi đã qua pipeline (ví dụ: các cột được tạo ra từ OneHotEncoder).                               |

---

## 💡 Ý nghĩa và Bước tiếp theo

- Notebook này không chỉ đơn thuần xử lý dữ liệu mà còn đóng gói toàn bộ logic tiền xử lý vào một đối tượng pipeline có thể tái sử dụng.
- Dữ liệu đầu ra từ bước này là nền tảng vững chắc để xây dựng và đánh giá các mô hình học có giám sát trong các notebook sau, cụ thể là:
    - **06_classification_modelling.ipynb**
    - **07_regression_modelling.ipynb**
