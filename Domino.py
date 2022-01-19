import random
import math

# Generate all dominoes pieces which can be avaiable 
def generate_stock():
    all_pieces = []
    for i in range(0,7):
        for j in range(6,-1,-1):
            if i < j or i==j:
                all_pieces.append([i,j])
    return all_pieces

def generate_players(stock_pieces):
    players = {'player':[],'computer':[]}
    for player in players.keys():
        player_dominoes = players[player]
        while len(player_dominoes) != 7:
            index = random.randrange(len(stock_pieces))
            player_dominoes.append(stock_pieces[index])
            stock_pieces.remove(stock_pieces[index])
    return players

def first_player(players):
    max_item = 0
    turn =''
    for player in players.keys():
        player_dominoes = players[player]
        for piece in player_dominoes:
            if piece[0] == piece[1] and max_item < piece[0]: # checking if we have double domino and we looking for the highest one
                max_item = piece[0]
                turn = player
    first_domino = [max_item,max_item]
    return([turn,first_domino])

def first_move(first_domino,players,turn):
    # putting domino piece on the table
    domino_snake = [first_domino]
    players[turn].remove(first_domino)
    return domino_snake

def changing_turn(turn):
    if turn == 'player':
        return 'computer'
    else:
        return 'player'

def generate_snake(domino_snake):
    snake = ""
    for piece_index in range(len(domino_snake)):
        if len(domino_snake) > 6:
            if piece_index < 3 or piece_index >= len(domino_snake) - 3:
                snake += str(domino_snake[piece_index])
            elif piece_index == 3:
                snake += '...'
        else:
            snake +=  str(domino_snake[piece_index])  
    return snake  

def user_input(players):
    move = 0
    move_index = 0
    player_dominoes = players['player']
    right_answer = False
    while right_answer == False:
        try:
            move = int(input(f"\nStatus: It's your turn to make a move. Enter your command."))
            move_index = int(math.fabs(move) - 1) 
            if move_index + 1 <= len(player_dominoes):
                right_answer = True
                return [move,move_index]
            else:
                print('\nInvalid input. Please try again.')
                return False
        except:
            print('\nInvalid input. Please try again.')
            return False

def computer_mind(players,domino_snake):
    computers_dominoes = players['computer']
    for piece in computers_dominoes:
            move_index = computers_dominoes.index(piece)
            if piece[0] == domino_snake[len(domino_snake) - 1][1]:
                move = move_index 
            elif piece[1] == domino_snake[0][0]:
                move = move_index * (-1)
            else:
                move = 0
                move_index = 0
    return ([move,move_index])

def inputs(turn):
    if turn == "computer":
        input(f'\nStatus: Computer is about to make a move. Press Enter to continue...')
        computer_move = computer_mind(players,domino_snake)
        return (computer_move)
    elif turn == "player":
        user_move = user_input(players)
        while user_move == False:
            user_move = user_input(players)
        else:
            return(user_move)

def game_printer(stock_pieces,domino_snake,players):
    computers_dominoes = players['computer']
    player_dominoes = players['player']
    page_break = "="*70
    print(f'{page_break}\nStock size: {len(stock_pieces)}\nComputer pieces: {len(computers_dominoes)}\n\n')
    snake = generate_snake(domino_snake)
    print(f'{snake}\n\nYour pieces:')
    for i in range(len(player_dominoes)):
        print(f'{i+1}:{player_dominoes[i]}')
    
        

def action_checker(players,turn,domino_snake,move,move_index,stock_pieces):
    domino_snake_last_part = domino_snake[len(domino_snake)-1]
    domino_snake_first_part = domino_snake[0]
    if not judge(stock_pieces,domino_snake,players):
        if move < 0:
            domino_snake_number = domino_snake_first_part[0]
            player_number = players[turn][move_index][1]
        elif move > 0:
            domino_snake_number = domino_snake_last_part[1]
            player_number = players[turn][move_index][0]
        if move != 0:
            if domino_snake_number == player_number:
                return True
            else:
                print('Illegal move. Please try again.')
                return False
        elif len(stock_pieces) != 0:
            return True
    


def action_maker(move,move_index,domino_snake,turn,players,stock_pieces):
    player_dominoes = players[turn]
    played_domino = player_dominoes[move_index]
    if move > 0:
        domino_snake.append(played_domino)
        player_dominoes.remove(played_domino)
        return ([domino_snake,player_dominoes,stock_pieces])
    elif move < 0:
        temp_list = [played_domino]
        for domino in domino_snake:
            temp_list.append(domino)
        domino_snake = temp_list
        player_dominoes.remove(played_domino)
        return ([domino_snake,player_dominoes,stock_pieces])
    else:
        extra_piece_index = random.randrange(len(stock_pieces))
        player_dominoes.append(stock_pieces[extra_piece_index])
        stock_pieces.remove(stock_pieces[extra_piece_index])
        return ([domino_snake,player_dominoes,stock_pieces])

def judge(stock_pieces,domino_snake,players):
    if len(players['computer']) == 0:
        game_printer(stock_pieces,domino_snake,players)
        print('Status: The game is over. The computer won!')
        return 'computer win'
    elif len(players['player']) == 0:
        game_printer(stock_pieces,domino_snake,players)
        print('Status: The game is over. You won!')
        return 'player win'
    elif len(stock_pieces) == 0:
        game_printer(stock_pieces,domino_snake,players)
        print("Status: The game is over. It's a draw!")
        return 'draw'
    else:
        return False
 
# def main():
turn = ""
end = False
while turn == "":
    stock_pieces = generate_stock()
    players = generate_players(stock_pieces)
    first_settings = first_player(players)
    turn = first_settings[0]
first_domino = first_settings[1]
domino_snake = first_move(first_domino,players,turn)
while end == False:
    turn = changing_turn(turn)
    game_printer(stock_pieces,domino_snake,players)
    move_list = inputs(turn)
    move = move_list[0]
    move_index = move_list[1]
    autorization = action_checker(players,turn,domino_snake,move,move_index,stock_pieces)
    if autorization:
        action = action_maker(move,move_index,domino_snake,turn,players,stock_pieces)
        if action == True:
            end = True
        else:
            domino_snake = action[0]
            players[turn] = action[1]
            stock_pieces = action[2]
    else:
        turn = changing_turn(turn)
        if judge(stock_pieces,domino_snake,players) != False:
            end = True
        