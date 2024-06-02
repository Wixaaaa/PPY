from src.quiz_brain import QuizBrain
from src.question_model import Question
import json
import random
import requests
import html

class Quiz:
    def __init__(self):
        self.questions = []
        self.scores = {}

    def load_questions_from_file(self, filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                questions_data = json.load(f)
                self.questions = [Question(q["question"], q["correct_answer"], q["choices"], q["category"]) for q in questions_data]
        except FileNotFoundError:
            print("File not found.")

    def add_question(self, question, correct_answer, choices, category):
        self.questions.append(Question(question, correct_answer, choices, category))

    def take_quiz(self, username, num_questions, category):
        filtered_questions = [q for q in self.questions if q.category == category]
        if not filtered_questions:
            print(f"No questions for {category}")
            return

        selected_questions = random.sample(filtered_questions, min(num_questions, len(filtered_questions)))
        quiz_brain = QuizBrain(selected_questions)

        while quiz_brain.has_more_questions():
            q_text = quiz_brain.next_question()
            print(q_text)
            for idx, choice in enumerate(quiz_brain.current_question.choices, 1):
                print(f"{idx}. {choice}")
            while True:
                answer_idx = input("Enter your answer (number): ")
                if answer_idx.isdigit() and 1 <= int(answer_idx) <= len(quiz_brain.current_question.choices):
                    selected_choice = quiz_brain.current_question.choices[int(answer_idx) - 1]
                    if quiz_brain.check_answer(selected_choice):
                        print("Good!")
                    else:
                        print(f"Wrong! The correct answer is: {quiz_brain.current_question.correct_answer}")
                    break
                else:
                    print("This answer does not exist. Enter correct number.")

        score, wrong, score_percent = quiz_brain.get_score()
        print(f"{username} scored {score} points out of {quiz_brain.question_no}. Wrong anwers: {wrong}. Final score: {score_percent}%.")

        if username not in self.scores:
            self.scores[username] = 0
        self.scores[username] += score
        self.save_scores()

    def save_scores(self):
        with open('scores.json', 'w', encoding='utf-8') as f:
            json.dump(self.scores, f, ensure_ascii=False, indent=4)

    def load_scores(self):
        try:
            with open('data/scores.json', 'r', encoding='utf-8') as f:
                self.scores = json.load(f)
        except FileNotFoundError:
            self.scores = {}

    def display_scores(self):
        print("Wyniki użytkowników:")
        for user, score in self.scores.items():
            print(f"{user}: Punkty - {score}")

    def save_questions(self):
        questions_data = [{
            "question": q.question_text,
            "correct_answer": q.correct_answer,
            "choices": q.choices,
            "category": q.category
        } for q in self.questions]
        with open('data/questions.json', 'w', encoding='utf-8') as f:
            json.dump(questions_data, f, ensure_ascii=False, indent=4)

    def fetch_questions_from_api(self, amount, category_id):
        parameters = {
            "amount": amount,
            "category": category_id,
            "type": "multiple"
        }
        response = requests.get(url="https://opentdb.com/api.php", params=parameters)
        if response.status_code == 200:
            question_data = response.json()["results"]
            for item in question_data:
                question = html.unescape(item["question"])
                choices = [html.unescape(choice) for choice in item["incorrect_answers"]]
                choices.append(correct_answer)
                if not any(q.question_text == question for q in self.questions):
                    self.add_question(question, correct_answer, choices, category_id)
            self.save_questions()
            print(f"Downloaded {amount} questions.")
        else:
            print("API connection error.")

