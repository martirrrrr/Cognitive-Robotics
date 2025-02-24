import time
import random
import utils

score = 0

quiz_questions = [
    {"question": "What is the capital of France?", "options": ["A) Madrid", "B) Berlin", "C) Paris", "D) Rome"], "correct_answer": "C"},
    {"question": "Who wrote 'Romeo and Juliet'?", "options": ["A) Charles Dickens", "B) William Shakespeare", "C) Jane Austen", "D) Mark Twain"], "correct_answer": "B"},
    {"question": "What is the chemical symbol for gold?", "options": ["A) Au", "B) Ag", "C) Pb", "D) Fe"], "correct_answer": "A"},
    {"question": "Which planet is known as the Red Planet?", "options": ["A) Venus", "B) Mars", "C) Jupiter", "D) Saturn"], "correct_answer": "B"},
    {"question": "How many continents are there on Earth?", "options": ["A) 5", "B) 6", "C) 7", "D) 8"], "correct_answer": "C"},
    {"question": "Who painted the Mona Lisa?", "options": ["A) Michelangelo", "B) Vincent van Gogh", "C) Leonardo da Vinci", "D) Pablo Picasso"], "correct_answer": "C"},
    {"question": "What is the longest river in the world?", "options": ["A) Amazon River", "B) Nile River", "C) Mississippi River", "D) Yangtze River"], "correct_answer": "B"},
    {"question": "Who discovered gravity?", "options": ["A) Albert Einstein", "B) Nikola Tesla", "C) Isaac Newton", "D) Galileo Galilei"], "correct_answer": "C"},
    {"question": "What is the largest ocean on Earth?", "options": ["A) Atlantic Ocean", "B) Indian Ocean", "C) Pacific Ocean", "D) Arctic Ocean"], "correct_answer": "C"},
    {"question": "What year did World War II end?", "options": ["A) 1943", "B) 1945", "C) 1947", "D) 1950"], "correct_answer": "B"},
    {"question": "What is the square root of 64?", "options": ["A) 6", "B) 7", "C) 8", "D) 9"], "correct_answer": "C"},
    {"question": "Who was the first man on the moon?", "options": ["A) Neil Armstrong", "B) Buzz Aldrin", "C) Michael Collins", "D) Yuri Gagarin"], "correct_answer": "A"},
    {"question": "What is the capital of Canada?", "options": ["A) Toronto", "B) Vancouver", "C) Ottawa", "D) Montreal"], "correct_answer": "C"},
    {"question": "What is the largest mammal on Earth?", "options": ["A) Elephant", "B) Blue Whale", "C) Giraffe", "D) Rhino"], "correct_answer": "B"},
    {"question": "In what year did the Titanic sink?", "options": ["A) 1910", "B) 1912", "C) 1920", "D) 1905"], "correct_answer": "B"},
    {"question": "Who invented the light bulb?", "options": ["A) Alexander Graham Bell", "B) Nikola Tesla", "C) Thomas Edison", "D) Albert Einstein"], "correct_answer": "C"},
    {"question": "What is the chemical symbol for water?", "options": ["A) O2", "B) H2O", "C) CO2", "D) H2"], "correct_answer": "B"},
    {"question": "What is the largest desert in the world?", "options": ["A) Sahara Desert", "B) Arabian Desert", "C) Gobi Desert", "D) Antarctic Desert"], "correct_answer": "D"},
    {"question": "What is the hardest natural substance on Earth?", "options": ["A) Gold", "B) Iron", "C) Diamond", "D) Platinum"], "correct_answer": "C"},
    {"question": "Which element has the atomic number 1?", "options": ["A) Oxygen", "B) Helium", "C) Hydrogen", "D) Carbon"], "correct_answer": "C"},
    {"question": "Who painted the Sistine Chapel?", "options": ["A) Raphael", "B) Michelangelo", "C) Leonardo da Vinci", "D) Vincent van Gogh"], "correct_answer": "B"},
    {"question": "What is the smallest country in the world?", "options": ["A) Monaco", "B) Vatican City", "C) San Marino", "D) Liechtenstein"], "correct_answer": "B"},
    {"question": "What is the capital of Italy?", "options": ["A) Florence", "B) Milan", "C) Rome", "D) Venice"], "correct_answer": "C"},
    {"question": "Which planet is closest to the Sun?", "options": ["A) Earth", "B) Venus", "C) Mercury", "D) Mars"], "correct_answer": "C"},
    {"question": "How many teeth does an adult human have?", "options": ["A) 28", "B) 30", "C) 32", "D) 34"], "correct_answer": "C"},
    {"question": "What is the boiling point of water?", "options": ["A) 90°C", "B) 95°C", "C) 100°C", "D) 110°C"], "correct_answer": "C"},
    {"question": "What is the smallest planet in our solar system?", "options": ["A) Earth", "B) Mercury", "C) Mars", "D) Venus"], "correct_answer": "B"},
    {"question": "What is the main ingredient in guacamole?", "options": ["A) Tomato", "B) Avocado", "C) Onion", "D) Pepper"], "correct_answer": "B"},
    {"question": "What is the largest island in the world?", "options": ["A) Australia", "B) Greenland", "C) New Guinea", "D) Borneo"], "correct_answer": "B"},
    {"question": "Who wrote 'The Odyssey'?", "options": ["A) Homer", "B) Virgil", "C) Shakespeare", "D) Plato"], "correct_answer": "A"},
    {"question": "Which country is the largest by land area?", "options": ["A) Canada", "B) United States", "C) Russia", "D) China"], "correct_answer": "C"},
    {"question": "Who discovered America?", "options": ["A) Christopher Columbus", "B) Ferdinand Magellan", "C) Marco Polo", "D) John Cabot"], "correct_answer": "A"},
    {"question": "What is the capital of Japan?", "options": ["A) Beijing", "B) Seoul", "C) Tokyo", "D) Bangkok"], "correct_answer": "C"},
    {"question": "Which is the tallest mountain in the world?", "options": ["A) K2", "B) Mount Everest", "C) Kilimanjaro", "D) Denali"], "correct_answer": "B"},
    {"question": "What is the currency of the United Kingdom?", "options": ["A) Dollar", "B) Euro", "C) Pound", "D) Franc"], "correct_answer": "C"},
    {"question": "What is the fastest land animal?", "options": ["A) Lion", "B) Leopard", "C) Cheetah", "D) Gazelle"], "correct_answer": "C"},
    {"question": "Who is known as the father of modern physics?", "options": ["A) Albert Einstein", "B) Isaac Newton", "C) Galileo Galilei", "D) Niels Bohr"], "correct_answer": "A"},
    {"question": "Which animal is the largest living species on Earth?", "options": ["A) Elephant", "B) Blue Whale", "C) Giraffe", "D) Great White Shark"], "correct_answer": "B"},
    {"question": "What is the capital of Australia?", "options": ["A) Sydney", "B) Melbourne", "C) Canberra", "D) Perth"], "correct_answer": "C"},
    {"question": "What is the longest bone in the human body?", "options": ["A) Femur", "B) Tibia", "C) Humerus", "D) Radius"], "correct_answer": "A"},
    {"question": "What is the tallest building in the world?", "options": ["A) Burj Khalifa", "B) Shanghai Tower", "C) Empire State Building", "D) CN Tower"], "correct_answer": "A"},
    {"question": "Which ocean is the largest?", "options": ["A) Atlantic Ocean", "B) Indian Ocean", "C) Pacific Ocean", "D) Arctic Ocean"], "correct_answer": "C"},
    {"question": "Who invented the telephone?", "options": ["A) Thomas Edison", "B) Alexander Graham Bell", "C) Nikola Tesla", "D) Guglielmo Marconi"], "correct_answer": "B"}
]

