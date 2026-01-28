"""
AirGuard - Flask Web Application
Ứng dụng web để trực quan hóa kết quả phân tích chất lượng không khí
"""

from flask import Flask, render_template, send_from_directory, request
import json
import pandas as pd
import os

app = Flask(__name__)

# Custom Jinja filter to pretty-print JSON
def pretty_json(value):
    """
    Filter to pretty-print JSON.
    If value is a string, it tries to parse it as JSON.
    If it's a dict/list, it dumps it.
    """
    # Handle single quotes from notebook outputs if they exist
    if isinstance(value, str):
        try:
            # Replace single quotes with double quotes for valid JSON
            # This is a simple replacement, might not cover all edge cases
            value_str = value.replace("'", '"')
            # For boolean values which are True/False in Python
            value_str = value_str.replace("True", "true").replace("False", "false")
            value = json.loads(value_str)
        except (json.JSONDecodeError, TypeError):
            # Not a valid JSON-like string, return as is
            return value
    
    if isinstance(value, (dict, list)):
        return json.dumps(value, indent=2, ensure_ascii=False)
    
    return value

app.jinja_env.filters['pretty_json'] = pretty_json

# Cấu hình đường dẫn
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(BASE_DIR, 'images')
DATA_DIR = os.path.join(BASE_DIR, 'data', 'processed')

# Hàm hỗ trợ để đọc dữ liệu
def load_json(filename):
    """Đọc file JSON"""
    filepath = os.path.join(DATA_DIR, filename)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def load_csv(filename, nrows=None):
    """Đọc file CSV"""
    filepath = os.path.join(DATA_DIR, filename)
    if os.path.exists(filepath):
        return pd.read_csv(filepath, nrows=nrows)
    return None

def get_image_path(filename):
    """Trả về đường dẫn tương đối của ảnh"""
    return f'/images/{filename}'

# Routes cho static files
@app.route('/images/<path:filename>')
def serve_image(filename):
    """Phục vụ file ảnh"""
    return send_from_directory(IMAGES_DIR, filename)

@app.route('/data/processed/<path:filename>')
def serve_processed_data(filename):
    """Phục vụ file dữ liệu đã xử lý"""
    return send_from_directory(DATA_DIR, filename)

# Trang chủ
@app.route('/')
def index():
    """Trang chủ - Tổng quan dự án"""
    return render_template('index.html')

# 01 - Tiền xử lý và EDA
@app.route('/preprocessing-eda')
def preprocessing_eda():
    """Trang tiền xử lý dữ liệu và phân tích thăm dò"""
    data = {
        'missing_rate': load_csv('01_missing_rate.csv'),
        'class_distribution': load_csv('01_class_distribution.csv'),
        'raw_data_sample': load_csv('01_raw_data_sample.csv', nrows=10),
        'cleaned_data_sample': load_csv('01_cleaned_data_sample.csv', nrows=10),
        'images': {
            'class_distribution': get_image_path('01_class_distribution.png')
        }
    }
    return render_template('01_preprocessing_eda.html', data=data)

# 02 - Chuẩn bị dữ liệu Semi-supervised
@app.route('/semi-dataset')
def semi_dataset():
    """Trang chuẩn bị dữ liệu cho Semi-supervised Learning"""
    data = {
        'dataset_sample': load_csv('02_dataset_for_semi_sample.csv', nrows=10)
    }
    return render_template('02_semi_dataset.html', data=data)

# 03 - Chuẩn bị đặc trưng
@app.route('/feature-preparation')
def feature_preparation():
    """Trang chuẩn bị đặc trưng"""
    data = {
        'feature_list': load_csv('03_feature_list.csv'),
        'cleaned_data': load_csv('03_cleaned_data_loaded.csv', nrows=10)
    }
    return render_template('03_feature_preparation.html', data=data)

