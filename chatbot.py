import os
import pandas as pd
from datetime import datetime
from sentence_transformers import SentenceTransformer, util


class FAQChatbot:
    """
    AI-powered FAQ Chatbot for Microfinance use-cases.
    Loads questions/answers from CSV and uses SentenceTransformer for semantic search.
    """
    def __init__(self, csv_path):
        """
        Initialize chatbot with FAQ data.
        Loads and cleans CSV, and precomputes question embeddings.
        """
        self._load_data(csv_path)
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        self.question_embeddings = self.embedder.encode(self.questions, convert_to_tensor=True)

    def _load_data(self, csv_path):
        """
        Load FAQ data from CSV file.
        Strips column names, drops incomplete rows.
        """
        try:
            self.faqs = pd.read_csv(csv_path, encoding='cp1252')
            self.faqs.columns = self.faqs.columns.str.strip().str.lower()
            self.faqs = self.faqs.dropna(subset=['question', 'answer'])
            self.questions = self.faqs['question'].tolist()
            self.answers = self.faqs['answer'].tolist()
        except Exception as e:
            raise ValueError(f"Error loading FAQ data: {e}")

    def get_best_match(self, user_input):
        """
        Get the single best matching FAQ question/answer for the user input.
        Returns: (matched_question, matched_answer, score)
        """
        try:
            user_embedding = self.embedder.encode(user_input, convert_to_tensor=True)
            similarities = util.cos_sim(user_embedding, self.question_embeddings)[0].cpu().numpy()
            best_idx = similarities.argmax()
            best_score = similarities[best_idx]
            return self.questions[best_idx], self.answers[best_idx], best_score
        except Exception as e:
            return "Error", "Sorry, I encountered an error processing your question.", 0.0

    def get_top_n_matches(self, user_input, n=3):
        """
        Return the top N FAQ matches for the user input, sorted by similarity.
        Returns a list of dicts with question, answer, score.
        """
        try:
            user_embedding = self.embedder.encode(user_input, convert_to_tensor=True)
            similarities = util.cos_sim(user_embedding, self.question_embeddings)[0].cpu().numpy()
            top_indices = similarities.argsort()[-n:][::-1]
            results = []
            for idx in top_indices:
                results.append({
                    "question": self.questions[idx],
                    "answer": self.answers[idx],
                    "score": similarities[idx]
                })
            return results
        except Exception as e:
            return []

    def save_unanswered(self, user_input, path='logs/unknown_questions.csv'):
        """
        Log unanswered user input for review and retraining.
        Includes timestamp for easier tracking.
        """
        os.makedirs(os.path.dirname(path), exist_ok=True)
        try:
            df = pd.read_csv(path)
        except FileNotFoundError:
            df = pd.DataFrame(columns=['timestamp', 'question'])

        new_row = pd.DataFrame({
            'timestamp': [datetime.utcnow().isoformat()],
            'question': [user_input]
        })
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv(path, index=False)