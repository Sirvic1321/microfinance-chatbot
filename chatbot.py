import os
import pandas as pd
from sentence_transformers import SentenceTransformer, util

class FAQChatbot:
    def __init__(self, csv_path):
        self.faqs = pd.read_csv(csv_path, encoding='cp1252')
        self.faqs.columns = self.faqs.columns.str.strip().str.lower()

        # Remove any rows with missing question or answer
        self.faqs = self.faqs.dropna(subset=['question', 'answer'])

        self.questions = self.faqs['question'].tolist()
        self.answers = self.faqs['answer'].tolist()
        # Sentence Embeddings
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        self.question_embeddings = self.embedder.encode(self.questions, convert_to_tensor=True)

    def get_best_match(self, user_input):
        user_embedding = self.embedder.encode(user_input, convert_to_tensor=True)
        similarities = util.cos_sim(user_embedding, self.question_embeddings)[0].cpu().numpy()
        best_idx = similarities.argmax()
        best_score = similarities[best_idx]
        # Return answer and score
        return self.questions[best_idx], self.answers[best_idx], best_score

    def get_top_n_matches(self, user_input, n=3):
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

    def save_unanswered(self, user_input, path='logs/unknown_questions.csv'):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        try:
            df = pd.read_csv(path)
        except FileNotFoundError:
            df = pd.DataFrame(columns=['question'])

        new_row = pd.DataFrame({'question': [user_input]})
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv(path, index=False)

