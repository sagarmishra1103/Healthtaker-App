from flask import Blueprint, render_template, request, url_for
import google.generativeai as genai

# Configure Gemini AI
genai.configure(api_key="AIzaSyB1AQBRcXw9b3dPAJcvpNZu3GEBolGbiZQ")
model = genai.GenerativeModel("gemini-1.5-flash")

# Create a Flask Blueprint for medicine-related routes
ai_suggestion_bp = Blueprint('ai', __name__)

def generate_ai_health_info(feeling, symptoms):
    """ Fetch structured health suggestions from Gemini AI with a personalized response """
    prompt = f"""
    Based on the user's feelings: '{feeling}' and symptoms: '{symptoms}', provide a summary of what the AI understood, explaining the possible causes of the symptoms and how they will inform the suggestions. Focus on providing detailed health suggestions that can help the user relax or manage their condition. Break the suggestions into 5 to 6 specific points, each sentences being two lines long. Include the following:

    The general cause or reason behind the symptom (e.g., cold, stress, fatigue) based on the condition and how it typically affects the body.
    Specific momentary relaxation techniques that can help alleviate the discomfort (e.g., breathing exercises, meditation, warm compress).
    Suggested changes in lifestyle for better health (e.g., vitamin C for cold).
    Over-the-counter medicines that can help with the condition, and when to take them (e.g., paracetamol for fever) only name the necessary drug.
    Predicition of diseases or conditions that the user is suffering on the basis of their symptoms and feelings in very few words.
    If the condition is severe, requires medical attention, only then suggest then seeing a doctor.

    Ensure the output follows this format without markdown also :
    
    Summary: <Summary>
    Suggestions: 
    <Suggestion 1>
    <Suggestion 2>
    <Suggestion 3>
    <Suggestion 4>
    <Suggestion 5>
    <Suggestion 6>
"""



    response = model.generate_content(prompt)
    if response and response.text:
        lines = response.text.split("\n")
        health_info = {
            "summary": "",
            "suggestions": []
        }

        for line in lines:
            if line.startswith("Summary:"):
                health_info["summary"] = line.replace("Summary:", "").strip()
            elif line.startswith("1.") or line.startswith("2.") or line.startswith("3.") or line.startswith("4.") or line.startswith("5.") or line.startswith("6."):
                health_info["suggestions"].append(line.strip())

        return health_info
    return None

@ai_suggestion_bp.route('/ai-suggestion', methods=['GET', 'POST'])
def get_ai_health_suggestion():
    response_data = None
    if request.method == 'POST':
        feeling = request.form.get('feelingInput')
        symptoms = request.form.get('symptomsInput')
        if feeling and symptoms:
            response_data = generate_ai_health_info(feeling, symptoms)

    return render_template('ai-suggestion.html', response=response_data)
