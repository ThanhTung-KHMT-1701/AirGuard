# Notebook 14: Baseline and Comprehensive Comparison

## Mục tiêu

So sánh toàn diện **6 phương pháp** Machine Learning cho bài toán phân loại AQI:

1. **Baseline Supervised** - Học từ labeled data only
2. **Self-Training** - Pseudo-labeling iterative
3. **Co-Training** - Dual-view semi-supervised (reserved)
4. **Label Propagation** - Graph-based hard propagation
5. **Label Spreading** - Graph-based soft propagation  
6. **Dynamic Threshold Self-Training** - FlexMatch-lite approach

**Mục đích**: Đưa ra khuyến nghị phương pháp phù hợp cho từng scenario

## Thiết lập thử nghiệm

### Tham số chung
- `SAMPLE_FRAC = 0.1` (10% dữ liệu cho tất cả methods)
- `RANDOM_STATE = 42`
- Cùng train/test split cutoff

### Tham số riêng từng method

#### Baseline Supervised
```python
# Chỉ dùng labeled data
# Không có hyperparameters đặc biệt
```

#### Self-Training
```python
TAU = 0.7
MAX_NEW_PER_ITER = 100
MAX_ITER = 10
```

#### Co-Training
```python
# Skipped in current version
# (Load từ notebook 11 nếu cần)
```

#### Label Propagation
```python
KERNEL = 'knn'
N_NEIGHBORS = 7
MAX_ITER = 30
# Binary classification (Healthy vs Unhealthy)
```

#### Label Spreading
```python
KERNEL = 'knn'
N_NEIGHBORS = 7
ALPHA = 0.2
MAX_ITER = 30
# Binary classification
```

#### Dynamic Threshold Self-Training
```python
TAU_BASE = 0.7
MAX_NEW_PER_ITER = 100
MAX_ITER = 10
USE_DYNAMIC = True
```

## Kết quả chính

### Output files
- `data/processed/14_baseline_metrics.json`
- `data/processed/14_comparison_summary.csv`

### Visualizations
- `images/14_01_f1_macro_comparison.png`: F1-macro bar chart
- `images/14_02_f1_heatmap.png`: Performance heatmap across classes
- `images/14_03_performance_vs_cost.png`: Performance vs computational cost
- `images/14_04_improvement_percentage.png`: % improvement over baseline

## Performance Summary

### F1-Macro Comparison

| Method | F1-Macro | Accuracy | Training Time | Memory |
|--------|----------|----------|---------------|--------|
| **Baseline Supervised** | 0.472 | 0.602 | 1× | Low |
| **Self-Training** | 0.680 | 0.614 | 10× | Low |
| **Co-Training** | 0.710* | 0.639* | 20× | Low |
| **Label Propagation** | 0.860** | 0.870** | 1× | High |
| **Label Spreading** | 0.870** | 0.880** | 1× | High |
| **Dynamic Threshold** | 0.685 | 0.617 | 10× | Low |

*Co-Training results từ notebook 11
**Graph-based dùng binary classification

### Improvement over Baseline

| Method | F1-Macro Δ | Relative Improvement |
|--------|-----------|----------------------|
| Self-Training | +0.208 | +44.1% |
| Co-Training | +0.238 | +50.4% |
| Label Propagation | +0.388** | +82.2% |
| Label Spreading | +0.398** | +84.3% |
| Dynamic Threshold | +0.213 | +45.1% |

**Caveat: Graph-based methods dùng binary classification nên không so sánh trực tiếp

## Insights chính

### 1. Method Categories

#### Supervised Learning
- **Baseline**: Chỉ dùng labeled data
- **Performance**: F1=0.472 (baseline reference)
- **Use case**: Khi có đủ labeled data

#### Iterative Pseudo-Labeling
- **Self-Training**: Simple, effective
- **Co-Training**: Best balance (nếu có 2 views)
- **Dynamic Threshold**: Tốt cho imbalanced data
- **Performance**: F1=0.68-0.71 (+44-50%)
- **Use case**: Medium labeled data (5-10%)

