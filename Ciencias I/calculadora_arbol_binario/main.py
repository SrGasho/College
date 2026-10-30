import sys

from calculator.evaluator import EvaluationError, evaluate_postorder
from calculator.parser import build_expression_tree
from calculator.tokenizer import ExpressionError


def main() -> None:
    expression = " ".join(sys.argv[1:]).strip()
    if not expression:
        expression = input("Escribe una expresión: ")

    try:
        root, postfix = build_expression_tree(expression)
        result = evaluate_postorder(root)
    except (ExpressionError, EvaluationError) as error:
        print(f"Error: {error}")
        return

    print(f"Postorden: {' '.join(result.postorder)}")
    print(f"Postfija: {' '.join(postfix)}")
    for step in result.steps:
        if step["action"] == "calculate":
            print(f"{step['left']} {step['value']} {step['right']} = {step['result']}")
    print(f"Resultado: {result.value}")


if __name__ == "__main__":
    main()
