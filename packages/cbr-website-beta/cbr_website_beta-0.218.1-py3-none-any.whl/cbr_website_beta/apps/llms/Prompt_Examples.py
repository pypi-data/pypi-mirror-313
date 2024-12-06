class Prompt_Examples:

    def __init__(self):
        pass

    def athena(self):
        return  ['Hello, what do you know about me?'                       ,
                 'What questions should I ask my CISO?'                    ,
                 'What is DORA?'                                           ,
                 'What are my legal responsibilities?'                     ,
                 'What is the best way to learn more about cyber security?']

    def chat_with_llms(self):
        return ["Hi",
                "In two words, what is your name, and who created you?",
                "Hi, what is your model"                  ,
                "Who created you?"                        ,
                "Write 1 paragraph about cyber security"  ,
                "What do you know about this current conversation. "
                    "Please list the exact questions and answers from the history provided" ,
                ]
    def no_system_prompt(self):
        return ['Hi, what is your language model?',
                'In one word, what is your AI language model?',
                '2+2',
                '40+2']