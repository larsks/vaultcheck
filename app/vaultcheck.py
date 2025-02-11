#!/usr/bin/python3

from flask import Flask, request
import time

app = Flask(__name__)

results = {}


@app.route("/report", methods=["POST"])
def report():
    data = request.form | {k: request.files[k].read().decode().strip() for k in request.files}
    if "nodename" in data:
        results[data['nodename']] = {
            "http_code": int(data.get("http_code", 0)),
            "content": data.get("content", ""),
            "when": time.time(),
        }
    return 'OK', {"Content-type": "text/plain"}


@app.route("/")
def index():
    response = []
    now = time.time()
    if results:
        maxlen = max(len(name) for name in results)
        for nodename, data in results.items():
            response.append(f"{nodename:{maxlen}} {data['http_code']:03} {now-data['when']:.2f}")

    return "\n".join(response) + '\n', {"Content-type": "text/plain"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
