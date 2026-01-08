#!/usr/bin/env python3

from labyrinth_game import (  #подключаем все созданные ранее модули
    constants,
    player_actions,
    utils,
)

#определяем состояние игрока
game_state = {
    'player_inventory': [], # Инвентарь игрока
    'current_room': 'entrance', # Текущая комната
    'game_over': False, # Значения окончания игры
    'steps_taken': 0 # Количество шагов
  }
 
#обрабатываем ввод игрока 
def process_command(game_state, command):
    player_command = command.split() #отделяем команду от аргумента
    
    #проверяем, точно ли игрок что-то ввёл
    if not player_command:
        print('Вы не ввели команду')
        return
    
    #вводим переменную для перемещения по односложным командам
    possible_directions = ['north', 'south', 'east', 'west'] 
    
    #если ввод игрока состоит из одного слова и это одно слово есть в списке
    #тогда добавляем go в начало
    if len(player_command) == 1 and player_command[0] in possible_directions:
        player_command.insert(0, 'go')
    
    #спасибо за возможность использовать эту конструкцию
    #понравилась куда больше, чем просто if/else
    match player_command:
        #если игрок решил осмотреться
        case ['look']:
            utils.describe_current_room(game_state)
            
        #если игрок решил использовать предмет   
        case ['use', item_name]:
            player_actions.use_item(game_state, item_name)
        
        #если игрок решил пойти в другую комнату
        case ['go', direction]:
            player_actions.move_player(game_state, direction)
            
        #если игрок решил взять предмет    
        case ['take', item_name]:
            player_actions.take_item(game_state, item_name)
            
        #если игрок решил посмотреть инвентарь    
        case ['inventory']:
            player_actions.show_inventory(game_state)
            
        #если игрок захотел решить загадку  
        case ['solve']:
            #особое условие для комнаты сокровищ
            if game_state['current_room'] == 'treasure_room':
                utils.attempt_open_treasure(game_state)
                
            #условие для всех остальных комнат с загадками
            else:
                utils.solve_puzzle(game_state)
                
        #если игроку нужна помощь       
        case ['help']:
            utils.show_help(constants.COMMANDS)
        
        #если игрок решил выйти из игры    
        case ['quit']:
            print('\n Спасибо за игру!')
            game_state['game_over'] = True
            
            
def main():
    #выводим приветственное сообщение
    print('\n Добро пожаловать в Лабиринт сокровищ!')
    
    #описываем начальную комнату
    utils.describe_current_room(game_state)
    
    #создаем цикл, который будет работать, пока игра не закончена
    while not game_state['game_over']:
    
        #считываем команду пользователя
        player_command = player_actions.get_input()
        process_command(game_state, player_command)
    
    
if __name__ == '__main__':
    main()

