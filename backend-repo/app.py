from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai
from google.genai import types
import time
import os
from dotenv import load_dotenv
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

load_dotenv()


app = Flask(__name__)
CORS(app)

answer_model = joblib.load(
    os.path.join(os.path.dirname(os.path.abspath(__file__)),
                 "answer_model.joblib")
)

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    raise ValueError("No GEMINI_API_KEY set in environment variables")

# Configure Gemini
# Configure Gemini using the new SDK
client = genai.Client(api_key=GEMINI_API_KEY)

# Function to get the correct model name

def get_generative_model():
    model="gemini-3.5-flash-lite",
    print(f"Initializing Gemini model: {model_name}")
    return genai.GenerativeModel(model_name)


# Initialize model

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok"}), 200





def generate_with_gemini(prompt):
    start = time.time()
    print("Sending request to Gemini...")

    try:
        
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt,
            config=types.GenerateContentConfig(
                thinking_config=types.ThinkingConfig(
                    thinking_level="minimal"
                ),
                max_output_tokens=700,
            ),
        )


        elapsed = time.time() - start
        print(f"Gemini generation took {elapsed:.2f} seconds")

        if response.text:
            return response.text

        print("Gemini returned an empty response.")
        return ""

    except Exception as e:
        print(
            f"Gemini failed after "
            f"{time.time() - start:.2f} seconds: {repr(e)}"
        )
        raise



        
        
@app.route('/', methods=['GET'])
def welcome():
    return jsonify({
        'message': 'Welcome to Interview Coach API',
        'endpoints': {
            'generate_questions': {
                'method': 'POST',
                'url': '/generate-questions',
                'parameters': {
                    'job_role': 'string (required)',
                    'company_name': 'string (optional)',
                    'project': 'string (optional)',
                    'experience_level': 'string (optional)'
                }
            },
            'generate_answer': {
                'method': 'POST',
                'url': '/generate-answer',
                'parameters': {
                    'question': 'string (required)',
                    'job_role': 'string (optional)',
                    'company_name': 'string (optional)',
                    'project': 'string (optional)',
                    'context': 'string (optional)'
                }
            }
        },
        'status': 'active'
    })        


@app.route('/generate-questions', methods=['POST'])
def generate_questions():
    try:
        data = request.json
        job_role = data.get('job_role')
        company_name = data.get('company_name', 'a company')
        project = data.get('project', 'relevant projects')
        experience_level = data.get('experience_level', 'mid-level')
        
        if not job_role:
            return jsonify({'error': 'Job role is required'}), 400
        
        prompt = f"""
        Generate exactly 5 interview questions for a {experience_level} {job_role} position at {company_name}.
        The candidate has experience with {project}.

        Requirements:
        1. Generate exactly 5 questions - no more, no less
        2. Questions should be numbered from 1 to 5
        3. Each question must be on a separate line
        4. Include a mix of:
           - Technical questions specific to {job_role}
           - Behavioral/situational questions
           - Problem-solving scenarios
        5. Tailor questions to {company_name}'s likely needs
        6. Consider the candidate's background in {project}

        Format strictly like this:
        1. First question?
        2. Second question?
        3. Third question?
        4. Fourth question?
        5. Fifth question?

        Do not include any additional text or explanations.
        """
        
        response = generate_with_gemini(prompt)
        if not response.strip():
            return jsonify({
                'error': 'Gemini returned an empty response. Check the backend terminal.'
            }), 502
        # Process the response to extract exactly 5 questions
        questions = []
        for line in response.split('\n'):
            line = line.strip()
            if line and line[0].isdigit():  # Only take numbered lines
                question = ' '.join(line.split()[1:])  # Remove the number
                questions.append(question)
                if len(questions) == 5:
                    break
        
        # If we didn't get 5 questions, fill the rest with placeholders
        if len(questions) < 5:
            print("Unexpected Gemini response:", repr(response))
            return jsonify({
                'error': 'Gemini did not return five numbered questions.',
                'response': response
            }), 502
        
        return jsonify({'questions': questions[:5]})  # Ensure exactly 5
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
        
@app.route('/generate-answer', methods=['POST'])
def generate_answer():
    try:
        data = request.json
        question = data.get('question')
        job_role = data.get('job_role', '')
        company_name = data.get('company_name', '')
        project = data.get('project', '')
        context = data.get('context', '')
        
        if not question:
            return jsonify({'error': 'Question is required'}), 400
        
        # prompt = f"""
        # You are helping a candidate prepare for a {job_role} position at {company_name}.
        # The candidate has experience with {project} and provided this context: {context}
        
        # Provide a comprehensive answer to this interview question:
        # Question: {question}
        
        # The answer should:
        # 1. Be tailored for {company_name}
        # 2. Highlight relevant experience with {project}
        # 3. Be concise but detailed (2-3 paragraphs)
        # 4. Include specific examples
        # 5. Use professional language
        
        # Answer:
        # """
        prompt = f"""
        **Role**: You're a senior {job_role} interviewing at {company_name}. 
        **Task**: Answer this question: "{question}" 

        **Context**:
        - Company Research: {company_name} is known for: [AI will insert relevant facts]
        - My Project: {project} ({context})
        - Job Requirements: {job_role} needs [AI will infer key skills]

        **Answer Requirements**:
        1. **Company Alignment**:
        - Open with how your experience relates to {company_name}'s mission/products
        - Use 1-2 facts about the company's tech stack/approach if known
        - Example: "At {company_name} where [specific observation], I..."

        2. **Project Demonstration**:
        - Use {project} as your primary case study
        - Include:
            - Technical specifics ("Used TensorFlow to...")
            - Quantifiable impact ("Improved efficiency by 30%...")
            - Lessons learned

        3. **Role-Specific**:
        - Highlight 3 {job_role} core competencies
        - Show progression from junior to senior thinking

        4. **Structure**:
        - 1-2 paragraphs max
        - STAR method (Situation-Task-Action-Result)
        - Action verbs: "Architected", "Optimized", "Led"

        **Example Framework**:
        "As [Company] emphasizes [value], my work on [Project] required [skill]. 
        When faced with [challenge], I [action] using [tech], resulting in [metric] improvement. 
        This experience directly applies to your [specific team/product] because..." 

        **Generate Answer**: 
        """
        answer = generate_with_gemini(prompt)
        return jsonify({
            'question': question,
            'answer': answer
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/evaluate-answer', methods=['POST'])
def evaluate_answer():
    data = request.get_json(silent=True) or {}

    answer = data.get('answer', '').strip()
    reference = data.get('reference_answer', '').strip()

    if not answer or not reference:
        return jsonify({
            "error": "Both answer and reference_answer are required."
        }), 400

    # ML classification
    predicted_label = answer_model.predict([answer])[0]
    reference_predicted_label = answer_model.predict([reference])[0]

    # Separate lexical similarity measurement
    
    vectorizer = TfidfVectorizer()

    try:
        vectors = vectorizer.fit_transform([answer, reference])
        similarity = cosine_similarity(
            vectors[0:1], vectors[1:2]
        )[0][0]
    except ValueError:
        similarity = 0.0


    return jsonify({
        "predicted_category": predicted_label,
        "reference_category": reference_predicted_label,
        "similarity_percent": round(float(similarity) * 100, 2)
    }), 200


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port)
