from apify_client import ApifyClient
import os 
from dotenv import load_dotenv
import requests
load_dotenv()

apify_client = ApifyClient(os.getenv("APIFY_API_TOKEN"))

# Fetch jobs from RemoteOK (Free, No Auth Required)
def fetch_remoteok_jobs(search_query, max_jobs=60):
    """Fetch remote jobs from RemoteOK API"""
    try:
        url = "https://remoteok.com/api"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            all_jobs = response.json()[1:]  # Skip first item (metadata)
            
            # Filter jobs based on search query
            filtered_jobs = []
            search_terms = search_query.lower().split(',')
            
            for job in all_jobs[:max_jobs * 2]:  # Get more to filter
                job_text = f"{job.get('position', '')} {job.get('company', '')} {job.get('tags', '')}".lower()
                
                # Check if any search term matches
                if any(term.strip() in job_text for term in search_terms):
                    filtered_jobs.append({
                        'title': job.get('position', 'N/A'),
                        'companyName': job.get('company', 'N/A'),
                        'location': 'Remote',
                        'url': job.get('url', ''),
                        'tags': ', '.join(job.get('tags', [])[:5]) if job.get('tags') else 'N/A'
                    })
                
                if len(filtered_jobs) >= max_jobs:
                    break
            
            return filtered_jobs[:max_jobs]
        
        return []
    except Exception as e:
        print(f"Error fetching RemoteOK jobs: {e}")
        return []


# Fetch jobs from Adzuna API (Free tier available)
def fetch_adzuna_jobs(search_query, location="india", max_jobs=60):
    """Fetch jobs from Adzuna API"""
    try:
        app_id = os.getenv("ADZUNA_APP_ID")
        app_key = os.getenv("ADZUNA_APP_KEY")
        
        if not app_id or not app_key:
            return []
        
        url = f"https://api.adzuna.com/v1/api/jobs/in/search/1"
        params = {
            "app_id": app_id,
            "app_key": app_key,
            "what": search_query,
            "where": location,
            "results_per_page": max_jobs,
            "content-type": "application/json"
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            jobs = []
            
            for job in data.get('results', []):
                jobs.append({
                    'title': job.get('title', 'N/A'),
                    'companyName': job.get('company', {}).get('display_name', 'N/A'),
                    'location': job.get('location', {}).get('display_name', 'N/A'),
                    'url': job.get('redirect_url', ''),
                    'description': job.get('description', '')[:200] + '...'
                })
            
            return jobs
        
        return []
    except Exception as e:
        print(f"Error fetching Adzuna jobs: {e}")
        return []


# LinkedIn job fetching disabled - Requires paid Apify actor
# def fetch_linkedin_jobs(search_query, location = "india", rows=60):
#     run_input = {
#             "title": search_query,
#             "location": location,
#             "rows": rows,
#             "proxy": {
#                 "useApifyProxy": True,
#                 "apifyProxyGroups": ["RESIDENTIAL"],
#             }
#         }
#     run = apify_client.actor("BHzefUZlZRKWxkTck").call(run_input=run_input)
#     jobs = list(apify_client.dataset(run["defaultDatasetId"]).iterate_items())
#     return jobs


# Fetch Naukri jobs based on search query and location
def fetch_naukri_jobs(search_query, location = "india", rows=60):
    try:
        run_input = {
            "keyword": search_query,
            "maxJobs": 60,
            "freshness": "all",
            "sortBy": "relevance",
            "experience": "all",
        }
        run = apify_client.actor("alpcnRV9YI9lYVPWk").call(run_input=run_input)
        jobs = list(apify_client.dataset(run["defaultDatasetId"]).iterate_items())
        return jobs
    except Exception as e:
        print(f"Error fetching Naukri jobs: {e}")
        return []
