import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os

class FAQChatbot:
    def __init__(self, csv_path):
        # Load FAQs
        self.faqs = pd.read_csv(csv_path)
        self.questions = self.faqs['question'].fillna("").tolist()
        self.answers = self.faqs['answer'].fillna("").tolist()

        # Build vectorizer and question vectors
        self.vectorizer = TfidfVectorizer()
        self.question_vectors = self.vectorizer.fit_transform(self.questions)

    def get_best_match(self, user_query):
        if not user_query.strip():
            return "", "Please enter a valid question.", 0.0

        # Transform user query
        user_vector = self.vectorizer.transform([user_query])

        # Compute cosine similarity
        similarities = cosine_similarity(user_vector, self.question_vectors)
        score = similarities[0].max()

        # Find best match
        index = similarities[0].argmax()
        matched_question = self.questions[index]
        matched_answer = self.answers[index]

        return matched_question, matched_answer, score

    def save_unanswered(self, user_query):
        filename = "unanswered.csv"
        df = pd.DataFrame([[user_query]], columns=['unanswered'])

        if os.path.isfile(filename):
            df_existing = pd.read_csv(filename)
            df_combined = pd.concat([df_existing, df], ignore_index=True)
            df_combined.to_csv(filename, index=False)
        else:
            df.to_csv(filename, index=False)
