# 📄 AI-Powered Job Recommender System

An intelligent job recommendation system that leverages Groq's LLaMA AI model to analyze resumes, identify skill gaps, and recommend relevant job opportunities from multiple job portals including RemoteOK, Adzuna, and Naukri.

## 🌟 Features

### 1. **Resume Analysis**

- Extract text from PDF resumes using PyMuPDF
- Generate intelligent resume summaries highlighting key skills, education, and experience
- AI-powered analysis using Groq LLaMA 3.3 70B model

### 2. **Skill Gap Analysis**

- Identify missing skills and certifications
- Highlight areas for improvement
- Provide actionable recommendations for career advancement

### 3. **Career Roadmap Generation**

- Personalized career development suggestions
- Certification recommendations
- Skills to learn for better job prospects
- Industry exposure guidance

### 4. **Job Recommendations**

- Automatic extraction of relevant job search keywords from resume
- Fetch remote job listings from RemoteOK (up to 30 jobs, no API key required)
- Fetch job listings from Adzuna API (India-focused, up to 30 jobs, free tier available)
- Fetch job listings from Naukri.com via Apify (up to 60 jobs)
- Display job titles, company names, locations, tags, and direct application links

### 5. **MCP Server Integration**

- FastMCP server implementation for programmatic access
- RESTful tools for fetching LinkedIn and Naukri jobs
- Async support for efficient job fetching

## 🛠️ Technology Stack

- **Frontend**: Streamlit (Interactive web interface)
- **AI/ML**: Groq LLaMA 3.3 70B Model
- **PDF Processing**: PyMuPDF (fitz)
- **Job APIs**: 
  - RemoteOK API (Free, no authentication required)
  - Adzuna API (Free tier available)
  - Apify Client (for Naukri job scraping)
- **Server**: FastMCP (Model Context Protocol)
- **Environment Management**: python-dotenv

## 📋 Prerequisites

- Python 3.11 or higher
- Groq API Key (Free tier available)
- Apify API Token (Optional, for Naukri jobs)
- Adzuna API Credentials (Optional, for Adzuna jobs)

## 🚀 Installation

1. **Clone the repository**

```bash
git clone <repository-url>
cd Generative-AI-Powered-Job-Recommender-System-main
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

Or using pyproject.toml:

```bash
pip install -e .
```

3. **Set up environment variables**

Create a `.env` file in the root directory and add your API keys:

```env
# Required: Groq API Key (Get from https://console.groq.com/)
GROQ_API_KEY=your_groq_api_key_here

# Optional: Apify API Token (Get from https://console.apify.com/)
APIFY_API_TOKEN=your_apify_api_token_here

# Optional: Adzuna API (Get from https://developer.adzuna.com/)
ADZUNA_APP_ID=your_adzuna_app_id_here
ADZUNA_APP_KEY=your_adzuna_app_key_here
```

## 📖 Usage

### Running the Streamlit App

```bash
streamlit run app.py
```

This will launch the web interface where you can:

1. Upload your resume (PDF format)
2. View AI-generated resume summary
3. See identified skill gaps
4. Get a personalized career roadmap
5. Click "Get Job Recommendations" to fetch relevant jobs from multiple sources

**Note**: 
- RemoteOK jobs work without any API key
- Adzuna and Naukri jobs require respective API credentials in `.env` file

### Running the MCP Server

```bash
python mcp_server.py
```

The MCP server exposes two tools:

- `fetchlinkedin(listofkey)` - Fetch jobs from LinkedIn
- `fetchnaukri(listofkey)` - Fetch jobs from Naukri

## 📁 Project Structure

```
Generative-AI-Powered-Job-Recommender-System-main/
│
├── app.py                  # Main Streamlit application
├── mcp_server.py          # FastMCP server for programmatic access
├── requirements.txt       # Python dependencies
├── pyproject.toml        # Project metadata and dependencies
├── README.md             # Project documentation
│
└── src/
    ├── __init__.py       # Package initializer
    ├── helper.py         # PDF extraction and OpenAI helper functions
    └── job_api.py        # Job fetching functions (LinkedIn & Naukri)
```

## 🔧 Configuration

### OpenAI Settings

- Model: `gpt-4o`
- Temperature: `0.5`
- Max Tokens: Configurable (default: 400-500)

### Job Fetching

- Default Location: India
- Default Rows: 60 jobs per source
- Proxy: Uses Apify residential proxies for LinkedIn scraping

## 🎨 UI Features

- Wide layout for better readability
- Styled result sections with black backgrounds
- Loading spinners for async operations
- Markdown formatting for job listings
- Direct links to job postings

## 🔐 API Keys Required

1. **OpenAI API Key**: Required for resume analysis, skill gap identification, and roadmap generation
   - Get it from: https://platform.openai.com/api-keys

2. **Apify API Token**: Required for scraping jobs from LinkedIn and Naukri
   - Get it from: https://console.apify.com/account/integrations

## 🧪 Core Functions

### helper.py

- `extract_text_from_pdf(uploaded_file)` - Extracts text from uploaded PDF
- `ask_openai(prompt, max_tokens)` - Sends prompts to OpenAI and returns responses

### job_api.py

- `fetch_linkedin_jobs(search_query, location, rows)` - Fetches LinkedIn jobs
- `fetch_naukri_jobs(search_query, location, rows)` - Fetches Naukri jobs

## 📊 Workflow

1. **Upload Resume** → System extracts text from PDF
2. **AI Analysis** → GPT-4o generates summary, identifies gaps, creates roadmap
3. **Display Results** → Formatted output with recommendations
4. **Job Search** → AI extracts relevant keywords from resume
5. **Job Fetching** → Parallel scraping from LinkedIn and Naukri
6. **Job Display** → Organized listing with direct application links

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## 📝 License

This project is open source. Please check the repository for license details.

## ⚠️ Disclaimer

- This tool uses web scraping for job data. Ensure compliance with the terms of service of LinkedIn and Naukri.
- API usage costs apply for both OpenAI and Apify services.
- Job availability and accuracy depend on third-party APIs.

## 🔮 Future Enhancements

- Support for multiple resume formats (DOCX, TXT)
- Additional job portals integration
- Save and track job applications
- Email notifications for new job postings
- Resume improvement suggestions
- Interview preparation tips based on job descriptions

## 📧 Support

For issues, questions, or suggestions, please open an issue in the repository.

---

**Made with ❤️ using OpenAI GPT-4o and Streamlit**
