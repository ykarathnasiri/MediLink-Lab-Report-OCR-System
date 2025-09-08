# 🏥 MediLink Lab Report OCR System

**AI-Powered Medical Lab Report Processing & Analysis Platform**

MediLink is an intelligent medical lab report processing system that leverages cutting-edge AI technologies to digitize, extract, and analyze medical lab reports. The system uses Google's Document AI for precise text extraction and Gemini AI for generating patient-friendly medical explanations in both English and Sinhala languages.

## 🌟 Key Features

### 🔍 Advanced OCR Processing
- **Deep Learning Model Integration**: Utilizes Google Document AI's trained deep learning models for accurate text extraction from medical lab reports
- **Multi-format Support**: Processes lab reports in JPEG, PNG, and PDF formats
- **High Accuracy**: Trained specifically for medical document processing with high precision

### 📊 Structured Data Extraction
- **Patient Information Extraction**: Automatically extracts patient details (name, age, UHID, reference numbers, dates)
- **Complete Blood Count (CBC) Analysis**: Processes WBC, Neutrophils, Lymphocytes, Monocytes, Eosinophils, and Basophils
- **Hemoglobin & RBC Parameters**: Extracts Hemoglobin, RBC count, MCV, Hematocrit, MCH, MCHC, RDW, and Platelet count
- **JSON Output**: Returns structured data in JSON format for easy integration

### 🤖 AI-Powered Medical Summaries
- **Gemini AI Integration**: Uses Google's Gemini 2.0 Flash model for medical interpretation
- **Bilingual Support**: Generates explanations in both English and Sinhala
- **Patient-Friendly Language**: Converts complex medical terminology into simple, understandable language
- **Clinical Context**: Provides health status interpretation based on lab values

### 🌐 RESTful API
- **FastAPI Framework**: High-performance, modern web framework
- **Easy Integration**: Simple API endpoints for seamless integration with other systems
- **File Upload Support**: Direct image upload capability
- **Real-time Processing**: Instant results with asynchronous processing

## 🎯 Use Cases

- **Healthcare Facilities**: Digitize and analyze lab reports efficiently
- **Patient Portals**: Provide patients with understandable explanations of their lab results
- **Medical Records Systems**: Automate data entry from paper lab reports
- **Telemedicine Platforms**: Enable remote lab report analysis and consultation
- **Research Applications**: Extract structured data for medical research and analytics

## 🛠️ Technology Stack

- **Backend**: FastAPI (Python)
- **OCR Engine**: Google Cloud Document AI
- **AI/ML**: Google Gemini 2.0 Flash
- **Authentication**: Google Cloud Authentication
- **Image Processing**: PIL (Pillow)
- **Server**: Uvicorn ASGI

## 📋 Prerequisites

- **Python**: 3.8 or higher
- **Google Cloud Platform Account** with the following APIs enabled:
  - Document AI API
  - Generative AI API (Gemini)
- **Google Cloud Service Account** with proper permissions:
  - Document AI Editor
  - Generative AI User
- **API Keys**: Gemini AI API key

## 🚀 Quick Start Guide

### 1. Clone and Setup Environment

```bash
# Navigate to your project directory
cd "d:\1. UNI\Projects\Lab report OCR\MediLink\Lab report OCR"

# Create and activate virtual environment
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate

# For macOS/Linux
source venv/bin/activate
```

### 2. Install Dependencies

Install all required packages using the requirements file:

```bash
pip install -r requirements.txt
```

**Core Dependencies:**
- `fastapi==0.115.11` - Modern web framework for building APIs
- `google-cloud-documentai==3.2.0` - Google's Document AI client library
- `google-generativeai==0.8.4` - Gemini AI integration
- `python-multipart==0.0.20` - File upload support
- `uvicorn==0.34.0` - ASGI server for running the application
- `python-dotenv==1.0.1` - Environment variable management
- `pillow==11.1.0` - Image processing capabilities
### 3. Google Cloud Setup & Authentication

#### Option 1: Service Account (Recommended for Production)

