import os
#import logging
from datetime import date, datetime, timedelta
from dataclasses import dataclass, asdict
# import time
import pytz
import random
import re
import requests
import json
# import ydb
 


 
class _JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime)):
            return obj.strftime("%Y-%m-%dT%H:%M:%SZ")   #obj.isoformat()
        if isinstance(obj, (date)):
            return obj.strftime("%Y-%m-%d")   #obj.isoformat()
        return json.JSONEncoder.default(obj)       
        
class _JSONDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(
            self, object_hook=self.object_hook, *args, **kwargs)
    def object_hook(self, obj):
        ret = {}
        for key, value in obj.items():
            
            try:
                if value.endswith("Z"):
                    obj[key] = datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
                else:
                    obj[key] = datetime.strptime(value, "%Y-%m-%d")
            except:
                pass
        
            # if key in {'timestamp', 'whatever'}:
            #     ret[key] = datetime.fromisoformat(value) 
            # else:
            #     ret[key] = value
        return obj#ret 
 
 
def date_now (timezone = 'Asia/Krasnoyarsk'):
    _Timezone = pytz.timezone(timezone)
    now = datetime.now(_Timezone)
    res = str (now.strftime("%Y-%m-%d"))
    return res

def date_now_2 (timezone = 'Asia/Krasnoyarsk'):
    _Timezone = pytz.timezone(timezone)
    now = datetime.now(_Timezone)
    
    return now

def datetime_now( timezone = 'Asia/Krasnoyarsk'):
    _Timezone = pytz.timezone(timezone)
    now = datetime.now(_Timezone)
    res = str (now.strftime("%Y-%m-%dT%H:%M:%SZ"))
    return res    

def str_date_after (days, timezone = 'Asia/Krasnoyarsk', inc=True):
    _Timezone = pytz.timezone(timezone)
    now = datetime.now(_Timezone) + timedelta(days) if inc else datetime.now(_Timezone) - timedelta(days)
    res = str (now.strftime("%Y-%m-%d"))
    return res

def date_after (days, timezone = 'Asia/Krasnoyarsk', inc=True):
    _Timezone = pytz.timezone(timezone)
    new_date = datetime.now(_Timezone) + timedelta(days) if inc else datetime.now(_Timezone) - timedelta(days)
    
    return new_date

def time_now (timezone = 'Asia/Krasnoyarsk'):
    _Timezone = pytz.timezone(timezone)
    now = datetime.now(_Timezone)
    res = str(now.strftime("%H:%M"))
    return res

def transform_date(date: datetime):

    months = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
           'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']
    #year,month,day = date.split('-')
    year = date.year
    month = date.month
    day = date.day

    return f'{day} {months[month - 1]}'# {year} года'

def compare_time_with_current_one (value, timezone = 'Asia/Krasnoyarsk'):
   _Timezone = pytz.timezone(timezone)
   hr = int(value[0:2])
   min = int(value[-2:])
   now = datetime.now(_Timezone)
   target_dt = now.replace(hour=hr, minute=min)

   #print (f' поступило время строкой = {value}, преобразовали в дату {target_dt}.  Сейчас время {now}. Результат сравнения получился {target_dt < now}')

   return target_dt < now

#получаем строку в виде номеров дней недели и проверяем, текущая день недели входит в строку или нет
def checking_day_of_week (value, timezone = 'Asia/Krasnoyarsk'):
   _Timezone = pytz.timezone(timezone)
   now = str(datetime.now(_Timezone).isoweekday())
   #print (f'Текущий день недели {now} строка разрешенных дней {value}')

   return now in value


