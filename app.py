import streamlit as st
from chatbot import FAQChatbot
import random

# --- Page Config ---
st.set_page_config(
    page_title="TrustMicro Chatbot 🤖",
    page_icon="💬",
    layout="centered"
)

# --- Master Suggestions ---
MASTER_SUGGESTIONS = [
    "How do I apply for a loan?",
    "What are your savings rates?",
    "How do I repay my loan?",
    "What documents do I need to open an account?",
    "Can I get a loan without collateral?",
    "What is the interest rate on loans?",
    "How long does it take to process a loan?",
    "Can I open a savings account online?",
    "Is there a penalty for late repayment?",
    "How can I check my loan balance?"
]

# --- Sidebar ---
with st.sidebar:
    st.title("💼 TrustMicro")
    st.markdown(
        """
        Welcome to the TrustMicro AI FAQ Assistant!  

        **Available Topics:**  
        - 💰 Loans  
        - 💸 Savings  
        - 📅 Repayments  
        - 🏦 Account Opening  
        - ❓ General Inquiries  

        ---
        💡 *Tip:* Type naturally—I’ll do my best to help you!
        """
    )
    st.caption("🧭 Powered by TrustMicro AI")

# --- Load Chatbot with Caching ---
@st.cache_resource
def load_bot():
    with st.spinner("Loading AI model... Please wait ⏳"):
        return FAQChatbot("faq_cleaned.csv")

bot = load_bot()

# --- Initialize Session State ---
if "history" not in st.session_state:
    st.session_state.history = []

if "suggested" not in st.session_state:
    st.session_state.suggested = random.sample(MASTER_SUGGESTIONS, 4)

# --- Helper: Refresh Suggested Questions ---
def refresh_suggestions(last_question):
    remaining = [q for q in MASTER_SUGGESTIONS if q.lower() != last_question.lower()]
    new_suggestions = random.sample(remaining, 4) if len(remaining) >= 4 else remaining
    st.session_state.suggested = new_suggestions

# --- App Title ---
st.title("💬 TrustMicro - Your AI FAQ Assistant")
st.markdown(
    """
    👋 Hello! I'm TrustMicro, your friendly Microfinance assistant.  
    Ask me about loans, savings, repayments, and more.  
    I'm here to help 24/7. 🌟
    """
)
st.divider()

# --- Display Conversation History (latest first) ---
if st.session_state.history:
    st.subheader("📜 Chat History")
    for chat in reversed(st.session_state.history):  # Latest on top
        with st.chat_message("user"):
            st.markdown(f"🧑‍💼 **You:** {chat['user']}")
        with st.chat_message("assistant"):
            st.markdown(chat['response'])
            st.caption(f"🤖 *Confidence Score:* `{chat['score']:.2f}`")
    st.divider()
else:
    st.info("🤖 Ready to answer your questions! Start by typing below.")

# --- Suggested Questions ---
st.subheader("💡 Suggested Questions")
suggested_cols = st.columns(len(st.session_state.suggested))
for idx, question in enumerate(st.session_state.suggested):
    if suggested_cols[idx].button(question):
        st.session_state.user_input = question
        st.session_state.submit_now = True

# --- User Input Field at Bottom ---
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Type your question here...")
    submitted = st.form_submit_button("Send")

if "submit_now" in st.session_state and st.session_state.submit_now:
    user_input = st.session_state.user_input
    submitted = True
    st.session_state.submit_now = False

# --- Processing User Input ---
if submitted and user_input:
    question, answer, score = bot.get_best_match(user_input)
    
    if score >= 0.80:
        response_text = f"✅ **Answer:** {answer}"
    elif score >= 0.55:
        response_text = (
            f"🤔 *I think you might be asking:*  \n"
            f"**Q:** {question}  \n"
            f"**A:** {answer}  \n\n"
            f"If this doesn't help, please try rephrasing for a better match! ✨"
        )
    else:
        response_text = (
            "⚠️ I'm sorry, I couldn't confidently answer that. "
            "Could you please rephrase your question?"
        )
        bot.save_unanswered(user_input)
        st.info("✨ *Your question has been saved for review to improve this assistant.*")

    # Add to history
    st.session_state.history.append({
        "user": user_input,
        "response": response_text,
        "score": score
    })

    # Refresh suggestions to avoid repeats
    refresh_suggestions(user_input)

# --- Footer ---
st.caption("🧭 Powered by TrustMicro AI")
