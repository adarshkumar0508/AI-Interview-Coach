
# train_model.py

import joblib
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report
)

# Small demonstration dataset.
# Labels are manually assigned for this prototype.
data = [
    ("Python is a programming language.", "Needs Improvement"),
    ("SQL is used to query databases.", "Needs Improvement"),
    ("A list stores multiple values.", "Needs Improvement"),
    ("A stack follows last in first out.", "Needs Improvement"),
    ("An API lets software systems communicate.", "Needs Improvement"),
    ("Machine learning learns patterns from data.", "Needs Improvement"),
    ("A database stores organized information.", "Needs Improvement"),
    ("A loop repeats a block of code.", "Needs Improvement"),

    (
        "Python is a high level programming language. "
        "It supports multiple programming paradigms and has "
        "libraries for automation, data analysis and web development.",
        "Good"
    ),
    (
        "SQL is used to retrieve and manipulate relational data. "
        "SELECT retrieves records, WHERE filters them, and JOIN "
        "combines related tables using common columns.",
        "Good"
    ),
    (
        "A stack follows last in first out. Push adds an item "
        "and pop removes the most recently added item. "
        "Stacks are useful for undo operations and function calls.",
        "Good"
    ),
    (
        "Machine learning enables systems to learn patterns from data. "
        "Supervised learning uses labelled examples, while "
        "unsupervised learning finds patterns in unlabelled data.",
        "Good"
    ),
    (
        "An API defines how software components communicate. "
        "For example, a Flask REST API can receive an HTTP request, "
        "process its data, and return a JSON response.",
        "Good"
    ),
    (
        "A database organizes and stores information. "
        "Relational databases use tables, rows and columns. "
        "SQL helps query and update the stored records.",
        "Good"
    ),
    (
        "A Python function is a reusable block of code. "
        "It can accept parameters, perform operations, and return "
        "a result. Functions improve readability and reuse.",
        "Good"
    ),
    (
        "A list is mutable, so its contents can be changed. "
        "A tuple is immutable, so its elements cannot normally "
        "be reassigned. Both can store multiple values.",
        "Good"
    ),

    (
        "I think Python is useful because it is easy and "
        "has many things. It is good for coding.",
        "Average"
    ),
    (
        "SQL works with data. There are tables and queries. "
        "We use it in databases for different purposes.",
        "Average"
    ),
    (
        "A stack is a data structure. It stores items and "
        "we can add or remove things from it.",
        "Average"
    ),
    (
        "Machine learning is a part of AI. It uses data "
        "and computers to make predictions.",
        "Average"
    ),
    (
        "An API connects applications. It sends and receives "
        "information between different systems.",
        "Average"
    ),
    (
        "A database keeps records. It can store lots of "
        "information and helps us retrieve it.",
        "Average"
    ),
    (
        "A function performs a task. We call it when we "
        "need that task in our program.",
        "Average"
    ),
    (
        "A list and a tuple both contain elements. "
        "They are useful in Python for storing data.",
        "Average"
    ),
]

texts = [answer for answer, label in data]
labels = [label for answer, label in data]

X_train, X_test, y_train, y_test = train_test_split(
    texts,
    labels,
    test_size=0.25,
    random_state=42,
    stratify=labels
)

model = Pipeline([
    ("tfidf", TfidfVectorizer(ngram_range=(1, 2))),
    ("classifier", LogisticRegression(max_iter=1000))
])

model.fit(X_train, y_train)

predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)
precision = precision_score(
    y_test, predictions, average="macro", zero_division=0
)
recall = recall_score(
    y_test, predictions, average="macro", zero_division=0
)
f1 = f1_score(
    y_test, predictions, average="macro", zero_division=0
)

print("\n===== MODEL EVALUATION =====")
print(f"Accuracy:  {accuracy:.2%}")
print(f"Precision: {precision:.2%}")
print(f"Recall:    {recall:.2%}")
print(f"F1-score:  {f1:.2%}")

print("\n===== CLASSIFICATION REPORT =====")
print(classification_report(y_test, predictions, zero_division=0))

# Save evaluation metrics for the dashboard
metrics = {
    "accuracy": float(accuracy),
    "precision": float(precision),
    "recall": float(recall),
    "f1_score": float(f1)
}

joblib.dump(metrics, "model_metrics.joblib")
print("Saved evaluation metrics: model_metrics.joblib")

# Train the final model on all labelled examples for use by Flask.
model.fit(texts, labels)
joblib.dump(model, "answer_model.joblib")

print("Saved trained model: answer_model.joblib")
