# Tài liệu: 02 - Chuẩn bị dữ liệu cho học bán giám sát

## 🎯 Mục tiêu

Mục tiêu chính của notebook này là tạo ra một tập dữ liệu chuyên biệt để **thử nghiệm và đánh giá hiệu quả của các thuật toán học bán giám sát (Semi-supervised Learning)**.

---

## 🔑 Vấn đề cốt lõi: Sự khan hiếm của dữ liệu có nhãn

Trong các kịch bản thực tế, việc thu thập dữ liệu (ví dụ: đo nồng độ PM2.5) thường diễn ra tự động và liên tục. Tuy nhiên, quá trình **gán nhãn** cho dữ liệu đó (ví dụ: phân loại mức độ AQI) lại đòi hỏi sự can thiệp của con người, tốn kém thời gian và chi phí. Kết quả là chúng ta thường có một lượng lớn dữ liệu **không có nhãn** và chỉ một phần nhỏ dữ liệu **có nhãn**.

Học bán giám sát ra đời để giải quyết bài toán này, bằng cách tận dụng thông tin ẩn chứa trong lượng lớn dữ liệu không nhãn để cải thiện hiệu suất của mô hình.

---

## 📝 Quy trình chuẩn bị dữ liệu

Để mô phỏng kịch bản trên, chúng tôi thực hiện quy trình sau:

### 1. Phân chia dữ liệu theo thời gian (Time-aware Split)

- Dữ liệu được chia thành hai tập:
    - **Tập huấn luyện (TRAIN)**: Dữ liệu trước ngày `2017-01-01`.
    - **Tập kiểm tra (TEST)**: Dữ liệu từ ngày `2017-01-01` trở đi.
- **Lý do**: Cách chia này đảm bảo rằng mô hình được huấn luyện trên dữ liệu quá khứ và được đánh giá trên dữ liệu tương lai, phản ánh đúng quy trình triển khai trong thực tế.

### 2. Giả lập tình huống thiếu nhãn

- **Hành động**: Trong **tập huấn luyện (TRAIN)**, chúng tôi tiến hành **che (mask) một cách ngẫu nhiên 95% nhãn** `aqi_class`.
- **Kết quả**:
    - **Tập TRAIN**: Chỉ còn lại 5% dữ liệu có nhãn. Đây là "dữ liệu vàng" mà mô hình có giám sát ban đầu (baseline) sẽ sử dụng. 95% còn lại sẽ là dữ liệu không nhãn để các thuật toán bán giám sát khai thác.
    - **Tập TEST**: Giữ lại 100% nhãn. Tập này được dùng để đánh giá cuối cùng, so sánh hiệu quả giữa các mô hình một cách công bằng.

### 3. Thêm cột `is_labeled`

- Một cột boolean mới có tên `is_labeled` được thêm vào để dễ dàng phân biệt giữa dữ liệu có nhãn (`True`) và không có nhãn (`False`) trong quá trình huấn luyện.

---

## 💾 Kết quả đầu ra

| Tệp                                           | Mô tả                                                                                                                              |
| --------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| `data/processed/02_dataset_for_semi.parquet`  | **Dataset chính**: Bộ dữ liệu hoàn chỉnh đã được phân chia và che nhãn, sẵn sàng cho các thí nghiệm học bán giám sát.                 |
| `data/processed/02_dataset_for_semi_sample.csv` | Một tệp mẫu chứa 500 dòng đầu tiên của bộ dữ liệu trên, giúp người dùng có cái nhìn nhanh về cấu trúc dữ liệu mà không cần tải tệp lớn. |

---

## 💡 Ý nghĩa và Bước tiếp theo

- Notebook này đã tạo ra một môi trường giả lập thực tế, cho phép chúng tôi đo lường chính xác **giá trị gia tăng** mà các phương pháp bán giám sát mang lại so với việc chỉ sử dụng một lượng nhỏ dữ liệu có nhãn.
- Bộ dữ liệu này sẽ là đầu vào cốt lõi cho các notebook tiếp theo, bao gồm:
    - **04_semi_self_training.ipynb**
    - **05_semi_co_training.ipynb**
    - **09_semi_supervised_report.ipynb**
3. **Tự động gán nhãn** cho dữ liệu chưa có nhãn (pseudo-labeling)

---

## 🔗 Notebooks liên quan

- **Trước đó:** [01_preprocessing_and_eda.md](./01_preprocessing_and_eda.md) - Tiền xử lý và EDA
- **Tiếp theo (nhánh Supervised):** [03_feature_preparation.md](./03_feature_preparation.md) - Chuẩn bị features cho Supervised Learning
- **Tiếp theo (nhánh Semi-supervised):** 
  - [04_semi_self_training.md](./04_semi_self_training.md) - Self-training algorithm
  - `05_semi_co_training.ipynb` - Co-training algorithm
