from flask import Flask, jsonify, render_template, request

from calculator.evaluator import EvaluationError, evaluate_postorder
from calculator.parser import build_expression_tree
from calculator.serializer import tree_to_dict
from calculator.tokenizer import ExpressionError


app = Flask(__name__)


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/api/calculate")
def calculate():
    data = request.get_json(silent=True) or {}
    expression = data.get("expression", "")

    try:
        root, postfix = build_expression_tree(expression)
    except ExpressionError as error:
        return jsonify({"ok": False, "error": str(error)}), 400

    try:
        evaluation = evaluate_postorder(root)
    except EvaluationError as error:
        return jsonify({
            "ok": False,
            "error": error.message,
            "error_node_id": error.node_id,
            "tree": tree_to_dict(root),
            "postfix": postfix,
            "postorder": error.postorder,
            "steps": error.steps,
        }), 422

    return jsonify({
        "ok": True,
        "tree": tree_to_dict(root),
        "postfix": postfix,
        "postorder": evaluation.postorder,
        "steps": evaluation.steps,
        "result": evaluation.value,
    })


if __name__ == "__main__":
    app.run(debug=True)
