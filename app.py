import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from src.helper import extract_text_from_pdf, ask_openai
from src.job_api import fetch_naukri_jobs, fetch_remoteok_jobs, fetch_adzuna_jobs
from src.advanced_analysis import (
    calculate_ats_score, extract_skills, calculate_job_match_score,
    estimate_salary_range, generate_interview_tips
)
from src.report_generator import generate_resume_report
import pandas as pd
import os

# Page Configuration
st.set_page_config(
    page_title="AI Resume Analyzer & Job Recommender",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1rem 0;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #667eea;
        margin: 10px 0;
    }
    .job-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #dee2e6;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .match-score-high {
        color: #28a745;
        font-weight: bold;
    }
    .match-score-medium {
        color: #ffc107;
        font-weight: bold;
    }
    .match-score-low {
        color: #dc3545;
        font-weight: bold;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding-left: 20px;
        padding-right: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'analysis_done' not in st.session_state:
    st.session_state.analysis_done = False
if 'resume_data' not in st.session_state:
    st.session_state.resume_data = {}

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/clouds/200/resume.png", width=150)
    st.title("🎯 AI Resume Analyzer")
    st.markdown("---")
    st.markdown("""
    ### Features
    - 📊 **ATS Score Analysis**
    - 💡 **Skill Gap Identification**
    - 🚀 **Career Roadmap**
    - 💼 **Smart Job Matching**
    - 📈 **Skills Analytics**
    - 📚 **Interview Preparation**
    - 💰 **Salary Insights**
    - 📄 **Download PDF Report**
    """)
    st.markdown("---")
    st.info("💡 **Tip:** Upload a well-formatted PDF resume for best results!")

# Main Header
st.markdown('<h1 class="main-header">📄 AI-Powered Resume Analyzer & Job Recommender</h1>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #6c757d; font-size: 1.2rem;'>Get instant resume analysis, ATS score, and personalized job recommendations</p>", unsafe_allow_html=True)
st.markdown("---")

# File Upload Section
uploaded_file = st.file_uploader(
    "📤 Upload Your Resume (PDF)",
    type=["pdf"],
    help="Upload your resume in PDF format for comprehensive analysis"
)

if uploaded_file:
    # Extract and analyze resume
    if not st.session_state.analysis_done:
        with st.spinner("🔍 Analyzing your resume... This may take a moment."):
            # Extract text
            resume_text = extract_text_from_pdf(uploaded_file)
            
            # Get AI analysis
            summary = ask_openai(
                f"Summarize this resume highlighting the skills, education, and experience in a professional manner:\n\n{resume_text}",
                max_tokens=500
            )
            
            gaps = ask_openai(
                f"Analyze this resume and identify missing skills, certifications, and experiences needed for better job opportunities. Be specific and actionable:\n\n{resume_text}",
                max_tokens=400
            )
            
            roadmap = ask_openai(
                f"Based on this resume, create a detailed future roadmap including: skills to learn, certifications to pursue, and industry exposure needed:\n\n{resume_text}",
                max_tokens=400
            )
            
            # Calculate ATS score
            ats_score = calculate_ats_score(resume_text)
            
            # Extract skills
            skills = extract_skills(resume_text, summary)
            
            # Generate interview tips (basic ones for now)
            interview_tips = generate_interview_tips("Software Engineer", skills['technical'])
            
            # Store in session state
            st.session_state.resume_data = {
                'resume_text': resume_text,
                'summary': summary,
                'gaps': gaps,
                'roadmap': roadmap,
                'ats_score': ats_score,
                'skills': skills,
                'interview_tips': interview_tips
            }
            st.session_state.analysis_done = True
    
    # Display results
    data = st.session_state.resume_data
    
    # Top Metrics Row
    st.markdown("## 📊 Quick Overview")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="ATS Score",
            value=f"{data['ats_score']['total_score']}/100",
            delta=data['ats_score']['grade']
        )
    
    with col2:
        st.metric(
            label="Total Skills",
            value=data['skills']['total_count'],
            delta="Identified"
        )
    
    with col3:
        st.metric(
            label="Technical Skills",
            value=len(data['skills']['technical']),
            delta=None
        )
    
    with col4:
        st.metric(
            label="Soft Skills",
            value=len(data['skills']['soft']),
            delta=None
        )
    
    st.markdown("---")
    
    # Tabs for organized content
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📋 Summary & Score",
        "💡 Skills Analysis",
        "🎯 Gaps & Roadmap",
        "💼 Job Recommendations",
        "📚 Interview Prep",
        "📄 Download Report"
    ])
    
    # Tab 1: Summary & ATS Score
    with tab1:
        col_left, col_right = st.columns([2, 1])
        
        with col_left:
            st.markdown("### 📝 Resume Summary")
            st.info(data['summary'])
        
        with col_right:
            st.markdown("### 🎯 ATS Compatibility")
            
            # ATS Score Gauge
            fig = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=data['ats_score']['total_score'],
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "ATS Score"},
                delta={'reference': 80},
                gauge={
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 50], 'color': "lightgray"},
                        {'range': [50, 80], 'color': "lightblue"},
                        {'range': [80, 100], 'color': "lightgreen"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 90
                    }
                }
            ))
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown(f"**Grade: {data['ats_score']['grade']}**")
        
        # ATS Breakdown
        st.markdown("### 📊 Score Breakdown")
        breakdown_df = pd.DataFrame([
            {"Category": k.replace('_', ' ').title(), "Score": v}
            for k, v in data['ats_score']['breakdown'].items()
        ])
        
        fig_bar = px.bar(
            breakdown_df,
            x='Score',
            y='Category',
            orientation='h',
            color='Score',
            color_continuous_scale='Blues'
        )
        fig_bar.update_layout(height=300, showlegend=False)
        st.plotly_chart(fig_bar, use_container_width=True)
    
    # Tab 2: Skills Analysis
    with tab2:
        st.markdown("### 💻 Technical Skills")
        if data['skills']['technical']:
            # Create skill tags
            tech_skills_html = " ".join([
                f'<span style="background-color: #667eea; color: white; padding: 5px 10px; border-radius: 5px; margin: 5px; display: inline-block;">{skill}</span>'
                for skill in data['skills']['technical']
            ])
            st.markdown(tech_skills_html, unsafe_allow_html=True)
        else:
            st.warning("No technical skills identified")
        
        st.markdown("### 🤝 Soft Skills")
        if data['skills']['soft']:
            soft_skills_html = " ".join([
                f'<span style="background-color: #764ba2; color: white; padding: 5px 10px; border-radius: 5px; margin: 5px; display: inline-block;">{skill}</span>'
                for skill in data['skills']['soft']
            ])
            st.markdown(soft_skills_html, unsafe_allow_html=True)
        else:
            st.warning("No soft skills identified")
        
        # Skills Distribution Chart
        st.markdown("### 📈 Skills Distribution")
        skills_data = pd.DataFrame({
            'Category': ['Technical', 'Soft'],
            'Count': [len(data['skills']['technical']), len(data['skills']['soft'])]
        })
        
        fig_pie = px.pie(
            skills_data,
            values='Count',
            names='Category',
            color_discrete_sequence=['#667eea', '#764ba2']
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    # Tab 3: Gaps & Roadmap
    with tab3:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🛠️ Skill Gaps & Missing Areas")
            st.warning(data['gaps'])
        
        with col2:
            st.markdown("### 🚀 Career Roadmap")
            st.success(data['roadmap'])
    
    # Tab 4: Job Recommendations
    with tab4:
        if st.button("🔍 Find Matching Jobs", type="primary", use_container_width=True):
            with st.spinner("Fetching personalized job recommendations..."):
                # Get job keywords
                keywords = ask_openai(
                    f"Based on this resume summary, suggest the best 3-5 job titles and keywords for searching jobs. Give a comma-separated list only, no explanation.\n\nSummary: {data['summary']}",
                    max_tokens=100
                )
                search_keywords_clean = keywords.replace("\n", "").strip()
                
                st.info(f"🔎 Search Keywords: **{search_keywords_clean}**")
                
                # Fetch jobs
                remoteok_jobs = fetch_remoteok_jobs(search_keywords_clean, max_jobs=20)
                adzuna_jobs = fetch_adzuna_jobs(search_keywords_clean, max_jobs=20)
                
                try:
                    naukri_jobs = fetch_naukri_jobs(search_keywords_clean, rows=20)
                except:
                    naukri_jobs = []
                
                all_jobs = []
                
                # Process RemoteOK jobs
                for job in remoteok_jobs:
                    match_score = calculate_job_match_score(
                        data['skills']['technical'],
                        job.get('title', ''),
                        job.get('tags', '')
                    )
                    all_jobs.append({
                        'source': 'RemoteOK',
                        'title': job.get('title', 'N/A'),
                        'company': job.get('companyName', 'N/A'),
                        'location': job.get('location', 'Remote'),
                        'url': job.get('url', ''),
                        'match_score': match_score,
                        'tags': job.get('tags', '')
                    })
                
                # Process Adzuna jobs
                for job in adzuna_jobs:
                    match_score = calculate_job_match_score(
                        data['skills']['technical'],
                        job.get('title', ''),
                        ''
                    )
                    all_jobs.append({
                        'source': 'Adzuna',
                        'title': job.get('title', 'N/A'),
                        'company': job.get('companyName', 'N/A'),
                        'location': job.get('location', 'N/A'),
                        'url': job.get('url', ''),
                        'match_score': match_score,
                        'tags': ''
                    })
                
                # Process Naukri jobs
                for job in naukri_jobs:
                    match_score = calculate_job_match_score(
                        data['skills']['technical'],
                        job.get('title', ''),
                        ''
                    )
                    all_jobs.append({
                        'source': 'Naukri',
                        'title': job.get('title', 'N/A'),
                        'company': job.get('companyName', 'N/A'),
                        'location': job.get('location', 'N/A'),
                        'url': job.get('url', ''),
                        'match_score': match_score,
                        'tags': ''
                    })
                
                # Sort by match score
                all_jobs.sort(key=lambda x: x['match_score'], reverse=True)
                
                if all_jobs:
                    st.markdown(f"### 💼 Found {len(all_jobs)} Jobs (Sorted by Match Score)")
                    
                    for idx, job in enumerate(all_jobs[:30], 1):
                        # Determine match score class
                        if job['match_score'] >= 70:
                            score_class = "match-score-high"
                            score_emoji = "🟢"
                        elif job['match_score'] >= 50:
                            score_class = "match-score-medium"
                            score_emoji = "🟡"
                        else:
                            score_class = "match-score-low"
                            score_emoji = "🔴"
                        
                        # Get salary estimate
                        salary = estimate_salary_range(job['title'])
                        
                        st.markdown(f"""
                        <div class="job-card">
                            <h4>{idx}. {job['title']}</h4>
                            <p><strong>🏢 Company:</strong> {job['company']}</p>
                            <p><strong>📍 Location:</strong> {job['location']}</p>
                            <p><strong>🌐 Source:</strong> {job['source']}</p>
                            <p><strong>💰 Est. Salary:</strong> {salary['min']} - {salary['max']} (Avg: {salary['avg']})</p>
                            <p>{score_emoji} <span class="{score_class}">Match Score: {job['match_score']}%</span></p>
                            {f"<p><strong>🏷️ Tags:</strong> {job['tags']}</p>" if job['tags'] else ""}
                            <a href="{job['url']}" target="_blank" style="text-decoration: none;">
                                <button style="background-color: #667eea; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer;">
                                    Apply Now →
                                </button>
                            </a>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.warning("No jobs found. Try updating your resume with more keywords.")
    
    # Tab 5: Interview Prep
    with tab5:
        st.markdown("### 📚 Interview Preparation Tips")
        
        for tip in data['interview_tips']:
            st.markdown(f"✅ {tip}")
        
        st.markdown("---")
        st.markdown("### 💡 General Interview Tips")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **Before the Interview:**
            - Research the company thoroughly
            - Prepare your introduction (Tell me about yourself)
            - Review common interview questions
            - Prepare questions to ask the interviewer
            - Test your tech setup (for virtual interviews)
            """)
        
        with col2:
            st.markdown("""
            **During the Interview:**
            - Dress professionally
            - Arrive 10-15 minutes early
            - Maintain eye contact and good posture
            - Listen carefully before answering
            - Use the STAR method for behavioral questions
            """)
    
    # Tab 6: Download Report
    with tab6:
        st.markdown("### 📄 Download Comprehensive Analysis Report")
        st.info("Generate a detailed PDF report with all your resume analysis, scores, and recommendations.")
        
        if st.button("📥 Generate PDF Report", type="primary", use_container_width=True):
            with st.spinner("Generating your comprehensive report..."):
                try:
                    pdf_path = generate_resume_report(
                        summary=data['summary'],
                        skills=data['skills'],
                        ats_score=data['ats_score'],
                        gaps=data['gaps'],
                        roadmap=data['roadmap'],
                        interview_tips=data['interview_tips'],
                        filename="resume_analysis_report.pdf"
                    )
                    
                    # Read the file
                    with open(pdf_path, "rb") as pdf_file:
                        pdf_bytes = pdf_file.read()
                    
                    st.success("✅ Report generated successfully!")
                    st.download_button(
                        label="📥 Download PDF Report",
                        data=pdf_bytes,
                        file_name="resume_analysis_report.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
                    
                    # Clean up
                    if os.path.exists(pdf_path):
                        os.remove(pdf_path)
                        
                except Exception as e:
                    st.error(f"Error generating report: {str(e)}")

else:
    # Landing page when no file is uploaded
    st.markdown("""
    <div style='text-align: center; padding: 50px;'>
        <h2>👋 Welcome to AI Resume Analyzer</h2>
        <p style='font-size: 1.2rem; color: #6c757d;'>
            Upload your resume to get started with comprehensive analysis including:
        </p>
        <ul style='text-align: left; max-width: 600px; margin: 30px auto; font-size: 1.1rem;'>
            <li>✅ ATS Compatibility Score</li>
            <li>✅ Detailed Skills Analysis</li>
            <li>✅ Career Gap Identification</li>
            <li>✅ Personalized Job Recommendations</li>
            <li>✅ Interview Preparation Tips</li>
            <li>✅ Salary Insights</li>
            <li>✅ Downloadable PDF Report</li>
        </ul>
        <p style='margin-top: 30px; font-size: 1.1rem;'>
            📤 Use the file uploader above to begin!
        </p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #6c757d; padding: 20px;'>
    <p>Built with ❤️ using Streamlit, Groq AI, and Multiple Job APIs</p>
    <p>© 2026 AI Resume Analyzer | All Rights Reserved</p>
</div>
""", unsafe_allow_html=True)
