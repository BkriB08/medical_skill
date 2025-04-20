from lib_class_dialog import Request
import intents

import lib_standard_dialogs
import sys
import inspect
import texts
from lib_class_dialog import GlobalDialog
import lib_gpt



class my_dialog1(GlobalDialog):
    
    def reply(self, request: Request):
        
        text, tts = ('Что Вас беспокоит?', f"Что Вас беспокоит?")

        return self.make_response(
            request,
            text,
            tts,
            )
    def handle_local_intents(self, request: Request):
        
        if intents.CONFIRM in request.intents or intents.INT_ANSWER_YES in request.intents:
            print('сработал интент. Переходим к my_dialog2')
            return my_dialog2()
        
        #
        if intents.REJECT in request.intents or intents.INT_NO in request.intents:
            return my_dialog2()



            


#!перечисляем лекарства и каждое отмечаем, выпили или нет
class  my_dialog2(GlobalDialog):
    
    def reply(self, request: Request):
        

        text, tts = texts.text_generation('вопрос 2', f"Сейчас мы задали вопрос 2. Напиши вопрос для yandexGPT?")

        return self.make_response(
            request,
            text,
            tts,
            )
        
    def handle_local_intents(self, request: Request):
        
        if intents.CONFIRM in request.intents or intents.INT_ANSWER_YES in request.intents:
            print('сработал интент. дем на yandexGPT')
            return lib_standard_dialogs.say_dont_understand_and_Goodbye()
        
        #
        if intents.REJECT in request.intents or intents.INT_NO in request.intents:
            return lib_standard_dialogs.say_dont_understand_and_Goodbye()

        #
        if intents.INT_DO_LATER in request.intents: 
            return lib_standard_dialogs.say_dont_understand_and_Goodbye()

        #е
        if intents.INT_REMIND_LIST_MEDICINE in request.intents: 
            return lib_standard_dialogs.say_dont_understand_and_Goodbye()
        
        if len(request.command) > 0:
            return my_dialog3()


#!перечисляем лекарства и каждое отмечаем, выпили или нет
class  my_dialog3(GlobalDialog):
    
    def reply(self, request: Request):
        
        text = lib_gpt.get_question_from_yandexGPT(request.command)

        tts = text

        return self.make_response(
            request,
            text,
            tts,
            )
        
    def handle_local_intents(self, request: Request):
        
        if intents.CONFIRM in request.intents or intents.INT_ANSWER_YES in request.intents:
            print('сработал интент. прощаемся')
            return lib_standard_dialogs.say_dont_understand_and_Goodbye()
        
        #
        if intents.REJECT in request.intents or intents.INT_NO in request.intents:
            return lib_standard_dialogs.say_dont_understand_and_Goodbye()

        #
        if intents.INT_DO_LATER in request.intents: 
            return lib_standard_dialogs.say_dont_understand_and_Goodbye()

        #е
        if intents.INT_REMIND_LIST_MEDICINE in request.intents: 
            return lib_standard_dialogs.say_dont_understand_and_Goodbye()



#Возвращаем список всех созданных разработчиком диалогов (как объектов)
#получаем список всех загруженных модулей (файлов). Далее оставляем только те, которык являются наследниками класса Dialog_Base
#Соответственно возвращаем список с объектами - наследниками класса Dialog_Base
#Далее создаем словарь DIALOGS, состоящий из списка Dialog_Base, но добавленными ключами id мудуля
# 
def _list_dialogs():
    current_module = sys.modules[__name__] #
    #print (f'__name__ = {__name__}')
    dialogs = []
    for name, obj in inspect.getmembers(current_module): 
        if inspect.isclass(obj) and issubclass(obj, GlobalDialog):
            dialogs.append(obj)
    #print (f'dialogs = {dialogs}')
    return dialogs


DIALOGS = {dialog.id(): dialog for dialog in _list_dialogs()}
#конец


