from answer import Answer

class QuestionData:
  def __init__(self, question: str, standard_answer: str, number):
    self.number = number
    self.question = question
    self.standard_answer = standard_answer
    self.chatbot_answers = []
  
  def add_answer(self, answer: Answer):
    self.chatbot_answers.append(answer)