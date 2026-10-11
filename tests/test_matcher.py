from src.matcher import analyze_resume


def test_resume_matching():

    resume_text = """
    I have experience with Python, SQL and Git.
    I developed a Python web application.
    """

    job_description = """
    We need a developer with Python, SQL, Git,
    Flask and Docker experience.
    """

    result = analyze_resume(
        resume_text,
        job_description
    )

    assert "python" in result["matching_skills"]
    assert "sql" in result["matching_skills"]
    assert "git" in result["matching_skills"]

    assert "flask" in result["missing_skills"]
    assert "docker" in result["missing_skills"]

    assert result["skill_coverage"] == 60.0

    assert 0 <= result["text_similarity"] <= 100


def test_empty_resume():

    try:

        analyze_resume(
            "",
            "Python developer with SQL experience"
        )

        assert False, "Expected ValueError"

    except ValueError:
        pass