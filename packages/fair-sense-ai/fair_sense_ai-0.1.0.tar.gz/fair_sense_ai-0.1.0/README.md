
# **Fair-Sense-AI**

Fair-Sense-AI is a cutting-edge, AI-driven platform designed to promote transparency, fairness, and equity by analyzing bias in textual and visual content. 

Whether you're addressing societal biases, identifying disinformation, or fostering responsible AI practices, Fair-Sense-AI equips you with the tools to make informed decisions.

---

## **Key Features**

### 📄 **Text Analysis**
- Detect and highlight biases within text, such as targeted language or phrases.
- Provide actionable feedback on the tone and fairness of the content.

### 🖼️ **Image Analysis**
- Extract embedded text from images and analyze it for potential biases.
- Generate captions for images and evaluate their fairness and inclusivity.

### 📂 **Batch Processing**
- Analyze large datasets of text or images efficiently.
- Automatically highlight problematic patterns across entire datasets.

### 📜 **AI Governance Insights**
- Gain detailed insights into ethical AI practices, fairness guidelines, and bias mitigation strategies.
- Explore topics like data privacy, transparency, and responsible AI deployment.

---

## **Installation Guide**

### **Prerequisites**

1. **Python 3.7+**
   Ensure you have Python installed. You can download it [here](https://www.python.org/downloads/).

2. **Tesseract OCR**  
   Required for extracting text from images.

   #### **Installation Instructions:**

   - **Ubuntu:**
     ```bash
     sudo apt-get update
     sudo apt-get install tesseract-ocr
     ```

   - **macOS (Homebrew):**
     ```bash
     brew install tesseract
     ```

   - **Windows:**
     Download and install Tesseract OCR from [this link](https://github.com/UB-Mannheim/tesseract/wiki).

---

### **Installing Fair-Sense-AI**

Install the Fair-Sense-AI package using pip:

```bash
pip install Fair-Sense-AI
```

---

## **Usage Instructions**

### **Launching the Application**

Run the following command to start Fair-Sense-AI:

```bash
Fair-Sense-AI
```

This will launch the Gradio-powered interface in your default web browser.

---

### **How to Use Fair-Sense-AI**

#### **1. Text Analysis**
- Go to the **Text Analysis** tab.
- Input or paste the text you want to analyze.
- Click **Analyze** to detect and highlight biases.

#### **2. Image Analysis**
- Go to the **Image Analysis** tab.
- Upload an image to analyze for biases in embedded text or captions.
- Click **Analyze** to review detailed results.

#### **3. Batch Text CSV Analysis**
- Go to the **Batch Text CSV Analysis** tab.
- Upload a CSV file with a column named `text`.
- Click **Analyze CSV** to process and analyze all entries.

#### **4. Batch Image Analysis**
- Go to the **Batch Image Analysis** tab.
- Upload multiple images to analyze biases in captions or embedded text.
- Click **Analyze Images** to view results.

#### **5. AI Governance Insights**
- Go to the **AI Governance and Safety** tab.
- Choose a predefined topic or input your own.
- Click **Get Insights** to receive actionable recommendations.

#### **6. AI Safety Risks Dashboard**
- Explore an interactive dashboard highlighting AI safety risks, their impact, and mitigation strategies.

---

## **Sample Data**

A CSV file with text column.
Images .

---

## **Troubleshooting**

### **Common Issues**

- **Models Download Slowly**: On first use, models are downloaded automatically. Ensure you have a stable internet connection.
- **Tesseract Not Found**: Verify Tesseract is installed and accessible in your system's PATH.
- **GPU Support**: Install PyTorch with CUDA support if you want GPU acceleration.

```bash
# Example: Installing PyTorch with CUDA 11.7 support
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu117
```

---
Here's the updated section:

---

## **Contact**

For inquiries or support, contact:

- **Name**: Shaina Raza  
- **Role**: Applied ML Scientist, Responsible AI  
- **Email**: [shaina.raza@vectorinstitute.ai](mailto:shaina.raza@torontomu.ca)  

---

## **License**

This project is licensed under the [Creative Commons License](https://creativecommons.org/licenses/).

---