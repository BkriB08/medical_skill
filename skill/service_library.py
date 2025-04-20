from datetime import date, datetime, timedelta
import pytz
import json
 


 
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
