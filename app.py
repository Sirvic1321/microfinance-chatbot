import streamlit as st
from chatbot import FAQChatbot
import random

# --- Page Configuration ---
st.set_page_config(
    page_title="TrustMicro Chatbot 🤖",
    page_icon="💬",
    layout="centered"
)

# --- Sidebar Info ---
with st.sidebar:
    st.title("💼 TrustMicro")
    st.markdown(
        """
        Welcome to the TrustMicro AI FAQ Assistant!

        *Available topics:*    
        - 💰 Loans    
        - 💸 Savings    
        - 📅 Repayments    
        - 🏦 Account Opening    
        - ❓ General Inquiries    

        ---  
        **Tip:** Type naturally—I'll do my best to help you!  
        """
    )
    st.caption("🧭 Powered by TrustMicro AI")

# --- Load and Cache Chatbot ---
@st.cache_resource
def load_bot():
    with st.spinner("Loading AI model... Please wait ⏳"):
        return FAQChatbot("faq_cleaned.csv")

bot = load_bot()

# --- Load all questions from CSV for Suggestions ---
all_questions = bot.questions

# Pre-prioritize most helpful, basic questions
priority_questions = [
    "How do I apply for a loan?",
    "What are your interest rates?",
    "How do I open an account?",
    "How can I repay my loan?"
]

# Fallback random pool
secondary_questions = [q for q in all_questions if q not in priority_questions]

# --- Suggestion Management in Session State ---
if "suggestions" not in st.session_state:
    st.session_state.suggestions = priority_questions.copy()

def get_next_suggestions():
    """ Rotate suggestions after each answer. """
    # Always include the priority questions first if not used
    remaining_priority = [q for q in priority_questions if q not in st.session_state.suggestions]
    if remaining_priority:
        return remaining_priority[:4]

    # Otherwise, sample from secondary pool
    return random.sample(secondary_questions, k=4)

# --- Initialize suggested_input flags ---
if "suggested_input" not in st.session_state:
    st.session_state.suggested_input = None

if "suggested_input_submitted" not in st.session_state:
    st.session_state.suggested_input_submitted = False

# --- Title and Welcome Message ---
st.title("💬 TrustMicro - Your AI FAQ Assistant")
st.markdown(
    """
    Hello! I'm TrustMicro, your friendly Microfinance assistant.
    Ask me about loans, savings, repayments, and more.
    I'm here to help 24/7.
    """
)
st.divider()

# --- Suggested Questions ---
st.subheader("💡 Quick Questions")
cols = st.columns(2)
for i, question in enumerate(st.session_state.suggestions):
    col = cols[i % 2]
    if col.button(f"❓ {question}", key=f"suggested_{i}"):
        st.session_state.suggested_input = question
        st.session_state.suggested_input_submitted = True

st.divider()

# --- Input Field with Form ---
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Type your question here...")
    submitted = st.form_submit_button("Send")

# --- Decide Which Input to Process ---
final_input = None
if submitted and user_input:
    final_input = user_input
elif st.session_state.get("suggested_input_submitted"):
    final_input = st.session_state.get("suggested_input")

# --- Answer Processing ---
if final_input:
    question, answer, score = bot.get_best_match(final_input)
    if score >= 0.7:
        st.success(f"**Answer:** {answer}")
    else:
        st.error("⚠️ I'm sorry, I couldn't confidently answer that. Please try rephrasing.")
        bot.save_unanswered(final_input)
        st.info("✨ *Your question has been saved for review to improve this assistant.*")

    # After answering, rotate suggestions
    st.session_state.suggestions = get_next_suggestions()
    st.session_state.suggested_input = None
    st.session_state.suggested_input_submitted = False

# --- Footer ---
st.caption("🧭 Powered by TrustMicro AI | Built with ❤️ using Sentence Transformers and Streamlit")