def parse_date(str, timezone = 'Asia/Krasnoyarsk'):
        
    day_list = {'первое':1, 'второе':2, 'третье':3, 'четвёртое':4,
    'пятое':5, 'шестое':6, 'седьмое':7, 'восьмое':8,
    'девятое':9, 'десятое':10, 'одиннадцатое':11, 'двенадцатое':12,
    'тринадцатое':13, 'четырнадцатое':14, 'пятнадцатое':15, 'шестнадцатое':16,
    'семнадцатое':17, 'восемнадцатое':18, 'девятнадцатое':19, 'двадцатое':20,
    'двадцать первое':21, 'двадцать второе':22, 'двадцать третье':23,
    'двадацать четвёртое':24, 'двадцать пятое':25, 'двадцать шестое':26,
    'двадцать седьмое':27, 'двадцать восьмое':28, 'двадцать девятое':29,
    'тридцатое':30, 'тридцать первое':31,'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'10':10,
    '11':11,'12':12,'13':13,'14':14,'15':15,'16':16,'17':17,'18':18,'19':19,'20':20,
    '21':21,'22':22,'23':23,'24':24,'25':25,'26':26,'27':27,'28':28,'29':29, '30':30,'31':31}
    month_list = {'января':1, 'февраля':2, 'марта':3, 'апреля':4, 'мая':5, 'июня':6,
        'июля':7, 'августа':8, 'сентября':9, 'октября':10, 'ноября':11, 'декабря':12}

    date = None
    words = str.split()
    print (f'строку разбили на слова {words}')
    for find_day in words:
        if find_day in day_list:
            for find_month in words:
                if find_month in month_list: 
                    print (f' find_month = {find_month} месяц {month_list[find_month]}, find_day = {find_day} число {day_list[find_day]}') 
                    
                    dt = date_now_2(timezone)
                    now_year=dt.year
                    now_month =dt.month
                    
                    year = now_year+1 if now_month > month_list[find_month] else now_year 
                    date = datetime(year, month_list[find_month], day_list[find_day])
                    print(f'получилась дата {date}')
                    return date
    return None

def find_numbers(s):
    return list(map(int, re.findall(r'\b\d+\b', s)))


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






def check_param_condition(param,value1,value2=None):
    #if param =='pressure':
    print(f' Проверяем границы полученных параметров: param = {param}, value1 = {value1}, value2 = {value2} ')
    match param:
        case 'pressure':
            if value1 > 180 or value2 > 300 or value2 < value1:
                return False
        case 'temperature':
            if value1 > 43 or value1 < 35:
                return False
        case 'weight':
            if value1 > 160 or value1 < 20:
                return False
        case 'pulse':
            if value1 > 300:
                return False
    return True


@dataclass
class Medicine:
    ids: str #Индекс в БД
    medication: str #наименование лекарства
    dosage: str = '' #Дозировка
    ReceptionTime: str  = '' #время приема лекарств
    executed: bool = False #отметка, что лекарство принято
    idRec: str = ''
    timestr_H: str = '' #время приема (часы)
    timestr_M: str = '' #время приема (минуты)


    def dump(self): #выводим как словарь для передачи в сессию
        return asdict(self)


def is_part_in_list(str_, words):
    for word in words:
        if word.lower() in str_.lower():
            return True
    return False





#определение запуска с вероятностью value в процентах. 
def need_of_start(value=0):
    #probability start in %
    i = random.randint(1, 100)
    print (f'генерируем вероятность запуска. Заданная вероятность {value}. Сгененрированно число {i}. Возвращенное значение {value >= i}')
    return False if value == 0 else value >= i








def average_in_list(value, index):
    k=0
    sum=0
    for i in value:
        if i["range"] == index:
            k+=1
            sum+=i["weight"]
    
    return 0 if sum==0 else round(sum/k,1)

def find_pos_next(value, index):
    for i in range(index+1,7):
        if not value[i]["weight"] == 0:
            return i    

def fill_in_empty_values (value):
    _value = value
    for i in range(0,7):
        if _value[i]["weight"] == 0:
            _value[i]["weight"] = round( (value[i-1]["weight"] + _value[find_pos_next(value, i)]["weight"])/2 ,1)
            
    return _value

