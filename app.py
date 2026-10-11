import streamlit as st
import pandas as pd

from src.resume_parser import extract_resume_text
from src.skill_extractor import extract_skills

from src.matcher import (
    analyze_resume,
    analyze_job_role,
    compare_all_job_roles,
    recommend_skills_to_learn,
    JOB_ROLES,
)


# =========================================================
# 1. PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide",
)


# =========================================================
# 2. APPLICATION HEADER
# =========================================================

st.title("📄 AI Resume Analyzer & Career Matcher")

st.write(
    """
    Upload your resume to discover your technical skills,
    compare your profile with different job roles, identify
    skill gaps, and explore what you could learn next.
    """
)

st.divider()


# =========================================================
# 3. SIDEBAR
# =========================================================

with st.sidebar:

    st.title("🚀 Career Matcher")

    st.write("### Features")

    st.write("📄 Resume PDF Parsing")
    st.write("🧠 Technical Skill Extraction")
    st.write("🎯 Job Role Matching")
    st.write("📊 Multiple Career Comparison")
    st.write("⚠️ Skill Gap Analysis")
    st.write("📚 Learning Recommendations")
    st.write("📝 Custom Job Matching")
    st.write("⬇️ Download Reports")

    st.divider()

    st.info(
        """
        Upload your resume to get started.

        The matching scores measure skill overlap.
        They do not predict hiring outcomes.
        """
    )


# =========================================================
# 4. RESUME UPLOAD
# =========================================================

st.header("1. Upload Your Resume")

uploaded_file = st.file_uploader(
    "Choose your resume in PDF format",
    type=["pdf"],
    help="Upload a text-based PDF resume. Maximum size: 10 MB.",
)


# =========================================================
# 5. WELCOME SCREEN
# =========================================================

if uploaded_file is None:

    st.info("👆 Upload a PDF resume to begin.")

    st.subheader("What can this application do?")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown("### 📄 Resume Analysis")

        st.write(
            "Extract resume text, count words, "
            "and identify recognized technical skills."
        )

    with col2:

        st.markdown("### 🎯 Career Matching")

        st.write(
            "Compare your resume against predefined "
            "job roles or a custom job description."
        )

    with col3:

        st.markdown("### 📚 Skill Gap Analysis")

        st.write(
            "Identify skills not detected in your resume "
            "and explore potential learning priorities."
        )


# =========================================================
# 6. PROCESS THE RESUME
# =========================================================

