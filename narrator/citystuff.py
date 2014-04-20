
from plots import Plot,PlotError,PlotState
import context
import items
import maps
import mapgen
import waypoints
import monsters
import dialogue
import services
import teams
import characters
import random
import worlds

#
#   **********************
#   ***   CITY_SCENE   ***
#   **********************
#
#  Create a new scene with a city in it. Register the following elements:
#   LOCALE: The new scene
#   CITY: The map feature containing the city
#   ENTRANCE: A waypoint for starting in/teleporting into the city
#
#  The city and map need to be populated, as well.
#

class CityOnEdgeOfCiv( Plot ):
    LABEL = "CITY_SCENE"
    def custom_init( self, nart ):
        """Create map, fill with city + services."""
        myscene = maps.Scene( 129, 129, sprites={maps.SPRITE_GROUND: "terrain_ground_forest.png", maps.SPRITE_WALL: "terrain_wall_lightbrick.png"},
            biome=context.HAB_FOREST, setting=self.setting,
            desctags=(context.MAP_WILDERNESS,context.DES_CIVILIZED,) )
        mymapgen = mapgen.EdgeOfCivilization( myscene )
        self.register_scene( nart, myscene, mymapgen, ident="LOCALE" )

        castle = self.register_element( "CITY", mapgen.CastleRoom( width=35,height=35,tags=(context.CIVILIZED,context.ROOM_PUBLIC), parent=myscene ) )
        myroom = mapgen.FuzzyRoom( tags=(context.ENTRANCE,), parent=castle )
        myteam = teams.Team( strength=0, default_reaction=characters.SAFELY_FRIENDLY)
        castle.contents.append( myteam )
        myent = waypoints.Well()
        myroom.contents.append( myent )
        myroom.contents.append( monsters.generate_npc(team=myteam) )
        myroom.contents.append( monsters.generate_npc(team=myteam) )

        self.register_element( "ENTRANCE", myent )

        self.chapter.world.add_entrance( myscene, myscene.name, worlds.W_CITY, myent, True )

        self.add_sub_plot( nart, "CITY_GENERALSTORE" )
        self.add_sub_plot( nart, "CITY_WEAPONSHOP" )
        self.add_sub_plot( nart, "CITY_LIBRARY" )
        self.add_sub_plot( nart, "CITY_INN" )
        self.add_sub_plot( nart, "CITY_TEMPLE" )
        for t in range( random.randint(1,4) ):
            self.add_sub_plot( nart, "ENCOUNTER" )

        return True






#  *****************************
#  ***   CITY_GENERALSTORE   ***
#  *****************************

class GenerallyGeneralStore( Plot ):
    LABEL = "CITY_GENERALSTORE"
    active = True
    scope = "BUILDING_INT"
    NAME_PATTERNS = ( "{0}'s Shop", "{0}'s Goods" )
    def custom_init( self, nart ):
        exterior = mapgen.BuildingRoom( tags=(context.CIVILIZED,) )
        exterior.special_c[ "window" ] = maps.SMALL_WINDOW
        exterior.special_c[ "sign1" ] = maps.SWORD_SIGN
        exterior.special_c[ "sign2" ] = maps.SHIELD_SIGN
        self.register_element( "_EXTERIOR", exterior, dident="CITY" )
        interior = maps.Scene( 50,50, sprites={maps.SPRITE_FLOOR: "terrain_floor_wood.png" },
            biome=context.HAB_BUILDING, setting=self.setting, desctags=(context.DES_CIVILIZED,) )
        igen = mapgen.BuildingScene( interior )
        gate_1 = waypoints.GateDoor()
        gate_2 = waypoints.GateDoor()
        gate_1.destination = interior
        gate_1.otherside = gate_2
        gate_2.destination = self.elements.get( "LOCALE" )
        gate_2.otherside = gate_1
        self.register_scene( nart, interior, igen, ident="BUILDING_INT", dident="LOCALE" )
        exterior.special_c[ "door" ] = gate_1
        int_mainroom = mapgen.SharpRoom( tags=(context.CIVILIZED,context.ROOM_PUBLIC), anchor=mapgen.south, parent=interior )
        int_mainroom.contents.append( gate_2 )
        int_mainroom.contents.append( maps.PILED_GOODS )
        int_mainroom.contents.append( maps.PILED_GOODS )
        gate_2.anchor = mapgen.south
        int_mainroom.decorate = mapgen.GeneralStoreDec()
        npc = monsters.generate_npc( job=monsters.base.Merchant )
        interior.name = random.choice( self.NAME_PATTERNS ).format( npc )
        gate_1.mini_map_label = "General Store"
        int_mainroom.contents.append( npc )
        self.register_element( "SHOPKEEPER", npc )
        self.shop = services.Shop( rank=self.rank+2 )
        self.add_sub_plot( nart, "SIDE_STORY", PlotState(rank=self.random_rank_in_chapter()).based_on( self ) )
        return True

    def SHOPKEEPER_offers( self, explo ):
        # Return list of shopkeeper offers.
        ol = list()
        ol.append( dialogue.Offer( "" ,
         context = context.ContextTag([context.SHOP,context.GENERALSTORE]), effect=self.shop ) )
        return ol

