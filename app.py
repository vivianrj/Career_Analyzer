from flask import Flask, render_template, request, send_file
import requests
import os
from dotenv import load_dotenv
from pdf_generator import generate_pdf
import markdown

load_dotenv()

app = Flask(__name__)

HF_TOKEN = os.getenv("HF_TOKEN")

API_URL = "https://router.huggingface.co/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}


def analyze_resume(resume, job):
    prompt = f"""
You are an advanced ATS Resume Analyzer.

Analyze the resume against the job description.

Return your response in this EXACT structured format:

ATS SCORE: <number>/100

SUMMARY:
Short professional summary of alignment.

STRENGTHS:
- Bullet point
- Bullet point

WEAKNESSES:
- Bullet point
- Bullet point

IMPROVEMENT ROADMAP (60 DAYS):

Weeks 1–2:
- Action step
- Action step

Weeks 3–4:
- Action step
- Action step

Weeks 5–8:
- Action step
- Action step

Resume:
{resume}

Job Description:
{job}
"""

    payload = {
        "model": "meta-llama/llama-3-8b-instruct",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(API_URL, headers=HEADERS, json=payload)
    data = response.json()

    if "choices" in data:
        return data["choices"][0]["message"]["content"]
    else:
        return f"AI Error: {data}"


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        resume = request.form.get("resume")
        job = request.form.get("job")

        if not resume or not job:
            return render_template("index.html", error="Please fill both fields.")

        result = analyze_resume(resume, job)

        # Convert markdown-like text to clean HTML
        formatted_result = markdown.markdown(result)

        # Extract ATS score
        score_line = result.split("\n")[0]
        score = score_line.replace("ATS SCORE:", "").strip()

        return render_template(
            "index.html",
            result=formatted_result,
            score=score
        )

    return render_template("index.html")


@app.route("/download", methods=["POST"])
def download():
    content = request.form.get("content")

    file_path = generate_pdf(content)

    return send_file(file_path, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