# 04 - Self-training
@app.route('/self-training')
def self_training():
    """Trang Self-training"""
    data = {
        'metrics': load_json('04_metrics_self_training.json'),
        'predictions_sample': load_csv('04_predictions_self_training_sample.csv', nrows=10),
        'alerts_sample': load_csv('04_alerts_self_training_sample.csv', nrows=10),
        'images': {
            'dynamics': get_image_path('04_self_training_dynamics.png')
        }
    }
    return render_template('04_self_training.html', data=data)

# 05 - Co-training
@app.route('/co-training')
def co_training():
    """Trang Co-training"""
    data = {
        'metrics': load_json('05_metrics_co_training.json'),
        'predictions_sample': load_csv('05_predictions_co_training_sample.csv', nrows=10),
        'alerts_sample': load_csv('05_alerts_co_training_sample.csv', nrows=10),
        'images': {
            'dynamics': get_image_path('05_co_training_dynamics.png')
        }
    }
    return render_template('05_co_training.html', data=data)

# 06 - Mô hình phân loại
@app.route('/classification')
def classification():
    """Trang mô hình phân loại"""
    data = {
        'metrics': load_json('06_metrics.json'),
        'metrics_file': '06_metrics.json',
        'classification_report': load_csv('06_classification_report.csv'),
        'classification_report_file': '06_classification_report.csv',
        'predictions_sample': load_csv('06_predictions_sample.csv', nrows=10),
        'predictions_sample_file': '06_predictions_sample.csv',
        'dataset_sample': load_csv('06_dataset_sample.csv', nrows=10),
        'dataset_sample_file': '06_dataset_sample.csv',
        'images': {
            'confusion_matrix': get_image_path('06_confusion_matrix.png')
        }
    }
    return render_template('06_classification.html', data=data)

# 07 - Mô hình hồi quy
@app.route('/regression')
def regression():
    """Trang mô hình hồi quy"""
    data = {
        'metrics': load_json('07_regression_metrics.json'),
        'metrics_file': '07_regression_metrics.json',
        'missing_values': load_csv('07_missing_values.csv'),
        'missing_values_file': '07_missing_values.csv',
        'predictions_sample': load_csv('07_regression_predictions_sample.csv', nrows=10),
        'predictions_sample_file': '07_regression_predictions_sample.csv',
        'dataset_sample': load_csv('07_regression_dataset_sample.csv', nrows=10),
        'dataset_sample_file': '07_regression_dataset_sample.csv',
        'images': {
            'actual_vs_predicted': get_image_path('07_actual_vs_predicted.png'),
            'target_distribution': get_image_path('07_target_distribution.png')
        }
    }
    return render_template('07_regression.html', data=data)

# 08 - Dự báo ARIMA
@app.route('/arima-forecasting')
def arima_forecasting():
    """Trang dự báo chuỗi thời gian ARIMA"""
    data = {
        'images': {
            'raw_timeseries': get_image_path('08_raw_timeseries_30days.png'),
            'rolling_statistics': get_image_path('08_rolling_statistics.png'),
            'acf_plot': get_image_path('08_acf_plot.png'),
            'pacf_plot': get_image_path('08_pacf_plot.png'),
            'forecast_vs_actual': get_image_path('08_forecast_vs_actual.png'),
            'hourly_seasonality': get_image_path('08_hourly_seasonality.png')
        }
    }
    return render_template('08_arima_forecasting.html', data=data)

# 09 - Báo cáo Semi-supervised
@app.route('/semi-supervised-report')
def semi_supervised_report():
    """Trang báo cáo Semi-supervised Learning"""
    data = {
        'images': {
            'supervised_vs_semi': get_image_path('09_supervised_vs_semi_supervised.png'),
            'self_training_dynamics': get_image_path('09_self_training_dynamics_report.png'),
            'self_training_timeline': get_image_path('09_self_training_station_timeline.png'),
            'self_training_alerts': get_image_path('09_self_training_top_alerts.png'),
            'co_training_dynamics': get_image_path('09_co_training_dynamics_report.png'),
            'co_training_timeline': get_image_path('09_co_training_station_timeline.png'),
            'co_training_alerts': get_image_path('09_co_training_top_alerts.png')
        }
    }
    return render_template('09_semi_supervised_report.html', data=data)

