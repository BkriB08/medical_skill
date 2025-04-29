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



            

