# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import ask_sdk_core.utils as ask_utils
from airtable import Airtable
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

rhyme_list=['6:Twinkle Twinkle','4:Humpty Dumpty','8:Black Sheep','8:Little Teapot','5:Diddle Diddle','8:Incy Wincy Spider',
            '8:Jack and Jill','8:Teddy Bear','4:ringa ringa','4:Dear Mother','4:Purple Cow','9:Easter','4:Papermint','7:Hot cross',
            '4:Christmas','5:Old Man','6:Old Mother','7:Zoo','8:Diamonds','4:Little Girl','9:Zoom Zoom Rhyme',
            '6:Chubby Cheeks','8:The Lion And The Unicorn','9:Clap Your Hands','8:Once I Caught A Fish Alive','5:Buckle My Shoe',
            '8:Ding Dong','8:Tommy Tucker','4:Star Light Star Bright','8:Tisket Tasket','4:Wise Old Owl','7:A Rose','8:Action',
            '4:After a Bath','5:All the little fishes','6:An Elephant','4:Are You Sleeping','4:Birds','8:Paper','8:Animal Sounds',
            '6:Butterfly','8:Johny','6:I Am Big Tree','5:Hickory Dickory','4:Good Morning','4:Good Afternoon','4:Evening Red',
            '8:Early To Bed and Early To Rise','8:Donkey','6:Charley']

base_id="app4JiFLLGALPPHpw"
api_key="key7pHwzc2vK0fSEz"

audio_base_id="appDUsXlQ4T6DH3IA"
audio_table_name="audio files"
audio_api_key="key7pHwzc2vK0fSEz"
audio_table = Airtable(audio_base_id, audio_table_name, audio_api_key)

search_record_start=audio_table.match('Name','start')
Audiofile_start=search_record_start['fields']['Attachments']

search_record_end=audio_table.match('Name','end')
Audiofile_end=search_record_end['fields']['Attachments']

search_record_wrong=audio_table.match('Name','wrong')
Audiofile_wrong=search_record_wrong['fields']['Attachments']

class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Welcome to Rhyme Tunes zone ! Here you can develope your  language , early literacy and reading skills ! So let's jump to your favorite rhyme. <audio src=\'"+str(Audiofile_start[0]['url'])+"\' />"+"Which rhyme do you want to play? For example you can choose twinkle twinkle or Humpty Dumpty and many more rhymes!For rules say help"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

num=0
lines=0
lyrics_table=None
class rhymeintentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("rhymeintent")(handler_input)

    def handle(self, handler_input):
        global num
        global lyrics_table
        global lines
        
        users_choice = handler_input.request_envelope.request.intent.slots["rhyme_name"].resolutions.resolutions_per_authority[0].values[0].value.name
        
        for name in rhyme_list:
            if users_choice.upper().strip()==(name[2:].upper().strip()):
                table_name=name[2:]
                lyrics_table = Airtable(base_id,table_name,api_key)
                num=1
                lines=int(name[0])
                search_record=lyrics_table.match('Name',num)
                air_ly=search_record['fields']['Lyrics']
                speak_output= str(air_ly) + "! Ok Now its your turn complete the rhyme."
                num=num+1
                break
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class lyricsintentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("lyricsintent")(handler_input)

    def handle(self, handler_input):
        global num
        global lyrics_table
        global lines
        
        users_choice = handler_input.request_envelope.request.intent.slots["rhyme_lyrics"].resolutions.resolutions_per_authority[0].values[0].value.name
        
        search_record=lyrics_table.match('Name',num)
        air_ly=search_record['fields']['Lyrics']
        
        if users_choice.upper() == str(air_ly).upper().strip():
            num=num+1
            search_record1=lyrics_table.match('Name',num)
            air_ly1=search_record1['fields']['Lyrics']
            speak_output=str(air_ly1) +"! continue the rhyme."
            
        elif users_choice.lower().strip() =="i dont know":
            search_record1=lyrics_table.match('Name',num)
            air_ly1=search_record1['fields']['Lyrics']
            speak_output="ok, next line is "+str(air_ly1) +"!continue the rhyme."
            
        else:
            speak_output="Wrong answer <audio src=\'"+str(Audiofile_wrong[0]['url'])+"\' /> Correct answer: " + str(air_ly)+"continue the rhyme"#+"!Well tryed !Start again by saying play twinkle twinkle or start twinkle twinkle! by this utterance you can also go with other rhymes too! or if you want to quit say goodbye! "
        
            
        if num>=lines:
            if speak_output=='rhyme ended':
                speak_output="<audio src=\'"+str(Audiofile_end[0]['url'])+"\' /> " + speak_output
            else:
                speak_output=speak_output + " <audio src=\'"+str(Audiofile_end[0]['url'])+"\' /> rhyme ended! Want to try another rhyme? Just say your favorite rhyme name or if you want quit say goodbye!"
                
        num=num+1
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Here are the rules for rhyme tunes! 1. First you have to choose your favorite rhyme! 2. Alexa will start with the rhyme that you have been choosen by giving the First sentence! next you have to complete it! 3. If you don't know the next line you can say I don't know! then alexa will give you the answer! Hope you understood the game! if you want me to repeat the rules again say help! You can now say your favorite rhyme!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Goodbye!Hope you enjoyed it"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class FallbackIntentHandler(AbstractRequestHandler):
    """Single handler for Fallback Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")
        speech = "Hmm, I'm not sure. You can say play  Twinkle Twinkle or start Twinkle Twinkle by this utterance you can also go with other rhymes too. What would you like to do?"
        reprompt = "I didn't catch that. What can I help you with?"

        return handler_input.response_builder.speak(speech).ask(reprompt).response

class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(lyricsintentHandler())
sb.add_request_handler(rhymeintentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()