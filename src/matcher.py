import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from src.skill_extractor import extract_skills


# ==================================================
# 1. JOB ROLE DATABASE
# ==================================================

JOB_ROLES = {
    "Python Developer": [
        "python",
        "sql",
        "git",
        "flask",
        "django",
        "rest api",
        "docker",
        "pytest"
    ],

    "Java Developer": [
        "java",
        "sql",
        "git",
        "spring boot",
        "hibernate",
        "rest api",
        "maven",
        "junit"
    ],

    "Full-Stack Developer": [
        "html",
        "css",
        "javascript",
        "react",
        "node.js",
        "sql",
        "git",
        "rest api",
        "docker"
    ],

    "Data Analyst": [
        "python",
        "sql",
        "excel",
        "power bi",
        "tableau",
        "pandas",
        "numpy",
        "statistics"
    ],

    "Machine Learning Engineer": [
        "python",
        "machine learning",
        "deep learning",
        "numpy",
        "pandas",
        "scikit-learn",
        "tensorflow",
        "pytorch",
        "sql"
    ],

    "Data Scientist": [
        "python",
        "sql",
        "statistics",
        "machine learning",
        "pandas",
        "numpy",
        "scikit-learn",
        "data visualization"
    ],

    "AI Engineer": [
        "python",
        "machine learning",
        "deep learning",
        "llm",
        "nlp",
        "pytorch",
        "tensorflow",
        "rag",
        "api"
    ],

    "Software Engineer": [
        "python",
        "java",
        "sql",
        "git",
        "data structures",
        "algorithms",
        "rest api",
        "testing"
    ]
}


# ==================================================
# 2. TEXT NORMALIZATION
# ==================================================

def normalize_text(text):

    return re.sub(
        r"\s+",
        " ",
        text.lower()
    ).strip()


# ==================================================
# 3. SKILL EXTRACTION
# ==================================================

def get_skills(text):

    return {
        skill.lower()
        for skill in extract_skills(text)
    }


# ==================================================
# 4. SKILL COVERAGE CALCULATION
# ==================================================

def calculate_skill_coverage(
    resume_text,
    job_description
):

    resume_skills = get_skills(resume_text)

    required_skills = get_skills(job_description)

    matching_skills = sorted(
        resume_skills.intersection(required_skills)
    )

    missing_skills = sorted(
        required_skills - resume_skills
    )

    if required_skills:

        coverage = (
            len(matching_skills)
            / len(required_skills)
        ) * 100

    else:

        coverage = 0.0

    return {
        "required_skills": sorted(required_skills),
        "matching_skills": matching_skills,
        "missing_skills": missing_skills,
        "skill_coverage": round(coverage, 2)
    }


# ==================================================
# 5. TEXT SIMILARITY
# ==================================================

def calculate_text_similarity(
    resume_text,
    job_description
):

    resume_text = normalize_text(resume_text)

    job_description = normalize_text(job_description)

    if not resume_text or not job_description:

        return 0.0

    try:

        vectorizer = TfidfVectorizer()

        vectors = vectorizer.fit_transform(
            [
                resume_text,
                job_description
            ]
        )

        similarity = cosine_similarity(
            vectors[0:1],
            vectors[1:2]
        )[0][0]

        return round(
            float(similarity * 100),
            2
        )

    except ValueError:

        return 0.0


# ==================================================
# 6. ANALYZE RESUME AGAINST CUSTOM JOB DESCRIPTION
# ==================================================

def analyze_resume(
    resume_text,
    job_description
):

    if not resume_text.strip():

        raise ValueError(
            "Resume text cannot be empty."
        )

    if not job_description.strip():

        raise ValueError(
            "Job description cannot be empty."
        )

    results = calculate_skill_coverage(
        resume_text,
        job_description
    )

    results["text_similarity"] = calculate_text_similarity(
        resume_text,
        job_description
    )

    return results


# ==================================================
# 7. ANALYZE RESUME AGAINST A PREDEFINED JOB ROLE
# ==================================================

def analyze_job_role(
    resume_text,
    job_role
):

    if not resume_text.strip():

        raise ValueError(
            "Resume text cannot be empty."
        )

    if job_role not in JOB_ROLES:

        raise ValueError(
            f"Unknown job role: {job_role}"
        )

    required_skills = JOB_ROLES[job_role]

    resume_skills = get_skills(resume_text)

    matching_skills = sorted(
        resume_skills.intersection(required_skills)
    )

    missing_skills = sorted(
        set(required_skills) - resume_skills
    )

    coverage = (
        len(matching_skills)
        / len(required_skills)
    ) * 100

    return {
        "job_role": job_role,
        "required_skills": sorted(set(required_skills)),
        "matching_skills": matching_skills,
        "missing_skills": missing_skills,
        "skill_coverage": round(coverage, 2)
    }


# ==================================================
# 8. COMPARE RESUME AGAINST MULTIPLE JOB ROLES
# ==================================================

def compare_all_job_roles(resume_text):

    if not resume_text.strip():

        raise ValueError(
            "Resume text cannot be empty."
        )

    results = []

    for job_role in JOB_ROLES:

        analysis = analyze_job_role(
            resume_text,
            job_role
        )

        results.append({
            "Job Role": job_role,
            "Skill Coverage (%)": analysis["skill_coverage"],
            "Matching Skills": len(
                analysis["matching_skills"]
            ),
            "Missing Skills": len(
                analysis["missing_skills"]
            )
        })

    results.sort(
        key=lambda item: item["Skill Coverage (%)"],
        reverse=True
    )

    return results


# ==================================================
# 9. LEARNING RECOMMENDATIONS
# ==================================================

def recommend_skills_to_learn(
    resume_text,
    job_role
):

    analysis = analyze_job_role(
        resume_text,
        job_role
    )

    return analysis["missing_skills"]