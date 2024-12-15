# API Development and Business Proposal

This project identifies the user's intent by analyzing the "message section" and "pages visited." It generates a customized email template based on the extracted intent.

The project uses EleutherAI/gpt-neo-1.3B for testing purposes due to hardware limitations. While this model may not always provide optimal results, it demonstrates the concept effectively.A screenshot of the llm model web app is included for reference. For improved performance, OpenAI API with a better model has also been implemented.The link to Implimentation will be shared via email.


### Features :

Accepts user input (name, email, message, and pages visited),
<br/>Scrapes relevant data from the provided URLs,
<br/>Uses an LLM to generate a customized email,
<br/>Returns the generated email response.

### Prerequisites :

Python 3.9 or later

### Running Locally :

git clone https://github.com/Dilip-code/email_generate_llm.git

cd email_generate_llm

pip install -r requirements.txt

uvicorn main:app --reload

The API will be running at: http://127.0.0.1:8000

### Running with Docker :

docker build -t email_generate_llm .

docker run -p 8000:8000 email_generate_llm

The API will be accessible at: http://127.0.0.1:8000
