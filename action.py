import constants

class Action:
    target = None
    blockers = None
    card = None
    
    def __init__(self):
        pass

    def get_identifier(self):
        pass

    def resolve_action(self, current_player = None, deck = None):
        pass

    def is_valid(self, players, player_index):
        #TODO: THis still
        return True

