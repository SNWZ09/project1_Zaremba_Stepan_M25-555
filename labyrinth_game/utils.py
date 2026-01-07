from labyrinth_game import constants 

#функция описания комнаты принмает словарь в качестве аргумента и получает из константы все данные
def describe_current_room(game_state):
    room_name = game_state['current_room'] #допустим, в словаре ключ будет называться room_name
    
    room_info = constant.ROOMS[room_name] #получаем всю информацию о комнате
    
    division_str = '_' #ввёл разделитель, чтобы было удобнее выводить информацию
    
    #теперь выводим её
    print(f'\n {division_str * 50} \n
        {room_name.upper()}')
    
    #описание комнаты
    print(f'\n {division_str * 50} \n
        {room_info['description']}')
    
    #проверяем, не нулевое ли значение предметов. Если не нулевое - выводим.
    room_items = room_info['items']
    if room_items:
        print(f'\n {division_str * 50} \n Заметные предметы: {', '.join(room_items)}')
    
    #выводим, какие выходы есть в комнате
    room_exits = room_info['exits'].keys()
    print(f'\n {division_str * 50} \n Выходы: {', '.join(room_exits)}')
    
    #так же, как и с предметами, идет проверка на наличие загадки.
    room_puzzle = room_info['puzzle']
    if room_puzzle:
        print(f'\n {division_str * 50} \n Кажется, здесь есть загадка (используйте команду solve).')

    
