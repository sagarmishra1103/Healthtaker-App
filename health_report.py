import io

from flask import Flask, render_template, redirect, session, request, jsonify
import google.generativeai as genai
from PIL import Image


# Configure Google Generative AI API
genai.configure(api_key="AIzaSyDkOwxM93DgUM0Rfdzwv9G_9VquWDJlUaw")
model = genai.GenerativeModel(model_name="gemini-1.5-flash")


def analyze_health_report():
    file = request.files['file']
    image = Image.open(io.BytesIO(file.read()))
    prompt = "Analyze this health report in two-three paragraphs"
    response = model.generate_content([prompt, image])
    return jsonify({"description": response.text})






