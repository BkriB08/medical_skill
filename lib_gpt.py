import json
import re
import requests
import uuid
from dotenv import load_dotenv
import os
from main3 import global_true_symptoms
from symptoms import list_all_symptoms
from service_library import _JSONDecoder

load_dotenv()

_token = os.getenv("")
_url = ""
_modelUri = ""


def get_promt (prompt_text ):
    prompt = {
        "modelUri": _modelUri,
        "completionOptions": {
            "stream": False,
            "temperature": 0.6,
            "maxTokens": "2000"
        },
        "messages": [
            {
                "role": "system",
                "text": "Ответь на вопрос пользователя."
            },
            {
                "role": "assistant",
                "text": prompt_text
            },   
            ],
        }
    
    payload = json.dumps(prompt)
    url = _url
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Api-Key {_token}"
    }
    response = requests.request("POST",url, headers=headers, data=payload)
    received_data = json.loads(response.text, cls=_JSONDecoder)
    return received_data.get("result",{}).get("alternatives",[{}])[0].get("message",{}).get("text",None)  



# получаем формулидованный ответ из ответа пациента
def get_answer_to_question_yandexGPT (question, answer, list_of_responses):
    
    gc_text = ''

    responses = ''
    for i in list_of_responses:
        responses += f" '{i}', "

    
    prompt_text =   f"пациенту задавался вопрос: '{question}'.  От пациента был получен ответ: '{answer}'."\
                    f"Соотнеси ответ пациента одним из вариантов ответа и выдай его в качестве ответа: {responses}."

    gc_text = get_promt(prompt_text)

    gc_text = gc_text.replace('ё', 'е') #убираем ё в ответах LLM
    gc_text = gc_text.strip("«»'/'?.,|){}[]!@#$")
    return gc_text

        



def get_other_intent_yandexGPT (answer):
    
    prompt_text =   f"на вопрос врача к пациенту'можете сообщить значение, которое Вы измерили' пациент ответил: '{answer}'. Сделай вывод, "\
                    f" по смыслу ответа. Выбери один из наиболее подходящих из предложенных вариантов: "\
                    f" 'измерю позже', 'не буду измерять', 'не спрашивай больше меня об этом', 'ни чего не подходит' "

    gc_text = get_promt(prompt_text)
    print(f'Входной текст: {prompt_text}. Получили текст ответа {gc_text}.')
        
    later = True if gc_text  == 'измерю позже' else False
    
    wont = True if gc_text  == 'не буду измерять' else False
    print (f' возвращаем later = {later}, wont = {wont}, promt = {prompt_text}, ответ = {gc_text}')
    return later, wont
  


#функция ведет диалог, используя языкову модель
def get_question_from_yandexGPT (prompt):
    
    gc_text = get_promt(prompt)
    print(f'Входной текст: {prompt}. Получили текст ответа {gc_text}.')


    return gc_text






    
def recomend (sympt):
    
    c_text = ''

    answer = ''
    
    prompt_text =   f"у пациента следующие симптомы: '{sympt}'."\
                    f"Сделай рекомендации для этих симптомов без связи с медицинскими препаратами и выдай результат."

    c_text = get_promt(prompt_text)

    c_text = c_text.replace('ё', 'е') #убираем ё в ответах LLM
    c_text = c_text.strip("«»'/'?.,|){}[]!@#$")
    return c_text


if __name__ == "__main__":
    
    

    res= recomend(global_true_symptoms)
    print (res)