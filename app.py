import streamlit as st
from chatbot import FAQChatbot

# --- Page configuration ---
st.set_page_config(
    page_title="TrustMicro Chatbot 🤖",
    page_icon="💬",
    layout="centered"
)

# --- Sidebar ---
with st.sidebar:
    st.title("💼 TrustMicro")
    st.markdown(
        """
        Welcome to the TrustMicro FAQ Assistant!  
        
        **Categories:**  
        - 📌 Loans  
        - 📌 Savings  
        - 📌 Repayments  
        - 📌 Account Opening  
        - 📌 General Inquiries  
        
        ---
        *Ask any question below to get started!*  
        """
    )

# --- Load the chatbot once (cached) ---
@st.cache_resource
def load_bot():
    st.info("Loading AI model... please wait ⏳")
    return FAQChatbot("faq_cleaned.csv")

bot = load_bot()

# --- Session State for Conversation History ---
if "history" not in st.session_state:
    st.session_state.history = []

# --- App Title and Introduction ---
st.title("💬 TrustMicro - Your AI FAQ Assistant")
st.markdown(
    """
    👋 Hi there! I'm **TrustMicro**, your friendly Microfinance assistant.  
    Ask me anything about **loans**, **savings**, **repayments**, and more!  
    I'm here to help you 24/7. 🌟
    """
)

st.divider()

# --- User Input Box ---
user_input = st.text_input("🔎 Type your question below:")

# --- Process User Input with Confidence Filtering ---
if user_input:
    question, answer, score = bot.get_best_match(user_input)
    response_text = ""

    if score >= 0.85:
        response_text = f"✅ **Answer:** {answer}"
    elif score >= 0.65:
        response_text = (
            f"🤔 *Did you mean:* \n"
            f"**Q:** {question} \n"
            f"**A:** {answer} \n\n"
            f"If this doesn't answer your question, please try rephrasing for even better results. 🪄"
        )
    else:
        response_text = (
            "⚠️ I'm sorry, I didn't quite understand that well enough to give an answer. "
            "Could you please rephrase your question?"
        )
        bot.save_unanswered(user_input)
        st.info("✨ *Your question has been saved for review to help improve this assistant.*")

    # Save this interaction in session history
    st.session_state.history.append(
        {"user": user_input, "response": response_text, "score": score}
    )

# --- Display Conversation History ---
if st.session_state.history:
    st.markdown("### 📜 Conversation History")
    for chat in st.session_state.history:
        st.markdown(f"**🧑‍💼 You:** {chat['user']}")
        st.markdown(f"{chat['response']}")
        st.caption(f"Confidence Score: `{chat['score']:.2f}`")
        st.divider()

# --- Footer ---
st.caption("🧭 Powered by TrustMicro AI | Built with ❤️ using Sentence Transformers and Streamlit")
from chatbot import FAQChatbot

# --- Page configuration ---
st.set_page_config(
    page_title="TrustMicro Chatbot 🤖",
    page_icon="💬",
    layout="centered"
)

# --- Sidebar ---
with st.sidebar:
    st.title("TrustMicro")
    st.markdown(
        """
        Welcome to the TrustMicro FAQ Assistant!  
        
        **Categories:**  
        - 📌 Loans  
        - 📌 Savings  
        - 📌 Repayments  
        - 📌 Account Opening  
        - 📌 General Inquiries  
        
        ---
        *Ask any question below to get started!*  
        """
    )

# --- Load the chatbot once (cached) ---
@st.cache_resource
def load_bot():
    st.info("Loading AI model... please wait ⏳")
    return FAQChatbot("faq_cleaned.csv")

bot = load_bot()

# --- Session State for Conversation History ---
if "history" not in st.session_state:
    st.session_state.history = []

# --- App Title and Introduction ---
st.title("💬 TrustMicro - Your AI FAQ Assistant")
st.markdown(
    """
    👋 Hi there! I'm **TrustMicro**, your friendly Microfinance assistant.  
    Ask me anything about **loans**, **savings**, **repayments**, and more!  
    I'm here to help you 24/7. 🌟
    """
)

st.divider()

# --- User Input Box ---
user_input = st.text_input("🔎 Type your question below:")

# --- Process User Input with Confidence Filtering ---
if user_input:
    question, answer, score = bot.get_best_match(user_input)
    response_text = ""

    if score >= 0.85:
        response_text = f"✅ **Answer:** {answer}"
    elif score >= 0.65:
        response_text = (
            f"🤔 *Did you mean:* \n"
            f"**Q:** {question} \n"
            f"**A:** {answer} \n\n"
            f"If this doesn't answer your question, please try rephrasing for even better results. 🪄"
        )
    else:
        response_text = (
            "⚠️ I'm sorry, I didn't quite understand that well enough to give an answer. "
            "Could you please rephrase your question?"
        )
        bot.save_unanswered(user_input)
        st.info("✨ *Your question has been saved for review to help improve this assistant.*")

    # Save this interaction in session history
    st.session_state.history.append(
        {"user": user_input, "response": response_text, "score": score}
    )

# --- Display Conversation History ---
if st.session_state.history:
    st.markdown("### 📜 Conversation History")
    for chat in st.session_state.history:
        st.markdown(f"**🧑‍💼 You:** {chat['user']}")
        st.markdown(f"{chat['response']}")
        st.caption(f"Confidence Score: `{chat['score']:.2f}`")
        st.divider()

# --- Footer ---
st.caption("🧭 Powered by TrustMicro AI | Built with ❤️ using Sentence Transformers and Streamlit")