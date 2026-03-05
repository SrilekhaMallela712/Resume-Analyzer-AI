import os
import re
import pandas as pd
import matplotlib.pyplot as plt

# Folder containing resumes
RESUME_FOLDER = r"C:\Users\admin\Desktop\sample resumes"

# Required skills for scoring
REQUIRED_SKILLS = ["Python", "Machine Learning", "AI", "Data Analysis", "NLP", "Deep Learning", "Pandas"]

# DataFrame to store extracted info
columns = ["Resume", "Name", "Education", "Skills", "Experience", "Score"]
df_resumes = pd.DataFrame(columns=columns)

# Function to extract info from a resume text
def extract_info(text):
    lines = text.strip().split("\n")
    name = lines[0] if lines else "Unknown"

    # Extract education
    edu_keywords = ["B.Tech", "M.Tech", "Bachelor", "Master", "PhD", "Graduation"]
    education = [line for line in lines if any(word in line for word in edu_keywords)]
    education = ", ".join(education) if education else "Not specified"

    # Extract skills
    skills_found = [skill for skill in REQUIRED_SKILLS if skill.lower() in text.lower()]

    # Extract experience in years
    exp_match = re.findall(r'(\d+)\s+years?', text, re.IGNORECASE)
    experience = sum([int(x) for x in exp_match]) if exp_match else 0

    # Score based on skills match
    score = len(skills_found)

    return name, education, skills_found, experience, score

# Process all .txt resumes in folder
for file in os.listdir(RESUME_FOLDER):
    if file.endswith(".txt"):
        with open(os.path.join(RESUME_FOLDER, file), "r", encoding="utf-8") as f:
            text = f.read()
            name, education, skills, experience, score = extract_info(text)
            df_resumes = pd.concat([df_resumes, pd.DataFrame([{
                "Resume": file,
                "Name": name,
                "Education": education,
                "Skills": ", ".join(skills),
                "Experience": experience,
                "Score": score
            }])], ignore_index=True)

# Rank resumes by score
df_resumes = df_resumes.sort_values(by="Score", ascending=False).reset_index(drop=True)

# Save CSV report
df_resumes.to_csv("resume_analysis_report.csv", index=False)
print("Resume analysis completed! Report saved as 'resume_analysis_report.csv'.")
print(df_resumes)

# ----------------- Visualization -----------------
# Create a bar chart of number of skills per candidate
plt.figure(figsize=(8,5))
plt.bar(df_resumes["Name"], df_resumes["Score"], color='skyblue')
plt.xlabel("Candidate")
plt.ylabel("Number of Matching Skills")
plt.title("Resume Skill Match Score")
plt.xticks(rotation=30)
plt.tight_layout()
plt.show()
