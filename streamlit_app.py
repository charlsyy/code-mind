import openai
import streamlit as st
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Api Section
openai.api_key = "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"

# Streamlit 
st.set_page_config(page_title="CodeMind - Your Personal Chatbot", layout="wide")

# CSS style
st.markdown(
    """
    <style>
    body {
        background-color: #f4f7fc;
        font-family: 'Poppins', sans-serif;
    }
    .title {
        color: #d35100;
        text-align: center;
        font-size: 45px;
        font-weight: 700;
        margin-bottom: 20px;
    }
    .subtitle {
        font-size: 20px;
        color: #d35100;
        text-align: center;
        margin-bottom: 40px;
    }
    .message {
        background-color: #d35100;
        border-radius: 10px;
        padding: 12px;
        margin-bottom: 15px;
        font-size: 18px;
        width: 90%;
        margin-left: auto;
        margin-right: auto;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
    .user-message {
        background-color: #d35100;
        border-radius: 10px;
        padding: 12px;
        margin-bottom: 15px;
        text-align: right;
        font-size: 18px;
        width: 90%;
        margin-left: auto;
        margin-right: auto;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
    .bot-message {
        border-radius: 10px;
        padding: 12px;
        margin-bottom: 15px;
        font-size: 18px;
        width: 90%;
        margin-left: auto;
        margin-right: auto;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        display: flex;
        align-items: center;
    }
    .bot-avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        margin-right: 15px;
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 20px;
        color: #4A90E2;
    }
    .send-button {
        background-color: #4A90E2;
        color: white;
        border: none;
        border-radius: 10px;
        padding: 12px 30px;
        cursor: pointer;
        font-weight: bold;
        font-size: 18px;
        transition: background-color 0.3s ease;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
    }
    .send-button:hover {
        background-color: #357ABD;
    }
    .feedback-button {
        background-color: #28a745;
        color: white;
        border-radius: 10px;
        padding: 10px 20px;
        font-size: 16px;
        cursor: pointer;
        font-weight: bold;
        transition: background-color 0.3s ease;
    }
    .feedback-button:hover {
        background-color: #218838;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# St Chat History
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "input_text" not in st.session_state:
    st.session_state.input_text = ""

# Main page title
st.markdown('<div class="title">Welcome to CodeMind 🤖</div>', unsafe_allow_html=True)

# User Feedback Section
with st.sidebar:
    st.markdown('<h2 style="color:#d35100;">User Feedback</h2>', unsafe_allow_html=True)
    feedback = st.text_area("Your feedback:", height=200)
    submit_feedback = st.button(
        "Submit Feedback",
        key="submit_feedback",
        help="Send your feedback to improve the bot experience.",
    )

    if submit_feedback and feedback.strip():  # Ensure feedback is not empty
        try:
            sender_email = "codemindfeedback@gmail.com"
            receiver_email = "codemindfeedbackk@gmail.com"
            password = "ranq awud kito tuoo"  # Store securely in production

            # Email server configuration and sending logic
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(sender_email, password)

            # Email message setup
            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = receiver_email
            message["Subject"] = "User Feedback for CodeMind"
            message.attach(MIMEText(feedback.strip(), "plain"))

            server.sendmail(sender_email, receiver_email, message.as_string())
            server.quit()

            st.success("Thank you for your feedback! It has been sent successfully. ✅")
        except Exception as e:
            st.error(f"An error occurred while sending feedback: {e} ❌")
    elif submit_feedback:
        st.warning("Feedback cannot be empty.", icon="⚠️")

# Instruction
st.markdown(
    '<div class="subtitle">I\'m your personal assistant. How can I assist you today?</div>',
    unsafe_allow_html=True,
)

# Display chat history
for chat in st.session_state.chat_history:
    if chat["sender"] == "You":
        st.markdown(
            f'<div class="user-message"><strong>{chat["sender"]}:</strong> {chat["message"]}</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""
            <div class="bot-message">
                <div class="bot-avatar">🤖</div>
                <div><strong>{chat["sender"]}:</strong> {chat["message"]}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# Input and send button section
col1, col2, col3 = st.columns([1, 12, 2])
with col2:
    st.session_state.input_text = st.text_input(
        "",
        key="user_input",
        label_visibility="collapsed",
        placeholder="Type your question here...",
        value=st.session_state.input_text,
    )

with col3:
    send_button = st.button("Send", key="send_button")

# Response Engine
if send_button:
    if st.session_state.input_text.strip():
        user_message = st.session_state.input_text.strip()
        st.session_state.chat_history.append({"sender": "You", "message": user_message})

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": user_message}],
            )
            bot_reply = response["choices"][0]["message"]["content"].strip()
            st.session_state.chat_history.append({"sender": "CodeMind", "message": bot_reply})
        except Exception as e:
            st.session_state.chat_history.append(
                {"sender": "CodeMind", "message": f"Error: {str(e)}"}
            )

        st.session_state.input_text = ""  # Clear input box
    else:
        st.warning("Message cannot be empty. Please type something.", icon="⚠️")
