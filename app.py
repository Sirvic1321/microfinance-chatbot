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

# --- Title and Welcome Message ---
st.title("💬 TrustMicro - Your AI FAQ Assistant")
st.markdown(
    """
    Hello! I'm TrustMicro, your friendly Microfinance assistant.  
    Ask me about loans, savings, repayments, and more. I'm here to help 24/7. 🌟
    """
)
st.divider()

# --- Master Question Pool (from your CSV or defined here) ---
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

# --- Setup Session State ---
if "suggested_input" not in st.session_state:
    st.session_state.suggested_input = None
if "suggestions" not in st.session_state:
    random.shuffle(master_questions)
    st.session_state.suggestions = master_questions[:4]

# --- Suggested Questions UI ---
st.subheader("💡 Try asking one of these:")

cols = st.columns(4)
for i, (col, question) in enumerate(zip(cols, st.session_state.suggestions)):
    if col.button(f"❓ {question}", key=f"suggested_{i}"):
        st.session_state.suggested_input = question

st.divider()

# --- Manual Input Field ---
st.subheader("🔎 Ask your own question:")
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Type your question here...")
    submitted = st.form_submit_button("Send")

# --- Determine which input to use ---
final_input = None
if submitted and user_input:
    final_input = user_input
elif st.session_state.suggested_input:
    final_input = st.session_state.suggested_input

# --- Process Input ---
if final_input:
    question, answer, score = bot.get_best_match(final_input)

    if score >= 0.7:
        st.success(f"✅ **Answer:** {answer}")
    else:
        st.error("⚠️ I'm sorry, I couldn't confidently answer that. Please try rephrasing your question.")
        bot.save_unanswered(final_input)
        st.info("✨ *Your question has been saved for review to improve this assistant.*")

    # Reset suggested_input so it's not "sticky" after processing
    st.session_state.suggested_input = None

# --- Footer ---
st.divider()
st.caption("🧭 Powered by TrustMicro AI")