def ask_question():
    global score
    # Randomly choose a question and remove it from the list
    current_question = random.choice(quiz_questions)
    quiz_questions.remove(current_question)  # Remove the question to avoid repetition

    utils.text_to_speech.say(str(current_question["question"]))
    #print(current_question["question"])

    for option in current_question["options"]:
        #print(option)
        utils.text_to_speech.say(str(option))
        time.sleep(1.0)

    #user_answer = input("Your answer (A, B, C, D): ").strip().upper()
    user_answer= utils.recognize_speech()

    if user_answer == current_question["correct_answer"]:
        utils.text_to_speech.say("Good!")
        #print("Correct!")
        score += 1
    else:
        #print("Incorrect.")
        utils.text_to_speech.say("Incorrect. Correct answer is:"+str(current_question["correct_answer"]))
        #print("Correct answer is: ", current_question["correct_answer"])

    utils.text_to_speech.say("Your score is "+str(score))
    #print(f"Your score is: {score}")


def retry_quiz():
    global score
    utils.text_to_speech.say("Do you want to retry?")
    #print("Retry?")

    user_answer = utils.recognize_speech()
    #user_answer = input("Would you like to try again? (yes/no): ").strip().lower()
    if user_answer == "yes":
        score = 0  # Reset the score for a new game
        play_quiz()
    else:
        utils.text_to_speech.say("Thank you for playing!")
        #print("Thank you for playing!")


def play_quiz():
    global score
    for i in range(10):
        ask_question()

    if score <= 5:
        utils.text_to_speech.say("You can do better!")
        #print("You can do better!")
    else:
        utils.text_to_speech.say("Congratulations!")
        #print("Congratulations!")

    retry_quiz()


# Start the quiz
    def main():
        try:
            play_quiz()
        except Exception as e:
            print("[ERROR] A problem occurred:", e)