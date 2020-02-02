import random
class GameState:
    def __init__(self):
        self.started = False
        self.players = []
        self.deck = [Card("Assassin")] * 4 + [Card("Duke")] * 4 + [Card("Cortessa")] * 4 + [Card("Captain")] * 4 + [Card("Ambassador")] * 4
        self.curr_player = 0
        self.in_conflict = None
        self.channel = None
        self.timer = None
        self.waiting_for_action = True
        self.waiting_for_permissions = False
        self.accepted_list = []
        self.prev = ""
    def add_cards(self, n_cards, player):
        if n_cards > len(self.deck):
            n_cards = len(self.deck)
        random.shuffle(self.deck)
        for i in range(n_cards):
            print(self.deck)
            player.cards.append(self.deck.pop())
        print("player.cards",player.cards)
    def next_turn(self):
        self.curr_player = (self.curr_player + 1) % len(self.players)

    def start_game(self):
        random.shuffle(self.players)
        self.started = True
    def tag_to_player(self, discord_tag):
        """Returns corresponding player object given the discord_tag"""
        for player in self.players:
            if player.discord_tag == discord_tag:
                return player
        return None

    def get_permissions(self, player):
        self.waiting_for_permissions = True
        self.accepted_list = [player]
   

class Card:
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return self.name   
    def __repr__(self):
        return self.name         

class Player:
    def __init__(self, discord_tag, curr_game):
        self.discord_tag = discord_tag
        self.coins = 7
        self.cards = []
        self.turned_cards = []
        self.alive = True
        self.curr_game = curr_game

  
    def zero_less_cards(self):
        """Return True if player has zero or less cards"""
        return len(self.cards) <= 0

    
    def get_cards(self):
        return str(self.cards)

    def call_duke_block(self):
        """ Initiate duke gamespace, """
        pass
    def call_duke(self):
        """ initiate this"""
        pass
    def call_contessa(self):
        """ Initiate contessa gamespace """
        pass
    def call_assassain(self):
        """ Initiate assassain shit """
        pass
    def call_captain(self):
        """ Initate captain shit """
        pass
    def call_captain_block(self):
        pass
    def call_ambassador(self):
        """ Initate ambassador stuff """
        pass
    def call_aid(self):
        """ Initiate aid thing """
        pass
    def invoke_duke(self):
        """ Give the player +3 coins """
        self.curr_game.get_permissions(self)

    def duke_block(self):
        """Block foreign aid"""
        pass
    def invoke_contessa(self):
        """ Block an assassination attempt """
        pass
    def invoke_captain(self,target_tag):
        """ Take 2 coins from another player"""
        self.coins += 2
        target_obj = self.curr_game.tag_to_player(target_tag)
        target_obj.coins -= 2
    def invoke_captain_block(self):
        pass
    
    def invoke_ambassador(self):
        """ Invoke Ambassador- Draw two cards from deck. Choose which if any to exchange, and return 2 """
        pass
    def invoke_income(self):
        """ Give the player + 1 coins """
        self.coins += 1
        self.curr_game.next_turn()
        
    
    def invoke_aid(self):
        """ Give the player +2 coins """
        self.coins += 2
        self.curr_game.next_turn()

    def coup(self):
        """ Pay 7 coins and launch coup against opponent, forcing a turnover of that player """ 
        assert(self.coins > 7, 'player has not enough coins for coup')
        self.coins -= 7

      #TODO: needs to interact with reset of program

    def turn_over(self,card_name):
        """ Turns over the card_name of the player """
        for card in self.cards:
            if card.name == card_name.name:
                self.turned_cards.append(card)
                self.cards.remove(card)
                return
        raise Exception("Card Doesn't Exist")
        
        

    def is_above_ten(self):
        return self.coins >= 10

