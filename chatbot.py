import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class FAQChatbot:
    def __init__(self, csv_path):
        self.faqs = pd.read_csv(csv_path, encoding='cp1252')
        self.faqs.columns = self.faqs.columns.str.strip().str.lower()

        # Remove any rows with missing question or answer
        self.faqs = self.faqs.dropna(subset=['question', 'answer'])

        self.questions = self.faqs['question'].tolist()
        self.answers = self.faqs['answer'].tolist()
        self.vectorizer = TfidfVectorizer()
        self.question_vectors = self.vectorizer.fit_transform(self.questions)

    def get_best_match(self, user_input):
        user_vec = self.vectorizer.transform([user_input])
        similarities = cosine_similarity(user_vec, self.question_vectors).flatten()
        best_idx = similarities.argmax()
        best_score = similarities[best_idx]
        # Return answer and score
        return self.questions[best_idx], self.answers[best_idx], best_score

    def get_top_n_matches(self, user_input, n=3):
        user_vec = self.vectorizer.transform([user_input])
        similarities = cosine_similarity(user_vec, self.question_vectors).flatten()
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
        try:
            df = pd.read_csv(path)
        except FileNotFoundError:
            df = pd.DataFrame(columns=['question'])

        new_row = pd.DataFrame({'question': [user_input]})
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv(path, index=False)

