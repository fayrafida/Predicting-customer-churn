from prometheus_client import start_http_server, Gauge
import time
import json

# Inisialisasi metrik Prometheus
accuracy = Gauge("model_accuracy", "Akurasi model churn prediction")
precision = Gauge("model_precision", "Precision model churn prediction")
recall = Gauge("model_recall", "Recall model churn prediction")
f1_score = Gauge("model_f1_score", "F1-score model churn prediction")
latency = Gauge("model_latency_ms", "Waktu inferensi rata-rata dalam milidetik")

def update_metrics():
    while True:
        try:
            with open("metrics.json", "r") as f:
                metrics = json.load(f)
                accuracy.set(metrics.get("accuracy", 0))
                precision.set(metrics.get("precision", 0))
                recall.set(metrics.get("rec", 0))  # "rec" dari metrics.json
                f1_score.set(metrics.get("f1_score", 0))
                latency.set(metrics.get("latency_ms", 0))
        except Exception as e:
            print("Gagal membaca file metrics.json:", e)
        time.sleep(10)

if __name__ == "__main__":
    print("Prometheus exporter aktif di http://localhost:8000/metrics")
    start_http_server(8000)
    update_metrics()
