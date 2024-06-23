# LLM-as-a-Judge Evaluation

This repository includes the code, dataset and results of our bachelor thesis about automatic evaluation of chatbots using LLM-as-a-Judge, at Linnaeus University. The authors are Vilgot Lundborg and Yuyao Duan. The program automatically evaluates the correctness of chatbot answers to a set of questions in history and biology, using another LLM to perform this evaluation. The chatbots whose answers are being evaluated are Llama 3 70B, ChatGPT 4, and Gemini Advanced. The LLM that evaluates the answers is the GPT-4o API. The GPT-4o API is instructed to grade the answers based on three parameters: relevance, completeness, and clarity, each being graded from 1 to 5, together with an explanation. An overall grade based on the average of the three grades is also calculated. The results are stored in JSON format in the results folder.

## How to run
1. Install the required libraries using `pip install openai pandas`.
2. Add your OpenAI API key as the parameter to the evaluator on line 19 in `main.py`.
3. Run `main.py`.
