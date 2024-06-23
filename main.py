from question_data import QuestionData
from answer import Answer
from dataset import Dataset
from evaluator import Evaluator
import time

start_time = time.time()


history_dataset = Dataset()
history_dataset.import_from_csv('data/history_data.csv', 0, 1, [(2, 'Llama'), (3, 'ChatGPT'), (4, 'Gemini')])

biology_dataset = Dataset()
biology_dataset.import_from_csv('data/biology_data.csv', 0, 1, [(2, 'Llama'), (3, 'ChatGPT'), (4, 'Gemini')])

history_sample = history_dataset.get_sample(10)
biology_sample = biology_dataset.get_sample(10)

eval = Evaluator("")

history_prompts = eval.create_prompts(history_sample)
biology_prompts = eval.create_prompts(biology_sample)

eval.evaluate_all(history_sample, history_prompts, 'results/history_results.json')
eval.evaluate_all(biology_sample, biology_prompts, 'results/biology_results.json')


end_time = time.time()
elapsed_time = round(end_time - start_time)
print(f'Elapsed time: {elapsed_time} seconds')
