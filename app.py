import os
import base64
import requests
from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>AgriScan APAC - Smart Crop Doctor</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 720px; margin: 40px auto; padding: 0 20px; background: #f4f7f4; color: #2d3748; }
        .card { background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.06); }
        h1 { color: #2e7d32; margin-top: 0; }
        label { font-weight: 600; display: block; margin-top: 15px; margin-bottom: 6px; }
        input[type="text"], input[type="password"], select, textarea { width: 100%; padding: 10px; border-radius: 6px; border: 1px solid #cbd5e0; box-sizing: border-box; }
        button { background: #2e7d32; color: white; border: none; padding: 12px 20px; border-radius: 6px; font-size: 16px; cursor: pointer; margin-top: 20px; width: 100%; font-weight: bold; }
        button:hover { background: #1b5e20; }
        .result { margin-top: 25px; padding: 20px; background: #e8f5e9; border-left: 5px solid #2e7d32; border-radius: 6px; white-space: pre-wrap; font-family: inherit; line-height: 1.6; }
        #loading { display: none; text-align: center; margin-top: 15px; color: #2e7d32; font-weight: bold; }
    </style>
    <script>
        function showLoading() {
            document.getElementById('loading').style.display = 'block';
            document.getElementById('submit-btn').style.opacity = '0.6';
            document.getElementById('submit-btn').innerText = 'Analyzing crop health...';
        }
    </script>
</head>
<body>
    <div class="card">
        <h1>🌾 AgriScan APAC</h1>
        <p>Zero-cost multimodal crop disease diagnosis and advisory for smallholder farmers using Gemini Flash.</p>
        
        <form method="POST" enctype="multipart/form-data" onsubmit="showLoading()">
            <label>Gemini API Key:</label>
            <input type="password" name="api_key" placeholder="AIzaSy..." value="{{ api_key }}" required>

            <label>Upload Crop / Leaf Photo:</label>
            <input type="file" name="image" accept="image/*" required>

            <label>Response Language:</label>
            <select name="language">
                <option value="English">English</option>
                <option value="Telugu">Telugu (తెలుగు)</option>
                <option value="Hindi">Hindi (हिंदी)</option>
                <option value="Tamil">Tamil (தமிழ்)</option>
                <option value="Gujarati">Gujarati (ગુજરાતી)</option>
                <option value="Bengali">Bengali (বাংলা)</option>
            </select>

            <label>Symptoms / Observations:</label>
            <textarea name="query" rows="2" placeholder="e.g., Yellow leaves with brown spots on tomato plant..."></textarea>

            <button type="submit" id="submit-btn">🔍 Diagnose Crop Health</button>
            <div id="loading">🌱 Gemini is inspecting the crop... please wait a few seconds.</div>
        </form>

        {% if result %}
        <div class="result">
            <h3>🌿 Diagnosis & Advisory:</h3>
            {{ result }}
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    api_key = ""
    if request.method == "POST":
        api_key = request.form.get("api_key", "").strip()
        language = request.form.get("language", "English")
        query = request.form.get("query", "What disease is this and how can I treat it?")
        image_file = request.files.get("image")

        if api_key and image_file:
            try:
                img_bytes = image_file.read()
                mime_type = image_file.mimetype or "image/jpeg"
                encoded_image = base64.b64encode(img_bytes).decode("utf-8")

                prompt = (
                    f"You are an expert agronomist in the Asia Pacific region. "
                    f"Analyze this plant photo and the farmer's observation: '{query}'. "
                    f"Provide an answer strictly translated into {language}.\n\n"
                    f"1. Suspected Disease or Pest\n"
                    f"2. Low-cost homemade or organic remedies locally accessible to rural farmers\n"
                    f"3. Practical prevention advice for next season."
                )

                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.6-flash:generateContent?key={api_key}"
                payload = {
                    "contents": [{
                        "parts": [
                            {"text": prompt},
                            {
                                "inline_data": {
                                    "mime_type": mime_type,
                                    "data": encoded_image
                                }
                            }
                        ]
                    }]
                }

                response = requests.post(url, json=payload, headers={"Content-Type": "application/json"}, timeout=35)
                data = response.json()

                if "error" in data:
                    result = f"API Error: {data['error']['message']}"
                else:
                    result = data["candidates"][0]["content"]["parts"][0]["text"]

            except Exception as e:
                result = f"Error: {str(e)}"

    return render_template_string(HTML_TEMPLATE, result=result, api_key=api_key)

if __name__ == "__main__":
    app.run(port=5000, debug=True)