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
        Welcome to the **TrustMicro AI FAQ Assistant**!  

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
    return FAQChatbot("faq_cleaned.csv")

bot = load_bot()

# --- Initialize Session State for Conversation History ---
if "history" not in st.session_state:
    st.session_state.history = []

# --- Title and Welcome Message ---
st.title("💬 TrustMicro - Your AI FAQ Assistant")
st.markdown(
    """
    **Hello!** I'm **TrustMicro**, your friendly Microfinance assistant.  
    Ask me about **loans**, **savings**, **repayments**, and more.  
    I'm here to help 24/7. 
    """
)
st.divider()

# --- Display Conversation History ABOVE the Input Box ---
if st.session_state.history:
    st.subheader("📜 Chat History")
    for chat in st.session_state.history:
        # User message
        with st.chat_message("user"):
            st.markdown(f"**🧑‍💼 You:** {chat['user']}")
        
        # Bot response with styling
        with st.chat_message("assistant"):
            st.markdown(chat['response'])
            st.caption(f"🤖 *Confidence Score:* `{chat['score']:.2f}`")
    st.divider()
else:
    st.info("🤖 *Ready to answer your questions! Start by typing below.*")

# --- Input Field at Bottom ---
user_input = st.chat_input("Type your question here...")

# --- Processing User Input with Confidence Filtering ---
if user_input:
    question, answer, score = bot.get_best_match(user_input)
    response_text = ""

    if score >= 0.85:
        response_text = f"✅ **Answer:** {answer}"
    elif score >= 0.65:
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
    st.session_state.history.append(
        {"user": user_input, "response": response_text, "score": score}
    )

# --- Footer ---
st.caption("🧭 Powered by TrustMicro AI | Built with ❤️ using Sentence Transformers and Streamlit")
