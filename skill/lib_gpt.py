import json
import re
import requests

from service_library import _JSONDecoder



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
                "role": "assistant",
                "text": prompt_text
            },   ]}
    url = _url
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Api-Key {_token}"
    }
    response = requests.post(url, headers=headers, json=prompt)
    received_data = json.loads(response.text, cls=_JSONDecoder)
    return received_data.get("result",{}).get("alternatives",[{}])[0].get("message",{}).get("text",None)  



# выделяем из строки значения давления
def extract_two_numbers_from_string(input_string):
    if input_string is None: return None, None
    pattern = r'\d+\s+на\s+\d+'  # шаблон для поиска чисел через "на"
    match = re.search(pattern, input_string)
    
    if match:
        numbers = match.group().strip().split(' на ')
        
        try:
            up = int(numbers[0])
            down = int(numbers[1])
            
            return up, down
        except ValueError:
            return None, None
            # pass  # обработка ситуации, если числа не удается привести к целым
    
    return None, None  # если не найдено совпадение или произошла ошибка

def extract_number_from_string(input_string):
    if input_string is None: return None
    pattern = r'\b\d+\b'  # шаблон для поиска чисел через "на"
    match = re.search(pattern, input_string)


    if match:
        try:
            number = int(match.group())
            # print(number)
            return number
        except ValueError:
            return None
            # pass  # обработка ситуации, если числа не удается привести к целым        
        
    else:
        return None

def extract_float_number(input_string):
    if input_string is None: return None
    input_string = input_string.replace(",", ".")
    for word in input_string.split():  # Разбиваем строку на слова
        try:
            return float(word)  # Пробуем преобразовать слово в число с плавающей точкой
        except ValueError:
            continue  # Если не получилось, переходим к следующему слову
    return None  # Если ничего не нашли, возвращаем None



# def get_other_intent_yandexGPT (answer):
    
#     prompt_text =   f"на вопрос врача к пациенту'можете сообщить значение, которое Вы измерили' пациент ответил: '{answer}'. Сделай вывод, "\
#                     f" по смыслу ответа. Выбери один из наиболее подходящих из предложенных вариантов: "\
#                     f" 'измерю позже', 'не буду измерять', 'не спрашивай больше меня об этом', 'ни чего не подходит' "

#     gc_text = get_promt(prompt_text)
#     print(f'Входной текст: {prompt_text}. Получили текст ответа {gc_text}.')
        
#     later = True if gc_text  == 'измерю позже' else False
    
#     wont = True if gc_text  == 'не буду измерять' else False
#     print (f' возвращаем later = {later}, wont = {wont}, promt = {prompt_text}, ответ = {gc_text}')
#     return later, wont
  


#функция ведет диалог, используя языкову модель
def get_question_from_yandexGPT (prompt):
    
    gc_text = get_promt(prompt)
    print(f'Входной текст: {prompt}. Получили текст ответа {gc_text}.')


    return gc_text

