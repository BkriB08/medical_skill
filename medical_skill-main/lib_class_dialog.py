import logging
import sys
import inspect
from abc import ABC, abstractmethod
from typing import Optional
import intents
logging.getLogger().setLevel(logging.DEBUG)

#константы 
STATE_RESPONSE_KEY = "session_state"
USER_STATE_RESPONSE_KEY = "user_state_update"
USERSTATE_RESPONSE_KEY = "user_state_update"
STATE_REQUEST_KEY = "session"

# Последние фразы пользователя
PREVIOUS_MOVES = "prev_moves"

# признак уточнения после того, как не смогли разобрать фразу.
# Если снова не разобрали - выходим
NEED_FALLBACK = "fallback"

# Эти состояния будут сохранены в fallback
MUST_BE_SAVE = {}

#признак повторного вызова
REPEAT = "repeatbool" 


#запоминаемые значения
REQ_VAL1 = "val1"
REQ_VAL2 = "val2"
REQ_VAL_global_true_symptoms = 'global_true_symptoms'
REQ_VAL_global_question_list = 'global_question_list'
REQ_VAL_global_symptom_key_list = 'global_symptom_key_list'
REQ_VAL_global_now_quation = 'global_now_quation'
REQ_VAL_global_diseases_with_symptom = 'global_diseases_with_symptom'
REQ_VAL_global_previous_phrase = 'global_previous_phrase'
REQ_VAL_global_finish_survey = 'global_finish_survey'

# Когда последний раз проверяли валидность токена
LAST_CHECK = "last_check"
PERMANENT_VALUES = {LAST_CHECK}

class Request:
    def __init__(self, request_body: dict):
        self.request_body = request_body

        
        logging.debug (f'Запустили создание класса Request.')        
        self.val1 = self.request_body.get("state", {}).get("session", {}).get(REQ_VAL1, None) #
        self.val2 = self.request_body.get("state", {}).get("session", {}).get(REQ_VAL2, None) #
        self.global_true_symptoms = self.request_body.get("state", {}).get("session", {}).get(REQ_VAL_global_true_symptoms, [])
        self.global_question_list = self.request_body.get("state", {}).get("session", {}).get(REQ_VAL_global_question_list, [])
        self.global_symptom_key_list = self.request_body.get("state", {}).get("session", {}).get(REQ_VAL_global_symptom_key_list, [])
        self.global_now_quation = self.request_body.get("state", {}).get("session", {}).get(REQ_VAL_global_now_quation, {})
        self.global_diseases_with_symptom = self.request_body.get("state", {}).get("session", {}).get(REQ_VAL_global_diseases_with_symptom, [])
        self.global_previous_phrase = self.request_body.get("state", {}).get("session", {}).get(REQ_VAL_global_previous_phrase, '')
        self.global_finish_survey = self.request_body.get("state", {}).get("session", {}).get(REQ_VAL_global_finish_survey, False)


        #список функций диалоговых веток
        self.Global_DIALOGS = []
        

         
    def __getitem__(self, key):
        return self.request_body[key]
    
     #!!!   
    @property
    def command(self):
        return self.request_body.get("request", {}).get("original_utterance", "")
   
    @property
    def command_shortly(self):
        return self.request_body.get("request", {}).get("command", "")
    
    @property
    def tokens(self):
        return self.request_body.get("request", {}).get("nlu", {}).get("tokens", [])

    @property
    def intents(self):
        return self.request_body.get("request", {}).get("nlu", {}).get("intents", {})

    @property
    def entities_list(self):
        return [
            entity["type"]
            for entity in self.request_body.get("request", {})
            .get("nlu", {})
            .get("entities", [])
        ]

    @property
    def type(self):
        return self.request_body.get("request", {}).get("type")

    @property
    def session(self) -> dict:
        return self.request_body.get("state", {}).get("session", {})

    @property
    def user(self):
        return self.request_body.get("state", {}).get("user", {})

    @property
    def application(self):
        return self.request_body.get("state", {}).get("application", {})

    @property
    def access_token(self):
        return (
            self.request_body.get("session", {})
            .get("user", {})
            .get("access_token", None)
        )

    @property
    def id_dialog(self):
        print (f'получили из запроса IDтекущего диалога =  {self.request_body.get("state", {}).get("session", {}).get("dialog")}')
        return self.request_body.get("state", {}).get("session", {}).get("dialog")

    @property
    def repeat(self):
        #print (f"признак повторного вызова  repeat = {self.request_body.get('session', {}).get('REPEAT', {})}")
        return self.request_body.get('session', {}).get('REPEAT', {}) if not self.request_body.get('session', {}).get('REPEAT', {}) is None else False 

    @property
    def authorization_complete(self):
        return self.request_body.get("account_linking_complete_event") is not None

    def slots(self, intent: str):
        return (
            self.request_body.get("request", {})
            .get("nlu", {})
            .get("intents", {})
            .get(intent, {})
            .get("slots", {})
            .keys()
        )

    def slot(self, intent: str, slot: str):
        return (
            self.request_body.get("request", {})
            .get("nlu", {})
            .get("intents", {})[intent]
            .get("slots", {})
            .get(slot, {})
            .get("value", None)
        )

    def entity(self, entity_type: str):
        return [
            entity["value"]
            for entity in self.request_body.get("request", {})
            .get("nlu", {})
            .get("entities", [])
            if entity["type"] == entity_type
        ]

    
    @property #получение значения переменной из запроса
    def timezone(self):
        return self.request_body.get('meta', {}).get('timezone','Asia/Novokuznetsk' )
    
    
