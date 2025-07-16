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
st.subheader("💡 Suggested Questions")
suggested = [
    "How do I apply for a loan?",
    "What are your savings rates?",
    "How do I repay my loan?",
    "What documents do I need to open an account?"
]

suggested_cols = st.columns(len(suggested))
for idx, question in enumerate(suggested):
    if suggested_cols[idx].button(question):
        st.session_state.user_input = question
    else:
        # Initialize if not clicked
        st.session_state.setdefault('user_input', '')

# --- Input Field at Bottom (text input + button for instant response) ---
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Type your question here...", value=st.session_state.get('user_input', ''))
    submitted = st.form_submit_button("Send")

# --- Processing User Input ---
if submitted and user_input:
    question, answer, score = bot.get_best_match(user_input)
    response_text = ""

    if score >= 0.75:
        response_text = f"✅ **Answer:** {answer}"
    elif score >= 0.55:
        response_text = (
            f"🤔 *I think you might be asking:* \n"
            f"**Q:** {question} \n"
            f"**A:** {answer} \n\n"
            f"If this doesn't help, please try rephrasing for a better match! ✨"
        )
    else:
        response_text = (
            "⚠️ I'm sorry, I couldn't confidently answer that. "
            "Could you please rephrase your question?"
        )
        bot.save_unanswered(user_input)
        st.info("✨ *Your question has been saved for review to improve this assistant.*")

    # Add interaction to conversation history
    st.session_state.history.append({
        "user": user_input,
        "response": response_text,
        "score": score
    })

# --- Display Conversation History (latest messages first) ---
if st.session_state.history:
    st.subheader("📜 Chat History")
    for chat in reversed(st.session_state.history):
        # User message
        with st.chat_message("user"):
            st.markdown(f"🧑‍💼 **You:** {chat['user']}")

        # Bot response
        with st.chat_message("assistant"):
            st.markdown(chat['response'])
            st.caption(f"🤖 *Confidence Score:* `{chat['score']:.2f}`")
else:
    st.info("🤖 Ready to answer your questions! Start by typing below.")

# --- Footer ---
st.caption("🧭 Powered by TrustMicro AI")
