from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
from bs4 import BeautifulSoup
import requests

app = FastAPI()

templates = Jinja2Templates(directory="templates")

model_name = "EleutherAI/gpt-neo-1.3B"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)
generator = pipeline("text-generation", model=model, tokenizer=tokenizer)


def identify_intent(generator, message, pages_visited):
    prompt = f"""
    Identify the intent of the user based on the following:
    - Message: {message}
    - Pages Visited: {', '.join(pages_visited)}
    Provide a concise summary of the user's intent.
    """
    result = generator(prompt, max_length=150, num_return_sequences=1)
    return result[0]["generated_text"].strip()

def scrape_page_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    
    title = soup.title.string if soup.title else "No title available"
    description = soup.find("meta", attrs={"name": "description"})
    description = description["content"] if description else "No description available"
    
    return {"url": url, "title": title, "description": description}

def generate_email(generator, intent, scraped_data):
    prompt = f"""
    Generate a professional email based on the following:
    - User Intent: {intent}
    - Scraped Data: {scraped_data}
    Use the following structure:
    - Greeting
    - Address the user's intent
    - Highlight relevant case studies
    - Include company introduction and portfolio links
    """
    result = generator(prompt, max_length=500, num_return_sequences=1)
    return result[0]["generated_text"].strip()


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/analyze-urls", response_class=HTMLResponse)
async def process_form(
    request: Request,
    message: str = Form(...),
    pages: str = Form(...)
):
    pages_visited = [page.strip() for page in pages.split(",")]
    intent = identify_intent(generator, message, pages_visited)
    scraped_data = [scrape_page_data(url) for url in pages_visited]
    email = generate_email(generator, intent, scraped_data)
    
    return templates.TemplateResponse(
        "result.html",
        {"request": request, "intent": intent, "email": email}
    )
