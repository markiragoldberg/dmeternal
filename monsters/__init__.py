import inspect
import base
import characters
import random
import chargen
import namegen
from dialogue import voice

import goblins

# Compile the monsters into a useful list.
MONSTER_LIST = []
def harvest( mod ):
    for name in dir( mod ):
        o = getattr( mod, name )
        if inspect.isclass( o ) and issubclass( o , base.Monster ) and o is not base.Monster:
            MONSTER_LIST.append( o )

harvest( goblins )

VOICE_TO_NAMEGEN = { voice.ORCISH: namegen.ORC, voice.ELVEN: namegen.ELF, \
    voice.DRACONIAN: namegen.DRAGON, voice.DWARVEN: namegen.DWARF, \
    voice.GREEK: namegen.GREEK, voice.KITTEH: namegen.JAPANESE, \
    voice.GNOMIC: namegen.GNOME, voice.HURTHISH: namegen.HURTHLING }

def generate_npc( species=None, job=None, gender=None, rank=None, team=None ):
    if not species:
        species = random.choice( characters.PC_SPECIES )
    if not job:
        job = random.choice( characters.PC_CLASSES )
    if not gender:
        gender = random.randint(0,1)
    if not rank:
        rank = random.randint(1,10)

    npc = characters.Character( species=species(), gender=gender )
    npc.roll_stats()
    npc.team = team

    ji = job( rank=rank, pc=npc )
    npc.levels.append( ji )
    chargen.give_starting_equipment( npc )

    # Generate a random name. This is gonna depend on the voice.
    myvoice = npc.get_voice()
    ng = namegen.DEFAULT
    for lang in myvoice:
        if lang in VOICE_TO_NAMEGEN:
            ng = VOICE_TO_NAMEGEN[ lang ]
            break
    npc.name = ng.gen_word()

    return npc

