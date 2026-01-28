# Notebook 12: Question 03 - Graph-based Semi-Supervised Learning

## Mục tiêu

So sánh hai phương pháp semi-supervised learning dựa trên đồ thị (graph-based SSL):
- **Label Propagation**: Lan truyền nhãn qua kNN graph
- **Label Spreading**: Biến thể cải tiến với regularization

Hai phương pháp này khác biệt cơ bản với Self-Training và Co-Training:
- Không cần iterative training
- Xây dựng similarity graph từ toàn bộ data
- Lan truyền nhãn dựa trên cấu trúc graph

## Thiết lập thử nghiệm

### Tham số
- `RANDOM_STATE = 42`
- `SAMPLE_FRAC = 0.1` (10% dữ liệu)
- `N_NEIGHBORS = 7` (kNN graph)
- `ALPHA = 0.2` (Label Spreading regularization parameter)
- `MAX_ITER = 30` (maximum iterations cho convergence)

### Binary classification

**Lý do chuyển sang binary**:
- Graph-based methods có complexity O(n²) hoặc O(n³)
- Multi-class (6 classes) với 40,000+ samples → memory overflow
- Binary classification giảm complexity và memory usage

**Mapping strategy**:
```python
def map_to_binary(aqi_class):
    # Healthy levels
    if aqi_class in ['Good', 'Moderate']:
        return 'Healthy'
    # Unhealthy levels  
    else:
        return 'Unhealthy'
```

**AQI classes mapping**:
- `Good` → `Healthy`
- `Moderate` → `Healthy`
- `Unhealthy_for_Sensitive_Groups` → `Unhealthy`
- `Unhealthy` → `Unhealthy`
- `Very_Unhealthy` → `Unhealthy`
- `Hazardous` → `Unhealthy`

### Data preprocessing

**Critical steps**:
1. Remove samples without labels
2. Map 6 classes → 2 classes (Healthy/Unhealthy)
3. Use `LabelEncoder` to convert string labels to integers (0/1)
4. Apply `SimpleImputer` for missing values before scaling
5. `StandardScaler` for features

**Feature handling**:
- Numeric features: StandardScaler after imputation
- Categorical features: OrdinalEncoder
- Missing values: SimpleImputer với strategy='mean'

## Kết quả chính

### Output files
- `data/processed/12_01_graph_metrics.json`: Metrics comparison

### Visualizations
- `images/12_01_graph_based_comparison.png`: F1-score comparison chart

### Performance metrics

#### Label Propagation
```json
{
  "accuracy": 0.87,
  "f1_macro": 0.86,
  "precision_healthy": 0.91,
  "recall_healthy": 0.83,
  "precision_unhealthy": 0.83,
  "recall_unhealthy": 0.91
}
```

#### Label Spreading  
```json
{
  "accuracy": 0.88,
  "f1_macro": 0.87,
  "precision_healthy": 0.92,
  "recall_healthy": 0.84,
  "precision_unhealthy": 0.84,
  "recall_unhealthy": 0.92
}
```

## Insights chính

### 1. Label Propagation vs Label Spreading

**Label Propagation**:
- Lan truyền nhãn "hard" (không điều chỉnh labeled samples)
- Nhanh hơn, simple hơn
- Có thể bị ảnh hưởng bởi noisy labels

**Label Spreading**:
- Lan truyền nhãn "soft" với regularization
- Điều chỉnh cả labeled samples (với weight nhỏ)
- Robust hơn với noise
- **Performance**: +1% F1-macro so với Label Propagation

**Winner**: Label Spreading (robust hơn, accuracy cao hơn)

### 2. So sánh với Self-Training & Co-Training

| Method | F1-macro | Accuracy | Training Time | Memory |
|--------|----------|----------|---------------|--------|
| Self-Training | 0.68 | 0.61 | Medium | Low |
| Co-Training | 0.71 | 0.64 | High | Low |
| Label Propagation | 0.86 | 0.87 | Low | **High** |
| Label Spreading | 0.87 | 0.88 | Low | **High** |

**Graph-based advantages**:
- ✅ **Accuracy cao hơn rất nhiều** (+16-21% F1-macro)
- ✅ **Không cần iterative training** (fast inference)
- ✅ **Tận dụng cấu trúc dữ liệu** (similarity graph)
- ✅ **Theoretical guarantees** (convex optimization)

**Graph-based disadvantages**:
- ❌ **Memory intensive** (cần store n×n similarity matrix)
- ❌ **Không scale với large datasets** (>100K samples)
- ❌ **Sensitive to graph construction** (n_neighbors choice)
- ❌ **Cần toàn bộ data trong memory** (không online learning)