def create_list_with_intervals(_list):
    data_start = _list[0]["weight_datetime"]
    date_finish = _list[len(_list)-1]["weight_datetime"]

    #print (f'разбиваем на интревалы: data_start= {data_start}, date_finish = {date_finish}')
    d = (date_finish- data_start) / 7
    ranges = [(i * d + data_start, (i+1)*d+data_start) for i in range(7)]
    ranges[6] = 6 * d + data_start, date_finish
    #print (f'разбиваем на интревалы: интервалы составляют ')
    #print(*ranges, sep="\n", end="\n\n")
    
    res=[]
    m=-1

    for t in ranges:
        m+=1
        #print (f'разбиваем на интревалы: смотрим, что попадает в интервал t[0]= {t[0]},  t[1] = { t[1]}')
        for i in _list:
            #print(f'if {i["weight_datetime"]} >= {t[0]} ({i["weight_datetime"] >= t[0]}) and {i["weight_datetime"]} <= {t[1]} ({i["weight_datetime"] <= t[1]}); ')
            if i["weight_datetime"] >= t[0] and i["weight_datetime"] <= t[1]:
                res.append({'weight': i["weight"], 'weight_datetime': i["weight_datetime"],'range':m})

    return res

def create_list(value):
    #print(f'входящий реестр: value')
    #print(*value, sep="\n", end="\n\n")
    #print(value)
    _value = create_list_with_intervals(value)
    
    #print(f"получили реестр, разбитый на интервалы:")
    #print(*_value, sep="\n", end="\n\n")
    #print(_value)
    
    res = []
    for i in range(0,7):
        res.append({"weight": average_in_list(_value, i), 'range': i})   
    #print(f'Собрали реестр в интервалы со средним: ')
    #print(*res, sep="\n", end="\n\n")
    #print(res)


    res = fill_in_empty_values(res)
    #print(f'заполнили пробелы в реестре: ')
    #print(*res, sep="\n", end="\n\n")
    #print(res)
    return res

def recalculation_of_intervals(value):
    _value = value
    for i in range(7):
        _value[i]["range"] =  _value[i]["range"] - 3
    return _value

def find_terend_in_weight(_list):
    new_list = create_list(_list)
    new_list = recalculation_of_intervals(new_list)
    #print(*new_list, sep="\n", end="\n\n")

    a=0
    b=0
    average = 0
    for row in new_list:
        a+=row['weight']*row['range']
        b+=row['range']*row['range']
        average+=row['weight']
    #print (f'a={a},  b={b}, a/b = {a/b}')

    average = round(average/7,1)
    increase = True if a/b > 0 else False
    return average, increase
    








#region определяем тренд в давлении


def average_in_list_pressure(value, index):
    k=0
    sum_up=0
    sum_down=0
    for i in value:
        if i["range"] == index:
            k+=1
            sum_up+=i["pressure_up"]
            sum_down+=i["pressure_down"]
    
    return {'sum_up':0,'sum_down':0} if sum_up==0 else {'sum_up':round(sum_up/k,0),'sum_down':round(sum_down/k,0)}

def find_pos_next_pressure(value, index):
    for i in range(index+1,7):
        if not value[i]["pressure_up"] == 0:
            return i    

def fill_in_empty_values_pressure (value):
    _value = value
    for i in range(0,7):
        if _value[i]["pressure_up"] == 0:
            _value[i]["pressure_up"] = round( (value[i-1]["pressure_up"] + _value[find_pos_next_pressure(value, i)]["pressure_up"])/2 ,0)
            _value[i]["pressure_down"] = round( (value[i-1]["pressure_down"] + _value[find_pos_next_pressure(value, i)]["pressure_down"])/2 ,0)
            
    return _value

