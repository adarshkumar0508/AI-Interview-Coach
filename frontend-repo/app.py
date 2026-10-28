import streamlit as st
import requests
import json

BACKEND_URL = "http://127.0.0.1:5001"






# Page setup
st.set_page_config(
    page_title="AI Interview Coach",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Configuration

BACKEND_URL = "http://127.0.0.1:5001"  # Update if your backend is hosted elsewhere
# BACKEND_URL = "http://localhost:5000"
# Conditional warning

# Health check

# Health check
def is_backend_live():
    try:
        response = requests.get(
            f"{BACKEND_URL}/health",
            timeout=5
        )
        if response.status_code != 200:
            return False

        return response.json().get("status") == "ok"

    except (requests.exceptions.RequestException, ValueError):
        return False


if not is_backend_live():
    st.warning(
        "⚠️ Make sure to run the backend server before using the AI Interview Coach."
    )



def call_backend(endpoint, data):
    try:
        response = requests.post(f"{BACKEND_URL}/{endpoint}", json=data)
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}


# Custom CSS

st.markdown("""
    <style>
        /* Base styles that work in both light and dark modes */
        .main {
            background-color: var(--background-color);
        }
        .stTextInput input, .stTextArea textarea {
            border-radius: 10px;
            padding: 10px;
            background-color: var(--input-bg);
            color: var(--text-color);
        }
        .stButton button {
            background-color: #4a6fa5;
            color: white;
            border-radius: 10px;
            padding: 10px 24px;
            font-weight: bold;
            border: none;
        }
        .stButton button:hover {
            background-color: #3a5a80;
        }
        .question-card {
            background-color: var(--card-bg);
            color: var(--text-color);
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 15px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .answer-card {
            background-color: var(--answer-bg);
            color: var(--text-color);
            border-radius: 10px;
            padding: 20px;
            margin-top: 10px;
            border-left: 4px solid #4a6fa5;
        }
        
        /* Dark mode variables */
        @media (prefers-color-scheme: dark) {
            :root {
                --background-color: #0e1117;
                --text-color: #f0f2f6;
                --input-bg: #262730;
                --card-bg: #1a1c24;
                --answer-bg: #262730;
            }
        }
        
        /* Light mode variables */
        @media (prefers-color-scheme: light) {
            :root {
                --background-color: #f5f7fa;
                --text-color: #2c3e50;
                --input-bg: #ffffff;
                --card-bg: #ffffff;
                --answer-bg: #f0f4f8;
            }
        }
        
        /* Force dark text in specific elements if needed */
        .stMarkdown, .stText, .stExpander {
            color: var(--text-color) !important;
        }
    </style>
""", unsafe_allow_html=True)
# Sidebar
with st.sidebar:
    st.title("💼 AI Interview Coach")
    st.markdown("""
        **Your personal interview preparation assistant**  
        Get tailored interview questions and expert answers for your dream job.
    """)
    
    st.markdown("---")
    st.markdown("### How to use:")
    st.markdown("1. Enter your target job role")
    st.markdown("2. Select your experience level")
    st.markdown("3. Get relevant questions")
    st.markdown("4. Practice with AI-generated answers")

    
    st.markdown("---")
    st.markdown("### About")
    st.markdown("This tool uses Google's Gemini AI to help you prepare for interviews by generating role-specific questions and model answers.")

    st.markdown("---")
    st.markdown("### 🔗 Extension Available")
    st.markdown("""
        Prefer using the tool directly in your browser?  
       
        Use the AI Interview Coach without opening the website!
    """)


# Main content
st.title("AI Interview Coach")


st.markdown("""
    Prepare for your next job interview with personalized questions and expert-crafted answers 
    tailored to your target role and experience level.
""")

# Tab interface
tab1, tab2, tab3, tab4 = st.tabs([
    "Generate Questions",
    "Practice Answers",
    "ML Answer Evaluation",
    "Model Performance"
])

with tab1:
    st.header("Generate Interview Questions")
    
    with st.form("question_form"):
        col1, col2 = st.columns(2)
        with col1:
            job_role = st.text_input("Job Role*", placeholder="e.g., Software Engineer")
            company_name = st.text_input("Company Name", placeholder="e.g., Google")
        with col2:
            experience_level = st.selectbox(
                "Experience Level",
                ("Entry-level", "Mid-level", "Senior", "Executive"),
                index=1
            )
            project = st.text_input("Your Relevant Project", placeholder="e.g., E-commerce platform")
        
        submitted = st.form_submit_button("Generate Questions")
        
        if submitted:
            if not job_role:
                st.error("Please enter a job role")
            else:
                with st.spinner("Generating tailored interview questions..."):
                    response = requests.post(
                        f"{BACKEND_URL}/generate-questions",
                        json={
                            "job_role": job_role,
                            "company_name": company_name,
                            "project": project,
                            "experience_level": experience_level.lower()
                        }
                    )
                    
                    if response.status_code == 200:
                        questions = response.json().get("questions", [])
                        # Store the original questions list in session state
                        st.session_state.questions_list = questions
                        st.session_state.job_role = job_role
                        st.session_state.company_name = company_name
                        st.session_state.project = project
                        
                        st.success(f"Questions tailored for {company_name or 'your target role'}:")
                        for i, question in enumerate(questions):
                            with st.expander(f"Question {i+1}"):
                                st.markdown(f"<div class='question-card'>{question}</div>", unsafe_allow_html=True)
                    else:
                        st.error(f"Error: {response.json().get('error', 'Unknown error')}")
