from semantic_eval import evaluate_answer

expected = "Python is a programming language."
student = "Python is used for programming."

score = evaluate_answer(expected, student)

print("Score:", score)
