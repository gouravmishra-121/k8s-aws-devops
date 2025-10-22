from flask import Flask, request, jsonify
from prometheus_client import Counter, Gauge, generate_latest, CONTENT_TYPE_LATEST
import os


app = Flask(__name__)


REQUESTS = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'http_status'])
IN_PROGRESS = Gauge('inprogress_requests', 'In-progress requests')


@app.route('/')
def index():
	IN_PROGRESS.inc()
	try:
		REQUESTS.labels(method=request.method, endpoint='/', http_status=200).inc()
		return jsonify({"message": "Hello from Flask on EKS!"})
	finally:
		IN_PROGRESS.dec()


@app.route('/health')
def health():
	return 'OK', 200


@app.route('/metrics')
def metrics():
	return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}


if __name__ == '__main__':
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port)