from io import BytesIO
from flask import Flask, request, jsonify, send_file
from . import tasks

application = Flask("image-randomizer")


@application.route("/randomize", methods=["POST"])
def randomize():
    if not request.mimetype.startswith("image/png"):
        return jsonify({"error": "Ooops! Só sei lidar com imagens PNG!"}), 400

    token = tasks.enqueue_randomize_image_task(request.get_data())
    return jsonify({"token": token}), 201


@application.route("/randomize/<token>/status", methods=["GET"])
def randomize_status(token):
    task = tasks.get_task_result(token)
    if task["status"] in ("errored",):
        return jsonify({"error": str(task["exc"])})

    return jsonify({"status": task["status"]})


@application.route("/randomize/<token>/result", methods=["GET"])
def randomize_result(token):
    task = tasks.get_task_result(token)
    if task["status"] not in ("finished",):
        return jsonify({"message": "not found"}), 404

    return send_file(BytesIO(task["result"]), mimetype="image/png")


@application.route("/sum_even_numbers", methods=["POST"])
def sum_even_numbers():
    if not request.mimetype.startswith("text/plain"):
        return jsonify({"error": "Ooops! Preciso de um arquivo de texto!"}), 400

    token = tasks.enqueue_sum_even_numbers(request.get_data())
    return jsonify({"token": token}), 201


@application.route("/sum_even_numbers/<token>/status", methods=["GET"])
def sum_even_numbers_status(token):
    task = tasks.get_task_result(token)
    if task["status"] in ("errored",):
        return jsonify({"error": str(task["exc"])})

    return jsonify({"status": task["status"]})


@application.route("/sum_even_numbers/<token>/result", methods=["GET"])
def sum_even_numbers_result(token):
    task = tasks.get_task_result(token)
    if task["status"] not in ("finished",):
        return jsonify({"message": "not found"}), 404

    return jsonify({"result": task["result"]})