def create_list_with_intervals_pressure(_list):
    data_start = _list[0]["pressure_datetime"]
    date_finish = _list[len(_list)-1]["pressure_datetime"]

    #print (f'разбиваем на интревалы: data_start= {data_start}, date_finish = {date_finish}')
    d = (date_finish- data_start) / 7
    ranges = [(i * d + data_start, (i+1)*d+data_start) for i in range(7)]
    ranges[6] = 6 * d + data_start, date_finish
    #print (f'разбиваем на интревалы: интервалы составляют ')
    #print(*ranges, sep="\n", end="\n\n")
    
    res=[]
    m=-1

    for t in ranges:
        m+=1
        #print (f'разбиваем на интревалы: смотрим, что попадает в интервал t[0]= {t[0]},  t[1] = { t[1]}')
        for i in _list:
            #print(f'if {i["weight_datetime"]} >= {t[0]} ({i["weight_datetime"] >= t[0]}) and {i["weight_datetime"]} <= {t[1]} ({i["weight_datetime"] <= t[1]}); ')
            if i["pressure_datetime"] >= t[0] and i["pressure_datetime"] <= t[1]:
                res.append({'pressure_up': i["pressure_up"],'pressure_down': i["pressure_down"],  'pressure_datetime': i["pressure_datetime"],'range':m})

    return res

def create_list_pressure(value):
    #print(f'входящий реестр: value')
    #print(*value, sep="\n", end="\n\n")
    #print(value)
    _value = create_list_with_intervals_pressure(value)
    
    #print(f"получили реестр, разбитый на интервалы:")
    #print(*_value, sep="\n", end="\n\n")
    #print(_value)
    
    res = []
    for i in range(0,7):
        res.append({"pressure_up": average_in_list_pressure(_value, i)['sum_up'], "pressure_down": average_in_list_pressure(_value, i)['sum_down'], 'range': i})   
    #print(f'Собрали реестр в интервалы со средним: ')
    #print(*res, sep="\n", end="\n\n")
    #print(res)


    res = fill_in_empty_values_pressure(res)
    #print(f'заполнили пробелы в реестре: ')
    #print(*res, sep="\n", end="\n\n")
    #print(res)
    return res

def recalculation_of_intervals_pressure(value):
    _value = value
    for i in range(7):
        _value[i]["range"] =  _value[i]["range"] - 3
    return _value

def find_terend_in_pressure(_list):
    new_list = create_list_pressure(_list)
    new_list = recalculation_of_intervals_pressure(new_list)
    #print(*new_list, sep="\n", end="\n\n")

    a_up=0
    a_down=0
    b=0
    average_up = 0
    average_down = 0
    for row in new_list:
        a_up+=row['pressure_up']*row['range']
        a_down+=row['pressure_down']*row['range']
        b+=row['range']*row['range']
        average_up+=row['pressure_up']
        average_down+=row['pressure_down']
    #print (f'a_up={a_up},  b={b}, a/b = {a_up/b}')

    average_up = round(average_up/7,1)
    average_down = round(average_down/7,1)
    increase = True if a_up/b > 0 else False
    return average_up,  average_down, increase
#endregion 






# #функция вычисляет калораж еды и активности и дает рекомендации
# def get_kkal_from_gigachat (text = 'на завтрак я съел овсяную кашу на молоке 1 чашка. ответь кратко, какая примерно калорийность еды?'):
#     # Используйте токен, полученный в личном кабинете из поля Авторизационные данные
#     token = 'ZjZmMmRjNzctYTQ4Zi00NjIwLWE5MzEtMzBiNDJhNmIyMjFhOmI2OWQzYmRkLWQ5NzctNGI5My1iNmMyLTcyYzg0YzA3YTBhZg=='
#     gc_text = ''
#     gc_kkal = 0
#     print(f'Запускаем гигачат')
#     with GigaChat(credentials=token, verify_ssl_certs=False) as giga:
#         gc_response = giga.chat(text)
#         print(gc_response.choices[0].message.content)
#         gc_text=gc_response.choices[0].message.content

#     print(f'Входной текст: {text}. Получили текст ответа {gc_text}, начинаем доставать калории.')
        
#     gc_text = gc_text.replace('.','')
#     gc_text = gc_text.replace(',','')
#     gc_text = gc_text.replace('*','')
#     print (f' gc_text = {gc_text}')
#     words = gc_text.split()
#     print (f' words = {words}')
#     for i in range(1, len(words)):
#         if words[i-1].isdigit():
#             print(words[i-1], words[i])
#             if words[i] == 'ккал':
#                 gc_kkal = int(words[i-1])
#     print(f'Входной текст: {text}. Получили текст ответа {gc_text}, посчитанные калории = {gc_kkal}.')
#     return gc_kkal

