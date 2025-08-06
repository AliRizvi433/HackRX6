# app/clause_classifier.py

from typing import List
from transformers import pipeline

classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

LABELS = [
    "Eligibility",
    "Coverage",
    "Exclusions",
    "Waiting Period",
    "Renewal",
    "Premium Payment",
    "Migration",
    "Tax Benefits",
    "Pre-existing Diseases",
    "General Conditions",
]

def classify_clause(text: str) -> str:
    result = classifier(text, LABELS)
    return result['labels'][0]  # Best-matching clause type