# 10 - Câu hỏi 01
@app.route('/question-01')
def question_01():
    """Trang câu hỏi 01"""
    data = {
        'images': {
            'f1_comparison': get_image_path('10_01_f1_macro_comparison.png'),
            'f1_heatmap': get_image_path('10_02_f1_macro_heatmap.png'),
            'f1_line_chart': get_image_path('10_03_f1_macro_line_chart.png')
        }
    }
    return render_template('10_question_01.html', data=data)

# 11 - Câu hỏi 02
@app.route('/question-02')
def question_02():
    """Trang câu hỏi 02"""
    data = {
        'images': {
            'co_training_default': get_image_path('11_01_co_training_default.png'),
            'co_training_line': get_image_path('11_02_co_training_line_chart.png')
        }
    }
    return render_template('11_question_02.html', data=data)

# 12 - Câu hỏi 03
@app.route('/question-03')
def question_03():
    """Trang câu hỏi 03"""
    data = {
        'images': {
            'graph_based_comparison': get_image_path('12_01_graph_based_comparison.png')
        }
    }
    return render_template('12_question_03.html', data=data)

# 13 - Câu hỏi 04
@app.route('/question-04')
def question_04():
    """Trang câu hỏi 04"""
    data = {
        'images': {
            'f1_comparison': get_image_path('13_01_f1_macro_comparison.png'),
            'f1_per_class': get_image_path('13_02_f1_per_class.png'),
            'recall_rare': get_image_path('13_03_recall_rare_classes.png'),
            'confidence_dist': get_image_path('13_DEBUG_confidence_distribution.png')
        }
    }
    return render_template('13_question_04.html', data=data)

# 14 - Baseline và So sánh
@app.route('/baseline-comparison')
def baseline_comparison():
    """Trang so sánh baseline"""
    data = {
        'images': {
            'f1_comparison': get_image_path('14_01_f1_macro_comparison.png'),
            'f1_heatmap': get_image_path('14_02_f1_heatmap.png'),
            'performance_vs_cost': get_image_path('14_03_performance_vs_cost.png'),
            'improvement_percentage': get_image_path('14_04_improvement_percentage.png')
        }
    }
    return render_template('14_baseline_comparison.html', data=data)

# Dashboard tương tác
@app.route('/interactive-dashboard', methods=['GET', 'POST'])
def interactive_dashboard():
    """Trang dashboard tương tác với tùy chỉnh thông số"""
    
    # Lấy tham số từ request, ưu tiên POST (form), sau đó GET (url args), cuối cùng là mặc định
    # request.values kết hợp cả form và args
    params = {
        'analysis_type': request.values.get('analysis_type', 'classification'),
        'num_samples': request.values.get('num_samples', '10'),
        'metric_type': request.values.get('metric_type', 'all'),
        'decimal_places': int(request.values.get('decimal_places', '2'))
    }
    
    # Chuyển đổi num_samples
    nrows = None if params['num_samples'] == 'all' else int(params['num_samples'])
    
    data = {}
    
    # Xử lý dữ liệu dựa trên loại phân tích
    if params['analysis_type'] == 'classification':
        metrics = load_json('06_metrics.json')
        predictions = load_csv('06_predictions_sample.csv', nrows=nrows)
        
        summary = {}
        if predictions is not None and not predictions.empty and 'actual' in predictions.columns and 'predicted' in predictions.columns:
            summary['Tổng số mẫu'] = len(predictions)
            summary['Số lượng dự đoán đúng'] = int((predictions['actual'] == predictions['predicted']).sum())
            summary['Tỷ lệ chính xác'] = (predictions['actual'] == predictions['predicted']).mean()
        
        data = { 'metrics': metrics, 'predictions': predictions, 'summary': summary }
            
    elif params['analysis_type'] == 'regression':
        metrics = load_json('07_regression_metrics.json')
        predictions = load_csv('07_regression_predictions_sample.csv', nrows=nrows)
        
        summary = {}
        if predictions is not None and not predictions.empty:
            summary['Tổng số mẫu'] = len(predictions)
            if 'actual' in predictions.columns and 'predicted' in predictions.columns:
                summary['Giá trị trung bình (Actual)'] = predictions['actual'].mean()
                summary['Giá trị trung bình (Predicted)'] = predictions['predicted'].mean()
                summary['Sai số tuyệt đối trung bình'] = (predictions['actual'] - predictions['predicted']).abs().mean()
        
        data = { 'metrics': metrics, 'predictions': predictions, 'summary': summary }
            
    elif params['analysis_type'] == 'semi_supervised':
        self_metrics = load_json('04_metrics_self_training.json')
        co_metrics = load_json('05_metrics_co_training.json')
        predictions = load_csv('04_predictions_self_training_sample.csv', nrows=nrows)
        
        combined_metrics = {}
        if self_metrics:
            for key, value in self_metrics.items():
                combined_metrics[f'Self-training: {key}'] = value
        if co_metrics:
            for key, value in co_metrics.items():
                combined_metrics[f'Co-training: {key}'] = value
        
        summary = {}
        if self_metrics and co_metrics:
            for metric_name in ['f1_macro', 'f1_weighted', 'accuracy']:
                if metric_name in self_metrics and metric_name in co_metrics:
                    diff = co_metrics[metric_name] - self_metrics[metric_name]
                    summary[f'Chênh lệch {metric_name} (Co > Self)'] = diff
        
        data = { 'metrics': combined_metrics, 'predictions': predictions, 'summary': summary }

    # Nếu không load được dữ liệu, trả về None để template hiển thị message
    if not data.get('metrics') and (data.get('predictions') is None or data.get('predictions').empty):
        data = None

    return render_template('interactive_dashboard.html', params=params, data=data)