#функция вычисляет калораж еды и активности и дает рекомендации
def get_kkal_from_yandexGPT (eat_lines):
    
    # Используйте токен, полученный в личном кабинете из поля Авторизационные данные
    token = os.getenv("TOKEN")
    gc_text = ''
    gc_kkal = 0
    prompt = {
        "modelUri": "gpt://b1gnm0fvekn5a1q9r0lj/yandexgpt-lite",
        "completionOptions": {
            "stream": False,
            "temperature": 0.6,
            "maxTokens": "2000"
        },
        "messages": [
            {
                "role": "system",
                "text": "Ты диетолог. Отвечай кратко. одним предложением. Обязательно дай приблизительное значение калорийности съеденной пищи"
            },


        ]
    }
    qw = {
                "role": "user",
                "text": "Сколько это примерно калориев?"                 
    }

    
    for s, q in zip (eat_lines["food_consumed"] , eat_lines["food_consumed_question"]):
        #text += s + ", "

        assistant = {
                "role": "assistant",
                "text": q
            }        
        user = {
                "role": "user",
                "text": s
            }
        prompt["messages"].append(assistant)
        prompt["messages"].append(user)

    prompt["messages"].append(qw)

    #text = text[:-2] + '. Сколько это калориев?'
    #print (f'text = {text}')
    print (f'prompt = {prompt}')

    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Api-Key {token}"
    }

    response = requests.post(url, headers=headers, json=prompt)
    result = response.text
    print (type (result))
    result = eval(response.text)
    print (type (result))
    print(f'result = {result}')
    #print(f' result["result"] = {result["result"]}')
    #print(f' result["result"]["alternatives"] = {result["result"]["alternatives"]}')
    #print(f' result["result"]["alternatives"][0] = {result["result"]["alternatives"][0]}')
    #print(f' result["result"]["alternatives"][0]["message"] = {result["result"]["alternatives"][0]["message"]}')
    #print(f' result["result"]["alternatives"][0]["message"]["text"] = {result["result"]["alternatives"][0]["message"]["text"]}')
    gc_text = result["result"]["alternatives"][0]["message"]["text"]

    
    '''
    result = {
        "result":
        {
            "alternatives":
                [{"message":
                  {"role":"assistant",
                   "text":"Приблизительно 350 ккал. Точная калорийность зависит от жирности молока, марки овсяной каши и количества крупы, которое вы обычно употребляете на завтрак."
                   },
                "status":"ALTERNATIVE_STATUS_FINAL"
                }],
            "usage":
                {"inputTextTokens":"47",
                 "completionTokens":"32",
                 "totalTokens":"79"},
            "modelVersion":"18.01.2024"
        }}
    '''

    print(f'Входной текст: {prompt}. Получили текст ответа {gc_text}, начинаем доставать калории.')
        
    gc_text = gc_text.replace('.','')
    gc_text = gc_text.replace(',','')
    gc_text = gc_text.replace('*','')
    words = gc_text.split()
    for i in range(1, len(words)):
        if words[i-1].isdigit():
            print(words[i-1], words[i])
            if words[i] == 'ккал' or words[i] == 'калорий':
                gc_kkal = int(words[i-1])
    print(f'words = {words}. Получили текст ответа {gc_text}, посчитанные калории = {gc_kkal}.')
    return gc_kkal





#рассчитываем количество потраченных на активность калориев
def get_energy_spent (val):

    energy_spent = 1200 #ежедневно истрачиваемые калории просто на поддержание жизни
    
    #Если есть данные по шагам, то рассчитываем, сколько калориев потрачено на хотьбу
    if 'steps' in val:
        energy_spent += val ["steps"] * 0.04

    #если занимался спортом, то добавляем средние 500 кал
    if 'sport' in val:
        if val ["sport"]:
            energy_spent += 500
    return energy_spent

