import pytest
from unittest.mock import patch, mock_open
from quiz import Quiz

QUIZ_CONTENTS = """How much is 2+2?,1,10,2,0,3
Which Python keyword is used to define a function?,def,class,print,return,1
How much is 10/2?,10,5,2,20,2
Which of the following instructors do you like the most?,Sarah,Bob,John,Tim,4"""


@pytest.fixture
@patch("builtins.open", new_callable=mock_open, read_data=QUIZ_CONTENTS)
def quiz(mock_file):
    return Quiz("instructor.txt")


@patch("builtins.open", new_callable=mock_open, read_data=QUIZ_CONTENTS)
def test_quiz_open_file(mock_file):
    """The constructor of the Quiz class must open the text file provided in argument"""
    q = Quiz("instructor.txt")
    mock_file.assert_called_once_with("instructor.txt", "r")


def test_quiz_get_question(quiz):
    """get_question receives an integer"""
    assert quiz.get_question(1) == "How much is 2+2?"


def test_quiz_get_answer(quiz):
    """get_answer receives an integer"""
    assert quiz.get_answer(1) == 3


def test_quiz_get_question_answer_invalid_id(quiz):
    """The argument to get_question and get_answer must be a valid integer, otherwise return None"""
    for value in [-100, 0, 100, "abc"]:
        assert quiz.get_question(0) is None
        assert quiz.get_answer(0) is None


@patch("builtins.open", new_callable=mock_open, read_data="3\n1\n2\n1\n")
def test_quiz_grade_open(mock_file, quiz):
    """Test the grading of a student file - the file must be opened and read"""
    result = quiz.grade("student.txt")
    mock_file.assert_called_once_with("student.txt", "r")


@patch("builtins.open", new_callable=mock_open, read_data="3\n1\n2\n1\n")
def test_quiz_grade_result(mock_file, quiz):
    """
    The result of grading is a dictionary:
    - the key "grade" holds the number of correct answers
    - the key "wrong" holds a list with all the questions with WRONG answers
    """
    result = quiz.grade("student.txt")
    assert result["score"] == 3
    assert result["wrong"] == [
        "Which of the following instructors do you like the most?"
    ]


@patch("builtins.open", new_callable=mock_open, read_data="3\n")
def test_quiz_grade_invalid_student_file(mock_file, quiz):
    """If the student file and the instructor files don't have the same number of questions / answers, raise an Exception"""
    with pytest.raises(RuntimeError):
        quiz.grade("student.txt")


def test_quiz_full_question(quiz):
    """String formatting. Valid example:
    Which of the following instructors do you like the most?
    1 Sarah
    2 Bob
    3 John
    4 Tim
    """
    output = quiz.get_full_question(4)
    lines = output.split("\n")
    assert "Which of the following instructors do you like the most?" in lines[0]
    assert lines[-1].startswith("4")
    assert lines[-1].endswith("Tim")
