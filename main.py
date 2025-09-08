import json
from fastapi import FastAPI, File, UploadFile
from google.cloud import documentai
import google.generativeai as genai
from typing import Dict
import io

# Initialize FastAPI
app = FastAPI()

# Google Document AI Configuration
client = documentai.DocumentProcessorServiceClient()
DOCUMENT_AI_PROCESSOR = "projects/947476598105/locations/us/processors/c221ae91df258460"

# Configure Gemini AI
GENAI_API_KEY = "AIzaSyC3sz1Y5ch3j5NHMS3yauHaWS2XfgOrukc"
genai.configure(api_key=GENAI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")


@app.post("/process_lab_report/")
async def process_lab_report(file: UploadFile = File(...)) -> Dict:
    try:
        # Read image file
        image_bytes = await file.read()
        raw_document = {"content": image_bytes, "mime_type": "image/jpeg"}

        # Process document with Google Document AI
        request = {"name": DOCUMENT_AI_PROCESSOR, "raw_document": raw_document}
        result = client.process_document(request=request)

        # Extract text & entities
        document_text = result.document.text
        entities = result.document.entities

        # Define structured data format
        structured_data = {
            "Patient Information": {
                "patient_name": None,
                "age": None,
                "uhid": None,
                "reference_number": None,
                "sample_date_time": None,
                "report_date_time": None,
                "patient_id": None,
            },
            "Complete Blood Count (CBC)": {
                "total_wbc": None,
                "neutrophils": None,
                "lymphocytes": None,
                "monocytes": None,
                "eosinophils": None,
                "basophils": None,
            },
            "Hemoglobin & RBC Parameters": {
                "hemoglobin": None,
                "rbc_count": None,
                "mcv": None,
                "hematocrit": None,
                "mch": None,
                "mchc": None,
                "rdw": None,
                "platelet_count": None,
            },
        }

        # Map extracted entities to labels
        for entity in entities:
            label = entity.type_
            value = entity.mention_text
            for category in structured_data:
                if label in structured_data[category]:
                    structured_data[category][label] = value

        # Generate medical summary using Gemini AI
        prompt = f"""
        As a medical professional, provide a simple explanation of these lab results and the patient's health status. dont use medical jargon. dont use spoken language. give an copy in Sinhala also. dont syas"Okay, here's a simplified explanation of __ lab results in plain language, followed by the Sinhala translation:\n\n**Simple Explanation:**\n\". give the explanation directly:
        
        Patient:
        - Name: {structured_data['Patient Information']['patient_name']}
        - Age: {structured_data['Patient Information']['age']}
        
        CBC Results:
        - WBC: {structured_data['Complete Blood Count (CBC)']['total_wbc']}
        - Neutrophils: {structured_data['Complete Blood Count (CBC)']['neutrophils']}
        - Lymphocytes: {structured_data['Complete Blood Count (CBC)']['lymphocytes']}
        - Monocytes: {structured_data['Complete Blood Count (CBC)']['monocytes']}
        - Eosinophils: {structured_data['Complete Blood Count (CBC)']['eosinophils']}
        - Basophils: {structured_data['Complete Blood Count (CBC)']['basophils']}
        
        RBC Parameters:
        - Hemoglobin: {structured_data['Hemoglobin & RBC Parameters']['hemoglobin']}
        - RBC Count: {structured_data['Hemoglobin & RBC Parameters']['rbc_count']}
        - MCV: {structured_data['Hemoglobin & RBC Parameters']['mcv']}
        - Hematocrit: {structured_data['Hemoglobin & RBC Parameters']['hematocrit']}
        - MCH: {structured_data['Hemoglobin & RBC Parameters']['mch']}
        - MCHC: {structured_data['Hemoglobin & RBC Parameters']['mchc']}
        - RDW: {structured_data['Hemoglobin & RBC Parameters']['rdw']}
        - Platelet Count: {structured_data['Hemoglobin & RBC Parameters']['platelet_count']}
        
        Provide an extremely simple explanation in 5 short sentences using everyday language.
        """

        gemini_response = model.generate_content(prompt)
        medical_summary = gemini_response.text if gemini_response else "Summary not generated."

        # Return structured JSON response
        return {
            "status": "success",
            "patient_name": structured_data["Patient Information"]["patient_name"],
            "age": structured_data["Patient Information"]["age"],
            "lab_results": structured_data,
            "medical_summary": medical_summary
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}
    

# uvicorn main:app --reload 