#!перечисляем лекарства и каждое отмечаем, выпили или нет
class main_branch(GlobalDialog):
    
    def reply(self, request: Request):

        #end_session = False
        text, tts = '',''
        

       
        list_of_drugs = request.get_list_of_medications


        #if request.repeat is None :
        #    #при первом запуске забираем данные из базы
        #    print(f"DEBAG reply.main_branch Формируем ответ для первого запуска функции")
        #    text = (f"Отлично! {request.name_user}, давайте вместе отметим, что вы сегодня выпили?\n")
        #    tts = (f"Отлично! {request.name_user}, давайте вместе отметим, что вы сегодня выпили?") 
             
        #else:
        #    list_of_drugs.pop(0) #так как запуск второй, то значит первую строчку мы обработали и удаляем ее
            #if intents.CONFIRM in request.intents:
            #    print ("ставим отметку в базе, что выпита")

        #print (f"DEBAG reply.main_branch получили список препаратов list_of_drugs = {list_of_drugs}")
        
        text += f"Вы выпили назначенный на {list_of_drugs[0].ReceptionTime} {list_of_drugs[0].medication} в дозировке {list_of_drugs[0].dosage}?"
        tts += f"Вы выпили назначенный на {list_of_drugs[0].ReceptionTime} {list_of_drugs[0].medication}  в дозировке {list_of_drugs[0].dosage}?"

        unfinished_dialogue = request.get_unfinished_dialogue
        textName = request.name_user +',' if not request.get_do_conditions else ''

        text = f'{unfinished_dialogue} {textName} {text}\n'
        tts = f'{unfinished_dialogue} {textName} {tts}'
        
        #if len(list_of_drugs) > 0 :
        #    text += f"Вы выпили назначенный на {list_of_drugs[0].ReceptionTime} {list_of_drugs[0].medication} в дозировке {list_of_drugs[0].dosage}?"
        #    tts += f"Вы выпили назначенный на {list_of_drugs[0].ReceptionTime} {list_of_drugs[0].medication}  в дозировке {list_of_drugs[0].dosage}?"
        #else:
        #    text = f"Больше нет назначенных лекарств, которые нужно выпить на текущий момент."
        #    tts = f"Больше нет назначенных лекарств, которые нужно выпить на текущий момент."
            #end_session = True

        #user_state_medicines = [x.dump() for x in list_of_drugs]
        
        request.do_conditions = True #отмечаем, что по крайней мере одно состояние мы опросили. нужно, чтобы попращаться
 
        print (f"DEBAG reply.main_branch сформироавли текстовый список препаратов text_line = {text}")    

        return self.make_response(
            request,
            text,
            tts,
            states={REPEAT: True},
            #user_state={MEDICINES: user_state_medicines},
            #end_session = end_session
        )

    def handle_local_intents(self, request: Request):
        
        
        if len(request.get_list_of_medications) > 0 and intents.CONFIRM in request.intents:
            #print ("DEBAG handle_local_intents.main_branch ставим отметку в базе, что выпита")

            lib_requests_ydb_medicine.put_mark_on_medicine(request, request.get_list_of_medications[0].ids)
            request.list_of_medications.pop(0) #первую строчку мы обработали и удаляем ее 
            
            if len(request.get_list_of_medications) == 0:
                request.unfinished_dialogue, _ = texts.text_generation('Ветка опроса выпитых таблеток. Сообщаем, что больше нет назначенных лекарств', f"Больше нет назначенных лекарств, которые нужно выпить на текущий момент.")

            #print ("DEBAG handle_local_intents.main_branch отработал запрос к базе данных, что выпита")
            return main_branch() if len(request.get_list_of_medications) > 0 else request.Global_DIALOGS.get(request.get_next_dialogue_line)()
        
        elif len(request.get_list_of_medications) > 0 and intents.REJECT in request.intents:
            return medicine_isnot_drunk()
        
        elif len(request.get_list_of_medications) == 0:
            return request.Global_DIALOGS.get(request.get_next_dialogue_line)() #return DEFAULT_DIALOG_CONDITION()#lib_standard_dialogs.Goodbye()
#        return main_branch()
