import csv
import os


class Quiz:
    def __init__(self, filename):
        """ Constructor: opens and reads file storing all information """
        self.quiz_questions = []
        self.quiz_options = []
        self.quiz_answers = []

        with open(filename, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                self.quiz_questions.append(row[0])
                self.quiz_options.append(row[1:5])
                self.quiz_answers.append(int(row[-1]))

    def get_question(self, num: int):
        """ Method: gets question based on a given number argument """
        if (type(num) != int) or num > len(self.quiz_questions) or num <= 0:
            return None
        else:
            return self.quiz_questions[num-1]

    def get_options(self, num: int):
        """ Method: gets question options based on a given number argument """
        if (type(num) != int) or num > len(self.quiz_questions) or num <= 0:
            return None
        else:
            return self.quiz_options[num-1]

    def get_answer(self, num: int):
        """ Method: gets the answer of the question based on a given number argument """
        if (type(num) != int) or num > len(self.quiz_questions) or num <= 0:
            return None
        else:
            return int(self.quiz_answers[num-1])

    def grade(self, path: str):
        """ Method: grades the student answers returning a score and a list of wrong answers the student got """
        score = 0
        wrong = []

        with open(path, 'r') as file:
            row = file.readlines()
            student_answers = [int(item.strip("\n"))
                               for item in row]  # list of student answers

        if len(self.quiz_questions) != len(student_answers):
            raise RuntimeError

        index = 1
        for answer in student_answers:
            if answer != self.get_answer(index):
                wrong.append(self.get_question(index))
                index += 1
            else:
                score += 1
                index += 1

        return {"score": score, "wrong": wrong}

    def get_full_question(self, question_num: int):
        """ Method: Returns a string of the full question with the question options based on a given user argument """
        question = self.get_question(question_num)
        options = self.get_options(question_num)

        return f"{question}\n1 {options[0]}\n2 {options[1]}\n3 {options[2]}\n4 {options[3]}"