class Dialog_Base(ABC):

    temp_context = dict()

        
    @classmethod
    def id(cls):
        return cls.__name__

    """Генерация ответа диалога"""

    @abstractmethod
    def reply(self, request):
        #функция ничего не делает. Будет переопределена 
        raise NotImplementedError() 

    """Проверка перехода к новому диалогу"""

    def move(self, request: Request):
        next_dialog = self.handle_local_intents(request)
        if next_dialog is None:
            next_dialog = self.handle_global_intents(request)
        return next_dialog

    @abstractmethod
    def handle_global_intents(self, request):
        raise NotImplementedError()

    @abstractmethod
    def handle_local_intents(self, request: Request) -> Optional[str]:
        raise NotImplementedError()

    @abstractmethod
    def fallback(self, request: Request):
        raise NotImplementedError()

    def make_response(
        self,
        request: Request,
        text,
        tts,
        states=None,
        user_state=None,
        directives=None,
        end_session=False,
        ):
        response = {
            "text": text[:1024],
            "tts": tts[:1024] ,
            
        }
        if directives is not None:
            response["directives"] = directives
        if end_session:
            response["end_session"] = end_session


        webhook_response = {
            "response": response,
            "version": "1.0",
            STATE_RESPONSE_KEY: {
                "dialog": self.id(),
                
                REQ_VAL1: request.val1, # 
                REQ_VAL2: request.val2, # 
                REQ_VAL_global_true_symptoms:       request.global_true_symptoms,
                REQ_VAL_global_question_list:       request.global_question_list,
                REQ_VAL_global_symptom_key_list:    request.global_symptom_key_list,
                REQ_VAL_global_now_quation:         request.global_now_quation,
                REQ_VAL_global_diseases_with_symptom: request.global_diseases_with_symptom,
                REQ_VAL_global_previous_phrase:     request.global_previous_phrase,
                REQ_VAL_global_finish_survey:       request.global_finish_survey,            
            },
        }

        # если передаем пустое множество, то очищаем все ключи
        if states == {}:
            webhook_response[STATE_RESPONSE_KEY] = {}
        else:
            #переносим предыдущие ключи в новый запрос
            for key, value in request.session.items():
                if key in PERMANENT_VALUES:
                    webhook_response[STATE_RESPONSE_KEY][key] = value
            
            # если переданы новые ключи или значения, обновляем или добовляем        
            if states is not None:
                webhook_response[STATE_RESPONSE_KEY].update(
                    (k, v) for k, v in states.items() if v is not None
                )
        if user_state is not None:
            webhook_response[USERSTATE_RESPONSE_KEY] = user_state

        prev_moves = request.session.get(PREVIOUS_MOVES, [])
        prev_moves.append(request.command)

        webhook_response[STATE_RESPONSE_KEY][PREVIOUS_MOVES] = prev_moves[-10:]



        return webhook_response