#  ********************
#  ***   CITY_INN   ***
#  ********************

class GenericInn( Plot ):
    LABEL = "CITY_INN"
    active = True
    scope = "BUILDING_INT"
    NAME_PATTERNS = ( "{0}'s Inn", "The {1} and {2}" )
    def custom_init( self, nart ):
        exterior = mapgen.BuildingRoom( tags=(context.CIVILIZED,) )
        exterior.special_c[ "window" ] = maps.SMALL_WINDOW
        exterior.special_c[ "sign1" ] = maps.DRINK_SIGN
        self.register_element( "_EXTERIOR", exterior, dident="CITY" )

        interior = maps.Scene( 50,50, sprites={maps.SPRITE_FLOOR: "terrain_floor_wood.png" },
            biome=context.HAB_BUILDING, setting=self.setting, desctags=(context.DES_CIVILIZED,) )
        igen = mapgen.BuildingScene( interior )

        gate_1 = waypoints.GateDoor()
        gate_2 = waypoints.GateDoor()
        gate_1.destination = interior
        gate_1.otherside = gate_2
        gate_2.destination = self.elements.get( "LOCALE" )
        gate_2.otherside = gate_1

        self.register_scene( nart, interior, igen, ident="BUILDING_INT", dident="LOCALE" )

        exterior.special_c[ "door" ] = gate_1
        int_mainroom = mapgen.SharpRoom( random.randint(12,20), random.randint(12,20),
         tags=(context.CIVILIZED,context.ROOM_PUBLIC), anchor=mapgen.south, parent=interior )
        int_mainroom.contents.append( gate_2 )
        int_mainroom.contents.append( waypoints.Bookshelf() )
        gate_2.anchor = mapgen.south
        int_mainroom.decorate = mapgen.TavernDec(win=maps.SMALL_WINDOW)

        npc = monsters.generate_npc()
        interior.name = random.choice( self.NAME_PATTERNS ).format( npc, random.choice(monsters.MONSTER_LIST).name, random.choice(monsters.MONSTER_LIST).name )
        gate_1.mini_map_label = "Inn"
        int_mainroom.contents.append( npc )
        self.register_element( "SHOPKEEPER", npc )

        int_mainroom.contents.append( maps.TABLE )
        int_mainroom.contents.append( maps.TABLE )
        int_mainroom.contents.append( maps.TABLE )

        int_bedroom = mapgen.SharpRoom( tags=(context.CIVILIZED,), parent=interior )
        int_bedroom.contents.append( maps.LIGHT_STAND )
        int_bedroom.decorate = mapgen.BedroomDec()


        self.shop = services.Inn()

        return True

    def SHOPKEEPER_offers( self, explo ):
        # Return list of shopkeeper offers.
        ol = list()
        ol.append( dialogue.Offer( "We have some space in the back." ,
         context = context.ContextTag([context.SERVICE,context.INN]), effect=self.shop ) )
        return ol


