import os
import papermill as pm

# Run notebooks end-to-end (semi-supervised + supervised + regression + ARIMA)
os.makedirs("notebooks/runs", exist_ok=True)

KERNEL = "KhaiPhaDuLieu"

# 1) Preprocessing + EDA
pm.execute_notebook(
    "notebooks/01_preprocessing_and_eda.ipynb",
    "notebooks/runs/01_preprocessing_and_eda.ipynb",
    parameters=dict(
        USE_UCIMLREPO=False,
        RAW_ZIP_PATH="data/raw/PRSA2017_Data_20130301-20170228.zip",
        OUTPUT_CLEANED_PATH="data/processed/01_cleaned.parquet",
        LAG_HOURS=[1, 3, 24],
    ),
    language="python",
    kernel_name=KERNEL,
)

# 2) NEW: Semi-supervised dataset preparation
pm.execute_notebook(
    "notebooks/02_semi_dataset_preparation.ipynb",
    "notebooks/runs/02_semi_dataset_preparation.ipynb",
    parameters=dict(
        CLEANED_PATH="data/processed/01_cleaned.parquet",
        OUTPUT_SEMI_DATASET_PATH="data/processed/02_dataset_for_semi.parquet",
        CUTOFF="2017-01-01",
        LABEL_MISSING_FRACTION=0.95,
        RANDOM_STATE=42,
    ),
    language="python",
    kernel_name=KERNEL,
)

# 3) Feature preparation for supervised baseline
pm.execute_notebook(
    "notebooks/03_feature_preparation.ipynb",
    "notebooks/runs/03_feature_preparation.ipynb",
    parameters=dict(
        CLEANED_PATH="data/processed/01_cleaned.parquet",
        OUTPUT_DATASET_PATH="data/processed/03_dataset_for_clf.parquet",
        DROP_ROWS_WITHOUT_TARGET=True,
    ),
    language="python",
    kernel_name=KERNEL,
)

# 4) Self-training
pm.execute_notebook(
    "notebooks/04_semi_self_training.ipynb",
    "notebooks/runs/04_semi_self_training.ipynb",
    parameters=dict(
        SEMI_DATASET_PATH="data/processed/02_dataset_for_semi.parquet",
        CUTOFF="2017-01-01",
        TAU=0.90,
        MAX_ITER=10,
        MIN_NEW_PER_ITER=20,
        VAL_FRAC=0.20,
        RANDOM_STATE=42,
        METRICS_PATH="data/processed/04_metrics_self_training.json",
        PRED_SAMPLE_PATH="data/processed/04_predictions_self_training_sample.csv",
        ALERTS_SAMPLE_PATH="data/processed/04_alerts_self_training_sample.csv",
        ALERT_FROM_CLASS="Unhealthy",
    ),
    language="python",
    kernel_name=KERNEL,
)

# 5) Co-training
pm.execute_notebook(
    "notebooks/05_semi_co_training.ipynb",
    "notebooks/runs/05_semi_co_training.ipynb",
    parameters=dict(
        SEMI_DATASET_PATH="data/processed/02_dataset_for_semi.parquet",
        CUTOFF="2017-01-01",
        TAU=0.90,
        MAX_ITER=10,
        MAX_NEW_PER_ITER=500,
        MIN_NEW_PER_ITER=20,
        VAL_FRAC=0.20,
        RANDOM_STATE=42,
        METRICS_PATH="data/processed/05_metrics_co_training.json",
        PRED_SAMPLE_PATH="data/processed/05_predictions_co_training_sample.csv",
        ALERTS_SAMPLE_PATH="data/processed/05_alerts_co_training_sample.csv",
        ALERT_FROM_CLASS="Unhealthy",
        VIEW1_COLS=None,
        VIEW2_COLS=None,
    ),
    language="python",
    kernel_name=KERNEL,
)

# 6) Supervised classification baseline
pm.execute_notebook(
    "notebooks/06_classification_modelling.ipynb",
    "notebooks/runs/06_classification_modelling.ipynb",
    parameters=dict(
        DATASET_PATH="data/processed/03_dataset_for_clf.parquet",
        CUTOFF="2017-01-01",
        METRICS_PATH="data/processed/06_metrics.json",
        PRED_SAMPLE_PATH="data/processed/06_predictions_sample.csv",
    ),
    language="python",
    kernel_name=KERNEL,
)

# 7) Regression
pm.execute_notebook(
    "notebooks/regression_modelling.ipynb",
    "notebooks/runs/regression_modelling_run.ipynb",
    parameters=dict(
        USE_UCIMLREPO=False,
        RAW_ZIP_PATH="data/raw/PRSA2017_Data_20130301-20170228.zip",
        LAG_HOURS=[1, 3, 24],
        HORIZON=1,
        TARGET_COL="PM2.5",
        OUTPUT_REG_DATASET_PATH="data/processed/07_dataset_for_regression.parquet",
        CUTOFF="2017-01-01",
        MODEL_OUT="07_regressor.joblib",
        METRICS_OUT="07_regression_metrics.json",
        PRED_SAMPLE_OUT="07_regression_predictions_sample.csv",
    ),
    language="python",
    kernel_name=KERNEL,
)

# 8) ARIMA
pm.execute_notebook(
    "notebooks/08_arima_forecasting.ipynb",
    "notebooks/runs/08_arima_forecasting.ipynb",
    parameters=dict(
        RAW_ZIP_PATH="data/raw/PRSA2017_Data_20130301-20170228.zip",
        STATION="Aotizhongxin",
        VALUE_COL="PM2.5",
        CUTOFF="2017-01-01",
        P_MAX=3,
        Q_MAX=3,
        D_MAX=2,
        IC="aic",
        ARTIFACTS_PREFIX="08_arima_pm25",
    ),
    language="python",
    kernel_name=KERNEL,
)

# 9) OPTIONAL: Summary report (read metrics and make charts)
pm.execute_notebook(
    "notebooks/09_semi_supervised_report.ipynb",
    "notebooks/runs/09_semi_supervised_report.ipynb",
    parameters=dict(
        BASELINE_METRICS_PATH="data/processed/06_metrics.json",
        SELF_METRICS_PATHS=["data/processed/04_metrics_self_training.json"],
        CO_METRICS_PATHS=["data/processed/05_metrics_co_training.json"],
        BASELINE_PRED_PATH="data/processed/06_predictions_sample.csv",
        SELF_ALERTS_PATH="data/processed/04_alerts_self_training_sample.csv",
        CO_ALERTS_PATH="data/processed/05_alerts_co_training_sample.csv",
        STATION_TO_PLOT=None,
        MAX_ROWS_PLOT=1500,
    ),
    language="python",
    kernel_name=KERNEL,
)

print("Đã chạy xong pipeline (semi-supervised + supervised + regression + ARIMA + report)")
