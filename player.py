import random


class ActionChooser:

    # ActionChooser turns a list of actions into a map of key to action
    def __init__(self, *actions):
        self._choices = {}
        for action in actions:
            key = action.get_key()
            if self._choices.get(key) is not None:
                raise ValueError(f"Duplicate key '{key}' in ActionChooser!!")
            self._choices[key] = action

    def get_choice(self):
        pass


class MonsterChooser(ActionChooser):

    # monsters don't get to choose the action
    # they act randomly
    def get_choice(self):
        key = random.choice(list(self._choices.keys()))
        return self._choices[key]


class PlayerChooser(ActionChooser):

    # player character gets a on-screen prompt for an action
    # the list will typically contain in-game and meta-game actions.
    def get_choice(self):
        while True:
            # print a list of options and prompt for input until the player makes a valid selection
            print("\n-------------  Enter your selection --------------")
            for (key, action) in self._choices.items():
                print(f"{key} ({action.get_prompt()}):")
            choice = input('>> ')
            print('--------------------------------------------------\n')
            try:
                # player made a valid choice, return the action chosen
                return self._choices[choice]
            except KeyError:
                # the user entered an invalid value
                # catch the error here, print an error message and prompt again
                print(f"[ERROR]:  Invalid input '{choice}'.  Please select from the menu.")


class Character:

    def __init__(self, player_type, name, chooser):
        self._player_type = player_type
        self._name = name
        self._curr_health_points = self._player_type.max_health_points
        self._foe = None
        self._chooser = chooser

    # attack your opponent
    def attack(self):
        print(f"{self.get_name()} attacked for {self._player_type.attack_damage} points of damage!!")
        self._foe.take_damage(self._player_type.attack_damage)

    # heal yourself
    # TODO: make the amount of healing variable
    def heal(self):
        print(f"{self.get_name()} got {self._player_type.healing_points} points of healing.")
        self._curr_health_points += self._player_type.healing_points
        if self._curr_health_points >= self._player_type.max_health_points:
            self._curr_health_points = self._player_type.max_health_points

    # show number of hit points left of dead status
    def show_status(self):
        if self.is_alive():
            print(f'{self.get_name()} has {self._curr_health_points} health points.')
        else:
            print(f'{self.get_name()} is dead!')

    # you got attacked, take damage
    # TODO:  Make the amount of damage variable
    def take_damage(self, damage):
        self._curr_health_points -= damage

    # the game tells you who your foe is via this method
    def set_foe(self, foe):
        self._foe = foe

    # get your name and class
    def get_name(self):
        return f'{self._name} the {self._player_type.name}'

    # are you still able to fight?
    def is_alive(self):
        return self._curr_health_points > 0

    # if the player can fight, return aa action chooser, else return None
    def get_chooser(self):
        if self.is_alive():
            return self._chooser
        else:
            return None


class Attack:

    def __init__(self, actor):
        self._actor = actor

    def do(self):
        self._actor.attack()

    @classmethod
    def get_prompt(cls):
        return "Attack"

    @classmethod
    def get_key(cls):
        return "a"


class Heal:

    def __init__(self, actor):
        self._actor = actor

    def do(self):
        self._actor.heal()

    @classmethod
    def get_prompt(cls):
        return "Heal"

    @classmethod
    def get_key(cls):
        return "h"


# The Fighter class stats
class Fighter:

    name = "Fighter"
    max_health_points = 100
    healing_points = 20
    attack_damage = 10


class Player(Character):

    def __init__(self, player_type, name, *game_actions):
        # player characters can attack, heal, or perform game level actions
        super().__init__(player_type, name, PlayerChooser(Attack(self), Heal(self), *game_actions))


# Goblin class stats
class Goblin:
    name = "Goblin"
    max_health_points = 50
    attack_damage = 10


class Monster(Character):

    def __init__(self, player_type, name):
        # Monsters can only attack
        super().__init__(player_type, name, MonsterChooser(Attack(self)))
