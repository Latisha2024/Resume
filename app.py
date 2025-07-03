from flask import Flask, request, jsonify, send_from_directory
import requests

app = Flask(__name__)

# Replace with your actual OpenRouter API key
OPENROUTER_API_KEY = "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"
MODEL = "meta-llama/llama-3.3-70b-instruct"  # You can change to other supported models

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

@app.route('/generate', methods=["POST"])
def generate():
    data = request.json
    name = data["name"]
    education = data["education"]
    experience = data["experience"]
    job_role = data["job_role"]

    prompt = f"""Write a professional resume and cover letter for:
Name: {name}
Education: {education}
Experience: {experience}
Job Role: {job_role}
First provide the Resume, then the Cover Letter."""

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=body)
        print("STATUS CODE:", response.status_code)
        print("RESPONSE TEXT:", response.text)

        if response.status_code != 200:
            return jsonify({"text": "Failed to generate response from OpenRouter."})

        result = response.json()
        generated_text = result["choices"][0]["message"]["content"]
        return jsonify({"text": generated_text})
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"text": "Something went wrong. Check the console for details."})

if __name__ == '__main__':
    app.run(debug=True)