with tab2:
    st.header("Practice with Model Answers")
    
    if "questions_list" not in st.session_state or not st.session_state.questions_list:
        st.warning("First generate questions in the previous tab")
    else:
        selected_question = st.selectbox(
            "Select a question to practice",
            st.session_state.questions_list
        )
        
        col1, col2 = st.columns(2)
        with col1:
            job_role_answer = st.text_input("Job Role (for answer)", value=st.session_state.get("job_role", ""))
            company_name_answer = st.text_input("Company Name (for answer)", value=st.session_state.get("company_name", ""))
        with col2:
            project_answer = st.text_input("Your Project (for answer)", value=st.session_state.get("project", ""))
        
        context = st.text_area("Additional Context About You", height=100,
                             placeholder="e.g., I led a team of 3 developers...")
        
        if st.button("Generate Answer"):
            with st.spinner("Generating expert answer..."):
                response = requests.post(
                    f"{BACKEND_URL}/generate-answer",
                    json={
                        "question": selected_question,
                        "job_role": job_role_answer,
                        "company_name": company_name_answer,
                        "project": project_answer,
                        "context": context
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    st.markdown("### Question")
                    st.markdown(f"<div class='question-card'>{selected_question}</div>", unsafe_allow_html=True)
                    
                    st.markdown("### Suggested Answer")
                    answer = data.get("answer", "")
                    st.session_state["generated_answer"] = answer
                    st.session_state["generated_question"] = selected_question

                    st.markdown(
                        f"<div class='answer-card'>{answer}</div>",
                        unsafe_allow_html=True
                    )
                else:
                    st.error(f"Error: {response.json().get('error', 'Unknown error')}")


with tab3:
    st.header("ML-Based Answer Evaluation")
    st.write(
        "Select an interview question, load its generated reference answer, "
        "and evaluate your response."
    )

    questions = st.session_state.get("questions_list", [])

    if questions:
        question = st.selectbox(
            "Select Interview Question",
            questions,
            key="ml_question"
        )
    else:
        question = st.text_input(
            "Interview Question",
            key="ml_question_manual"
        )
        st.info("Generate questions in the first tab to select from your questions.")

    if st.button(
        "Use Generated Answer as Reference",
        key="use_reference_answer"
    ):
        generated_answer = st.session_state.get("generated_answer", "")
        generated_question = st.session_state.get("generated_question", "")

        if not generated_answer:
            st.warning("Generate a model answer in the Practice Answers tab first.")
        elif generated_question != question:
            st.warning(
                "This reference answer belongs to a different question. "
                "Generate an answer for the selected question in Practice Answers first."
            )
        else:
            st.session_state["ml_reference_answer"] = generated_answer
            st.rerun()

    reference_answer = st.text_area(
        "Reference Answer",
        key="ml_reference_answer"
    )

    candidate_answer = st.text_area(
        "Your Answer",
        key="ml_candidate"
    )

    if st.button("Evaluate My Answer", key="ml_evaluate_answer"):
        if not candidate_answer.strip() or not reference_answer.strip():
            st.warning("Enter both answers before evaluating.")
        else:
            try:
                response = requests.post(
                    f"{BACKEND_URL}/evaluate-answer",
                    json={
                        "question": question,
                        "answer": candidate_answer,
                        "reference_answer": reference_answer
                    },
                    timeout=15
                )

                if response.ok:
                    result = response.json()
                    col1, col2 = st.columns(2)

                    with col1:
                        st.subheader("Gemini Reference Answer")
                        st.info(
                            f"ML Category: {result['reference_category']}"
                        )

                    with col2:
                        st.subheader("Your Answer")
                        st.success(
                            f"ML Category: {result['predicted_category']}"
                        )
                    st.metric(
                        "Text Similarity",
                        f"{result['similarity_percent']}%"
                    )
                    st.caption(
                        "Similarity measures text overlap, not factual "
                        "correctness. The ML classifier is a prototype."
                    )
                else:
                    try:
                        error = response.json().get(
                            "error", "Evaluation failed."
                        )
                    except ValueError:
                        error = "Evaluation failed."
                    st.error(error)

            except requests.exceptions.RequestException:
                st.error(
                    "Cannot connect to the backend. "
                    "Check that Flask is running on port 5001."
                )

with tab4:
    st.header("ML Model Performance")
    st.write("Evaluation metrics measured on the held-out test dataset.")

    import os
    import joblib

    metrics_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "..",
        "backend-repo",
        "model_metrics.joblib"
    )

    if os.path.exists(metrics_path):
        metrics = joblib.load(metrics_path)

        col1, col2 = st.columns(2)
        col1.metric("Accuracy", f"{metrics['accuracy']:.2%}")
        col2.metric("Precision", f"{metrics['precision']:.2%}")

        col3, col4 = st.columns(2)
        col3.metric("Recall", f"{metrics['recall']:.2%}")
        col4.metric("F1-Score", f"{metrics['f1_score']:.2%}")

        st.warning(
            "These preliminary results are based on only 6 test examples. "
            "They may not represent performance on new interview answers."
        )
    else:
        st.error(
            "Metrics file not found. Train the model using train_model.py first."
        )
