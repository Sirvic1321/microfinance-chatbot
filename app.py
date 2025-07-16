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

# --- Title and Welcome Message ---
st.title("💬 TrustMicro - Your AI FAQ Assistant")
st.markdown(
    """
    Hello! I'm TrustMicro, your friendly Microfinance assistant.  
    Ask me about loans, savings, repayments, and more. I'm here to help 24/7. 🌟
    """
)
st.divider()

# --- Suggested Questions (Top 4 from CSV) ---
st.subheader("💡 Try asking:")
top_questions = [
    "How do I apply for a loan?",
    "What are the requirements for opening an account?",
    "How do I repay my loan?",
    "What is the interest rate on savings?"
]

# Handle suggestion click logic
suggested_input = None
for i, q in enumerate(top_questions):
    if st.button(q, key=f"suggested_{i}"):
        suggested_input = q  # store the selected question

# --- Manual Input Field ---
st.divider()
st.subheader("🔎 Ask your own question:")
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Type your question here...")
    submitted = st.form_submit_button("Send")

# Determine source of input
final_input = suggested_input if suggested_input else (user_input if submitted else None)

# --- Process Input (whether from suggestions or manual input) ---
if final_input:
    question, answer, score = bot.get_best_match(final_input)

    if score >= 0.8:
        st.success(f"✅ **Answer:** {answer}")
    elif score >= 0.6:
        st.warning(
            f"🤔 *I think you might be asking:*  \n"
            f"**Q:** {question}  \n\n"
            f"**A:** {answer}  \n\n"
            "If this doesn't help, please try rephrasing! ✨"
        )
    else:
        st.error("⚠️ I'm sorry, I couldn't confidently answer that. Please rephrase.")
        bot.save_unanswered(final_input)
        st.info("✨ *Your question has been saved for review to improve this assistant.*")

# --- Footer ---
st.divider()
st.caption("🧭 Powered by TrustMicro AI | Built with ❤️ using Sentence Transformers and Streamlit")
