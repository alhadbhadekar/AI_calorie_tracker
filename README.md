# 🥗 AI Food Calorie Estimator

An interactive Streamlit application that uses **OpenAI GPT-4o Vision** to analyze images of food and estimate nutritional information such as calories, macros (protein, carbs, fat), ingredient composition, and serving size.

This tool is designed for **wellness tracking, learning, and awareness**, not for strict medical guidance.

---

## 🚀 Features

* Upload or capture food images directly in the browser
* AI-powered food recognition
* Estimates:

  * **Calories (kcal)**
  * **Protein / Carbs / Fat (grams)**
  * **Likely ingredients & dish description**
  * **Serving size approximation**
* Clean and simple **Streamlit UI**
* Works locally or in the cloud

---

## 🧠 Powered By

* **OpenAI GPT-4o Vision** for image + text understanding
* **Streamlit** for the web interface
* **Pillow (PIL)** for image processing

---

## 🛠️ Installation & Setup

1. **Clone the Repository:**

```bash
git clone <your-repo-url>
cd <project-folder>
```

2. **Create a Virtual Environment:**

```bash
python3 -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

3. **Install Dependencies:**

```bash
pip install -r requirements.txt
```

4. **Set Your OpenAI API Key:**
   Create a `.env` file in the project root:

```bash
OPENAI_API_KEY=your_openai_api_key_here
```

5. **Run the App:**

```bash
streamlit run app.py
```

---

## 📸 How to Use

1. Launch the application.
2. Upload a food image **or** use your device camera.
3. Wait a few seconds while the AI analyzes the dish.
4. View the estimated nutritional breakdown.

---

## ⚠️ Disclaimer

This application is intended for **educational and wellness support** only.
Nutritional estimates may vary based on preparation method, ingredients, and serving size.
For dietary decisions, consult a **licensed nutritionist or healthcare provider**.

---

## 👤 Author

**Alhad Bhadekar**
Software Development Engineer

---

## 📄 License

This project is open for personal and non-commercial use. Modify freely for your needs!
