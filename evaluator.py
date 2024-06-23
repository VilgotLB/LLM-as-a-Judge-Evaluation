from question_data import QuestionData
from dataset import Dataset
from openai import OpenAI
import json

class Evaluator:
  base_prompt = """Your task is to grade a set of answers to a question according to how correct they are based on the provided standard answer.

The grades should be based on the following parameters:
{}
Each parameter should be graded on a scale from 1 to 5:
1: Poor - The parameter is not met at all.
2: Fair - The parameter is partially met but with significant gaps.
3: Good - The parameter is mostly met but with some minor issues.
4: Very Good - The parameter is well met with only minor issues.
5: Excellent - The parameter is fully met with no issues.

If a parameter seems to fall between two grades, choose the grade that best reflects the overall performance of the parameter.

In the "Evaluation" field, you must go over each parameter and clearly elaborate on how well the answer meets each parameter.

The standard answer will be provided and should be used as the basis for your grading.

The output shall be in JSON format as an array of objects called \"results\", with each object having three key-value pairs: 
1. \"Answer\", with the answer number.
2. \"Evaluation\", which is an object containing a key-value pair for each of the parameters ({}), and an explanation for how well the parameter is met. 
3. \"Grades\", which is an object containing a key-value pair for each of the parameters ({}), and the grade for each parameter (integer from 1 to 5).

Here is the question, standard answer, and the answers:

"""

  def __init__(self, api_key):
    self.client = OpenAI(api_key=api_key)

  def create_prompt(self, question_data: QuestionData):
    params = [("Relevance", "The answer avoids introducing any additional aspects that are not included in the standard answer."),
              ("Completeness", "The answer covers all aspects of the standard answer."),
              ("Clarity", "The answer is direct, well-structured and easy to understand.")]
    param_string = ""
    for count, param in enumerate(params):
      param_string += f'{count+1}: {param[0]}: {param[1]}\n'
    
    param_names = [f'\"{element[0]}\"' for element in params]
    param_summary = ", ".join(param_names)
    
    prompt = self.base_prompt.format(param_string, param_summary, param_summary)

    qString = ""
    qString += f'Question: {question_data.question}\n\n'
    qString += f'Standard answer: {question_data.standard_answer}\n\n'
    for count, answer in enumerate(question_data.chatbot_answers):
      qString += f'Answer {count+1}: {answer.content}\n\n'

    prompt += qString

    return prompt
  
  def create_prompts(self, dataset: Dataset):
    prompts = []
    for question_data in dataset.questions:
      prompts.append(self.create_prompt(question_data))
    return prompts
  
  def grade_question(self, prompt):
    completion = self.client.chat.completions.create(
      model="gpt-4o",
      messages=[
        {"role": "user", "content": prompt}
      ],
      response_format={ "type": "json_object" }
    )
    response = json.loads(completion.choices[0].message.content)
    grades = [item['Grades'] for item in sorted(response['results'], key=lambda x: x['Answer'])]
    for answer in grades:
      sum = 0
      for grade in answer.values():
        sum += grade
      overall_grade = round(sum / 3, 2)
      answer['Overall grade'] = overall_grade
    return response
  
  def evaluate_all(self, dataset: Dataset, prompts, filename: str):
    all_data = []

    for i, question in enumerate(dataset.questions):
      data = {
        "Question number": question.number,
        "Question": question.question,
        "Standard answer": question.standard_answer,
        "Answers": []
      }

      results = self.grade_question(prompts[i])
      results = results['results']
      for count, answer in enumerate(question.chatbot_answers):
        answer_data = {}
        answer_data['Chatbot'] = answer.chatbot
        answer_data['Answer'] = answer.content
        answer_data['Evaluation'] = results[count]['Evaluation']
        answer_data['Relevance'] = results[count]['Grades']['Relevance']
        answer_data['Completeness'] = results[count]['Grades']['Completeness']
        answer_data['Clarity'] = results[count]['Grades']['Clarity']
        answer_data['Overall grade'] = results[count]['Grades']['Overall grade']
        data['Answers'].append(answer_data)
      
      all_data.append(data)
    
    with open(filename, 'w') as json_file:
      json.dump(all_data, json_file, indent=2)
  