else:

    try:

        # -------------------------------------------------
        # 6.1 CHECK FILE SIZE
        # -------------------------------------------------

        if uploaded_file.size > 10 * 1024 * 1024:

            st.error(
                "The uploaded file exceeds 10 MB. "
                "Please upload a smaller PDF."
            )

            st.stop()

        # -------------------------------------------------
        # 6.2 EXTRACT RESUME TEXT
        # -------------------------------------------------

        with st.spinner("Reading your resume..."):

            resume_text = extract_resume_text(uploaded_file)

        if not resume_text or not resume_text.strip():

            st.warning(
                "No readable text was found in this PDF. "
                "It may be scanned or image-based. "
                "OCR support may be required."
            )

            st.stop()

        st.success("Resume uploaded and processed successfully!")

        st.divider()

        # -------------------------------------------------
        # 6.3 EXTRACT TECHNICAL SKILLS
        # -------------------------------------------------

        skills = extract_skills(resume_text)

        skills = sorted(
            set(skills),
            key=lambda skill: skill.lower(),
        )

        word_count = len(resume_text.split())

        character_count = len(resume_text)

        # =================================================
        # 7. RESUME OVERVIEW
        # =================================================

        st.header("2. Resume Overview")

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Total Words",
                word_count,
            )

        with col2:

            st.metric(
                "Total Characters",
                character_count,
            )

        with col3:

            st.metric(
                "Technical Skills Detected",
                len(skills),
            )

        st.divider()

        # =================================================
        # 8. EXTRACTED RESUME TEXT
        # =================================================

        st.header("3. Extracted Resume Text")

        with st.expander(
            "View extracted resume text",
            expanded=False,
        ):

            st.text_area(
                "Resume Content",
                value=resume_text,
                height=300,
                disabled=True,
                key="resume_text_display",
            )

        st.download_button(
            label="⬇️ Download Extracted Resume Text",
            data=resume_text,
            file_name="extracted_resume.txt",
            mime="text/plain",
            key="download_resume_text",
        )

        st.divider()

        # =================================================
        # 9. TECHNICAL SKILL ANALYSIS
        # =================================================

        st.header("4. Technical Skills Analysis")

        if skills:

            st.success(
                f"Detected {len(skills)} unique technical skills."
            )

            skill_columns = st.columns(3)

            for index, skill in enumerate(skills):

                with skill_columns[index % 3]:

                    st.markdown(
                        f"✅ **{skill.title()}**"
                    )

            skills_df = pd.DataFrame(
                {
                    "Detected Skills": skills,
                }
            )

            with st.expander("View skills in a table"):

                st.dataframe(
                    skills_df,
                    use_container_width=True,
                    hide_index=True,
                )

            st.download_button(
                label="⬇️ Download Detected Skills",
                data=skills_df.to_csv(index=False),
                file_name="detected_skills.csv",
                mime="text/csv",
                key="download_detected_skills",
            )

        else:

            st.warning(
                "No skills from the current skill dictionary "
                "were detected. This does not necessarily mean "
                "your resume lacks technical skills."
            )

        st.divider()

        # =================================================
        # 10. CAREER MATCHING SYSTEM
        # =================================================

        st.header("5. Career Matching System")

        st.write(
            """
            Choose one of the following options to analyze
            your resume against job requirements.
            """
        )

        analysis_mode = st.radio(
            "Choose your analysis mode",
            [
                "Analyze a Job Role",
                "Compare All Job Roles",
                "Custom Job Description",
            ],
            key="analysis_mode",
        )

        # =================================================
        # OPTION 1: ANALYZE ONE JOB ROLE
        # =================================================

        if analysis_mode == "Analyze a Job Role":

            st.subheader("🎯 Analyze a Specific Career")

            selected_role = st.selectbox(
                "Select your target job role",
                list(JOB_ROLES.keys()),
                key="selected_job_role",
            )

            st.write("### Commonly Associated Skills")

            role_skills = JOB_ROLES[selected_role]

            st.write(
                ", ".join(role_skills)
            )

            st.caption(
                "These are predefined example requirements. "
                "Actual requirements vary by employer and position."
            )

            if st.button(
                "🚀 Analyze Selected Role",
                type="primary",
                key="analyze_selected_role",
            ):

                try:

                    result = analyze_job_role(
                        resume_text,
                        selected_role,
                    )

                    st.success(
                        f"Analysis completed for {selected_role}!"
                    )

                    # -------------------------------------
                    # MATCHING SUMMARY
                    # -------------------------------------

                    col1, col2, col3 = st.columns(3)

                    with col1:

                        st.metric(
                            "Skill Coverage",
                            f"{result['skill_coverage']:.2f}%",
                        )

                    with col2:

                        st.metric(
                            "Matching Skills",
                            len(result["matching_skills"]),
                        )

                    with col3:

                        st.metric(
                            "Skills Not Detected",
                            len(result["missing_skills"]),
                        )

                    # -------------------------------------
                    # PROGRESS BAR
                    # -------------------------------------

                    st.subheader("📊 Skill Coverage")

                    coverage = float(
                        result["skill_coverage"]
                    )

                    st.progress(
                        max(0.0, min(1.0, coverage / 100.0))
                    )

                    # -------------------------------------
                    # MATCHING SKILLS
                    # -------------------------------------

                    col1, col2 = st.columns(2)

                    with col1:

                        st.subheader("✅ Matching Skills")

                        if result["matching_skills"]:

                            for skill in result["matching_skills"]:

                                st.write(f"✅ {skill.title()}")

                        else:

                            st.info(
                                "No matching skills were detected."
                            )

                    with col2:

                        st.subheader("📚 Skills to Learn")

                        if result["missing_skills"]:

                            for skill in result["missing_skills"]:

                                st.write(f"📌 {skill.title()}")

                        else:

                            st.success(
                                "All predefined skills for this "
                                "role were detected in your resume."
                            )

                    # -------------------------------------
                    # RECOMMENDATIONS
                    # -------------------------------------

                    st.divider()

                    st.subheader(
                        "🗺️ Suggested Learning Priorities"
                    )

                    learning_skills = recommend_skills_to_learn(
                        resume_text,
                        selected_role,
                    )

                    if learning_skills:

                        st.write(
                            """
                            Consider prioritizing the following
                            skills if they are relevant to your
                            career goals:
                            """
                        )

                        for number, skill in enumerate(
                            learning_skills,
                            start=1,
                        ):

                            st.write(
                                f"{number}. {skill.title()}"
                            )

                    else:

                        st.success(
                            "No gaps were detected in the "
                            "predefined skill list."
                        )

                    # -------------------------------------
                    # DOWNLOAD REPORT
                    # -------------------------------------

                    role_report = pd.DataFrame(
                        {
                            "Required Skill": result[
                                "required_skills"
                            ],
                            "Status": [
                                (
                                    "Matched"
                                    if skill in result[
                                        "matching_skills"
                                    ]
                                    else "Not detected"
                                )
                                for skill in result[
                                    "required_skills"
                                ]
                            ],
                        }
                    )

                    st.download_button(
                        label="⬇️ Download Role Analysis Report",
                        data=role_report.to_csv(index=False),
                        file_name="job_role_analysis.csv",
                        mime="text/csv",
                        key="download_role_report",
                    )

                    st.caption(
                        "Skill coverage measures overlap with "
                        "a predefined list. It is not a hiring "
                        "probability or a complete measure of "
                        "your suitability for the role."
                    )

                except ValueError as error:

                    st.error(str(error))

        # =================================================
        # OPTION 2: COMPARE ALL JOB ROLES
        # =================================================

        elif analysis_mode == "Compare All Job Roles":

            st.subheader("📊 Compare Multiple Careers")

            st.write(
                """
                Compare the skills detected in your resume
                against all available predefined job roles.
                """
            )

            if st.button(
                "📈 Compare All Careers",
                type="primary",
                key="compare_all_roles",
            ):

                try:

                    results = compare_all_job_roles(
                        resume_text
                    )

                    results_df = pd.DataFrame(results)

                    st.subheader("Career Comparison Results")

                    st.dataframe(
                        results_df,
                        use_container_width=True,
                        hide_index=True,
                    )

                    # -------------------------------------
                    # CHART
                    # -------------------------------------

                    st.subheader(
                        "📈 Skill Coverage by Job Role"
                    )

                    chart_data = results_df.set_index(
                        "Job Role"
                    )[["Skill Coverage (%)"]]

                    st.bar_chart(chart_data)

                    # -------------------------------------
                    # BEST MATCH
                    # -------------------------------------

                    if results:

                        best_role = results[0]

                        st.success(
                            f"Highest skill overlap: "
                            f"{best_role['Job Role']} "
                            f"({best_role['Skill Coverage (%)']:.2f}%)."
                        )

                        st.info(
                            "This identifies the role with the "
                            "highest overlap against our predefined "
                            "skill lists. It does not guarantee "
                            "job readiness or employment."
                        )

                    # -------------------------------------
                    # DOWNLOAD RESULTS
                    # -------------------------------------

                    st.download_button(
                        label="⬇️ Download Career Comparison",
                        data=results_df.to_csv(index=False),
                        file_name="career_comparison.csv",
                        mime="text/csv",
                        key="download_career_comparison",
                    )

                except ValueError as error:

                    st.error(str(error))

        # =================================================
        # OPTION 3: CUSTOM JOB DESCRIPTION
        # =================================================

        elif analysis_mode == "Custom Job Description":

            st.subheader("📝 Custom Job Description Matching")

            st.write(
                """
                Paste a specific job description when you want
                to compare your resume against a particular vacancy.
                """
            )

            job_description = st.text_area(
                "Paste the job description",
                height=220,
                placeholder=(
                    "Example: Python Developer with SQL, Flask, "
                    "Git, Docker and REST API experience."
                ),
                key="custom_job_description",
            )

            if st.button(
                "🚀 Analyze Custom Job",
                type="primary",
                key="analyze_custom_job",
            ):

                if not job_description.strip():

                    st.warning(
                        "Please enter a job description first."
                    )

                else:

                    try:

                        result = analyze_resume(
                            resume_text,
                            job_description,
                        )

                        st.success(
                            "Custom job analysis completed!"
                        )

                        col1, col2, col3 = st.columns(3)

                        with col1:

                            st.metric(
                                "Skill Coverage",
                                f"{result['skill_coverage']:.2f}%",
                            )

                        with col2:

                            st.metric(
                                "Text Similarity",
                                f"{result['text_similarity']:.2f}%",
                            )

                        with col3:

                            st.metric(
                                "Matching Skills",
                                len(result["matching_skills"]),
                            )

                        st.subheader("📊 Skill Coverage")

                        st.progress(
                            max(
                                0.0,
                                min(
                                    1.0,
                                    result["skill_coverage"] / 100.0,
                                ),
                            )
                        )

                        col1, col2 = st.columns(2)

                        with col1:

                            st.subheader("✅ Matching Skills")

                            if result["matching_skills"]:

                                for skill in result[
                                    "matching_skills"
                                ]:

                                    st.write(f"✅ {skill.title()}")

                            else:

                                st.info(
                                    "No matching skills detected."
                                )

                        with col2:

                            st.subheader("⚠️ Skills Not Detected")

                            if result["missing_skills"]:

                                for skill in result[
                                    "missing_skills"
                                ]:

                                    st.write(f"📌 {skill.title()}")

                            else:

                                st.success(
                                    "All recognized required skills "
                                    "were detected."
                                )

                        # ---------------------------------
                        # DOWNLOAD CUSTOM JOB REPORT
                        # ---------------------------------

                        custom_report = pd.DataFrame(
                            {
                                "Required Skill": result[
                                    "required_skills"
                                ],
                                "Status": [
                                    (
                                        "Matched"
                                        if skill in result[
                                            "matching_skills"
                                        ]
                                        else "Not detected"
                                    )
                                    for skill in result[
                                        "required_skills"
                                    ]
                                ],
                            }
                        )

                        st.download_button(
                            label="⬇️ Download Custom Job Report",
                            data=custom_report.to_csv(index=False),
                            file_name="custom_job_match_report.csv",
                            mime="text/csv",
                            key="download_custom_report",
                        )

                        st.caption(
                            "Skill coverage and text similarity "
                            "measure overlap. Neither score predicts "
                            "hiring outcomes."
                        )

                    except ValueError as error:

                        st.error(str(error))

        st.divider()

        # =================================================
        # 11. PROJECT LIMITATIONS
        # =================================================

        with st.expander(
            "ℹ️ About this application's limitations"
        ):

            st.write(
                """
                1. Skill extraction uses a predefined dictionary.
                2. Unrecognized skills may not be detected.
                3. Mentioning a skill does not prove proficiency.
                4. Job-role requirements are example skill lists.
                5. Actual requirements vary between employers.
                6. Skill coverage measures overlap, not job readiness.
                7. Text similarity does not establish qualifications.
                8. The scores do not predict hiring outcomes.
                9. Scanned PDFs may require OCR support.
                """
            )

    except Exception as error:

        st.error(
            f"An error occurred while processing your resume: {error}"
        )


# =========================================================
# 12. FOOTER
# =========================================================

st.divider()

st.caption(
    "AI Resume Analyzer & Career Matcher | "
    "Python • Streamlit • Pandas • Scikit-learn"
)