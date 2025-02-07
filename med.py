from flask import Blueprint, render_template, request, url_for
import google.generativeai as genai

# Configure Gemini AI
genai.configure(api_key="AIzaSyB1AQBRcXw9b3dPAJcvpNZu3GEBolGbiZQ")
model = genai.GenerativeModel("gemini-1.5-flash")

# Create a Flask Blueprint for medicine-related routes
medicine_bp = Blueprint('medicine', __name__)

def generate_medicine_info(medicine_name):
    """ Fetch structured medicine information from Gemini API """
    prompt = f"""
    Provide detailed structured information (1n 200 words) about this medicine '{medicine_name}'. 
    Ensure output follows this format without markdown:
    
    Medicine Name: the sicnetif name of <Medicine_Name> is <scientific name>.and this medicine is manufacutred by <manufacturer name>
    Medicine Type/Category: <Category>
    Dosage (Age-wise): Dosage can be vary with the Age groups
    for <Age group1> : <Dosage_Details with age groups> like wise
    Side Effects: <Side_Effects>
    Usage: <Usage>
    Precautions: <Precautions>
    Interactions: <Interactions>
    Storage Instructions: <Storage>
    Warnings: <Warnings>
    """

    response = model.generate_content(prompt)
    if response and response.text:
        lines = response.text.split("\n")
        medicine_info = { 
            "name": "", "type": "", "dosage": "", "side_effects": "",
            "usage": "", "precautions": "", "interactions": "", "storage": "", "warnings": ""
        }

        for line in lines:
            key_map = {
                "Medicine Name:": "name",
                "Medicine Type/Category:": "type",
                "Dosage (Age-wise):": "dosage",
                "Side Effects:": "side_effects",
                "Usage:": "usage",
                "Precautions:": "precautions",
                "Interactions:": "interactions",
                "Storage Instructions:": "storage",
                "Warnings:": "warnings"
            }
            for key, field in key_map.items():
                if key in line:
                    medicine_info[field] = line.replace(key, "").strip()

        return medicine_info
    return None

@medicine_bp.route('/medicine-info', methods=['GET', 'POST'])
def get_medicine_info():
    response_data = None
    if request.method == 'POST':
        medicine_name = request.form.get('medicineInput')
        if medicine_name:
            response_data = generate_medicine_info(medicine_name)

    return render_template('medicine_information.html', response=response_data)
