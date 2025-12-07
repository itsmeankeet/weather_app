from google import genai
import os
import requests
from google.genai import types
import streamlit as st
from langchain_core.prompts import PromptTemplate
from src.weather_app.utils import generate_response

# --- Google GenAI setup ---
weather_function = types.FunctionDeclaration(
    name="get_weather",
    description="Fetch real-time weather information for a given city. Use this tool whenever the user asks about weather, temperature, humidity, or climate of a place.",
    parameters={
        "type": "object",
        "properties": {
            "city": {
                "type": "string",
                "description": "Name of the city to fetch weather information for."
            }
        },
        "required": ["city"]
    }
)

tools = types.Tool(function_declarations=[weather_function])
config = types.GenerateContentConfig(tools=[tools])
client = genai.Client()

# --- Streamlit UI ---
st.set_page_config(page_title="Weather App", page_icon="☀️", layout="centered")
st.markdown("<h1 style='text-align: center; color: #4B8BBE;'>🌤 Weather Checker App</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Get real-time weather updates for any city.</p>", unsafe_allow_html=True)

# Centered input box
city = st.text_input("Enter the city name:", "Kathmandu", max_chars=50)

# Button with color
if st.button("Check Weather", key="check_btn"):
    if city:
        # Create the prompt
        prompt = PromptTemplate(template="What is the weather of {city}?", input_variables=["city"])
        contents = [
            types.Content(
                role="user",
                parts=[types.Part(text=prompt.format(city=city))]
            )
        ]
        # Call your custom response generator
        response = generate_response(config, contents, client)

        # Display result in a card-style box
        st.markdown(
            f"""
            <div style="
                border-radius: 10px;
                padding: 15px;
                background: linear-gradient(135deg, #81ecec, #74b9ff);
                color: #2d3436;
                font-size: 18px;
                text-align: center;
                box-shadow: 2px 2px 12px rgba(0,0,0,0.2);
            ">
                {response}
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.warning("⚠️ Please enter a city name to check the weather.")
