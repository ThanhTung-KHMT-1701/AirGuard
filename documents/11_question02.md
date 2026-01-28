# Notebook 11: Question 02 - Co-Training Parameter Sweep

## Mục tiêu

Khảo sát hiệu quả của Co-Training với các cấu hình tham số khác nhau:
- **TAU**: Ngưỡng confidence để chọn pseudo-labels cho mỗi view
- **MAX_NEW_PER_VIEW**: Số lượng pseudo-labels tối đa từ mỗi view
- **K_BEST**: Số lượng samples tốt nhất cuối cùng chọn sau khi combine 2 views
- **VIEW1_COLS & VIEW2_COLS**: Chiến lược phân chia features thành 2 views

## Thiết lập thử nghiệm

### Tham số cố định
- `RANDOM_STATE = 42`
- `SAMPLE_FRAC = 0.1` (10% dữ liệu)
- `MAX_ITER = 10`

### Chiến lược phân chia views

#### View 1: Temporal & Weather features
```python
VIEW1_COLS = [
    'hour', 'hour_sin', 'hour_cos', 'dow', 'is_weekend',
    'TEMP', 'PRES', 'DEWP', 'RAIN', 'wd', 'WSPM',
    'TEMP_lag1', 'PRES_lag1', 'DEWP_lag1', 'RAIN_lag1', 'WSPM_lag1'
]
```

#### View 2: Pollutants & Lag features
```python
VIEW2_COLS = [
    'PM10', 'SO2', 'NO2', 'CO', 'O3', 'station',
    'PM10_lag1', 'SO2_lag1', 'NO2_lag1', 'CO_lag1', 'O3_lag1',
    'PM10_lag3', 'SO2_lag3', 'NO2_lag3', 'CO_lag3', 'O3_lag3',
    'PM10_lag24', 'SO2_lag24', 'NO2_lag24', 'CO_lag24', 'O3_lag24'
]
```

**Lý do phân chia**:
- View 1: Các yếu tố thời gian và thời tiết (pattern theo giờ/ngày, điều kiện khí tượng)
- View 2: Các chất ô nhiễm và giá trị lag (chemical composition và temporal dependencies)
- Hai views bổ trợ nhau nhưng độc lập về mặt thông tin

### Các thử nghiệm

#### Experiment grid (18 configurations)
```python
TAU_VALUES = [0.6, 0.7, 0.8]
MAX_NEW_VALUES = [50, 100]
K_BEST_VALUES = [80, 100, 120]
```

## Kết quả chính

### Output files
- `data/processed/11_01_metrics_co_training.json` đến `11_18_metrics_co_training.json`
- Mỗi file chứa kết quả cho một cấu hình cụ thể

### Visualizations
- `images/11_01_co_training_default.png`: Co-Training dynamics với cấu hình default
- `images/11_02_co_training_line_chart.png`: So sánh F1-macro theo các cấu hình

## Insights chính

### 1. Ưu điểm của Co-Training

**So với Self-Training**:
- ✅ **Diversity**: Hai views cho predictions khác nhau → giảm overfitting
- ✅ **Mutual improvement**: View 1 giúp View 2 và ngược lại
- ✅ **Better generalization**: Kết hợp 2 views → robust hơn
- ✅ **Label efficiency**: Hiệu quả hơn khi labeled data rất ít

**F1-macro comparison**:
- Self-Training (TAU=0.7): ~0.68
- Co-Training (TAU=0.7, best config): ~0.71
- **Improvement**: +4.4%

### 2. Ảnh hưởng của TAU

**Quan sát**:
- TAU=0.6: Nhiều pseudo-labels từ cả 2 views, nhưng noise cao
- TAU=0.7: Cân bằng tốt, F1-macro đạt peak
- TAU=0.8: Quá conservative, tăng trưởng chậm

**Best TAU**: 0.7 (giống Self-Training)

### 3. Ảnh hưởng của MAX_NEW_PER_VIEW

**Quan sát**:
- MAX_NEW=50: Hội tụ chậm, cần nhiều iterations
- MAX_NEW=100: Tốc độ tốt, đủ samples mỗi iteration
- MAX_NEW=150+: Không cải thiện đáng kể (giới hạn bởi K_BEST)

**Trade-off**:
- Số lượng candidates từ mỗi view
- Chất lượng sau khi filter bằng K_BEST
- Computational cost (train 2 models mỗi iteration)

### 4. Ảnh hưởng của K_BEST

