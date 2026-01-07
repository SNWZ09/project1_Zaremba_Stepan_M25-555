#!/usr/bin/env python3

from labyrinth_game import constants, player_actions, utils #подключаем все созданные ранее модули

#определяем состояние игрока
game_state = {
    'player_inventory': [], # Инвентарь игрока
    'current_room': 'entrance', # Текущая комната
    'game_over': False, # Значения окончания игры
    'steps_taken': 0 # Количество шагов
  }
  

def main():
    #выводим приветственное сообщение
    print('Добро пожаловать в Лабиринт сокровищ!')
    
    #описываем начальную комнату
    utils.describe_current_room(game_state)
    
    #создаем цикл, который будет работать, пока игра не закончена
    while game_state['game_over'] != True:
        #считываем команду пользователя
        player_command = input()
    
    
if __name__ == '__main__':
    main()