# So sánh mô hình
@app.route('/model-comparison', methods=['GET', 'POST'])
def model_comparison():
    """Trang so sánh các mô hình khác nhau"""

    # Lấy tham số, đặt mặc định cho GET
    if request.method == 'POST':
        models_to_compare = request.form.getlist('models')
        metric_to_compare = request.form.get('comparison_metric', 'f1_macro')
    else: # GET
        models_to_compare = ['classification', 'self_training', 'co_training'] # So sánh mặc định
        metric_to_compare = 'f1_macro'

    params = {
        'models': models_to_compare,
        'comparison_metric': metric_to_compare
    }
    
    comparison_results = None
    detailed_stats = None
    
    if len(params['models']) >= 1:
        results = []
        metric_name = params['comparison_metric']
        
        model_configs = {
            'classification': {'file': '06_metrics.json', 'name': 'Classification Model'},
            'regression': {'file': '07_regression_metrics.json', 'name': 'Regression Model'},
            'self_training': {'file': '04_metrics_self_training.json', 'name': 'Self-training'},
            'co_training': {'file': '05_metrics_co_training.json', 'name': 'Co-training'}
        }
        
        for model_key in params['models']:
            if model_key in model_configs:
                config = model_configs[model_key]
                metrics = load_json(config['file'])
                
                if metrics and metric_name in metrics:
                    score = metrics[metric_name]
                    results.append({'model_name': config['name'], 'score': score})
        
        if results:
            results.sort(key=lambda x: x['score'], reverse=True)
            
            for idx, result in enumerate(results):
                result['rank'] = idx + 1
                if idx == 0:
                    result['comment'] = 'Hiệu suất tốt nhất'
                elif idx == len(results) - 1 and len(results) > 1:
                    result['comment'] = 'Cần cải thiện'
                else:
                    result['comment'] = 'Hiệu suất tốt'
            
            comparison_results = results
            
            scores = [r['score'] for r in results]
            detailed_stats = {
                'Điểm cao nhất': max(scores),
                'Điểm thấp nhất': min(scores),
                'Điểm trung bình': sum(scores) / len(scores),
                'Chênh lệch (Max - Min)': max(scores) - min(scores),
                'Số mô hình so sánh': len(scores)
            }
    
    return render_template('model_comparison.html', 
                         params=params, 
                         comparison_results=comparison_results,
                         detailed_stats=detailed_stats)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
