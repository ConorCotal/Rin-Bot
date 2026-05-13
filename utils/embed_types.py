from enum import Enum

#############################################
# Generyczny Typ Embedu, 
# można go rozbudować o różne style, kolory, miniaturki itp. w zależności od potrzeb.
#############################################
class EmbedType(Enum):
    INFO = "info"
    TICKET = "ticket"
    EVENT = "event"
    HELP = "help"