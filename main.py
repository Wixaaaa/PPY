from src.question_model import Question
from src.quiz_brain import QuizBrain
from src.quiz import Quiz

def main():
    categories = {
            "1": "General Knowledge",
            "2": "Science & Nature",
            "3": "Sports",
            "4": "History",
            "5": "Art",
            "7": "Animals",
            "8": "Science: Computers",
            "9": "Entertainment: Video Games",
            "10": "Entertainment: Music",
            "11": "Entertainment: Film",
            "12": "Entertainment: Books"
    }
    category_ids = {
            "General Knowledge": 9,
            "Science & Nature": 17,
            "Sports": 21,
            "History": 23,
            "Art": 25,
            "Geography": 22,
            "Entertainment: Books": 10,
            "Entertainment: Film": 11,
            "Entertainment: Music": 12,
            "Entertainment: Video Games": 15,
            "Science: Computers": 18,
            "Animals": 27    
    }

    quiz = Quiz()
    quiz.load_scores()
    quiz.load_questions_from_file('data/questions.json')

    while True:
        print("\nMenu:")
        print("1. Start quiz")
        print("2. Add question")
        print("3. Show scores")
        print("4. Get new questions from OTDB")
        print("5. Exit")

        choice = input("Select option: ")
            
        if choice == "1":
            while True:
                username = input("Enter your username: ")
                if username:
                    break
                else:
                    username = input("Enter your username: ")
            print("Choose category:")
            for key, value in categories.items():
                print(f"{key}. {value}")
            category_choice = input("Choose category (number): ")
            selected_category = category_ids.get(categories.get(category_choice, "General Knowledge"))
            if selected_category:
                available_questions = sum(1 for q in quiz.questions if q.category == selected_category)
                if available_questions > 0:
                    print(f"Available questions: {available_questions}")
                    num_questions = int(input(f"How many question do you want? (Max: {available_questions}): "))
                    if 0 < num_questions <= available_questions:
                        quiz.take_quiz(username, num_questions, selected_category)
                    else:
                        print("Choose correct number of questions.")
                else:
                    print(f"No available questions.")
            else:
                print("Incorrect category.")
        elif choice == "2":
            while True:
                question = input("Enter question: ")
                correct_answer = input("Enter correct answer: ")
                choices = input("Enter possible wrong answers separated by commas: ").split(",")
                choices.append(correct_answer)
                print("Choose categpry:")
                for key, value in categories.items():
                    print(f"{key}. {value}")
                category_choice = input("Choose category (number): ")
                category = category_ids.get(categories.get(category_choice, "General Knowledge"))
                if not any(q.question_text == question for q in quiz.questions):
                    quiz.add_question(question, correct_answer, choices, category)
                    break
                else:
                    print("This question already exist. Add new one!")
            quiz.save_questions()
        elif choice == "3":
            quiz.display_scores()
        elif choice == "4":
            amount = int(input("How many new questions do you want to get? "))
            print("Choose category:")
            for key, value in categories.items():
                print(f"{key}. {value}")
            category_choice = input("Choose category (number): ")
            category_id = category_ids[categories.get(category_choice, "General Knowledge")]
            quiz.fetch_questions_from_api(amount, category_id)
        elif choice == "5":
            break
        else:
            print("Wrong option, try again.")


if __name__ == "__main__":
    main()
