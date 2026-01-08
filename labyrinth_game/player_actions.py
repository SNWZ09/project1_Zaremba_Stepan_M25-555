from labyrinth_game import constants, utils #подключаем все созданные ранее модули

#функция отображения инвентаря, принимает аргумент - словарь
def show_inventory(game_state):
    player_inventory = game_state['player_inventory'] #присваеваем переменной инвентарь
    
    division = '_' * 50 #ввёл разделитель, чтобы было удобнее выводить информацию
    #проверяем его наполнение
    if player_inventory: 
        print(f'\n {division} \n В инвентаре следующие предметы: {', '.join(player_inventory)}.')
    else:
        print('\n Ваш инвентарь пуст')
        
 #ввод пользователя  
def get_input(prompt="> "):
    try:
        player_command = input(prompt).lower() #приводим в нижний регистр для "унификации" ответов и вводов
        return player_command
    except (KeyboardInterrupt, EOFError):
        print("\n Выход из игры.")
        return "quit" 
        
#функция перемещения
def move_player(game_state, direction):
    room_name = game_state['current_room']
    room_exits = constants.ROOMS[room_name]['exits'] #берем все выходы, которые есть у нашей комнаты
    
    #проверяем, есть ли такой выход, какой ввёл пользователь
    if direction in room_exits:
        next_room = room_exits[direction]
        game_state['current_room'] = next_room #переходим в следующую комнату
        game_state['steps_taken'] += 1 #увеличиваем шаг
        utils.describe_current_room(game_state) #описываем следующую комнату
    else:
        print('\n Нельзя пойти в этом направлении.')

#функция взятия предмета
def take_item(game_state, item_name):
    room_name = game_state['current_room']
    room_items = constants.ROOMS[room_name]['items'] #берем все предметы, которые есть у нашей комнаты
    
    #добавим вариант, если игрок попытается поднять сундук
    if item_name == 'treasure_chest':
        print('\n Вы не можете поднять сундук, он слишком тяжелый.')
        return
    
    #проверяем, есть ли такой предмет, какой ввёл пользователь
    if item_name in room_items:
        game_state['player_inventory'].append(item_name) #добавляем ему в инвентарь
        room_items.remove(item_name) #удаляем из комнаты предмет
        print('\n Вы подняли: ', item_name)
    else:
        print('\n Такого предмета здесь нет.')
        
#юзаем предметы
def use_item(game_state, item_name):
    #проверяем, есть ли введенный предмет в инвентаре игрока
    if item_name not in game_state['player_inventory']:
        print('\n У вас нет такого предмета.')
        
    #делаем вывод для факела
    if item_name == 'torch':
        print('\n Вы зажгли факел. Вокруг стало намного светлее.')
        
    #делаем вывод для меча    
    elif item_name == 'sword':
        print('\n Вы взяли в руки меч. Вы чувствуете уверенность перед предстоящими трудностями.')
        
    #делаем вывод для шкатулки    
    elif item_name == 'bronze_box':
        print('\n Вы открыли бронзовую шкатулку.')
        
        #если у игрока нет до этого момента ключа - он обнаружит его в шкатулке
        if 'rusty_key' not in game_state['player_inventory']:
            print('\n Внутри был ржавый ключ!')
            game_state['player_inventory'].append('rusty_key')
            
        #если ключ был - шкатулка окажется пустой
        else:
            print('\n К сожалению, шкатулка оказалась пустой.')
     
    #все остальные предметы игрок не знает, как использовать 
    else:
        print('\n Вы не знаете, как и где использовать этот предмет.')

    
