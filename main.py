import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv
from PIL import Image
import base64
import io

# Load API Key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Page settings
st.set_page_config(
    page_title="AI Food Calorie Estimator",
    page_icon="🍽️",
    layout="centered"
)

# ─────────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────────
st.sidebar.title("ℹ️ About This App")

st.sidebar.markdown("""
This app identifies food from an image and estimates:
- Calories (kcal)
- Protein / Carbs / Fat (g)
- Serving size and ingredients
""")

st.sidebar.markdown("---")

st.sidebar.markdown("""
### Tech Stack
- OpenAI GPT-4o Vision
- Streamlit UI
- PIL Image Handling
""")

st.sidebar.markdown("---")

st.sidebar.markdown("""
### Author  
**Alhad Bhadekar**  
Software Development Engineer  
""", unsafe_allow_html=True)

st.sidebar.markdown("---")

st.sidebar.markdown("""
### Disclaimer  
This app is for **educational and wellness support purposes only**.
Nutritional estimates may vary depending on preparation method, ingredients, and portion size.
Always consult a certified nutritionist for medical or dietary decisions.
""")

# ─────────────────────────────────────────────
# Header
# ─────────────────────────────────────────────
st.markdown(
    "<h1 style='text-align:center; color:#B8860B;'>🥗 AI Food Calorie Estimator 🍣</h1> ",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='text-align:center;'>Upload or take a picture of your meal</p>",
    unsafe_allow_html=True
)

# ─────────────────────────────────────────────
# Image → Base64 Converter
# ─────────────────────────────────────────────
def encode_image_to_base64(image):
    buffer = io.BytesIO()
    image.save(buffer, format=image.format or "JPEG")
    return base64.b64encode(buffer.getvalue()).decode("utf-8")

# ─────────────────────────────────────────────
# Vision Query Function
# ─────────────────────────────────────────────
def analyze_food(image):
    base64_img = encode_image_to_base64(image)

    system_prompt = """
You are a nutrition expert analyzing food images to provide accurate and concise nutritional information.


# Nutritional Analysis Task
You must:
- Identify the most likely food item(s)
- Infer realistic preparation method, regional variations, and ingredient composition when helpful
- If multiple possible dishes exist, select the most probable based on visual cues (texture, color, garnish, plating)
- If uncertain, state the uncertainty clearly and provide your best reasonable estimate


When estimating nutrition:
- Base calorie and macro values on common nutrition reference tables and restaurant-standard servings
- If portion size seems larger or smaller than standard, adjust estimates proportionally
- When sugar and fiber cannot be visually confirmed, infer from typical recipe composition


Always produce **two parts** in response:


1) **Human-Readable Summary**
- Food Name
- Description (1–2 lines)
- Typical Ingredients
- Likely Serving Size (a simple measurement, e.g., "1 plate", "1 bowl", "120g", "1 slice")


2) **Structured Nutrition Output (exact field names, no extra text)**
Use this format and only this format:


food_name: "<string>"
serving_description: "<string>"
calories: <float>
fat_grams: <float>
protein_grams: <float>
carbs_grams: <float>
sugar_grams: <float>
fiber_grams: <float>
confidence_level: "High" | "Medium" | "Low"
"""


    user_prompt = """
Identify the food and return:
Food Name
Description


Then structured nutrition:
food_name: "<name>"
serving_description: "<amount>"
calories: <number>
fat_grams: <number>
protein_grams: <number>
carbs_grams: <number>
sugar_grams: <number>
fiber_grams: <number>
confidence_level: "High|Medium|Low"
"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": user_prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_img}"}}
                ]
            }
        ],
        max_tokens=250
    )
    return response.choices[0].message.content

# ─────────────────────────────────────────────
# Upload or Camera Input
# ─────────────────────────────────────────────
uploaded = st.file_uploader("📤 Upload Image", type=["jpg", "jpeg", "png"])
camera = st.camera_input("📸 Or take a photo")

image = None
if uploaded:
    image = Image.open(uploaded)
elif camera:
    image = Image.open(camera)

# ─────────────────────────────────────────────
# Run Analysis
# ─────────────────────────────────────────────
if image:
    st.image(image, caption="Image selected", use_column_width=True)

    with st.spinner("🍽️ Analyzing food..."):
        result = analyze_food(image)

    st.markdown("### ✅ Food Analysis Result")
    st.markdown(result)

# ─────────────────────────────────────────────
# Footer
# ─────────────────────────────────────────────
st.markdown("""
<hr>
<div style='text-align:center; font-size:0.9em; line-height:1.6;'>
    <p>© 2025 FoodAI Nutrition Assistant | Developed by <strong>Alhad Bhadekar</strong></p>
    <p style='max-width:650px; margin:auto; font-size:0.85em; color:#BBBBBB;'>
        <em>
        Disclaimer: This application provides approximate calorie and nutrition estimations. 
        Actual values may vary. This is not medical or dietary advice.
        </em>
    </p>
</div>
""", unsafe_allow_html=True)
