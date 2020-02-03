# discord-coup - right now ignore the 50% duke 100% reset and kill branch, just work on master, was testing something -MH 10:57PM 2/2/2020 NZDT
A Discord bot for playing the game Coup. A WIP.

## Working features
NB: default prefix is: ' (single quotation mark)
* 'income - adds one coin to the player 
* 'coup @player - if you have 7 or more coins, you are allowed to coup someone using their Discord tag.

## TODO
I personally advocate for refactoring the program - specifically the GameState.players from a "list" type to a "dict" in order to remove the redundancy of tag_to_player.
