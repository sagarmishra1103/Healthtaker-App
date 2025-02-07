import io

from flask import Flask, render_template, redirect, session, request, jsonify
import google.generativeai as genai
from PIL import Image


# Configure Google Generative AI API
genai.configure(api_key="AIzaSyDkOwxM93DgUM0Rfdzwv9G_9VquWDJlUaw")
model = genai.GenerativeModel(model_name="gemini-1.5-flash")


def analyze_health_report():
    try:
        # Validate if file is uploaded
        if 'file' not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files['file']

        # Validate file type (ensure it's an image)
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        # Open the image
        image = Image.open(io.BytesIO(file.read()))

        # Enhanced AI prompt for structured analysis
        prompt = """
        You are an AI medical assistant. Analyze the provided health report image and extract relevant details.
        Provide a structured response including:
        - **Patient Information** (if available)
        - **Key Observations**
        - **Possible Diagnosis**
        - **Suggested Next Steps**
        - **Warnings or Concerns**
        
        Ensure the response is concise, medically informative, and easy to understand for a non-expert.
        """

        # Generate AI response
        response = model.generate_content([prompt, image])

        # Check if response is valid
        if response and hasattr(response, 'text'):
            structured_response = response.text.strip().split("\n\n")
            return jsonify({
                "patient_info": structured_response[0] if len(structured_response) > 0 else "Not available",
                "observations": structured_response[1] if len(structured_response) > 1 else "No observations found",
                "diagnosis": structured_response[2] if len(structured_response) > 2 else "No diagnosis available",
                "next_steps": structured_response[3] if len(structured_response) > 3 else "No next steps suggested",
                "warnings": structured_response[4] if len(structured_response) > 4 else "No warnings mentioned"
            })
        else:
            return jsonify({"error": "Failed to analyze the report"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500
