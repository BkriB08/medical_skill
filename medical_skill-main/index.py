import json
import logging
from lib_class_dialog import Request
from lib_standard_dialogs import DIALOGS as DIALOGS_standart
from dialogs import DIALOGS as DIALOGS_dialogs
from service_library import _JSONDecoder
from dialogs import my_dialog1 as DEFAULT_DIALOG

logging.getLogger().setLevel(logging.DEBUG)



def handler(event, context):
    
    #print(f"START. Получили event {event}")
    print (f"***********START**************. Получили event {event}")
    
    if type(event) is not dict:
        event = json.loads(event, cls=_JSONDecoder)

    request = Request(event)
    # print(f"Создали объект request класса Request")


    #Переносим список всех диалоговых функций в глобальную переменную
    request.Global_DIALOGS = DIALOGS

    if request.id_dialog is None:
        print (f'DEBAG id_dialog = {request.id_dialog}. Нет данных о предыдуще запуске навыка. Запускаем функцию формирования заданий на сессияю')
        #получаем ссылку на следующую диалоговую ветку
        #dialog =  DIALOGS.get(DEFAULT_DIALOG)()
        return DEFAULT_DIALOG().reply(request)   #dialog.reply(request) 
    
    previous_dialog_module = DIALOGS.get(request.id_dialog, DEFAULT_DIALOG)()
    
    next_dialog_module = previous_dialog_module.move(request)                      #получаем объект следующего диалога
    
    print(f"DEBAG2 GLOBAL  previous_dialog_module = {previous_dialog_module}, next_dialog_module = {next_dialog_module}")



    if next_dialog_module is not None:
        return next_dialog_module.reply(request)
    else:
        return previous_dialog_module.fallback(request)


DIALOGS = DIALOGS_dialogs|DIALOGS_standart
# DIALOGS = DIALOGS|DIALOGS_recording
