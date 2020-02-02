import discord
import game
import random

prefix = "'"

def is_equal(m, command):
    return m.content.split(" ")[0] == prefix + command


game_state = game.GameState()


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def output_to_channel(self, c, info):
        await c.send(info)

    async def on_message(self, message):
        if not message.content.startswith("'"):
            return

        print("mentions",message.mentions)
        if is_equal(message, "join") and not game_state.started:
            found = False
            for player in game_state.players:
                if player.discord_tag == message.author:
                    found = True
                    break

            if not found:
                game_state.players.append(game.Player(message.author, game_state))
                await message.channel.send(message.author.mention + ", you have been added to the game.")
                await message.channel.send("Currently there are " + str(len(game_state.players)) + " players.")
            else:
                await message.channel.send(message.author.mention + ", you have already been added.")
                await message.channel.send("Currently there are " + str(len(game_state.players)) + " players.")
        
        elif is_equal(message, "players"):
            await message.channel.send("List of players currently joined:")
            for player in game_state.players:
                await message.channel.send(player.discord_tag.mention)
        
        elif is_equal(message, "start") and not game_state.started:
            game_state.channel = message.channel
            game_state.start_game()
            await message.channel.send("Game has started. Please check your DMs for the cards. The order of players is as follows:")
            for player in game_state.players:
                await message.channel.send(player.discord_tag.mention)
                game_state.add_cards(2, player)
                dm = await player.discord_tag.create_dm()
                await dm.send(f"**DiscordCoup - NEW GAME STARTED**\nCards: {player.get_cards()}\nCoins: {player.coins}")

        elif is_equal(message, "coins") and game_state.started:
            output = "Here are the coins:\n"
            for player in game_state.players:
                output += f"{player.discord_tag.mention}: {player.coins}\n" 
            await message.channel.send(output)
        
        elif game_state.in_conflict is not None and game_state.in_conflict != message.author:
            await message.channel.send(f"{message.author.mention}, someone is being couped, you must wait for their move.")
            return

        elif game_state.in_conflict == message.author:
            if not is_equal(message, "discard"):
                await message.channel.send(f"{message.author.mention}, wrong command, you can only call 'discard when couped.")
                return
            # TODO: implement card debt: if game_state.tag_to_player(message.author).zero_less_cards():
            if len(message.content.split()) != 2:
                await message.channel.send(f"{message.author.mention}, someting wong")
                return
            index_to_discard = message.content.split()[1]
            if not index_to_discard.isdigit():
                await message.channel.send(f"{message.author.mention}, someting wong")
                return
            index_to_discard = int(index_to_discard)
            if 0 <= index_to_discard <= 1: # the input was successful
                name_of_discarded = game_state.tag_to_player(message.author).cards[index_to_discard].name
                game_state.tag_to_player(message.author).turn_over(game_state.tag_to_player(message.author).cards[index_to_discard])
                await message.channel.send(f"{message.author.mention} just revealed a card: {name_of_discarded}")
                game_state.next_turn()
                game_state.in_conflict = None
                print(game_state.tag_to_player(message.author).cards)
                return
            else:
                await message.channel.send(f"{message.author.mention}, someting wong")
                return

        elif is_equal(message, "income") and game_state.started and game_state.players[game_state.curr_player].discord_tag == message.author:
            if game_state.players[game_state.curr_player].is_above_ten():
                await message.channel.send("You must perform a coup!")
                return
            game_state.players[game_state.curr_player].invoke_income()
            await message.channel.send(f"{message.author.mention} incomed. Coins: {game_state.players[game_state.curr_player - 1].coins}")
        
        elif is_equal(message, "coup") and game_state.started and game_state.players[game_state.curr_player].discord_tag == message.author and len(message.mentions) == 1:
            if game_state.tag_to_player(message.mentions[0]) is None:
                await message.channel.send(f"Hey {message.author.mention}, I do not believe that {message.mentions[0].mention} is in game!")
                return
            if message.mentions[0] == message.author:
                await message.channel.send(f"{message.author.mention}, you can't coup yourself sadly. ;(")
                return
            if game_state.players[game_state.curr_player].coins < 7:
                await message.channel.send(f"You do not have enough coins (7)! Coins: {game_state.players[game_state.curr_player].coins}")
                return
            dm = await message.mentions[0].create_dm()
            await dm.send(f"You've been couped. Pick a card to discard based on index (0-based e.g. if your cards were ['Duke', 'Ambassador'], to remove Duke type 'discard 0).\nCurrent cards: {game_state.tag_to_player(message.mentions[0]).cards}")
            game_state.in_conflict = message.mentions[0]
            game_state.tag_to_player(message.author).coup()
            await message.channel.send(f"{message.author.mention} coups {message.mentions[0].mention}")
        


        print('Message from {0.author}: {0.content}'.format(message))

client = MyClient()
client.run('insert token here') # FOR ANYTHING USING THIS BOT, PUT YOUR TOKEN IN THE QUOTATION MARKS
