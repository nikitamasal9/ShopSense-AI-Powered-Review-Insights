from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from transformers import pipeline

emotion_pipeline = pipeline("text-classification", model="SamLowe/roberta-base-go_emotions", top_k=1)
intent_pipeline = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

class ReviewAnalysis(APIView):
    def post(self, request):
        review_text = request.data.get("review")

        if not review_text:
            return Response({"error": "Review text is required"}, status=400)

        # Emotion Classification
        emotion_result = emotion_pipeline(review_text)
        emotion = emotion_result[0][0]['label']

        # Intent Classification
        intent_labels = ["praise intent", "complaint intent"]
        intent_result = intent_pipeline(review_text, candidate_labels=intent_labels)
        intent = intent_result['labels'][0]  # Get the highest scoring label

        response_data = {
            "review": review_text,
            "emotion": emotion,
            "intent": intent
        }
        return Response(response_data)
