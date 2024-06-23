from question_data import QuestionData
from answer import Answer
import pandas as pd
import random

class Dataset:
  def __init__(self):
    self.questions = []

  def add_question(self, question: QuestionData):
    self.questions.append(question)
  
  def set_questions(self, questions):
    self.questions = questions
  
  def import_from_csv(self, filename: str, question_column, standard_column, answer_columns):
    data=pd.read_csv(filename)
    for row_number, (index, row) in enumerate(data.iterrows()):
      q = QuestionData(row.iloc[question_column], row.iloc[standard_column], row_number+1)
      for element in answer_columns:
        answer = Answer(element[1], row.iloc[element[0]])
        q.add_answer(answer)
      self.questions.append(q)
  
  def get_question(self, number):
    return self.questions[number-1]
  
  def get_sample(self, N):
    new_dataset = Dataset()
    sample = random.sample(self.questions, N)
    sorted_sample = sorted(sample, key=lambda obj: obj.number)
    new_dataset.set_questions(sorted_sample)
    return new_dataset