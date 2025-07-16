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

# --- Load and Cache Chatbot ---
@st.cache_resource
def load_bot():
    with st.spinner("Loading AI model... Please wait ⏳"):
        return FAQChatbot("faq_cleaned.csv")

bot = load_bot()

# --- Initialize Session State ---
if "history" not in st.session_state:
    st.session_state.history = []

if "suggestions" not in st.session_state:
    st.session_state.suggestions_pool = [
        "How do I apply for a loan?",
        "What documents do I need for a loan?",
        "What is the interest rate for loans?",
        "How can I repay my loan?",
        "How do I open an account?",
        "Can I save money with TrustMicro?",
        "How long does loan approval take?",
        "Is there a penalty for late repayment?",
        "Can I get a loan without collateral?",
        "What types of loans do you offer?",
        "What is the minimum savings amount?",
        "How do I check my account balance?",
        "Do you offer group loans?",
        "Can I repay through mobile money?",
        "What are your operating hours?",
        "Where is your nearest branch?",
        "How do I close my account?",
        "Do you have an app?",
        "Can I get a statement of account?",
        "What is the maximum loan amount?",
        "Do you have business loans?",
        "What is your customer care number?",
        "Can I top up an existing loan?",
        "How do I change my account details?",
        "Do you offer insurance products?",
        "What happens if I can't repay?",
        "How do I schedule a repayment?",
        "Are your services Sharia compliant?",
        "Do you charge account maintenance fees?",
        "How do I contact TrustMicro?"
    ]
    st.session_state.suggestions = random.sample(
        st.session_state.suggestions_pool, 4
    )

if "suggested_input" not in st.session_state:
    st.session_state.suggested_input = ""
    st.session_state.suggested_input_submitted = False

# --- Handle Suggestion Button Clicks with Proper State ---
def on_suggestion_click(question):
    st.session_state.suggested_input = question
    st.session_state.suggested_input_submitted = True
    st.experimental_rerun()

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

# --- User Input Field at Bottom (text input + button for instant response) ---
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Type your question here...")
    submitted = st.form_submit_button("Send")

# --- Process Input or Suggestion Click ---
final_input = None
if submitted and user_input:
    final_input = user_input
elif st.session_state.suggested_input_submitted:
    final_input = st.session_state.suggested_input
    st.session_state.suggested_input_submitted = False

if final_input:
    question, answer, score = bot.get_best_match(final_input)
    response_text = ""

    if score >= 0.60:
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
        bot.save_unanswered(final_input)
        st.info("✨ *Your question has been saved for review to improve this assistant.*")

    # Show the answer
    st.markdown("---")
    with st.chat_message("assistant"):
        st.markdown(response_text)
        st.caption(f"🤖 *Confidence Score:* `{score:.2f}`")

    # Rotate suggestions after each valid interaction
    st.session_state.suggestions = random.sample(
        st.session_state.suggestions_pool, 4
    )

# --- Suggested Questions Section ---
st.subheader("💡 Quick Questions")
cols = st.columns(2)
for i, question in enumerate(st.session_state.suggestions):
    col = cols[i % 2]
    col.button(
        f"❓ {question}",
        key=f"suggested_{i}",
        on_click=on_suggestion_click,
        args=(question,)
    )

# --- Footer ---
st.caption("🧭 Powered by TrustMicro AI")
