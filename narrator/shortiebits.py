from plots import Plot,PlotError,PlotState,Chapter
import context
import items
import maps
import randmaps
import waypoints
import monsters
import dialogue
import services
import teams
import characters
import namegen
import random
import container

# Shortie Done-in-one Dungeon Monkey Adventure
# - A small adventure, typically consisting of a single dungeon or wilderness
#   area.
# - Despite the limited area, see how interesting you can make it.
# - This will be dynamically loaded into an existing campaign.

class ShortieStub( Plot ):
    LABEL = "SHORTIE"

    # This plot gets placed in the global scripts and sets itself as the
    # "world" of its chapter. This means that all scenes generated by subplots
    # should be stored inside the plot itself, making cleanup easy. I hope.
    scope = True
    active = True

    SHORTIE_GRAMMAR = {
        # [ADVENTURE] is the top level token- it will expand into a number of
        # high level tokens.
        "[ADVENTURE]": [ "[IMPERILED_PLACE] [ENEMY_BASE] [ENEMY_GOAL]",
            ],

        "[ENEMY_BASE]": [ "SDI_ENEMY_FORT SDI_ENEMY_BARRACKS SDI_BLOCKED_GATE",
            "SDI_HIDDEN_BASE SDI_WILD_DUNGEON SDI_ENEMY_BARRACKS"
            ],

        "[ENEMY_GOAL]": [ "SDI_SUPERWEAPON",
            "SDI_BOSSFIGHT"
            ],

        "[IMPERILED_PLACE]": [ "SDI_AMBUSH SDI_VILLAGE",
            "SDI_OUTPOST SDI_RECON", "SDI_VILLAGE SDI_RECON"
            ],
        "[TEST]": [ "SDI_TESTCOMBAT",
            ],
    }
    def custom_init( self, nart ):
        """Create the world + chapter."""
        self.chapter = Chapter( start_rank=nart.start_rank, end_rank=nart.end_rank, world=self )
        self.chapter.root = self
        self.contents = container.ContainerList(owner=self)
        self.rank = nart.start_rank
        if not self.setting:
            self.setting = context.SET_RENFAN

        # Generate a plot outline for the adventure. We will do this using a
        # context free grammar expansion of the token [ADVENTURE]. The resultant
        # string will be a list of subplot request labels.
        subplot_list = self.register_element( "shortie_outline", list( dialogue.grammar.convert_tokens( "[TEST]", self.SHORTIE_GRAMMAR ).split() ) )
        print subplot_list

        # Assemble the outline into an adventure. Basically, add a subplot of
        # each generated type, in order. Each subplot describes a stage of the
        # mini adventure- usually a single scene, maybe also several scenes or
        # part of a scene, whatever.
        prev_subplot = self
        genplots = list()
        for spr in subplot_list:
            prev_subplot = self.add_sub_plot( nart, spr,
                PlotState().based_on(prev_subplot) )
            genplots.append( prev_subplot )

        # Set the adventure entrance to the IN_SCENE of the first generated
        # subplot.
        self._adventure_entrance = (genplots[0].elements.get( "IN_SCENE" ),genplots[0].elements.get( "IN_ENTRANCE" ))

        return True

    def begin_adventure( self, camp, exit_destination, exit_entrance ):
        # Unpack the adventure entrance stored during generation.
        camp.destination,camp.entrance = self._adventure_entrance
        self._adventure_exit = (exit_destination, exit_entrance)

    def end_adventure( self, camp ):
        # Remove this adventure from campaign, move PCs to original place.
        camp.destination,camp.entrance = self._adventure_exit
        camp.scripts.remove( self )
        self.remove()

# Each shortie component should include an "IN_SCENE" and "IN_ENTRANCE" for use
# if it is the first component generated. It may also contain an "OUT_SCENE" and
# "OUT_ENTRANCE" which, if present, will be the connection to the next
# component.

