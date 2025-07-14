import streamlit as st
from chatbot import FAQChatbot

# --- Load the chatbot ---
@st.cache_resource
def load_bot():
    return FAQChatbot("faq_clean.csv")

bot = load_bot()

# --- App Title ---
st.title("TrustMicro - FAQ Chatbot")
st.markdown("""
Welcome to the TrustMicro Microfinance Bank FAQ Chatbot.  Type your question below and get instant answers!
""")

# --- User Input ---
user_input = st.text_input("Ask your question:")

# --- Process Input ---
if user_input:
    question, answer, score = bot.get_best_match(user_input)
    if score < 0.3:
        st.error("Sorry, I don't have an answer for that. Please try asking something else.")
    else:
        st.success(f"**Answer:** {answer}")

st.markdown("---")
st.caption("Powered by TrustMicro AI")