1. **Create Google Cloud Project**
   - Visit [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select an existing one

2. **Enable Required APIs**
   ```bash
   gcloud services enable documentai.googleapis.com
   gcloud services enable generativelanguage.googleapis.com
   ```

3. **Create Service Account**
   - Go to IAM & Admin > Service Accounts
   - Click "Create Service Account"
   - Grant roles:
     - `Document AI Editor`
     - `Generative AI User`
   - Download the JSON key file

4. **Set Authentication**
   ```bash
   # Windows PowerShell
   $env:GOOGLE_APPLICATION_CREDENTIALS="path\to\your-service-account-key.json"
   
   # Windows Command Prompt
   set GOOGLE_APPLICATION_CREDENTIALS=path\to\your-service-account-key.json
   
   # macOS/Linux
   export GOOGLE_APPLICATION_CREDENTIALS=/path/to/your-service-account-key.json
   ```

#### Option 2: Application Default Credentials (Development)

```bash
gcloud auth application-default login
```

### 4. Configure Document AI Processor

1. Navigate to [Document AI Console](https://console.cloud.google.com/ai/document-ai)
2. Create a new processor:
   - Type: **Form Parser** or **Document OCR**
   - Location: **us** (United States)
3. Copy the Processor ID from the processor details
4. Update the `DOCUMENT_AI_PROCESSOR` variable in `main.py`

### 5. Set Up Gemini AI

1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Generate a new API key
3. Update the `GENAI_API_KEY` variable in `main.py`
4. **Security Note**: For production, use environment variables instead of hardcoding API keys

### 6. Run the Application

```bash
# Start the development server
uvicorn main:app --reload

# The API will be available at:
# http://localhost:8000
# API Documentation: http://localhost:8000/docs
```

## 📡 API Documentation

### Endpoint Overview

The MediLink API provides a single, powerful endpoint for processing lab reports:

**Base URL**: `http://localhost:8000`
**Interactive Documentation**: `http://localhost:8000/docs`

### POST /process_lab_report/

Processes a medical lab report image and returns structured data with AI-generated medical summaries.

#### Request Details

**Method**: `POST`
**Content-Type**: `multipart/form-data`
**Authentication**: None (add authentication as needed for production)

**Parameters**:
- `file` (required): Lab report image file
  - **Supported formats**: JPEG, PNG, PDF
  - **Max file size**: 10MB (configurable)
  - **Field name**: `file`

#### Example Request

```bash
# Using cURL
curl -X POST "http://localhost:8000/process_lab_report/" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@lab_report_sample.jpg"

# Using Python requests
import requests

url = "http://localhost:8000/process_lab_report/"
files = {'file': open('lab_report_sample.jpg', 'rb')}
response = requests.post(url, files=files)
print(response.json())
```

#### Success Response (200 OK)

```json
{
  "status": "success",
  "patient_name": "John Doe",
  "age": "45",
  "lab_results": {
    "Patient Information": {
      "patient_name": "John Doe",
      "age": "45",
      "uhid": "UH123456",
      "reference_number": "REF789012",
      "sample_date_time": "2025-09-08 10:30:00",
      "report_date_time": "2025-09-08 15:45:00",
      "patient_id": "PID001"
    },
    "Complete Blood Count (CBC)": {
      "total_wbc": "7.2 x10^3/µL",
      "neutrophils": "65%",
      "lymphocytes": "25%",
      "monocytes": "8%",
      "eosinophils": "2%",
      "basophils": "0%"
    },
    "Hemoglobin & RBC Parameters": {
      "hemoglobin": "14.2 g/dL",
      "rbc_count": "4.8 x10^6/µL",
      "mcv": "88 fL",
      "hematocrit": "42%",
      "mch": "29 pg",
      "mchc": "33 g/dL",
      "rdw": "13.5%",
      "platelet_count": "250 x10^3/µL"
    }
  },
  "medical_summary": "Your blood test results show that you are in good health. Your red blood cells are normal, which means your body is getting enough oxygen. Your white blood cells are also normal, indicating no signs of infection. Your platelet count is healthy, so your blood can clot properly if you get injured. All your blood values are within the normal ranges for someone your age.\n\nසිංහල පරිවර්තනය: ඔබේ රුධිර පරීක්ෂණ ප්‍රතිඵල පෙන්වන්නේ ඔබ යහපත් සෞඛ්‍ය තත්වයකින් සිටින බවයි. ඔබේ රතු රුධිර කණිකා සාමාන්‍යයි, එයින් අදහස් වන්නේ ඔබේ ශරීරයට ප්‍රමාණවත් ඔක්සිජන් ලැබෙන බවයි. ඔබේ සුදු රුධිර කණිකා ද සාමාන්‍යයි, එයින් දැක්වෙන්නේ කිසිම ආසාදන සලකුණක් නොමැති බවයි."
}
```

#### Error Response (400/500)

```json
{
  "status": "error",
  "message": "Document processing failed: Invalid file format"
}
```

### Response Field Descriptions

| Field | Type | Description |
|-------|------|-------------|
| `status` | String | Request status (`success` or `error`) |
| `patient_name` | String | Extracted patient name |
| `age` | String | Patient age |
| `lab_results` | Object | Structured lab data organized by categories |
| `medical_summary` | String | AI-generated explanation in English and Sinhala |

## 🔧 Configuration & Customization

### Environment Variables

Create a `.env` file in the project root for secure configuration:

```env
# Google Cloud Configuration
GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account.json
DOCUMENT_AI_PROCESSOR=projects/your-project/locations/us/processors/your-processor-id

# Gemini AI Configuration
GENAI_API_KEY=your-gemini-api-key

# Application Settings
HOST=0.0.0.0
PORT=8000
DEBUG=False
MAX_FILE_SIZE=10485760  # 10MB in bytes
```

### Customizing Medical Summaries

To modify the AI-generated summaries, edit the prompt in `main.py`:

```python
# Locate this section in main.py and customize the prompt
prompt = f"""
As a medical professional, provide a simple explanation of these lab results...
[Customize this prompt to change the output style]
"""
```

### Adding New Lab Parameters

To extract additional lab values:

1. **Update the structured_data dictionary** in `main.py`
2. **Train your Document AI processor** with new field examples
3. **Add the new fields** to the extraction logic

## 🔬 Document AI Training & Optimization

### Training Your Custom Processor

For optimal results with your specific lab report formats:

1. **Collect Training Data**
   - Gather 50-100 sample lab reports
   - Ensure variety in formats and layouts
   - Include reports from different laboratories

2. **Label Training Data**
   - Use Document AI's labeling interface
   - Mark key fields (patient info, lab values, dates)
   - Maintain consistent labeling standards

3. **Train and Deploy**
   - Upload labeled data to Document AI
   - Train the processor (may take several hours)
   - Test with validation dataset
   - Deploy the trained model

### Supported Lab Report Types

The system is optimized for:
- **Complete Blood Count (CBC)** reports
- **Basic Metabolic Panel** reports  
- **Lipid Panel** reports
- **Liver Function Tests**
- **Thyroid Function Tests**
- **General chemistry panels**

## 🚨 Troubleshooting Guide

### Common Issues and Solutions

#### 1. Authentication Errors
**Error**: `google.auth.exceptions.DefaultCredentialsError`
**Solutions**:
```bash
# Verify service account file exists
ls -la path/to/service-account.json

# Re-set environment variable
$env:GOOGLE_APPLICATION_CREDENTIALS="C:\path\to\service-account.json"

# Test authentication
gcloud auth application-default login
```

#### 2. Document AI Processing Failures
**Error**: `Document processing failed`
**Solutions**:
- Verify processor ID is correct
- Check image file size (< 10MB)
- Ensure image is clear and legible
- Validate supported file format (JPEG, PNG, PDF)

#### 3. Gemini AI API Errors
**Error**: `API key invalid` or `Quota exceeded`
**Solutions**:
```python
# Check API key validity
import google.generativeai as genai
genai.configure(api_key="your-api-key")
model = genai.GenerativeModel("gemini-2.0-flash")
# Test with simple prompt
response = model.generate_content("Hello")
```

#### 4. Import/Module Errors
**Error**: `ModuleNotFoundError`
**Solutions**:
```bash
# Reinstall dependencies
pip uninstall -r requirements.txt -y
pip install -r requirements.txt

# Check Python version
python --version  # Should be 3.8+

# Activate virtual environment
venv\Scripts\activate
```

#### 5. File Upload Issues
**Error**: `File upload failed`
**Solutions**:
- Check file permissions
- Verify Content-Type header
- Ensure file is not corrupted
- Test with sample images from `/data/` folder

### Performance Optimization