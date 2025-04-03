from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from transformers import pipeline

# Load emotion and intent models
emotion_pipeline = pipeline("text-classification", model="SamLowe/roberta-base-go_emotions", top_k=1)
intent_pipeline = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Emotion groups
EMOTION_GROUPS = {
    "happy": [
        "admiration", "amusement", "approval", "caring", "excitement",
        "gratitude", "joy", "love", "optimism", "pride", "relief", "surprise"
    ],
    "sadness": [
        "disappointment", "grief", "remorse", "sadness"
    ],
    "anger": [
        "anger", "annoyance", "disapproval", "disgust"
    ],
    "fear": [
        "embarrassment", "fear", "nervousness"
    ],
    "curiosity": [
        "confusion", "curiosity", "realization"
    ],
    "desire": [
        "desire"
    ],
    "neutral": [
        "neutral"
    ]
}

# Function to map an emotion to its group
def map_emotion_to_group(emotion_label):
    for group, labels in EMOTION_GROUPS.items():
        if emotion_label in labels:
            return group
    return "unknown" 

class ReviewAnalysis(APIView):
    def post(self, request):
        review_text = request.data.get("review")

        if not review_text:
            return Response({"error": "Review text is required"}, status=400)

        # Emotion Classification
        emotion_result = emotion_pipeline(review_text)
        specific_emotion = emotion_result[0][0]['label']
        emotion_group = map_emotion_to_group(specific_emotion)


        # Intent Classification
        intent_labels = ["praise intent", "complaint intent"]
        intent_result = intent_pipeline(review_text, candidate_labels=intent_labels)
        intent = intent_result['labels'][0]

        # Intent Classification (Specific Scope)
        intent_scope = [
            "packaging condition", 
            "delivery experience", 
            "overall product quality", 
            "value for money", 
            "product aesthetics", 
            "product durability"
        ]
        scope_result = intent_pipeline(review_text, candidate_labels=intent_scope)
        scope = scope_result['labels'][0]
        scope_scores = dict(zip(scope_result['labels'], scope_result['scores']))

        response_data = {
            "review": review_text,
            "emotion": {
                "group": emotion_group,
                "specific": specific_emotion 
            },
            "intent": intent,
            "scope": scope,
            "scope_scores": scope_scores
        }
        return Response(response_data)
