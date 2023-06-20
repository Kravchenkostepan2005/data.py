import openai
from fastapi import FastAPI
from pydantic import BaseModel
from bs4 import BeautifulSoup

app = FastAPI()
API_KEY = "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"
openai.api_key = API_KEY

model_id = "gpt-3.5-turbo"


class EmailRequest(BaseModel):
    html: str

@app.post("/extract_text_from_email")
def extract_text_from_email(request: EmailRequest):
    soup = BeautifulSoup(request.html, "html.parser")
    email_text = soup.get_text(separator=" ")

    prompt = f"Create a summary for an email: {email_text}"

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=100,
        temperature=0.7,
        n=1,
        stop=None,
    )

    summary = response.choices[0].text.strip()

    return {"summary": summary}
