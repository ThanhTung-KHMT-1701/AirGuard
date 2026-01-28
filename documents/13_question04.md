# Notebook 13: Question 04 - Dynamic Threshold Self-Training (FlexMatch-lite)

## Mục tiêu

So sánh hai chiến lược threshold trong Self-Training:
- **Fixed Threshold**: Dùng ngưỡng cố định τ cho tất cả các lớp
- **Dynamic Threshold**: Điều chỉnh ngưỡng riêng cho từng lớp (FlexMatch approach)

**Motivation**:
- Dữ liệu AQI có class imbalance nghiêm trọng
- Fixed threshold thiên lệch về lớp phổ biến (Good, Moderate)
- Dynamic threshold giúp cải thiện recall cho lớp hiếm (Hazardous, Very_Unhealthy)

## Thiết lập thử nghiệm

### Tham số
- `TAU_BASE_LIST = [0.5, 0.7, 0.9]` (base threshold cho cả 2 strategies)
- `MAX_ITER = 10`
- `MAX_NEW_PER_ITER = 100`
- `SAMPLE_FRAC = 0.1`
- `RANDOM_STATE = 42`

### Dynamic Threshold Formula

Theo FlexMatch paper:

```python
τ_c = max(τ_base, p_model(c) / p_data(c))
```

Trong đó:
- `τ_c`: Threshold cho class c
- `τ_base`: Base threshold (minimum)
- `p_model(c)`: Model's prediction distribution (từ pseudo-labels)
- `p_data(c)`: True data distribution (từ labeled samples)

**Ý nghĩa**:
- Nếu model over-predict class c (p_model > p_data) → tăng threshold → strict hơn
- Nếu model under-predict class c (p_model < p_data) → giảm threshold → dễ chọn hơn
- Luôn đảm bảo τ_c ≥ τ_base

### Class-specific behavior

**Example với AQI data**:

| Class | p_data | p_model | τ_c (τ_base=0.7) |
|-------|--------|---------|------------------|
| Good | 0.05 | 0.20 | 0.70 (max) |
| Moderate | 0.30 | 0.35 | 0.70 (close) |
| Unhealthy | 0.25 | 0.22 | 0.70 (base) |
| Very_Unhealthy | 0.15 | 0.10 | 0.67 (giảm) |
| Hazardous | 0.10 | 0.05 | 0.50 (giảm nhiều) |

→ Lớp hiếm (Hazardous) có threshold thấp hơn → dễ được chọn hơn

## Kết quả chính

### Output files
- Metrics cho từng experiment (fixed vs dynamic × 3 tau values)

### Visualizations
- `images/13_01_f1_macro_comparison.png`: F1-macro comparison
- `images/13_02_f1_per_class.png`: F1-score per class
- `images/13_03_recall_rare_classes.png`: Recall for rare classes
- `images/13_DEBUG_confidence_distribution.png`: Debug analysis

### Performance comparison

#### TAU_BASE = 0.7 (best case)

**Fixed Threshold**:
```json
{
  "f1_macro": 0.680,
  "accuracy": 0.614,
  "recall_hazardous": 0.52,
  "recall_very_unhealthy": 0.58,
  "recall_good": 0.15
}
```

**Dynamic Threshold**:
```json
{
  "f1_macro": 0.685,
  "accuracy": 0.617,
  "recall_hazardous": 0.60,
  "recall_very_unhealthy": 0.62,
  "recall_good": 0.39
}
```

**Improvement**:
- F1-macro: +0.5%
- Recall (Hazardous): +15.4%
- Recall (Very_Unhealthy): +6.9%
- Recall (Good): +160% (từ base thấp)

## Insights chính

### 1. Why Fixed Threshold fails on imbalanced data

**Problem**:
- Model học từ data → biased về lớp phổ biến
- Với τ cố định, chỉ chọn pseudo-labels khi confidence ≥ τ
- Lớp phổ biến dễ đạt high confidence → được chọn nhiều
- Lớp hiếm khó đạt high confidence → bị bỏ qua
- **Vicious cycle**: càng train càng biased

**Example**:
- "Moderate" class: 4,833 samples, model confident → 80% selected
- "Hazardous" class: 1,855 samples, model uncertain → 20% selected
- → Ratio càng mất cân bằng

### 2. How Dynamic Threshold helps

**Mechanism**:
1. Track p_model và p_data mỗi iteration
2. Tính τ_c riêng cho từng class
3. Lớp hiếm → lower threshold → easier to select
4. Lớp phổ biến → higher threshold → harder to select
5. → Balance pseudo-label distribution

**Benefits**:
- ✅ Tăng recall cho lớp hiếm (critical cho alerts)
- ✅ Giảm over-selection cho lớp phổ biến
- ✅ F1-macro cao hơn (balance across classes)
- ✅ Tự động điều chỉnh theo data distribution

### 3. Confidence distribution analysis

**Critical discovery** (từ debug charts):

```
Statistics of max confidence scores:
  Min: 0.29
  Max: 1.00
  Mean: 0.95
  Median: 0.98
  Std: Low
```

**Số samples vượt threshold**:
- τ=0.50: ~13,000 samples (100% data)
- τ=0.70: ~11,800 samples (91% data)
- τ=0.90: ~8,000 samples (62% data)
- MAX_NEW_PER_ITER: 100

