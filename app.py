import streamlit as st
from src.helper import extract_text_from_pdf, ask_openai
from src.job_api import fetch_naukri_jobs, fetch_remoteok_jobs, fetch_adzuna_jobs

st.set_page_config(page_title="Job Recommender", layout="wide")
st.title("📄AI Job Recommender")
st.markdown("Upload your resume and get job recommendations from multiple free job portals.")

uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])

if uploaded_file:
    with st.spinner("Extracting text from your resume..."):
        resume_text = extract_text_from_pdf(uploaded_file)

    with st.spinner("Summarizing your resume..."):
        summary = ask_openai(f"Summarize this resume highlighting the skills, edcucation, and experience: \n\n{resume_text}", max_tokens=500)

    
    with st.spinner("Finding skill Gaps..."):
        gaps = ask_openai(f"Analyze this resume and highlight missing skills, certifications, and experiences needed for better job opportunities: \n\n{resume_text}", max_tokens=400)


    with st.spinner("Creating Future Roadmap..."):
        roadmap = ask_openai(f"Based on this resume, suggest a future roadmap to improve this person's career prospects (Skill to learn, certification needed, industry exposure): \n\n{resume_text}", max_tokens=400)
    
    # Display nicely formatted results
    st.markdown("---")
    st.header("📑 Resume Summary")
    st.markdown(f"<div style='background-color: #000000; padding: 15px; border-radius: 10px; font-size:16px; color:white;'>{summary}</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.header("🛠️ Skill Gaps & Missing Areas")
    st.markdown(f"<div style='background-color: #000000; padding: 15px; border-radius: 10px; font-size:16px; color:white;'>{gaps}</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.header("🚀 Future Roadmap & Preparation Strategy")
    st.markdown(f"<div style='background-color: #000000; padding: 15px; border-radius: 10px; font-size:16px; color:white;'>{roadmap}</div>", unsafe_allow_html=True)

    st.success("✅ Analysis Completed Successfully!")


    if st.button("🔎Get Job Recommendations"):
        with st.spinner("Fetching job recommendations..."):
            keywords = ask_openai(
                f"Based on this resume summary, suggest the best job titles and keywords for searching jobs. Give a comma-separated list only, no explanation.\n\nSummary: {summary}",
                max_tokens=100
            )

            search_keywords_clean = keywords.replace("\n", "").strip()

        st.success(f"Extracted Job Keywords: {search_keywords_clean}")

        with st.spinner("Fetching jobs from multiple sources..."):
            # Fetch from RemoteOK (Free, always works)
            remoteok_jobs = fetch_remoteok_jobs(search_keywords_clean, max_jobs=30)
            
            # Try Adzuna (Free but needs API keys)
            adzuna_jobs = fetch_adzuna_jobs(search_keywords_clean, max_jobs=30)
            
            # Try Naukri (Apify - may or may not work)
            try:
                naukri_jobs = fetch_naukri_jobs(search_keywords_clean, rows=30)
            except:
                naukri_jobs = []

        # Display RemoteOK Jobs
        if remoteok_jobs:
            st.markdown("---")
            st.header("🌍 Remote Job Opportunities (RemoteOK)")
            for job in remoteok_jobs:
                st.markdown(f"**{job.get('title')}** at *{job.get('companyName')}*")
                st.markdown(f"- 📍 {job.get('location')}")
                if job.get('tags'):
                    st.markdown(f"- 🏷️ Tags: {job.get('tags')}")
                if job.get('url'):
                    st.markdown(f"- 🔗 [View Job]({job.get('url')})")
                st.markdown("---")

        # Display Adzuna Jobs
        if adzuna_jobs:
            st.markdown("---")
            st.header("💼 Jobs from Adzuna (India)")
            for job in adzuna_jobs:
                st.markdown(f"**{job.get('title')}** at *{job.get('companyName')}*")
                st.markdown(f"- 📍 {job.get('location')}")
                if job.get('url'):
                    st.markdown(f"- 🔗 [View Job]({job.get('url')})")
                st.markdown("---")

        # Display Naukri Jobs
        if naukri_jobs:
            st.markdown("---")
            st.header("💼 Jobs from Naukri.com")
            for job in naukri_jobs:
                st.markdown(f"**{job.get('title')}** at *{job.get('companyName')}*")
                st.markdown(f"- 📍 {job.get('location')}")
                job_link = job.get('url') or job.get('jobUrl') or job.get('link') or job.get('jobLink')
                if job_link:
                    st.markdown(f"- 🔗 [View Job]({job_link})")
                st.markdown("---")
        
        # Show message if no jobs found
        if not remoteok_jobs and not adzuna_jobs and not naukri_jobs:
            st.warning("No jobs found from any source. Try refining your resume or search keywords.")