class ShortCombatTest( Plot ):
    LABEL = "SDI_TESTCOMBAT"
    active = True
    scope = True
    def custom_init( self, nart ):
        # Create the scene where the ambush will happen- a wilderness area with
        # a road.
        myscene = maps.Scene( 50, 50, 
            sprites={maps.SPRITE_WALL: "terrain_wall_woodfort.png", maps.SPRITE_GROUND: "terrain_ground_forest.png",
             maps.SPRITE_FLOOR: "terrain_floor_gravel.png" },
            biome=context.HAB_FOREST, setting=self.setting, fac=self.elements.get("ANTAGONIST"),
            desctags=(context.MAP_WILDERNESS,) )
        mymapgen = randmaps.ForestScene( myscene )
        self.register_scene( nart, myscene, mymapgen, ident="LOCALE" )

        # Create the ambush room in the middle- this is where the IN_ENTRANCE
        # will go.
        myroom = randmaps.rooms.FuzzyRoom( parent=myscene )
        myent = waypoints.Well()
        myroom.contents.append( myent )

        for t in range( random.randint(1,3) ):
            self.add_sub_plot( nart, "ENCOUNTER" )

        room = mymapgen.DEFAULT_ROOM()
        self.register_element( "_ROOM", room, dident="LOCALE" )
        signpost = waypoints.Signpost()
        self.register_element( "_SIGN", signpost, dident="_ROOM" )
        signpost.plot_locked = True
        signpost.mini_map_label = "Signpost"

        self.do_message = False

        # Save this component's data for the next component.
        self.register_element( "IN_SCENE", myscene )
        self.register_element( "IN_ENTRANCE", myent )
        self.register_element( "OUT_SCENE", myscene )
        self.register_element( "OUT_ENTRANCE", signpost )

        return True
    def _SIGN_menu( self, thingmenu ):
        thingmenu.desc = "This appears to be the way out."
        thingmenu.add_item( "Leave this adventure.", self.use_sign )
    def use_sign( self, explo ):
        self.do_message = True
        self.chapter.root.end_adventure( explo.camp )
    def t_START( self, explo ):
        if self.do_message:
            explo.alert( "This subplot remains." )


#  SDI_ENEMY_FORT

# SDI_ENEMY_BARRACKS

# SDI_BLOCKED_GATE

# SDI_HIDDEN_BASE

# SDI_WILD_DUNGEON

# SDI_SUPERWEAPON

# SDI_BOSSFIGHT


# SDI_AMBUSH
# The party has been ambushed! Oh noes!

class BasicAmbush( Plot ):
    LABEL = "SDI_AMBUSH"
    def custom_init( self, nart ):
        # Create the scene where the ambush will happen- a wilderness area with
        # a road.
        myscene = maps.Scene( 50, 50, 
            sprites={maps.SPRITE_WALL: "terrain_wall_woodfort.png", maps.SPRITE_GROUND: "terrain_ground_forest.png",
             maps.SPRITE_FLOOR: "terrain_floor_gravel.png" },
            biome=context.HAB_FOREST, setting=self.setting, fac=self.elements.get("ANTAGONIST"),
            desctags=(context.MAP_WILDERNESS,) )
        mymapgen = randmaps.ForestScene( myscene )
        self.register_scene( nart, myscene, mymapgen, ident="LOCALE" )

        # Create the ambush room in the middle- this is where the IN_ENTRANCE
        # will go.
        myroom = randmaps.rooms.FuzzyRoom( parent=myscene )
        myent = waypoints.Well()
        myroom.contents.append( myent )


        # If we have been provided with an OUT_ENTRANCE, link back to that from
        # the beginning of the road. Otherwise, this is a one way trip.
        if self.elements.get( "OUT_SCENE", None ):
            # This isn't the first component in the adventure.
            oe = self.elements.get( "OUT_ENTRANCE", None )
            if oe:
                # Create a two-way gate to here.
                pass
            else:
                # Create one-way passage to here.
                pass

        # Save this component's data for the next component.
        self.register_element( "IN_SCENE", myscene )
        self.register_element( "IN_ENTRANCE", myent )
        self.register_element( "OUT_SCENE", myscene )
        self.register_element( "OUT_ENTRANCE", None )

        return True


# SDI_VILLAGE

# SDI_OUTPOST

# SDI_RECON

