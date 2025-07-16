import streamlit as st
import random
from chatbot import FAQChatbot

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

# --- Master Questions Pool (from CSV or manually here) ---
master_questions = [
    "How do I apply for a loan?",
    "What are the requirements for opening an account?",
    "How do I repay my loan?",
    "What is the interest rate on savings?",
    "What documents do I need for a loan?",
    "How long does it take to get a loan approved?",
    "How can I check my loan balance?",
    "Can I repay my loan early?",
    "Do you offer group loans?",
    "What is the minimum savings amount?",
    "How do I withdraw from my savings?",
    "Is there a penalty for early withdrawal?",
    "Can I open an account online?",
    "What is the maximum loan amount?",
    "Do you offer business loans?",
    "How are interest rates calculated?",
    "How often do I make repayments?",
    "Do you offer mobile banking?",
    "What happens if I miss a repayment?",
    "Can I top up my existing loan?",
    "Are there any hidden charges?",
    "What is the customer care number?",
    "Where are your branches located?",
    "How secure is my account?",
    "What is the loan tenure?",
    "Can I get a statement of account?",
    "How do I update my account details?",
    "Do you require collateral?",
    "How do I close my account?",
    "Can I nominate someone on my account?",
    "How do I reset my PIN?",
    "Do you offer ATM services?",
    "Are there charges on withdrawals?",
    "Can I get a loan without salary?",
    "What happens on loan default?",
    "How do I change my repayment schedule?",
    "What are your operating hours?",
    "Do you have an app?",
    "How do I contact support?"
]

# --- Define Priority Starter Questions ---
priority_questions = [
    "How do I apply for a loan?",
    "What are the requirements for opening an account?"
]

# --- Function to Create Next Suggestions List ---
def get_next_suggestions():
    # Remove priority from master pool
    remaining = [q for q in master_questions if q not in priority_questions]
    random.shuffle(remaining)
    # Always include 2 priority first, then 2 random
    return priority_questions[:2] + remaining[:2]

# --- Session State Setup ---
if "suggested_input" not in st.session_state:
    st.session_state.suggested_input = None
if "suggestions" not in st.session_state:
    st.session_state.suggestions = get_next_suggestions()

# --- App Header ---
st.title("💬 TrustMicro - Your AI FAQ Assistant")
st.markdown(
    """
    Hello! I'm TrustMicro, your friendly Microfinance assistant.  
    Ask me about loans, savings, repayments, and more. I'm here to help 24/7. 🌟
    """
)
st.divider()

# --- Suggestions Section ---
st.subheader("💡 Try asking one of these:")
cols = st.columns(4)
for i, (col, question) in enumerate(zip(cols, st.session_state.suggestions)):
    if col.button(f"❓ {question}", key=f"suggested_{i}"):
        st.session_state.suggested_input = question

st.divider()

# --- Manual Input Section ---
st.subheader("🔎 Ask your own question:")
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Type your question here...")
    submitted = st.form_submit_button("Send")

# --- Decide Which Input to Process ---
final_input = None
if submitted and user_input:
    final_input = user_input
elif st.session_state.suggested_input:
    final_input = st.session_state.suggested_input

# --- Process Input and Respond ---
if final_input:
    question, answer, score = bot.get_best_match(final_input)

    if score >= 0.60:
        st.success(f"✅ **Answer:** {answer}")
    else:
        st.error("⚠️ I'm sorry, I couldn't confidently answer that. Please try rephrasing your question.")
        bot.save_unanswered(final_input)
        st.info("✨ *Your question has been saved for review to improve this assistant.*")

    # After answering, generate new rotating suggestions
    st.session_state.suggestions = get_next_suggestions()
    st.session_state.suggested_input = None

# --- Footer ---
st.divider()
st.caption("🧭 Powered by TrustMicro AI | Built with ❤️ using Sentence Transformers and Streamlit")