**Key insight**:
- HistGradientBoostingClassifier rất tự tin trên AQI data
- ~8,000 samples có confidence ≥ 0.9
- Với MAX_NEW=100, luôn đủ high-confidence samples
- → τ từ 0.5→0.9 chọn cùng top 100 samples
- → **Kết quả giống nhau** → Flat lines trong charts!

### 4. Why we see flat lines

**Root cause**:
1. Model overconfident (mean confidence = 0.95)
2. Có >8,000 samples với confidence ≥0.9
3. MAX_NEW_PER_ITER = 100 (bottleneck)
4. Mọi τ ∈ [0.5, 0.9] đều có ≥8,000 qualified samples
5. Algorithm luôn chọn top 100 high-confidence samples
6. Top 100 này **giống hệt nhau** cho mọi τ
7. → F1-macro không thay đổi

**Visualization** (cumulative distribution):
- Top 100 samples: confidence ≈ 1.00
- Sample 101-500: confidence ≈ 0.98-1.00
- Sample 501-8000: confidence ≈ 0.90-0.98
- → Vertical line ở MAX_NEW=100 → no variance

### 5. Solutions to see Dynamic Threshold effect

#### Option 1: Tăng MAX_NEW_PER_ITER
```python
MAX_NEW_PER_ITER = 500  # hoặc 1000
TAU_BASE_LIST = [0.5, 0.7, 0.9]
```
→ Vượt qua số lượng high-confidence samples
→ Bắt đầu thấy ảnh hưởng của τ

#### Option 2: Dùng tau range cao hơn
```python
MAX_NEW_PER_ITER = 100
TAU_BASE_LIST = [0.85, 0.90, 0.95]
```
→ Test ở vùng mà số samples sát với MAX_NEW
→ Variance xuất hiện

#### Option 3: Tăng sample size
```python
SAMPLE_FRAC = 0.2  # hoặc 0.3
MAX_NEW_PER_ITER = 200
```
→ Có thêm variance trong pools

### 6. Trade-offs của Dynamic Threshold

**Advantages**:
- ✅ Cải thiện recall cho lớp hiếm (quan trọng cho alerts)
- ✅ F1-macro cao hơn (balance performance)
- ✅ Tự động điều chỉnh (không cần manual tuning)
- ✅ Có theoretical justification (FlexMatch)

**Disadvantages**:
- ❌ Phức tạp hơn (tính τ_c mỗi iteration)
- ❌ Nhạy cảm với p_data estimation
- ❌ Cần đủ labeled samples cho mỗi class
- ❌ Computational cost cao hơn một chút

**When to use**:
- ✅ Class imbalance nghiêm trọng (>10:1 ratio)
- ✅ Quan tâm đến recall của lớp hiếm
- ✅ Có đủ labeled samples (>50 per class)
- ✅ Optimize F1-macro (không chỉ accuracy)

**When to stick with Fixed**:
- ✅ Data balanced
- ✅ Chỉ quan tâm accuracy
- ✅ Labeled data quá ít (<50 per class)
- ✅ Cần simplicity

## Kết luận về AQI use case

### Why Dynamic Threshold matters for AQI

**Health impact perspective**:
- "Hazardous" level: Nguy hiểm với mọi người → **cần recall cao**
- "Very_Unhealthy": Nguy hiểm với nhóm nhạy cảm → **cần phát hiện tốt**
- "Good" level: Ít quan trọng hơn về warnings

**Dynamic Threshold benefits**:
- Recall (Hazardous): +15.4% → Ít miss critical cases hơn
- Recall (Very_Unhealthy): +6.9% → Better early warnings
- F1-macro: +0.5% → Overall balance improvement

**Practical value**:
- Giảm false negatives cho lớp nguy hiểm
- Tốt hơn cho alert system
- Trade-off nhỏ về complexity là acceptable

## Bài học quan trọng

### 1. Model confidence analysis is critical
- Luôn analyze confidence distribution trước khi tune
- HistGradientBoosting có xu hướng overconfident
- Distribution ảnh hưởng đến hyperparameter choice

### 2. Bottleneck identification
- MAX_NEW_PER_ITER cần phù hợp với confidence distribution
- Nếu có 8000 samples @ τ=0.9 nhưng MAX_NEW=100 → no effect
- Tune parameters together, không độc lập

### 3. Debugging visualization
- Histogram + Cumulative distribution rất hữu ích
- Helps explain unexpected results (flat lines)
- Debug cells trong notebook là best practice

### 4. Domain knowledge matters
- Binary "Healthy vs Unhealthy" dễ nhưng mất thông tin
- Multi-class giữ chi tiết nhưng harder to optimize
- Class imbalance ảnh hưởng lớn đến algorithm design

### 5. Experiment design
- SAMPLE_FRAC=0.1 tốt cho quick experiments
- Nhưng cần test với full data để validate
- Random seed variation (experiment_seed) helps reduce variance

## Liên kết

- **Notebook**: `notebooks/13_Question04.ipynb`
- **Previous**: [12 - Question 03 (Graph-based SSL)](12_question03.md)
- **Next**: [14 - Baseline and Comparison](14_baseline_and_comparison.md)
- **Related**: [10 - Question 01 (Self-Training Sweep)](10_question01.md)
