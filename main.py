import os
from openai import OpenAI

client = OpenAI()

# -----------------------------
# GPT Helper
# -----------------------------
def gpt_call(system_prompt, user_prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.7
    )

    return response.choices[0].message.content.strip()


# -----------------------------
# AI Skill Extraction
# -----------------------------
def extract_skills(text):
    system_prompt = """
You are an expert career analyzer.
Extract skills accurately from text.
Return ONLY a comma separated list.
No explanations.
"""

    user_prompt = f"Extract skills from the following text:\n\n{text}"

    result = gpt_call(system_prompt, user_prompt)

    skills = [s.strip().lower() for s in result.split(",") if len(s.strip()) > 1]

    return skills


# -----------------------------
# Gap Analysis
# -----------------------------
def compute_gaps(user_skills, job_skills):
    user_set = set(user_skills)
    job_set = set(job_skills)

    missing = list(job_set - user_set)
    existing = list(job_set & user_set)

    return missing, existing


# -----------------------------
# AI Roadmap Generation
# -----------------------------
def generate_roadmap(missing_skills):
    if not missing_skills:
        return "All required skills are covered. Focus on advanced portfolio-level projects."

    system_prompt = """
You are a career planning AI.
Generate structured, practical, detailed learning plans.
Be specific.
"""

    user_prompt = f"""
Create a detailed 30-day roadmap to master the following skills:
{missing_skills}

Structure it as:

Week 1:
Week 2:
Week 3:
Week 4:

Include learning goals and mini projects.
"""

    roadmap = gpt_call(system_prompt, user_prompt)

    return roadmap


# -----------------------------
# Adaptive Replanning
# -----------------------------
def adapt_plan(missing_skills):
    completed = input("\nEnter skills you completed (comma separated), or press Enter to skip:\n")

    if completed.strip() == "":
        print("\nNo updates made.")
        return missing_skills

    completed_list = [skill.strip().lower() for skill in completed.split(",")]

    updated_missing = list(set(missing_skills) - set(completed_list))

    print("\nUpdated Missing Skills:", updated_missing)

    updated_roadmap = generate_roadmap(updated_missing)

    print("\nUPDATED ROADMAP:")
    print(updated_roadmap)

    return updated_missing


# -----------------------------
# Main Agent
# -----------------------------
if __name__ == "__main__":
    resume = input("Paste Resume:\n")
    job = input("\nPaste Dream Job Description:\n")

    print("\nExtracting skills using GPT...")

    user_skills = extract_skills(resume)
    job_skills = extract_skills(job)

    print("\nUser Skills:", user_skills)
    print("Job Skills:", job_skills)

    missing, existing = compute_gaps(user_skills, job_skills)

    print("Missing Skills:", missing)

    roadmap = generate_roadmap(missing)

    print("\nGenerated AI Roadmap:")
    print(roadmap)

    adapt_plan(missing)
