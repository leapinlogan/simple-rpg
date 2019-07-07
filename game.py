from player import *


class Game:

    """This is a simple RPG with a command line interface.  It's used to demonstrate good python programming practices.

    """

    # These class are actions the player-character can take to manage the game actions
    # They are event callbacks using the double dispatch pattern
    # if you add another action, be sure to update _create_player() and _is_game_action()
    class End:

        """This class is used to notify the game of a Quit event

        """
        def __init__(self, actor):
            self._actor = actor

        def do(self):
            self._actor.end()

        @classmethod
        def get_prompt(cls):
            return "Quit"

        @classmethod
        def get_key(cls):
            return "q"

    class ShowStatus:
        """This class is used to notify the game of a show player status event

        """

        def __init__(self, actor):
            self._actor = actor

        def do(self):
            self._actor.show_player_status()

        @classmethod
        def get_prompt(cls):
            return "Show Status"

        @classmethod
        def get_key(cls):
            return "s"

    class Restart:
        """This class is used to notify the game of a restart event

        """

        def __init__(self, actor):
            self._actor = actor

        def do(self):
            self._actor.start()

        @classmethod
        def get_prompt(cls):
            return "Restart Game"

        @classmethod
        def get_key(cls):
            return "r"

    def __init__(self):
        self._game_is_running = False
        self._round = None
        self._player = None
        self._monster = None

    def _show_game_status(self):
        if self._game_is_running:
            print("\n\t\t*** Game On! ***\n")
        else:
            print("\n\n\t\t*** Game Over! ***")

    def show_player_status(self):
        self._player.show_status()
        self._monster.show_status()

    def end(self):
        self._game_is_running = False
        self.show_player_status()
        self._show_game_status()

    # on game (re)start, create a new set of players and start the match
    def start(self):
        self._create_player()
        self._create_monster()
        self._player.set_foe(self._monster)
        self._monster.set_foe(self._player)
        self._game_is_running = True
        self._show_game_status()
        print(f"Welcome {self._player.get_name()}!!")
        self.show_player_status()

    @classmethod
    def _get_player_class(cls):
        chooser = PlayerChooser("Select a Player Class", Fighter, Mage, Rogue)
        class_ = chooser.get_choice()
        return class_

    # create a player character
    def _create_player(self):
        name = input("Enter the player's name:  ")
        player_class = Game._get_player_class()
        # Add all game actions to actions choices for player character
        self._player = Player(player_class, name, Game.ShowStatus(self), Game.End(self), Game.Restart(self))

    # create a monster to battle
    # TODO:  create random monster type
    def _create_monster(self):
        chooser = MonsterChooser(Goblin, Hobgoblin)
        monster_class_ = chooser.get_choice()
        self._monster = Monster(monster_class_, "Gobby")

    # This is ued to check is the action is one of the game events
    # if you create a new game action, update this method
    @staticmethod
    def _is_game_action(action):
        return action.get_key() in (Game.End.get_key(), Game.ShowStatus.get_key(), Game.Restart.get_key())

    # main method to run a game
    # player character goes first
    def run(self):
        self.start()
        player_turn = True
        while self._game_is_running:
            # player and monster take turns
            if player_turn:
                chooser = self._player.get_chooser()
            else:
                chooser = self._monster.get_chooser()
            # if the character did not return an action, it means it can't do anything
            # this ends the game
            if chooser is not None:
                action = chooser.get_choice()
                # if the action is a 'game' action, skip the monsters turn
                if Game._is_game_action(action):
                    player_turn = True
                else:
                    player_turn = not player_turn
                action.do()
            else:
                self.end()


if __name__ == "__main__":
    Game().run()
