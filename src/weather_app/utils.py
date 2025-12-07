
import requests
from google.genai import types
import os
from dotenv import load_dotenv
load_dotenv()
def get_weather(city: str):
    API_KEY = os.getenv("OPEN_WEATHER_MAP")
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()
    return data


def generate_response(config, contents, client):
    response = client.models.generate_content(
        model= "gemini-2.0-flash",
        contents = contents,
        config = config
    )

    if (response.candidates[0].content.parts[0].function_call):
        tool_call = response.candidates[0].content.parts[0].function_call
        if tool_call.name == "get_weather":
            result = get_weather(**tool_call.args)

            function_response_part = types.Part.from_function_response(
                name=tool_call.name,
                response={"result": result},
            )

            contents.append(response.candidates[0].content) # Append the content from the model's response.
            contents.append(types.Content(role="user", parts=[function_response_part]))
            final_response = client.models.generate_content(
                model="gemini-2.0-flash",
                config=config,
                contents=contents,
            )

            return final_response.candidates[0].content.parts[0].text
        
        else:
            return response.candidates[0].content.parts[0].text