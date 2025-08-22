
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from reddit_scrapper import reddit_crawler
from llm import summarize_problems, generate_solutions
from exporter import save_to_markdown, markdown_to_pdf

app = FastAPI()

from fastapi.responses import FileResponse

# PDF download endpoint
@app.get("/download/pdf")
def download_pdf():
    return FileResponse(
        "solutions.pdf",
        media_type="application/pdf",
        filename="solutions.pdf"
    )

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this to your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Backend is running!"}

@app.get("/scrape/{subreddit}")
def scrape_and_analyze(subreddit: str, limit: int = 10):
    """Fetch Reddit posts, summarize with LLM, and generate solutions"""
    data = reddit_crawler(subreddit, limit)
    if not data:
        return {"error": f"No data found for subreddit: {subreddit}"}

    summary = summarize_problems(data)
    solutions = generate_solutions(summary)

    # Save outputs
    save_to_markdown(solutions)
    markdown_to_pdf()

    return {
        "summary": summary,
        "solutions": solutions,
        "pdf_file": "solutions.pdf"
    }