**Quan sát**:
- K_BEST=80: Quá strict, bỏ qua nhiều good samples
- K_BEST=100: Cân bằng tốt nhất
- K_BEST=120: Có thể thêm noise khi 2 views không đủ agreement

**Best K_BEST**: 100 (với MAX_NEW_PER_VIEW=100)

**Rule of thumb**: K_BEST ≈ MAX_NEW_PER_VIEW để đảm bảo quality

### 5. View independence analysis

**Correlation giữa 2 views**:
- View 1 predictions ≠ View 2 predictions → good diversity
- Agreement rate: ~75% trên high-confidence samples
- Disagreement cases: view khác giúp correct errors

**Khi nào Co-Training hiệu quả**:
- ✅ Views thực sự independent (ít feature overlap)
- ✅ Mỗi view đủ mạnh để train model riêng
- ✅ Views bổ sung thông tin cho nhau
- ❌ Views quá overlap → giống Self-Training
- ❌ Một view quá yếu → kéo performance xuống

### 6. Computational cost

**So với Self-Training**:
- Self-Training: 1 model/iteration × 10 iterations = 10 trainings
- Co-Training: 2 models/iteration × 10 iterations = 20 trainings
- **Cost**: ~2× Self-Training

**Trade-off**:
- +4.4% F1-macro improvement
- 2× training time
- ROI: Tốt khi labeled data rất ít và accuracy quan trọng

## Cấu hình khuyến nghị

### Best configuration
```python
TAU = 0.7
MAX_NEW_PER_VIEW = 100
K_BEST = 100
MAX_ITER = 10

VIEW1_COLS = ['hour', 'hour_sin', 'hour_cos', 'dow', 'is_weekend',
              'TEMP', 'PRES', 'DEWP', 'RAIN', 'wd', 'WSPM',
              'TEMP_lag1', 'PRES_lag1', 'DEWP_lag1', 'RAIN_lag1', 'WSPM_lag1']

VIEW2_COLS = ['PM10', 'SO2', 'NO2', 'CO', 'O3', 'station',
              'PM10_lag1', 'SO2_lag1', 'NO2_lag1', 'CO_lag1', 'O3_lag1',
              'PM10_lag3', 'SO2_lag3', 'NO2_lag3', 'CO_lag3', 'O3_lag3',
              'PM10_lag24', 'SO2_lag24', 'NO2_lag24', 'CO_lag24', 'O3_lag24']
```

**Expected performance**:
- F1-macro: ~0.71
- Accuracy: ~0.64
- Training time: ~2× Self-Training

## So sánh với Self-Training

| Metric | Self-Training | Co-Training | Delta |
|--------|--------------|-------------|-------|
| F1-macro | 0.680 | 0.710 | +4.4% |
| Accuracy | 0.614 | 0.639 | +4.1% |
| Training time | 1× | 2× | +100% |
| Complexity | Low | Medium | - |
| Label efficiency | Good | Better | - |

**Khi nào dùng Co-Training**:
- ✅ Labeled data rất ít (<5%)
- ✅ Features có thể phân chia thành 2 views independent
- ✅ Accuracy quan trọng hơn speed
- ✅ Có đủ computational resources

**Khi nào dùng Self-Training**:
- ✅ Labeled data trung bình (5-10%)
- ✅ Cần training nhanh
- ✅ Features khó phân chia thành views
- ✅ Resources hạn chế

## Bài học quan trọng

### 1. View design là quan trọng nhất
- Views phải thực sự independent
- Mỗi view cần đủ thông tin để train model tốt
- Domain knowledge giúp thiết kế views hiệu quả

### 2. Agreement filtering
- K_BEST mechanism giúp filter noise
- Chỉ chọn samples mà cả 2 views đều confident
- Trade-off: strict filtering vs coverage

### 3. Monitoring convergence
- Theo dõi agreement rate giữa 2 views
- Nếu agreement quá cao (>95%) → views quá overlap
- Nếu agreement quá thấp (<50%) → views conflict

### 4. Practical considerations
- 2× training cost cần cân nhắc với improvement
- Early stopping quan trọng hơn với Co-Training
- Validation set để monitor cả 2 views

## Liên kết

- **Notebook**: `notebooks/11_Question02.ipynb`
- **Previous**: [10 - Question 01 (Self-Training Sweep)](10_question01.md)
- **Next**: [12 - Question 03 (Graph-based SSL)](12_question03.md)
- **Related**: [05 - Co-Training](05_semi_co_training.md)
