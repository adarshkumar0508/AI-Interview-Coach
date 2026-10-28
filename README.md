# 🎤 AI Interview Coach

**Your personal AI-powered interview preparation assistant.** AI Interview Coach helps candidates build confidence and prepare for job interviews with role-specific questions and AI-generated sample answers powered by Google's Gemini AI.

## ✨ Features

- 🎯 **Role-specific questions** — Generate interview questions tailored to a target job title.
- 📊 **Experience-level customization** — Prepare for entry-level, mid-level, and senior roles.
- 🏢 **Company-specific preparation** — Add a target company for more contextual interview practice.
- 💡 **AI-generated model answers** — Get sample answers for generated questions using Gemini AI.
- 🔍 **Personalized context** — Include your background, skills, and projects to tailor responses.
- 🧠 **Machine-learning answer evaluation** — Classify answers as *Good*, *Average*, or *Needs Improvement* and compare candidate responses with reference answers using cosine similarity.
- 📈 **Model performance dashboard** — View accuracy, precision, recall, and F1-score from the trained evaluation model.
- 🌙 **Dark/light appearance** — The interface is designed to support dark and light themes, depending on the app configuration.

## 🧰 Tech Stack

| Component | Technologies |
|---|---|
| Frontend | Python, Streamlit |
| Backend | Python, Flask, Flask-CORS |
| Generative AI | Google Gemini API (`google-genai`) |
| Machine learning | scikit-learn, TF-IDF, Logistic Regression, cosine similarity |
| Model persistence | Joblib |
| Deployment | Render (as described in the project overview) |
| Production server | Gunicorn (backend deployment) |

## 🏗️ Architecture

1. The user enters a job role, experience level, target company, and relevant background.
2. The Streamlit frontend sends requests to the Flask REST API.
3. The backend uses Gemini AI to generate interview questions and sample answers.
4. The answer-evaluation endpoint uses a trained TF-IDF/Logistic Regression model to classify answers and computes cosine similarity against a reference answer.
5. The frontend displays generated content, answer-evaluation output, and saved model-performance metrics.

> **Note:** Cosine similarity measures textual similarity, not factual correctness. The machine-learning classification is a prototype and should be interpreted in light of the size and quality of its training dataset.

## 📁 Repository Structure

```text
AI-Interview-Coach/
├── backend-repo/
│   ├── app.py
│   ├── train_model.py
│   ├── answer_model.joblib
│   ├── model_metrics.joblib
│   └── ...
├── frontend-repo/
│   ├── app.py
│   └── ...
└── README.md
```

*The exact files may differ depending on your current repository version.*

## ⚙️ Run Locally

### Prerequisites

- Python 3.10+ recommended
- A Google Gemini API key
- Git

### 1. Clone the repository

```bash
git clone https://github.com/adarshkumar0508/AI-Interview-Coach.git
cd AI-Interview-Coach
```

### 2. Configure the backend

```bash
cd backend-repo
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file in `backend-repo/` and add your API key:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

Start the backend:

```bash
python app.py
```

The backend is configured to run on port `5001` in the local setup described for this project. If your `app.py` uses a different port, use that port instead.

### 3. Configure the frontend

Open a **second terminal** from the repository root:

```bash
cd frontend-repo
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Make sure the frontend's backend URL points to your local Flask server, for example:

```python
BACKEND_URL = "http://127.0.0.1:5001"
```

Start Streamlit:

```bash
streamlit run app.py
```

Open the local URL shown in the terminal, usually `http://localhost:8501`.

## 🤖 Train the Answer Evaluation Model

From the backend directory, activate its virtual environment and run:

```bash
python train_model.py
```

This trains and saves the answer-classification model and its evaluation metrics. The exact metrics depend on the training examples and train/test split. With a very small manually labeled dataset, metrics can vary substantially and should be treated as preliminary.

## 🚀 Deployment

The project overview describes deployment with **Render**:
- Deploy the Flask backend as a web service using Gunicorn.
- Deploy the Streamlit frontend as a separate service.
- Configure the backend URL in the frontend to use the deployed backend URL.
- Add `GEMINI_API_KEY` as a secret environment variable in the backend service settings. Do not commit API keys or `.env` files to GitHub.

Deployment settings and start commands depend on the current `render.yaml`, `Procfile`, and dependency files in your repository. Verify those files before deploying.

**Cold starts:** The hosted backend may take around 30 seconds to respond on its first request after inactivity, as noted in the project overview.

## 🔐 Security

- Never commit your `.env` file or API keys.
- Use environment variables for secrets.
- Keep local virtual environments (`venv/`) out of version control.

## 🛣️ Future Improvements

- Expand and validate the labeled answer dataset.
- Evaluate the model on a larger, representative test set.
- Improve feedback beyond lexical similarity.
- Add more detailed interview history and progress tracking.

## 👤 Author

**Adarsh Kumar Rai**

GitHub: [@adarshkumar0508](https://github.com/adarshkumar0508)

## 📄 License

No license has been specified yet. Add a `LICENSE` file if you want to define how others may use, modify, and distribute this project.
