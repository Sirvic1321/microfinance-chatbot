import streamlit as st
import random
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

# --- Load All Possible Suggestions from CSV Data ---
if "all_suggestions" not in st.session_state:
    all_questions = bot.faqs['question'].dropna().tolist()
    st.session_state.all_suggestions = list(set(all_questions))

# --- Initialize Session State ---
if "history" not in st.session_state:
    st.session_state.history = []

if "suggestions" not in st.session_state:
    st.session_state.suggestions = random.sample(st.session_state.all_suggestions, k=min(5, len(st.session_state.all_suggestions)))

# --- Title and Welcome Message ---
st.title("💬 TrustMicro - Your AI FAQ Assistant")
st.markdown(
    """
    Hello! I'm TrustMicro, your friendly Microfinance assistant.
    Ask me about loans, savings, repayments, and more.
    I'm here to help 24/7. 🌟
    """
)
st.divider()

# --- Display Conversation History (normal order) ---
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
    st.info("🤖 Ready to answer your questions! Start by typing below or selecting a suggestion.")

# --- Show Suggested Questions ---
st.subheader("💡 Suggested Questions")
cols = st.columns(3)
for idx, q in enumerate(st.session_state.suggestions):
    with cols[idx % 3]:
        if st.button(q, key=f"suggestion_{idx}"):
            st.session_state.selected_suggestion = q

# --- Input Field (text input + button) ---
with st.form(key="chat_form", clear_on_submit=True):
    if "selected_suggestion" in st.session_state:
        default_value = st.session_state.pop("selected_suggestion")
    else:
        default_value = ""
    user_input = st.text_input("Type your question here...", value=default_value)
    submitted = st.form_submit_button("Send")

# --- Processing User Input Immediately ---
if submitted and user_input:
    question, answer, score = bot.get_best_match(user_input)
    response_text = ""

    if score >= 0.8:
        response_text = f"✅ **Answer:** {answer}"
    elif score >= 0.6:
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

    # Refresh suggestions from the master pool for next turn
    st.session_state.suggestions = random.sample(st.session_state.all_suggestions, k=min(5, len(st.session_state.all_suggestions)))

# --- Footer ---
st.caption("🧭 Powered by TrustMicro AI")
