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
    
        return FAQChatbot("faq_cleaned.csv")

bot = load_bot()

# --- Initialize Session State ---
if "history" not in st.session_state:
    st.session_state.history = []

if "new_message" not in st.session_state:
    st.session_state.new_message = None

# --- Input Field at Bottom (text input + button for instant response) ---
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Type your question here...")
    submitted = st.form_submit_button("Send")

if submitted and user_input:
    question, answer, score = bot.get_best_match(user_input)

    if score >= 0.60:
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

    # Save message instantly
    st.session_state.new_message = {
        "user": user_input,
        "response": response_text,
        "score": score
    }

# --- Display Conversation History (new message first) ---
st.title("💬 TrustMicro Assistant")
st.markdown(
    """
    Hello! I'm TrustMicro, your Microfinance assistant.
    Ask me about loans, savings, repayments, and more.
    I'm here to help 24/7.
    """
)
st.divider()

if st.session_state.new_message:
    st.session_state.history.append(st.session_state.new_message)
    st.session_state.new_message = None  # Clear it after use

if st.session_state.history:
    st.subheader("📜 Chat History")
    for chat in st.session_state.history:
        with st.chat_message("user"):
            st.markdown(f"🧑‍💼 **You:** {chat['user']}")
        with st.chat_message("assistant"):
            st.markdown(chat['response'])
            st.caption(f"🤖 *Confidence Score:* `{chat['score']:.2f}`")
    st.divider()
else:
    st.info("🤖 Ready to answer your questions! Start by typing below.")

# --- Footer ---
st.caption("🧭 Powered by TrustMicro AI | Built with ❤️ using Streamlit + Sentence Transformers")
