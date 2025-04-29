import json
import re
import requests
import uuid

import service_library
from service_library import _JSONDecoder

# Используйте токен, полученный в личном кабинете из поля Авторизационные данные

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
    try:
        response = requests.request("POST",url, headers=headers, data=payload)
        received_data = json.loads(response.text, cls=_JSONDecoder)
        return received_data.get("result",{}).get("alternatives",[{}])[0].get("message",{}).get("text",None)  
    except:
        return ""

def get_token_sber():

    url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

    payload = 'scope=GIGACHAT_API_PERS'
    
    RqUID = str(uuid.uuid4())
    
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'application/json',
    'RqUID': RqUID,
    'Authorization': 'Basic ZjZmMmRjNzctYTQ4Zi00NjIwLWE5MzEtMzBiNDJhNmIyMjFhOmI3MjljZTIzLTdlZjUtNGMwZS1hNzY0LTNlOWYyOTY3MjM0Yw=='
    }

    response = requests.request("POST", url, headers=headers, data=payload, verify=False)
    
    text = str(response.text)
    
    # Регулярное выражение для поиска строки внутри фигурных скобок
    # result = re.search(r'{.*}', text)

   
    response_data = json.loads(response.text, cls=_JSONDecoder)




    return response_data.get("access_token",None)

def get_promt_sber (token, prompt_text,  content_text = 'Ты медицинский эксперт'):
    payload = json.dumps({
    "model": "GigaChat",
    "messages": [
        {
        "role": "system",
        "content": content_text
        },
        {
        "role": "user",
        "content": prompt_text
        }
    ],
    "stream": False,
    "update_interval": 0
    })
    
    headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Authorization': f'Bearer {token}'
    }

    print(headers)
    print(payload)
    response = requests.request("POST", _url_sber, headers=headers, data=payload, verify=False)

    print(response.text)
    print(type(response))
    return response.text#response.get("text",None)  




# получаем формулидованный ответ из ответа пациента
def get_answer_to_question_yandexGPT (question, answer, list_of_responses):
    
    gc_text = ''

    # формируем текс запроса
    responses = ''
    for i in list_of_responses:
        responses += f" '{i}', "
    
    responses += f" 'нет подходящего ответа' "
    
    # # убираем последнюю запятую
    # responses = responses[:-2] + responses[-1]
    
    
    prompt_text =   f"пациенту задавался вопрос: '{question}'.  От пациента был получен ответ: '{answer}'."\
                    f"Соотнеси ответ пациента одним из вариантов ответа и выдай его в качестве ответа: {responses}."

    gc_text = get_promt(prompt_text)
    
    if gc_text is None:
        return 'ошибка'
    
    gc_text = gc_text.replace('ё', 'е') #убираем ё в ответах LLM
    print(f'Входной текст: {prompt_text}. Получили текст ответа {gc_text}.')
        
    for i in list_of_responses:
        if i in gc_text:
            return i
    
    return 'нет подходящего ответа'
    


# получаем формулидованный ответ из ответа пациента
def get_float_to_question_yandexGPT (question, answer):
    
    gc_text = ''
    
    prompt_text =   f"пациенту задавался вопрос: '{question}'.  От пациента был получен ответ: '{answer}'. "\
                    f"напиши, какое это число?."

    gc_text = get_promt(prompt_text)
    
    if gc_text is None:
        return 'ошибка'
    print (f'Входной текст: {prompt_text}. Получили текст ответа {gc_text}.')
    return service_library.extract_float_number(gc_text)
    

    


def get_answer_yandexGPT (answer):
    
    prompt_text =   f"перефразируй рекомендацию'{answer}'. "

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


if __name__ == "__main__":
    
    
    #----------- запрос гигачат------------
    token = get_token_sber()
    print(get_promt_sber(token, 'если я кашлюю, что со мной'))
    #-----------конец запрос гигачат------------
    
    #----------- запрос яндекс gpt------------
    # print(get_answer_to_question_yandexGPT("какой у Вас кашель", "У меня кашель тяжело без выделения макроты", ["сухой","с мокротой"]))
    #-----------конец запрос яндекс gpt------------