#### Graph-Based SSL
- **Label Propagation/Spreading**: Highest accuracy
- **Performance**: F1=0.86-0.87 (+82-84%)
- **Use case**: Small data (<50K), low labeled ratio (<1%)
- **Limitation**: Binary only (memory constraint)

### 2. When to use each method

#### Baseline Supervised
✅ **Use when**:
- Có đủ labeled data (>10K samples)
- Không có budget cho labeling thêm
- Cần simplicity và fast inference
- F1=0.47 đủ cho use case

❌ **Avoid when**:
- Labeled data quá ít (<1K)
- Cần maximize accuracy
- Có unlabeled data sẵn

#### Self-Training
✅ **Use when**:
- Labeled data trung bình (1K-5K)
- Có nhiều unlabeled data
- Features không dễ phân chia thành views
- Cần balance giữa accuracy và complexity

❌ **Avoid when**:
- Model không confident (confidence < 0.7)
- Labeled data quá ít (< 500)
- Cần best accuracy (dùng graph-based)

#### Co-Training
✅ **Use when**:
- Có thể thiết kế 2 views independent
- Labeled data rất ít (<1K)
- Cần accuracy cao hơn Self-Training
- Có computational resources

❌ **Avoid when**:
- Features không thể split thành 2 views
- Views quá overlap (correlation > 0.8)
- Training time critical

#### Label Propagation/Spreading
✅ **Use when**:
- Dataset nhỏ (<50K samples)
- Labeled ratio rất thấp (<1%)
- Cần accuracy cao nhất
- Binary classification acceptable
- Có đủ memory

❌ **Avoid when**:
- Dataset lớn (>100K)
- Cần multi-class classification
- Memory hạn chế
- Online learning required

#### Dynamic Threshold
✅ **Use when**:
- Class imbalance nghiêm trọng
- Quan tâm recall của lớp hiếm
- Optimize F1-macro (không chỉ accuracy)
- Có đủ labeled samples per class

❌ **Avoid when**:
- Data balanced
- Labeled data quá ít per class (<50)
- Chỉ quan tâm accuracy

### 3. Computational Cost Analysis

#### Training Time (relative to baseline)

| Method | Training Time | Iterations | Models/Iter |
|--------|---------------|------------|-------------|
| Baseline | 1× | 1 | 1 |
| Self-Training | 10× | 10 | 1 |
| Co-Training | 20× | 10 | 2 |
| Label Prop/Spread | 1× | - | - |
| Dynamic Threshold | 10× | 10 | 1 |

#### Memory Usage

| Method | Memory | Reason |
|--------|--------|--------|
| Baseline | Low | Single model |
| Self-Training | Low | Single model, iterative |
| Co-Training | Low | Two small models |
| Label Prop | **High** | n×n similarity matrix |
| Label Spread | **High** | n×n similarity matrix |
| Dynamic | Low | Single model + τ_c array |

#### Inference Time

| Method | Inference | Scalability |
|--------|-----------|-------------|
| Baseline | Fast | Excellent |
| Self-Training | Fast | Excellent |
| Co-Training | Medium | Good (2 models) |
| Label Prop | **Slow** | Poor (need all data) |
| Label Spread | **Slow** | Poor (need all data) |
| Dynamic | Fast | Excellent |

### 4. Label Efficiency Comparison

**Scenario**: 10% labeled data

| Method | F1-Macro | Label Efficiency Score* |
|--------|----------|------------------------|
| Baseline | 0.472 | 1.00 (baseline) |
| Self-Training | 0.680 | 1.44 |
| Co-Training | 0.710 | 1.50 |
| Label Prop | 0.860** | 1.82** |
| Label Spread | 0.870** | 1.84** |
| Dynamic | 0.685 | 1.45 |

*Label Efficiency Score = (F1 / Baseline F1)
**Binary classification

**Insight**: Graph-based methods có label efficiency cao nhất nhưng giới hạn ở binary

### 5. Robustness Analysis

#### To Class Imbalance
- ❌ Baseline: Rất yếu (F1=0.0 cho "Good" class)
- ⚠️ Self-Training: Có vấn đề, cải thiện chậm
- ✅ Co-Training: Tốt hơn nhờ dual views
- ✅ Label Prop/Spread: Tốt (graph structure helps)
- ✅✅ Dynamic Threshold: Tốt nhất (designed for imbalance)