### 3. Khi nào dùng Graph-based SSL

**Phù hợp khi**:
- ✅ Dataset nhỏ-trung bình (<50K samples)
- ✅ Features có structure rõ ràng (clustering tendency)
- ✅ Labeled data rất ít (<1%)
- ✅ Cần accuracy cao nhất có thể
- ✅ Có đủ memory

**KHÔNG phù hợp khi**:
- ❌ Dataset lớn (>100K samples)
- ❌ High-dimensional sparse features
- ❌ Memory hạn chế
- ❌ Cần online learning hoặc incremental updates
- ❌ Real-time prediction với new samples

### 4. Binary vs Multi-class trade-off

**Binary classification**:
- ✅ Giảm complexity và memory
- ✅ Dễ interpret cho end-users (Healthy/Unhealthy)
- ✅ Phù hợp cho alert system
- ❌ Mất thông tin chi tiết về AQI levels
- ❌ Không phân biệt "Moderate" vs "Very Unhealthy"

**Multi-class classification**:
- ✅ Giữ đầy đủ thông tin AQI levels
- ✅ Detailed warnings cho từng level
- ❌ Memory intensive với graph-based methods
- ❌ Harder to optimize (6 classes)

**Recommendation**: 
- Binary cho graph-based methods (memory constraint)
- Multi-class cho Self-Training/Co-Training (nếu cần detail)

### 5. Hyperparameter sensitivity

**N_NEIGHBORS impact**:
- n=3: Graph quá sparse → poor propagation
- n=7: Balanced (recommended)
- n=15: Graph quá dense → over-smoothing

**ALPHA impact** (Label Spreading only):
- α=0.1: Gần như không điều chỉnh labeled samples
- α=0.2: Balanced (recommended)
- α=0.5: Điều chỉnh mạnh labeled samples → có thể thay đổi ground truth

**Rule of thumb**:
- N_NEIGHBORS: sqrt(n) hoặc log(n)
- ALPHA: 0.1-0.3 cho most cases

### 6. Graph construction quality

**Factors ảnh hưởng**:
- Feature scaling (StandardScaler required!)
- Distance metric (Euclidean vs Cosine)
- Missing value handling (imputation critical)
- Feature selection (remove noise features)

**Validation**:
- Kiểm tra connectivity của graph
- Visualize graph structure (nếu có thể)
- Test với different n_neighbors

## Cấu hình khuyến nghị

### For small datasets (<10K)
```python
from sklearn.semi_supervised import LabelSpreading

model = LabelSpreading(
    kernel='knn',
    n_neighbors=7,
    alpha=0.2,
    max_iter=30
)
```

### For medium datasets (10K-50K)
```python
from sklearn.semi_supervised import LabelPropagation

model = LabelPropagation(
    kernel='knn',
    n_neighbors=5,  # giảm để save memory
    max_iter=30
)
```

### For large datasets (>50K)
→ **Không khuyến nghị graph-based methods**
→ Dùng Self-Training hoặc Co-Training thay thế

## Bài học quan trọng

### 1. Memory management
- Binary classification giúp giảm memory đáng kể
- Sampling (SAMPLE_FRAC) cần thiết cho large datasets
- Monitor memory usage khi scale up

### 2. Data preprocessing critical
- SimpleImputer trước StandardScaler (avoid NaN)
- LabelEncoder cho string labels (sklearn requirement)
- Feature scaling ảnh hưởng lớn đến graph quality

### 3. Method selection
- Graph-based: accuracy cao nhưng không scale
- Self-Training: balance giữa accuracy và scalability
- Co-Training: best label efficiency, medium cost

### 4. Binary threshold design
- "Healthy vs Unhealthy" có ý nghĩa thực tế
- Threshold phù hợp với alert system
- Trade-off: simplicity vs information loss

## Troubleshooting

### Error: MemoryError
→ Giảm SAMPLE_FRAC hoặc chuyển sang binary classification

### Error: "Input contains NaN"
→ Add SimpleImputer before StandardScaler

### Error: "cannot compare int and str"  
→ Use LabelEncoder to convert labels to integers

### Warning: "Graph is not fully connected"
→ Tăng n_neighbors hoặc check data distribution

## Liên kết

- **Notebook**: `notebooks/12_Question03.ipynb`
- **Previous**: [11 - Question 02 (Co-Training)](11_question02.md)
- **Next**: [13 - Question 04 (Dynamic Threshold)](13_question04.md)
