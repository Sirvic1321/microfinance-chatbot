import streamlit as st
from chatbot import FAQChatbot

# --- Load the chatbot ---
@st.cache_resource
def load_bot():
    return FAQChatbot("faq_cleansed.csv")

bot = load_bot()

# --- App Title ---
st.title("TrustMicro - FAQ Chatbot")
st.markdown("""
Hi I'm your TrustMicro Microfinance Assistant.
""")

# --- User Input ---
user_input = st.text_input("Ask me anything about loans, savings, repayments, etc.:")

# --- Process Input ---
if user_input:
    question, answer, score = bot.get_best_match(user_input)
    if score < 0.7:
        st.error("I'm sorry, I didn't understand that. Could you rephrase your query please?")
        bot.save_unanswered(user_input)
    else:
        st.success(f"**Answer:** {answer}")

st.markdown("---")
st.caption("Powered by TrustMicro AI ")
