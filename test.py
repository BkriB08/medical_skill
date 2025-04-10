from symptoms import list_all_symptoms
from main3 import diagnose
from lib_gpt import get_answer_to_question_yandexGPT

def YPT_symptom ():
    symptom = get_answer_to_question_yandexGPT("какой симптом вас беспокоит?", initial_symptom_name , list_all_symptoms)
    print (symptom)