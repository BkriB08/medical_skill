from lib_class_dialog import Request
from lib_class_dialog import GlobalDialog
import sys
import inspect
import texts




class say_remind_later_and_Goodbye(GlobalDialog):
    def reply(self, request: Request):
        #text = "Хорошо, я сейчас отключусь, но уточню, выпили ли Вы таблетки позже."
        #tts = "Хорошо, я сейчас отключусь, но уточню, выпили ли Вы таблетки позже."
        text, tts = texts.text_generation('отключусь, но уточню, выпили ли таблетки позже', f"Хорошо, я сейчас отключусь, но уточню, выпили ли Вы таблетки позже.")        
        return self.make_response(request, text, tts, end_session=True)      


class say_talk_later_and_Goodbye(GlobalDialog):
    def reply(self, request: Request):
        #text = "Хорошо, я вернусь к Вам позже."
        #tts = "Хорошо, я вернусь к Вам позже."
        text, tts = texts.text_generation('Хорошо, я вернусь к Вам позже', f"Хорошо, я вернусь к Вам позже.")        
        return self.make_response(request, text, tts, end_session=True)      


class say_dont_remind_and_Goodbye(GlobalDialog):
    def reply(self, request: Request):
        #text = "Хорошо, я больше не буду напоминать об этом лекарстве сегодня."
        #tts = "Хорошо, я больше не буду напоминать об этом лекарстве сегодня."
        text, tts = texts.text_generation('Больше не будем напоминать об этом лекарстве сегодня', f"Хорошо, я больше не буду напоминать об этом лекарстве сегодня.")        
        return self.make_response(request, text, tts, end_session=True)      

class say_dont_understand_and_Goodbye(GlobalDialog):
    def reply(self, request: Request):
        #text = "К сожалению, я не поняла Вас. Вернусь к Вам позже."
        #tts = "К сожалению, я не поняла Вас. Вернусь к Вам позже."
        text, tts = texts.text_generation('говорим, что не поняли и вернемся позже', f"К сожалению, я не поняла Вас. Вернусь к Вам позже.")        
        return self.make_response(request, text, tts, end_session=True)      

class say_dont_understand_and_repeat(GlobalDialog):
    def reply(self, request: Request):
        #text = "К сожалению, я не поняла Вас.  Повторите пожалуйста."
        #tts = "К сожалению, я не поняла Вас. Повторите пожалуйста."
        text, tts = texts.text_generation('говорим, что не поняли и просим повторить', f"К сожалению, я не поняла Вас. Повторите пожалуйста.")        
        return self.make_response(request, text, tts )



class Set_Mark_and_Goodbye(GlobalDialog):
    def reply(self, request: Request):

        unfinished_dialogue = request.get_unfinished_dialogue
        if len (unfinished_dialogue) == 0:
            #text = f"Хорошо, я отметила. Хорошего дня."
            #tts = f"Хорошо, я отметила. Хорошего дня."
            text, tts = texts.text_generation('одна фраза. говорим, что все отметили и прощаемся', f"Хорошо, я отметила. Хорошего дня.")        
        else:
            #text = f"{unfinished_dialogue} Ваши сегодняшние данные записала. Хорошего дня."
            #tts = f"{unfinished_dialogue} Ваши сегодняшние данные записала. Хорошего дня."
            text, tts = texts.text_generation('заканчиваем предыдущую фразу, затем говорим, что все отметили и прощаемся', f"Ваши сегодняшние данные записала. Хорошего дня.")        
            text = f"{unfinished_dialogue} {text}"
            tts = f"{unfinished_dialogue} {tts}"            
        return self.make_response(request, text, tts, end_session=True)      


class HaveMistake(GlobalDialog):
    def reply(self, request: Request):
        text = (
            "Прошу прощения, в навыке возникла непредвиденная ошибка.\n"
            "Мы её обязательно исправим. Возвращайтесь чуть позже."
        )
        tts = (
            "Прошу прощения, в навыке возникла непредвиденная ошибка. Мы её обязательно исправим. Возвращайтесь чуть позже."
        )        
        return self.make_response(request, text, tts, end_session=True)

class Registration_is_needed(GlobalDialog):
    def reply(self, request: Request):
        text = (
            "Для работы с навыком нужно авторизоваться в аккаунт яндекс. Как зарегистрируетесь, обязательно вернитесь к нам."
        )
        tts = (
            "Для работы с навыком нужно авторизоваться в аккаунт яндекс. Как зарегистрируетесь, обязательно вернитесь к нам."
        )        
        return self.make_response(request, text, tts, end_session=True)

class Goodbye(GlobalDialog):
    def reply(self, request: Request):
        #text, tts = texts.text_generation('Финальная фраза. Прощаемся', f"Я все отметила. До свидания.")
        #"Возвращайтесь в любое время. До свидания!", "Возвращайтесь в любое время. До свидания!"


        unfinished_dialogue = request.get_unfinished_dialogue
        if len (unfinished_dialogue) == 0:
            #text = f"Хорошо, я отметила. Хорошего дня."
            #tts = f"Хорошо, я отметила. Хорошего дня."
            text, tts = texts.text_generation('одна фраза. говорим, что все отметили и прощаемся', f"Хорошо, я отметила. Хорошего дня.")        
        else:
            #text = f"{unfinished_dialogue} Ваши сегодняшние данные записала. Хорошего дня."
            #tts = f"{unfinished_dialogue} Ваши сегодняшние данные записала. Хорошего дня."
            text, tts = texts.text_generation('заканчиваем предыдущую фразу, затем говорим, что все отметили и прощаемся', f"Ваши сегодняшние данные записала. Хорошего дня.")        
            text = f"{unfinished_dialogue} {text}"
            tts = f"{unfinished_dialogue} {tts}"    
        return self.make_response(request, text, tts, end_session=True)


class SorryAndGoodbye(GlobalDialog):
    def reply(self, request: Request):
        #text = (
        #    "Прошу прощения, я очень стараюсь вас понять.\n"
        #    "Но пока не получается. Вернусь к Вам позже.\n"
        #    "До свидания!"
        #)

        #tts = text
        text, tts = texts.text_generation('говорим, что не поняли и вернемся позже', f"К сожалению, я не поняла Вас. Вернусь к Вам позже.")        


        return self.make_response(request, text, tts, end_session=True)


class I_cant_do_that(GlobalDialog):
    def reply(self, request: Request):
        text, tts = texts.text_generation('говорим, не умеем это делать', f"К сожалению, еще этого не умею. Но я учусь.")        


        return self.make_response(request, text, tts, end_session=True)

class Exit(GlobalDialog):
    def reply(self, request: Request):
        text, tts = "", ""
        return self.make_response(request, text, tts, end_session=True)



#Возвращаем список всех созданных разработчиком диалогов (как объектов)
#получаем список всех загруженных модулей (файлов). Далее оставляем только те, которык являются наследниками класса Dialog_Base
#Соответственно возвращаем список с объектами - наследниками класса Dialog_Base
# 
def _list_dialogs():
    current_module = sys.modules[__name__] #
    # print (f'__name__ = {__name__}')
    dialogs = []
    for name, obj in inspect.getmembers(current_module): 
        if inspect.isclass(obj) and issubclass(obj, GlobalDialog):
            dialogs.append(obj)
    # print (f'dialogs = {dialogs}')
    return dialogs


DIALOGS = {dialog.id(): dialog for dialog in _list_dialogs()}
#конец
