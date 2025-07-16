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

# --- Load All Suggestions from CSV (as-is) ---
all_suggestions = bot.faqs['question'].dropna().tolist()

# --- Title and Welcome Message ---
st.title("💬 TrustMicro - Your AI Assistant")
st.markdown(
    """
    Hello! I'm TrustMicro, your friendly Microfinance assistant.
    Ask me about loans, savings, repayments, and more.
    I'm here to help 24/7. 
    """
)
st.divider()

# --- Show ALL Suggested Questions Exactly as in CSV ---
st.subheader("💡 Suggested Questions")
for q in all_suggestions:
    if st.button(q, key=q):
        st.session_state.selected_suggestion = q

st.divider()

# --- Input Field (with autofill from suggestions) ---
with st.form(key="chat_form", clear_on_submit=True):
    default_value = st.session_state.pop("selected_suggestion", "")
    user_input = st.text_input("Type your question here...", value=default_value)
    submitted = st.form_submit_button("Send")

# --- Processing User Input ---
if submitted and user_input:
    question, answer, score = bot.get_best_match(user_input)
    if score >= 0.8:
        st.success(f"✅ **Answer:** {answer}")
    elif score >= 0.6:
        st.warning(
            f"🤔 *I think you might be asking:* \n\n"
            f"**Q:** {question}\n\n"
            f"**A:** {answer}\n\n"
            "If this doesn't help, please try rephrasing!"
        )
    else:
        st.error(
            "⚠️ I'm sorry, I couldn't confidently answer that. "
            "Could you please rephrase your question?"
        )
        bot.save_unanswered(user_input)
        st.info("✨ *Your question has been saved for review to improve this assistant.*")

# --- Footer ---
st.caption("🧭 Powered by TrustMicro AI")
