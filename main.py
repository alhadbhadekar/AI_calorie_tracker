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
You are a highly accurate food recognition and nutritional analysis assistant.
You identify meals from images and estimate calories and macros based on visual appearance.
If uncertain, provide the most reasonable likely estimate.
Always respond concisely and clearly.
"""

    user_prompt = """
Identify the food shown in this image and provide a nutritional estimate.

Return the result in this exact format:

Food Name: <name>
Description: <short description>
Likely Ingredients: <list>
Estimated Serving Size: <grams or simple measure>
Estimated Calories: <number> kcal
Estimated Macros:
- Protein: <g>
- Carbs: <g>
- Fat: <g>
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
