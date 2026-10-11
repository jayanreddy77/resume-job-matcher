import re


# List of technical skills our application can recognize.
SKILLS = [
    "python",
    "java",
    "c++",
    "c",
    "sql",
    "mysql",
    "mongodb",
    "html",
    "css",
    "javascript",
    "react",
    "node.js",
    "flask",
    "django",
    "fastapi",
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "data science",
    "pandas",
    "numpy",
    "scikit-learn",
    "pytorch",
    "tensorflow",
    "computer vision",
    "natural language processing",
    "git",
    "github",
    "docker",
    "linux",
    "rest api",
    "aws",
    "azure",
]


def extract_skills(resume_text):
    """
    Identify known technical skills in resume text.

    Args:
        resume_text: Text extracted from a resume PDF.

    Returns:
        A list of unique skills found in the resume.
    """

    text = resume_text.lower()

    found_skills = []

    for skill in SKILLS:

        # Match the skill as a separate term.
        pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"

        if re.search(pattern, text):
            found_skills.append(skill)

    return found_skills