#  ************************
#  ***   CITY_LIBRARY   ***
#  ************************

class GenericLibrary( Plot ):
    LABEL = "CITY_LIBRARY"
    active = True
    scope = "BUILDING_INT"
    def custom_init( self, nart ):
        locale = self.elements.get( "LOCALE" )
        exterior = mapgen.BuildingRoom( tags=(context.CIVILIZED,) )
        exterior.special_c[ "window" ] = maps.DARK_WINDOW
        exterior.special_c[ "sign1" ] = maps.BOOK_SIGN
        self.register_element( "_EXTERIOR", exterior, dident="CITY" )
        interior = maps.Scene( 50,50, sprites={maps.SPRITE_FLOOR: "terrain_floor_wood.png" },
            biome=context.HAB_BUILDING, setting=self.setting, desctags=(context.DES_CIVILIZED,) )
        igen = mapgen.BuildingScene( interior )
        interior.name = "{0} Library".format( locale )
        gate_1 = waypoints.GateDoor()
        gate_2 = waypoints.GateDoor()
        gate_1.destination = interior
        gate_1.otherside = gate_2
        gate_1.mini_map_label = "Library"
        gate_2.destination = locale
        gate_2.otherside = gate_1
        self.register_scene( nart, interior, igen, ident="BUILDING_INT", dident="LOCALE" )
        exterior.special_c[ "door" ] = gate_1
        int_mainroom = mapgen.SharpRoom( tags=(context.CIVILIZED,context.ROOM_PUBLIC), anchor=mapgen.south, parent=interior )
        int_mainroom.contents.append( gate_2 )
        int_mainroom.contents.append( waypoints.Bookshelf() )
        gate_2.anchor = mapgen.south
        int_mainroom.decorate = mapgen.LibraryDec(win=maps.BRIGHT_WINDOW)
        if random.randint(1,100) == 23:
            npc = monsters.generate_npc( job=characters.Ninja )
        else:
            npc = monsters.generate_npc( job=random.choice((characters.Mage,characters.Mage,characters.Necromancer,
                characters.Mage,characters.Mage,characters.Necromancer,characters.Bard) ))
        int_mainroom.contents.append( npc )
        self.register_element( "SHOPKEEPER", npc )
        int_mainroom.contents.append( maps.DESK )
        int_mainroom.contents.append( maps.TABLE )
        self.shop = services.Shop( services.MAGIC_STORE, rank=self.rank+5, allow_misc=False, allow_magic=True, num_items=9 )
        self.add_sub_plot( nart, "SIDE_STORY", PlotState(rank=self.random_rank_in_chapter()).based_on( self ) )
        return True

    def SHOPKEEPER_offers( self, explo ):
        # Return list of shopkeeper offers.
        ol = list()
        ol.append( dialogue.Offer( "Knowledge is power. Some knowledge is more powerful than others." ,
         context = context.ContextTag([context.SHOP,context.MAGICGOODS]), effect=self.shop ) )
        return ol

#  ***********************
#  ***   CITY_TEMPLE   ***
#  ***********************

