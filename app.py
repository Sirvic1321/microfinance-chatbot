import random
import streamlit as st
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

# --- Load Chatbot ---
@st.cache_resource
def load_bot():
    with st.spinner("Loading AI model... Please wait ⏳"):
        return FAQChatbot("faq_cleaned.csv")

bot = load_bot()

# --- Session State Initialization ---
if "suggestions_pool" not in st.session_state:
    st.session_state.suggestions_pool = [
    "How do I apply for a loan?",
    "What are the requirements for a microloan?",
    "Can I apply for a loan without a salary account?",
    "How long does loan approval take?",
    "Can I apply for a loan if I have bad credit?",
    "Do I need a guarantor to get a loan?",
    "What is the minimum and maximum amount I can borrow?",
    "How do I repay my loan?",
    "What happens if I miss a repayment?",
    "Can I repay my loan early?",
    "Can I reschedule my loan repayment?",
    "What is the loan repayment duration?",
    "What interest rate do you charge on loans?",
    "Is the interest rate fixed or variable?",
    "Do interest rates change after loan approval?",
    "How do you calculate interest on loans?",
    "How do I open a savings account?",
    "What is the minimum deposit to open an account?",
    "Do you offer interest on savings accounts?",
    "Can I open an account online?",
    "Is there a savings plan for kids?",
    "What’s the difference between savings and fixed deposit?",
    "How do I register for USSD banking?",
    "Can I check my balance using USSD?",
    "Is there a mobile app I can use?",
    "Can I transfer money with USSD?",
    "Is USSD banking safe?",
    "Are there any charges on savings accounts?",
    "Do you charge a loan processing fee?",
    "What is the penalty for late loan repayment?",
    "Is there a fee to close my account?",
    "How can I contact customer care?",
    "Where is your head office located?",
    "Can I speak to an agent online?",
    "What should I do if I lose my ATM card?",
    "How do I lodge a complaint?",
    "What services do you offer?",
    "Is the bank licensed?",
    "How long have you been in operation?",
    "What makes your bank different?"
]


if "suggestions" not in st.session_state:
    st.session_state.suggestions = [
          "How do I apply for a loan?",
    "What are the requirements for a microloan?",
    "How do I open a savings account?",
    "What is the minimum deposit to open an account?"
]

if "final_input" not in st.session_state:
    st.session_state.final_input = ""

if "response_text" not in st.session_state:
    st.session_state.response_text = ""
    st.session_state.confidence_score = 0.0

# --- Title ---
st.title("💬 TrustMicro - Your AI FAQ Assistant")
st.markdown("""
Hello! I'm TrustMicro, your friendly Microfinance assistant.
Ask me about loans, savings, repayments, and more. I'm here to help 24/7.
""")
st.divider()

# --- Chat Form ---
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Type your question here...")
    submitted = st.form_submit_button("Send")

if submitted and user_input:
    st.session_state.final_input = user_input

# --- Suggestion Buttons ---
st.subheader("💡 Quick Questions")
cols = st.columns(2)
for i, q in enumerate(st.session_state.suggestions):
    if cols[i % 2].button(f"❓ {q}", key=f"btn_{i}"):
        st.session_state.final_input = q

# --- Answer Processing ---
if st.session_state.final_input:
    question, answer, score = bot.get_best_match(st.session_state.final_input)

    if score >= 0.85:
        response = f"✅ **Answer:** {answer}"
    elif score >= 0.65:
        response = (
            f"🤔 *I think you might be asking:*  \n"
            f"**Q:** {question}  \n"
            f"**A:** {answer}  \n\n"
            f"If this doesn't help, please try rephrasing for a better match! ✨"
        )
    else:
        response = (
            "⚠️ I'm sorry, I couldn't confidently answer that. "
            "Could you please rephrase your question?"
        )
        bot.save_unanswered(st.session_state.final_input)
        st.info("✨ *Your question has been saved to improve this assistant.*")

    st.markdown(f"🧑‍💼 **You:** {st.session_state.final_input}")
    st.markdown(response)
    st.caption(f"🤖 *Confidence Score:* `{score:.2f}`")

    # Refresh next suggestions
    st.session_state.suggestions = random.sample(
        st.session_state.suggestions_pool, 4
    )

    # Reset input
    st.session_state.final_input = ""
