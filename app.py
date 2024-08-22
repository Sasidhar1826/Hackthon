import streamlit as st
import requests
import json
import random

# Import quiz questions from the external file
from quiz_questions import quiz_questions

# Set up your Gemini API key securely
GEMINI_API_KEY = "AIzaSyBkyu7ABEMNLxCIfxBk7-Yl4if0lS8QtJE"

# Function to generate financial advice using Gemini API
def get_financial_advice(question):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"  # Example URL, verify with actual API docs
    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": GEMINI_API_KEY
    }
    data = {
        "contents": [{
            "parts": [{
                "text": f"You are a financial expert. Answer the following question about finances: {question}"
            }]
        }]
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        # Parse the response correctly based on the API's response structure
        response_json = response.json()
        try:
            answer = response_json["candidates"][0]["content"]["parts"][0]["text"]
            return answer
        except KeyError:
            st.error("Unexpected response format from Gemini API")
            return None
    else:
        st.error(f"Failed to get an answer from Gemini API: {response.status_code}")
        return None

# Function to display a random quiz question
def show_quiz():
    # Store the current question and state of submission in session state
    if "current_question" not in st.session_state or st.session_state.submitted:
        st.session_state.current_question = random.choice(quiz_questions)
        st.session_state.submitted = False
    
    question = st.session_state.current_question

    st.write(f"### Quiz: {question['question']}")
    
    # Display the options as radio buttons
    user_answer = st.radio("Choose an answer:", question["options"], key="selected_answer")
    
    if st.button("Submit Answer") and not st.session_state.submitted:
        st.session_state.submitted = True
        if user_answer == question["answer"]:
            st.success("Correct! ")
        else:
            st.error(f"Incorrect. The correct answer is: {question['answer']}")

        # Reset the session state
        st.session_state.submitted = False
        st.session_state.current_question = random.choice(quiz_questions)


# Streamlit UI for WealthWise
def main():
    st.title("WealthWise: Your Personal Financial Assistant")
    st.subheader("Empowering Young Adults to Make Smart Financial Choices")

    # Tabs for Advice and Quiz sections
    tab1, tab2 = st.tabs(["Get Financial Advice", "Financial Knowledge Quiz"])

    # Get Financial Advice tab
    with tab1:
        user_input = st.text_input("Ask WealthWise a financial question or get advice on a topic:")
        
        if st.button("Get Financial Advice"):
            if user_input:
                advice = get_financial_advice(user_input)
                if advice:
                    st.write("### WealthWise Advice:")
                    st.write(advice)
            else:
                st.warning("Please enter a question to get advice.")
    
    # Financial Knowledge Quiz tab
    with tab2:
        st.write("Test your financial knowledge with our quiz!")
        show_quiz()

    # Sidebar with additional features
    st.sidebar.header("Features")
    st.sidebar.write("• Personalized financial advice")
    st.sidebar.write("• Instant tips on budgeting, saving, and managing debt")
    st.sidebar.write("• Weekly financial tasks to practice")
    st.sidebar.write("• Fun quizzes to test your knowledge")

if __name__ == "__main__":
    main()