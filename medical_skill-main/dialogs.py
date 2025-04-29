from lib_class_dialog import Request
import intents

import lib_standard_dialogs
import sys
import inspect
import texts
from lib_class_dialog import GlobalDialog
import lib_gpt

from diagnosis.disease_do import get_text_question
from diagnosis.disease_do import take_answer
from diagnosis.disease_do import calc_probability


class my_dialog1(GlobalDialog):
    
    def reply(self, request: Request):
        
        # генерация вопроса пользователю
        new_qwestion, _ = get_text_question(request)
        request.global_previous_phrase = new_qwestion
        
        if  new_qwestion == 'exit':
            request.global_finish_survey = True
            text = "К сожалению, такого симптома нет в мои базе данных."
            tts = text
        else:
            text, tts = new_qwestion, new_qwestion

        return self.make_response(
            request,
            text,
            tts,
            )
    def handle_local_intents(self, request: Request):
        
        # если раньше нам не задавали вопрос, то значит получили текстовый ввод первого симптома
        if len(request.global_now_quation) == 0:
            
            return my_dialog1()
        
        take_answer (request.command, request)
        
        if request.global_finish_survey:
            return my_dialog2()
        else:
            return my_dialog1()        

            


class  my_dialog2(GlobalDialog):
    
    def reply(self, request: Request):
        
        print(request.global_diseases_with_symptom)
        print('*****')
        print(request.global_true_symptoms)

        # получаем 3 наиболее вероятных заболеванияслабость
        top_three_diseases = calc_probability(request.global_diseases_with_symptom, request.global_true_symptoms)   

        # Выводим результаты
        strr = 'Наиболее вероятные диагнозы: '
        for disease in top_three_diseases:
            strr += f"{disease['name']} - вероятность {disease['probability']} процентов. "
        
        strr +=  ' На этом все. обращайтесь.'  
        print(strr)

        text, tts = strr, strr

        return self.make_response(
            request,
            text,
            tts,
            end_session = True,
            )
        
    def handle_local_intents(self, request: Request):
        
        if intents.CONFIRM in request.intents or intents.INT_ANSWER_YES in request.intents:
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
            return lib_standard_dialogs.Set_Mark_and_Goodbye()



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
