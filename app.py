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

# --- Load and Cache Chatbot ---
@st.cache_resource
def load_bot():
    st.info("Loading AI model... Please wait ⏳")
    return FAQChatbot("faq_cleaned.csv")

bot = load_bot()

# --- Initialize Session State for Conversation History ---
if "history" not in st.session_state:
    st.session_state.history = []

# --- App Title and Welcome ---
st.title("💬 TrustMicro - Your AI FAQ Assistant")
st.markdown(
    """
    **Hello! I'm TrustMicro, your Microfinance assistant.**  
    Ask me about **loans, savings, repayments**, and more.  
    I'm here to help **24/7**. 
    """
)
st.divider()

# --- Display Chat History (ABOVE Input) ---
if st.session_state.history:
    st.subheader("📜 Chat History")
    for chat in st.session_state.history:
        # User message
        with st.chat_message("user"):
            st.markdown(f"🧑‍💼 **You:** {chat['user']}")

        # Bot response with styling
        with st.chat_message("assistant"):
            st.markdown(chat['response'])
            st.caption(f"🤖 *Confidence Score:* `{chat['score']:.2f}`")
    st.divider()
else:
    st.info("*Ready to answer your questions!* Start by typing below.")

# --- Input Box at Bottom of App ---
user_input = st.chat_input("Type your question here...")

# --- Process User Input with Confidence Filter ---
if user_input:
    question, answer, score = bot.get_best_match(user_input)

    # Build a friendly, dynamic response
    if score >= 0.85:
        response_text = f"✅ **Answer:** {answer}"
    elif score >= 0.65:
        response_text = (
            f"🤔 *I think you might be asking:* \n"
            f"**Q:** {question} \n"
            f"**A:** {answer} \n\n"
            f"If this doesn't help, please try rephrasing your query!"
        )
    else:
        response_text = (
            "⚠️ I'm sorry, I couldn't confidently answer that. "
            "Could you please rephrase your question?"
        )
        # Save low-confidence questions for review
        bot.save_unanswered(user_input)
        st.info("✨ *Your question has been saved to improve this assistant.*")

    # Add interaction to conversation history
    st.session_state.history.append({
        "user": user_input,
        "response": response_text,
        "score": score
    })

# --- Footer ---
st.markdown("---")
st.caption("🧭 Powered by **TrustMicro AI**")