class GenericTemple( Plot ):
    LABEL = "CITY_TEMPLE"
    active = True
    scope = "BUILDING_INT"
    def custom_init( self, nart ):
        exterior = mapgen.BuildingRoom( tags=(context.CIVILIZED,) )
        exterior.special_c[ "window" ] = maps.STAINED_GLASS
        exterior.special_c[ "sign1" ] = maps.ANKH_SIGN
        self.register_element( "_EXTERIOR", exterior, dident="CITY" )

        locale = self.elements.get( "LOCALE" )
        interior = maps.Scene( 50,50, sprites={maps.SPRITE_FLOOR: "terrain_floor_bigtile.png",
            maps.SPRITE_INTERIOR: "terrain_int_temple.png" },
            biome=context.HAB_BUILDING, setting=self.setting, desctags=(context.DES_CIVILIZED,) )
        igen = mapgen.BuildingScene( interior )
        interior.name = "{0} Temple".format( locale )

        gate_1 = waypoints.GateDoor()
        gate_2 = waypoints.GateDoor()
        gate_1.destination = interior
        gate_1.otherside = gate_2
        gate_1.mini_map_label = "Temple"
        gate_2.destination = locale
        gate_2.otherside = gate_1

        self.register_scene( nart, interior, igen, ident="BUILDING_INT", dident="LOCALE" )

        exterior.special_c[ "door" ] = gate_1
        int_mainroom = mapgen.SharpRoom( tags=(context.CIVILIZED,context.ROOM_PUBLIC), anchor=mapgen.south, parent=interior )
        int_mainroom.contents.append( gate_2 )
        int_mainroom.contents.append( maps.ANKH_ALTAR )
        gate_2.anchor = mapgen.south
        int_mainroom.decorate = mapgen.TempleDec(win=maps.STAINED_GLASS)

        npc = monsters.generate_npc( job=random.choice((characters.Priest, characters.Priest,
            characters.Priest, characters.Priest, characters.Priest, characters.Priest, characters.Priest,
            characters.Druid, characters.Druid, characters.Priest, characters.Monk, characters.Knight) ))
        int_mainroom.contents.append( npc )
        self.register_element( "SHOPKEEPER", npc )

        self.shop = services.Temple()

        return True

    def SHOPKEEPER_offers( self, explo ):
        # Return list of shopkeeper offers.
        ol = list()
        ol.append( dialogue.Offer( "Remember that it is better to give than to receive, which is why we insist that you pay up front." ,
         context = context.ContextTag([context.SERVICE,context.HEALING]), effect=self.shop ) )
        return ol


#  ***************************
#  ***   CITY_WEAPONSHOP   ***
#  ***************************

class GenericWeaponShop( Plot ):
    LABEL = "CITY_WEAPONSHOP"
    active = True
    scope = "BUILDING_INT"
    NAME_PATTERNS = ( "{0}'s Arms", "{0}'s Weapons" )
    def custom_init( self, nart ):
        exterior = mapgen.BuildingRoom( tags=(context.CIVILIZED,) )
        exterior.special_c[ "window" ] = maps.SMALL_WINDOW
        exterior.special_c[ "sign1" ] = maps.WEAPONS_SIGN
        self.register_element( "_EXTERIOR", exterior, dident="CITY" )

        interior = maps.Scene( 50,50, sprites={maps.SPRITE_FLOOR: "terrain_floor_wood.png" },
            biome=context.HAB_BUILDING, setting=self.setting, desctags=(context.DES_CIVILIZED,) )
        igen = mapgen.BuildingScene( interior )

        gate_1 = waypoints.GateDoor()
        gate_2 = waypoints.GateDoor()
        gate_1.destination = interior
        gate_1.otherside = gate_2
        gate_2.destination = self.elements.get( "LOCALE" )
        gate_2.otherside = gate_1

        self.register_scene( nart, interior, igen, ident="BUILDING_INT", dident="LOCALE" )

        exterior.special_c[ "door" ] = gate_1
        int_mainroom = mapgen.SharpRoom( tags=(context.CIVILIZED,context.ROOM_PUBLIC), anchor=mapgen.south, parent=interior )
        int_mainroom.contents.append( gate_2 )
#        int_mainroom.contents.append( waypoints.Anvil() )
        gate_2.anchor = mapgen.south
        int_mainroom.decorate = mapgen.WeaponShopDec()

        npc = monsters.generate_npc( job=monsters.base.Merchant )
        interior.name = random.choice( self.NAME_PATTERNS ).format( npc )
        gate_1.mini_map_label = "Weapon Shop"
        int_mainroom.contents.append( npc )
        self.register_element( "SHOPKEEPER", npc )

        self.shop = services.Shop( ware_types=services.WEAPON_STORE, rank=self.rank+2,
         allow_misc=False, allow_magic=True, num_items=14 )

        return True

    def SHOPKEEPER_offers( self, explo ):
        # Return list of shopkeeper offers.
        ol = list()
        ol.append( dialogue.Offer( "This is my shop. There is not much here yet." ,
         context = context.ContextTag([context.SHOP,context.WEAPON]), effect=self.shop ) )
        return ol

