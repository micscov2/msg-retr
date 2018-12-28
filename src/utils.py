import sys

switcher = {
                   "JOIN" : 0,
                    "MSG" : 2,
                "PRIVMSG" : 3,
               "REGISTER" : 4,
              "BROADCAST" : 1
          }

def get_code_from_str(str_msg):

    return switcher[str_msg]
