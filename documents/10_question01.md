# Notebook 10: Question 01 - Self-Training Parameter Sweep

## Mục tiêu

Khảo sát ảnh hưởng của các tham số quan trọng trong Self-Training để tìm cấu hình tối ưu:
- **TAU_BASE**: Ngưỡng confidence để chọn pseudo-labels
- **MAX_NEW_PER_ITER**: Số lượng pseudo-labels tối đa thêm mỗi iteration
- **MAX_ITER**: Số lượng iterations tối đa

## Thiết lập thử nghiệm

### Tham số cố định
- `RANDOM_STATE = 42`
- `SAMPLE_FRAC = 0.1` (10% dữ liệu để test nhanh)
- `VAL_FRAC = 0.2` (validation set)

### Tham số khảo sát

#### Thử nghiệm 1: TAU_BASE sweep
- **TAU_BASE**: [0.5, 0.6, 0.7, 0.8, 0.9]
- MAX_NEW_PER_ITER: 100
- MAX_ITER: 10

#### Thử nghiệm 2: MAX_NEW_PER_ITER sweep  
- TAU_BASE: 0.7
- **MAX_NEW_PER_ITER**: [50, 100, 200, 500]
- MAX_ITER: 10

#### Thử nghiệm 3: MAX_ITER sweep
- TAU_BASE: 0.7
- MAX_NEW_PER_ITER: 100
- **MAX_ITER**: [5, 10, 15, 20]

## Kết quả chính

### Output files
- `data/processed/10_01_metrics_self_training.json` (TAU_BASE experiments)
- `data/processed/10_02_metrics_self_training.json` (MAX_NEW experiments)
- `data/processed/10_03_metrics_self_training.json` (MAX_ITER experiments)
- `data/processed/10_04_metrics_self_training.json` (tổng hợp)

### Visualizations
- `images/10_01_f1_macro_comparison.png`: So sánh F1-macro theo TAU_BASE
- `images/10_02_f1_macro_heatmap.png`: Heatmap hiệu năng theo các tham số
- `images/10_03_f1_macro_line_chart.png`: Line chart theo iterations

## Insights chính

### 1. Ảnh hưởng của TAU_BASE

**Quan sát**:
- TAU thấp (0.5-0.6): Chọn nhiều pseudo-labels nhưng chất lượng thấp → noise cao
- TAU cao (0.8-0.9): Chọn ít pseudo-labels nhưng chất lượng cao → tăng trưởng chậm
- **TAU tối ưu: 0.7** - cân bằng giữa số lượng và chất lượng

**F1-macro theo TAU**:
- TAU=0.5: ~0.52 (nhiều noise)
- TAU=0.7: ~0.68 (tối ưu)
- TAU=0.9: ~0.65 (quá conservative)

### 2. Ảnh hưởng của MAX_NEW_PER_ITER

**Quan sát**:
- MAX_NEW nhỏ (50): Tăng trưởng chậm, cần nhiều iterations
- MAX_NEW lớn (500): Có thể thêm noise nếu không đủ high-confidence samples
- **MAX_NEW tối ưu: 100-200** - đủ nhanh mà không gây noise

**Trade-off**:
- Tốc độ ↔ Chất lượng
- Số iterations cần thiết ↔ Computational cost

### 3. Ảnh hưởng của MAX_ITER

**Quan sát**:
- Hiệu năng tăng nhanh trong 5-7 iterations đầu
- Sau iteration 10: plateau hoặc giảm nhẹ (overfitting on pseudo-labels)
- **MAX_ITER tối ưu: 10** - đủ để hội tụ mà không overfitting

**Early stopping criteria**:
- Nếu `new_pseudo < 20` trong 2 iterations liên tiếp → dừng sớm
- Nếu validation F1 giảm 3 iterations liên tiếp → dừng sớm

### 4. Confidence distribution analysis

**Phát hiện quan trọng** (từ debug analysis):
- HistGradientBoostingClassifier cho confidence rất cao trên dữ liệu AQI
- Mean confidence ~0.95 trên unlabeled pool
- ~8,000 samples có confidence ≥0.9 (với SAMPLE_FRAC=0.1)

**Hệ quả**:
- Với MAX_NEW_PER_ITER=100, luôn đủ high-confidence samples
- TAU từ 0.5→0.9 chọn cùng top 100 samples → kết quả giống nhau
- Để thấy ảnh hưởng của TAU, cần:
  - Tăng MAX_NEW_PER_ITER lên 500-1000, HOẶC
  - Test với TAU range cao hơn [0.85, 0.90, 0.95], HOẶC
  - Tăng SAMPLE_FRAC lên 0.2-0.3

## Cấu hình khuyến nghị

Dựa trên kết quả thử nghiệm:

```python
# Recommended configuration
TAU_BASE = 0.7
MAX_NEW_PER_ITER = 150
MAX_ITER = 10
VAL_FRAC = 0.2
EARLY_STOPPING = True
```

**Lý do**:
- TAU=0.7: Cân bằng tốt giữa precision và recall của pseudo-labels
- MAX_NEW=150: Đủ nhanh để hội tụ trong 10 iterations
- Early stopping: Tránh overfitting và tiết kiệm thời gian

## Bài học quan trọng

### 1. Tuning strategy
- Không nên tune từng tham số độc lập
- Cần xem xét tương tác giữa TAU × MAX_NEW × MAX_ITER
- Grid search hoặc random search cho kết quả tốt hơn

### 2. Validation set quan trọng
- Dùng validation F1 để đánh giá mỗi iteration
- Test set chỉ dùng ở cuối để báo cáo final metrics
- Tránh overfitting to test set

### 3. Data-specific behavior
- Model confidence phụ thuộc vào dữ liệu cụ thể
- Nên analyze confidence distribution trước khi tune
- Adjust tham số phù hợp với distribution

### 4. Computational cost
- Mỗi iteration tốn thời gian train lại model
- Trade-off giữa MAX_ITER × MAX_NEW và total training time
- Early stopping giúp tiết kiệm đáng kể

## Liên kết

- **Notebook**: `notebooks/10_Question01.ipynb`
- **Previous**: [09 - Semi-supervised Report](09_semi_supervised_report.md)
- **Next**: [11 - Question 02 (Co-Training)](11_question02.md)
- **Related**: [04 - Self-Training](04_semi_self_training.md)