#### To Noise
- ✅ Baseline: Không bị noise từ pseudo-labels
- ❌ Self-Training: Nhạy cảm với noisy pseudo-labels
- ⚠️ Co-Training: Agreement mechanism giảm noise
- ✅ Label Spreading: Regularization giúp robust
- ⚠️ Dynamic Threshold: Phụ thuộc vào p_data estimate

#### To Hyperparameters
- ✅ Baseline: Ít hyperparameters
- ❌ Self-Training: Rất nhạy với TAU
- ❌ Co-Training: Nhạy với TAU, K_BEST, view design
- ⚠️ Label Prop: Nhạy với N_NEIGHBORS
- ⚠️ Label Spread: Thêm ALPHA parameter
- ❌ Dynamic: Nhạy với TAU_BASE và p_data

## Decision Tree - Method Selection

```
START
│
├─ Dataset size > 100K? 
│  ├─ YES → Self-Training hoặc Dynamic Threshold
│  └─ NO → Continue
│
├─ Memory limited?
│  ├─ YES → Self-Training, Co-Training, hoặc Dynamic
│  └─ NO → Continue
│
├─ Labeled ratio < 1%?
│  ├─ YES → Label Spreading (nếu size OK)
│  └─ NO → Continue
│
├─ Binary classification OK?
│  ├─ YES → Label Spreading (best accuracy)
│  └─ NO → Continue
│
├─ Can design 2 independent views?
│  ├─ YES → Co-Training
│  └─ NO → Continue
│
├─ Class imbalance severe?
│  ├─ YES → Dynamic Threshold
│  └─ NO → Self-Training
```

## Recommendations by Use Case

### Use Case 1: Alert System cho AQI
**Requirement**: High recall cho lớp nguy hiểm

**Recommended**: Dynamic Threshold Self-Training
- ✅ Tăng recall cho Hazardous/Very_Unhealthy
- ✅ Acceptable F1-macro (0.685)
- ✅ Multi-class support
- ✅ Scalable

### Use Case 2: Research với Small Dataset
**Requirement**: Highest accuracy possible

**Recommended**: Label Spreading
- ✅ Highest F1-macro (0.87)
- ✅ Tốt với labeled ratio thấp
- ⚠️ Binary only
- ⚠️ Không scale với large data

### Use Case 3: Production System với Large Data
**Requirement**: Balance accuracy, speed, scalability

**Recommended**: Self-Training hoặc Co-Training
- ✅ Good accuracy (F1=0.68-0.71)
- ✅ Scalable
- ✅ Fast inference
- ✅ Multi-class support

### Use Case 4: Limited Labeled Budget
**Requirement**: Maximum leverage of unlabeled data

**Recommended**: Co-Training
- ✅ Best label efficiency trong scalable methods
- ✅ F1=0.71 với 10% labels
- ⚠️ Cần thiết kế views carefully

## Bài học quan trọng

### 1. No silver bullet
- Không có phương pháp nào tốt nhất cho mọi case
- Trade-offs: accuracy ↔ speed ↔ memory ↔ scalability
- Domain knowledge + constraints → best choice

### 2. Binary vs Multi-class
- Binary: Simple, memory-efficient, dễ optimize
- Multi-class: Chi tiết hơn, harder, cần nhiều data
- Graph-based bắt buộc binary với large dataset

### 3. Validation strategy
- Validation set critical cho iterative methods
- Test set chỉ dùng cuối cùng
- Monitor convergence để early stopping

### 4. Implementation complexity
- Baseline/Self-Training: Easy
- Co-Training: Medium (view design tricky)
- Graph-based: Easy (sklearn built-in)
- Dynamic Threshold: Medium (cần implement τ_c)

### 5. Production considerations
- Inference speed quan trọng cho real-time
- Memory footprint ảnh hưởng deployment
- Retraining frequency phụ thuộc method
- Model interpretability varies

## Liên kết

- **Notebook**: `notebooks/14_Baseline_And_Comparison.ipynb`
- **Previous**: [13 - Question 04 (Dynamic Threshold)](13_question04.md)
- **Related**: All previous notebooks (01-13)