class GlobalDialog(Dialog_Base):
    
    def reply(self, request: Request):
        pass  # Здесь не нужно пока ничего делать

    def handle_global_intents(self, request):
        # Глобальные команды, обрабатываются в первую очередь

        if intents.HELP in request.intents:
            return Help_Diag()


        '''
        # Глобальные команды, обрабатываются в первую очередь
        if intents.HELP in request.intents:
            return HelpMenu()

        # Глобальные команды
        if intents.MAIN_MENU in request.intents:
            return Todo()
        '''


    def handle_local_intents(self, request: Request):
        pass  # Здесь не нужно пока ничего делать

    def fallback(self, request: Request):
        if request.session.get(NEED_FALLBACK, False):
            text =  "Прошу прощения, я очень стараюсь вас понять.\n Но пока не получается. Возможно, мне стоит отдохнуть. Возвращайтесь позже. До свидания!"
            tts = "Прошу прощения, я очень стараюсь вас понять.\n Но пока не получается. Возможно, мне стоит отдохнуть. Возвращайтесь позже. До свидания!"

            return self.make_response(request, text, tts, end_session=True)
        else:
            save_state = {}
            # Сохраним текущее состояние
            for save in MUST_BE_SAVE:
                if save in request.session:
                    save_state.update({save: request.session[save]})
            save_state[NEED_FALLBACK] = True
            text = f"Извините, я вас не поняла. Пожалуйста, повторите.\n "
            tts =  f"Извините, я вас не поняла. Пожалуйста, повторите."
    
            return self.make_response(
                request,
                text,
                tts,
                states=save_state,
            )
 
 
    def repeat_dialog(self, request: Request, text='', tts=''):

        save_state = {}
        # Сохраним текущее состояние
        for save in MUST_BE_SAVE:
            if save in request.session:
                save_state.update({save: request.session[save]})
        
        text = f"Извините, я вас не поняла. Пожалуйста, повторите.\n "
        tts =  f"Извините, я вас не поняла. Пожалуйста, повторите."

        return self.make_response(
            request,
            text,
            tts,
            states=save_state,
        )


class Exit_Diag(GlobalDialog):
    def reply(self, request: Request):
        text, tts = "Готово, проверяйте", "Готово, проверяйте"
        return self.make_response(request, text, tts, end_session=True)
               
        

class Help_Diag(GlobalDialog):
    def reply(self, request: Request):
        text = (
            "Этот навык предназначен для помощи пациентам и людям после операции в соблюдении рекомендаций врача, а так же в удаленном мониторинге состояния пациента.\n"
            "Для получения доступа к навыку и приложению врача необходимо связаться с представителем НИИ КПССЗ по телефону 8-906-936-1020.\n"
            "Спасибо!"
        )

        tts = text
        return self.make_response(request, text, tts)
    

 
def _list_dialogs():
    current_module = sys.modules[__name__] #
    #print (f'__name__ = {__name__}')
    dialogs = []
    for name, obj in inspect.getmembers(current_module): 
        if inspect.isclass(obj) and issubclass(obj, Dialog_Base):
            dialogs.append(obj)
    #print (f'dialogs = {dialogs}')
    return dialogs


DIALOGS = {dialog.id(): dialog for dialog in _list_dialogs()}
#конец


