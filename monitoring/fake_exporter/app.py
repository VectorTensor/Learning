
from flask import Flask, Response
import random
import time

app = Flask(__name__)


@app.route("/metrics")
def metrics():
    temp = random.uniform(20.0, 30.0)
    cpu = random.uniform(0.1, 0.9)
    time_100 = random.uniform(0.0, 10.0)
    time_200 = random.uniform(0.0, 10.0)
    return Response(
        f"# HELP app_temperature_celsius Fake temperature\n"
        f"# TYPE app_temperature_celsius gauge\n"
        f"app_temperature_celsius {temp}\n"
        f"# HELP app_cpu_usage_percent Fake CPU usage\n"
        f"# TYPE app_cpu_usage_percent gauge\n"
        f"app_cpu_usage_percent {cpu}\n"
        f"time_to_crawl{{report_id=\"100\"}} {time_100}\n"
        f"time_to_crawl{{report_id=\"101\"}} {time_100}\n",
        mimetype="text/plain"
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
