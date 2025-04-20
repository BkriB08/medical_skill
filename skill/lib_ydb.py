# import logging
# import service_library
# import secrets
# import json
# import ydb
# from service_library import _JSONEncoder, _JSONDecoder



 


    
  
# def get_count_patients_on_device(request):
#     text_query = f'SELECT id FROM PatientList WHERE yandexid = "{request.id_user}"'
#     try:
        
#         with ydb.QuerySessionPool(request.driver) as pool:      
#             result_sets = pool.execute_with_retries(text_query)
        
#         rows = result_sets[0].rows    
#         return len(rows)
    
#     except Exception as e: 
#         err = f'Ошибка получения id пользователя по yandexid. запрос = {text_query}. Ошибка {e}'
#         print(err)
#         logging.error (err)
#         return None


# # если вообще записи нет, то параметры вообще еще не снимались. 
# def set_unknown_intents (request):
#     _data = service_library.date_now (request.timezone)
#     pk = secrets.token_urlsafe(12)

#     text = f'Пользователь id={request.base_id_user} с именем {request.name_user} в модуле {request.id_dialog} произнес нераспознанную фразу: {request.last_command}'



#     json_str = " "
#     text_query = f"UPSERT INTO unknown_intents ( id, date_of_event, event, message) VALUES ('{pk}', DATE('{_data}'), '{json_str}', '{text}')"
#     singleline_text = text_query.replace('\n', ' ')
#     try:
        
#         logging.debug (f'set_unknown_intents запрос в БД {singleline_text}')

        
#         with ydb.QuerySessionPool(request.driver) as pool:      
#             pool.execute_with_retries(text_query)
        
        
#         return True    
    
#     except Exception as e: 
#         err = f'Ошибка сохранения нераспознанных фраз. запрос = {singleline_text}. Ошибка {e}'
#         print(err)
#         logging.error (err)
#         return False      
    
    


# def settingup_monitoring_to_base (request, value='weight', set=True):
#     request.settings[value] = set
    
#     json_str = json.dumps(request.settings, indent=4, cls=_JSONEncoder)

#     text_query = f"UPDATE PatientList SET settings = \'{json_str}\' WHERE id = '{request.base_id_user}'"
    
#     try:
#         logging.debug (f'settingup_monitoring_to_base запрос в БД {text_query}')

        
#         with ydb.QuerySessionPool(request.driver) as pool:      
#             pool.execute_with_retries(text_query)
        
        
#         return True    
    
#     except Exception as e: 
#         err = f'Ошибка осохранение настроек пациента settings. запрос = {text_query}. Ошибка {e}'
#         print(err)
#         logging.error (err)
#         return False    

    