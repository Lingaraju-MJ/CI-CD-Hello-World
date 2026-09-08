from flask import Flask, Response
from prometheus_client import CONTENT_TYPE_LATEST, Counter, generate_latest

from app import get_greeting

web = Flask(__name__)
hits = Counter("hello_requests_total", "Times the home page was opened")


@web.route("/")
def home():
    hits.inc()
    return get_greeting()


@web.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


if __name__ == "__main__":
    web.run(host="0.0.0.0", port=8000)
