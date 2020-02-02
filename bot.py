import discord
import game
import random
import time

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

        """PRINT THE MESSAGE, IF THE MESSAGE DOES NOT START WITH PREFIX OR THE MESSAGE WAS FROM THE BOT ITSELF, RETURN"""

        print('Message from {0.author}: {0.content}'.format(message))
        if not message.content.startswith("'") or message.author == client.user:
            return

        """UTILITY FUNCTIONS - KILL AND RESET GAME (TAKE PRIORITY)"""

        if message.content == "'kill":
            await message.channel.send(f"{message.author.mention}, I am quitting, goodbye!")
            raise SystemExit # hacky way of quiting application
            return
        elif message.content == "'reset":   # reset now works
            global game_state
            game_state = game.GameState()
            await message.channel.send(f"{message.author.mention}, the game has been reset.")
        
        """ START NOT NEEDED """

        if game_state.timer is not None:
            time_elapsed = time.time() - game_state.timer
            if is_equal(message, "dukeblock"):
                pass
            elif is_equal(message, "continue"):
                if time_elapsed > 3:
                    game_state.timer = None
                    prev = ""
                    message.channel.send(f"")
            else:
                message.channel.send(f"Sorry {message.author.mention}, that is not a valid command (must be 'dukeblock or 'continue) at this time due to a countdown initiated.")
        """
        print("mentions",message.mentions)
        """


        """GAME NOT STARTED"""

        if not game_state.started:
            if is_equal(message, "join"):
                found = False
                for player in game_state.players:
                    if player.discord_tag == message.author:
                        found = True
                        break
                output = ""
                if not found: #successfully joined
                    game_state.players.append(game.Player(message.author, game_state))
                    output += message.author.mention + ", added to the game.\n"
                    output += "Players: " + str(len(game_state.players))
                else: #already joined
                    output += message.author.mention + ", you are already added.\n"
                    output += "Players: " + str(len(game_state.players))
                await message.channel.send(output)
            
            elif is_equal(message, "players"):
                if len(game_state.players) == 0:
                    await message.channel.send(f"{message.author.mention}, there are no players in the game currently.")
                    return
                output = ""
                output += f"{message.author.mention}, here are the list of players:\n"
                for player in game_state.players:
                    output += player.discord_tag.mention + "\n"
                await message.channel.send(output)
            elif is_equal(message, "start") and not game_state.started:
                game_state.channel = message.channel
                game_state.start_game()
                await message.channel.send("Game has started. Check your DMs. Player order: ")
                for player in game_state.players:
                    await message.channel.send(player.discord_tag.mention)
                    game_state.add_cards(2, player)
                    dm = await player.discord_tag.create_dm()
                    await dm.send(f"**DiscordCoup - NEW GAME STARTED**\nCards: {player.get_cards()}\nCoins: {player.coins}")
            return
        """GAME IS STARTED"""

        if game_state.started:

            """COINS"""
            
            if is_equal(message, "coins"):
                output = "Coins: \n"
                for player in game_state.players:
                    output += f"{player.discord_tag.mention}: {player.coins}\n" 
                await message.channel.send(output)
            
            """WAITING FOR ACTION"""

            if game_state.waiting_for_action:

                """If not player's turn"""

                if game_state.players[game_state.curr_player].discord_tag != message.author:
                    await message.channel.send("Not your turn.")
                    return
                elif is_equal(message, "income"): #income
                    if game_state.players[game_state.curr_player].is_above_ten():
                        await message.channel.send("10+ coins, must perform Coup.")
                        return
                    game_state.players[game_state.curr_player].invoke_income()
                    await message.channel.send(f"{message.author.mention} incomed. Coins: {game_state.players[game_state.curr_player - 1].coins}")
                    game_state.waiting_for_action = True
                elif is_equal(message, "foreignaid"): #foreign aid
                    await message.channel.send(f"{message.author.mention} claimed foreign aid. Challenge with 'c, or pass with 'p.")
                    game_state.prev = "foreginaid"
                    game_state.waiting_for_action = False
                    return
                elif is_equal(message, "coup") and len(message.mentions) != 1: #coup
                    await message.channel.send("Command is: 'Coup @player")
                    return
                elif is_equal(message, "coup") and len(message.mentions) == 1:
                    if game_state.tag_to_player(message.mentions[0]) is None:
                        await message.channel.send(f"{message.mentions[0].mention} is not in the game.")
                        return
                    elif message.mentions[0] == message.author:
                        await message.channel.send(f"Cannot Coup yourself.")
                        return
                    elif game_state.players[game_state.curr_player].coins < 7:
                        await message.channel.send(f"Need 7 coins, you have: {game_state.players[game_state.curr_player].coins}.")
                        return
                    dm = await message.mentions[0].create_dm()
                    await dm.send(f"You have been Couped. Discard a card. Type 'discard 0, etc.\nCurrent cards: {game_state.tag_to_player(message.mentions[0]).cards}.")
                    game_state.in_conflict = message.mentions[0]
                    game_state.tag_to_player(message.author).coup()
                    await message.channel.send(f"{message.author.mention} Coups --> {message.mentions[0].mention}")
                    game_state.waiting_for_action = False
                elif is_equal(message, "duke"):
                    game_state.tag_to_player(message.author).invoke_duke()
                    await message.channel.send(f"{message.author.mention} calls Duke.")
                    game_state.waiting_for_action = False
                return


            
            """ SOMEONE IS BEING COUPED BUT SOMEONE TALKED WHO WASN'T BEING COUPOED """

            """NOT WAITING FOR ACTION"""

            if not game_state.waiting_for_action:
                
                """when someone does action that can be called"""
                if game_state.waiting_for_permissions:
                    if is_equal(message, "c"): #if someone challenges
                        await message.channel.send(f"{message.author.mention} challenges")
                        game_state.waiting_for_permissions = False
                        game_state.waiting_for_action = True
                        game_state.next_turn
                        return
                    elif is_equal(message, "p"): #if someone passed, check if added
                        found = False
                        for player in game_state.accepted_list:
                            if player.discord_tag == message.author:
                                found = True
                                break
                        output = ""
                        if not found: #add to accepted list
                            game_state.accepted_list.append(game_state.tag_to_player(message.author))
                            await message.channel.send("Passed.")
                            #check if all players has passed
                            await message.channel.send(len(game_state.accepted_list))
                            await message.channel.send(len(game_state.players))
                            if len(game_state.players) == len(game_state.accepted_list):
                                await message.channel.send("Everyone passed, action allowed.")
                                game_state.waiting_for_permissions = False
                                game_state.waiting_for_action = True
                                game_state.next_turn
                            return
                                
                        else: #already accepted
                            output += message.author.mention + ", you are already added.\n"
                            await message.channel.send("You have already passed.")
                            return
                    
                """Check player's turn"""

                """game_state.in_conflict is not None and"""

                if game_state.in_conflict != message.author:
                    await message.channel.send("Wait your turn.")
                    return
                else:
                    # TODO: implement card debt: if game_state.tag_to_player(message.author).zero_less_cards():
                    if len(message.content.split()) != 2:
                        await message.channel.send("Type 'discard [number].")
                        return
                    index_to_discard = message.content.split()[1]
                    if not index_to_discard.isdigit():
                        await message.channel.send("Type 'discard [number].")
                        return
                    index_to_discard = int(index_to_discard)
                    if 0 <= index_to_discard <= 1: # the input was successful
                        name_of_discarded = game_state.tag_to_player(message.author).cards[index_to_discard].name
                        game_state.tag_to_player(message.author).turn_over(game_state.tag_to_player(message.author).cards[index_to_discard])
                        await message.channel.send(f"{message.author.mention} discarded {name_of_discarded}")
                        game_state.next_turn()
                        game_state.in_conflict = None
                        game_state.waiting_for_action = True
                        print(game_state.tag_to_player(message.author).cards)
                        return
                    else:
                        await message.channel.send("Invalid number")
                        return

client = MyClient()
token = ""
with open("token.txt") as f:
    token = f.readline().strip()
client.run(token) # FOR ANYONE USING THIS BOT, PUT YOUR TOKEN IN A TEXT FILE NAMED token.txt IN THE SAME DIRECTORY
