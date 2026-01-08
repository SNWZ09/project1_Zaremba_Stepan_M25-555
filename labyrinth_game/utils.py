from labyrinth_game import constants, player_actions 

#функция описания комнаты принмает словарь в качестве аргумента и получает из константы все данные
def describe_current_room(game_state):
    room_name = game_state['current_room']
    room_info = constants.ROOMS[room_name] #получаем всю информацию о комнате
    
    division = '_' * 80 #ввёл разделитель, чтобы было удобнее выводить информацию
    
    #теперь выводим её
    print(f'\n {division} \n {room_name.upper()}')
    
    #описание комнаты
    print(f'\n {division} \n {room_info['description']}')
    
    #проверяем, не нулевое ли значение предметов. Если не нулевое - выводим.
    room_items = room_info['items']
    if room_items:
        print(f'\n {division} \n Заметные предметы: {', '.join(room_items)}')
    
    #выводим, какие выходы есть в комнате
    room_exits = room_info['exits'].keys()
    print(f'\n {division} \n Выходы: {', '.join(room_exits)}')
    
    #так же, как и с предметами, идет проверка на наличие загадки.
    room_puzzle = room_info['puzzle']
    if room_puzzle:
        print(f'\n {division} \n Кажется, здесь есть загадка (используйте команду solve).')

def solve_puzzle(game_state):
    room_name = game_state['current_room']
    room_info = constants.ROOMS[room_name] #получаем всю информацию о комнате
    puzzle_info = room_info['puzzle'] #получаем информацию конкретно о загадке комнаты
    
    #проверим, есть ли вообще загадка
    if not puzzle_info:
        print('\n В этой комнате загадок нет')

        return #завершаем выполнение функции, если загадок нет
        
    puzzle_question, puzzle_answer = puzzle_info #присваиваем переменным загадку и ответ на неё + выводим условия загадки
    print(f'\n Комната содержит следующую загадку: \n {puzzle_question}')
    
    player_answer = player_actions.get_input('\n Ваш ответ на загадку: ') #получаем ответ игрока
    
    if player_answer.lower() == puzzle_answer.lower():
        print('\n Вы верно решили загадку! Поздравляем!!')
        room_info['puzzle'] = None
        
        if room_name == 'hall':
            print('\n Назвав правильное число, вы замечаете, что буквы надписи начали двигаться, создав уникальный узор с сообщением по центру: Ученье - свет. Неученье - тьма.')
        
        elif room_name == 'trap_room':
            print('\n Вы чудом избежали смертельного ранения, после чего решили уйти из этой комнаты подальше')
            
        elif room_name == 'library':
            print('\n Получив правильный ответ, свиток засверкал. "Ученье - свет. Неученье - тьма", промолвили вы, наблюдая, как древний манускрипт превращается в ключ от сокровищницы. В инвентарь был добавлен ключ от сокровищницы. Знания - сила.')
            game_state['player_inventory'].append('treasure_key')
        
        elif room_name == 'torture_room':
            print('\n Вы решаете ещё раз осмотреть комнату. Может быть, ответ "3" был секретом к чему-то большему, находящемуся в этой комнате? Вы окидываете взглядом все инструменты и устройства. Вам становится не по себе, и вы решаете поскорее уйти.')
            
        
        else:
            print('\n Загадка успешно решена, но изменений вы не заметили. Зато потренировали мозг.')
    
    else:
        print('\n Неверно. Попробуйте снова.')
        
#логика победы    
def attempt_open_treasure(game_state):
    room_name = game_state['current_room']
    room_info = constants.ROOMS[room_name] #получаем всю информацию о комнате
    puzzle_info = room_info['puzzle'] #получаем информацию конкретно о загадке комнаты
    
    #проверка наличия ключа в инвентаре
    if 'treasure_key' in game_state['player_inventory']:
        print('\n Вы применяете ключ, и замок щёлкает. Сундук открыт!')
            
            #если ключ есть и игрок открыл сундук - удаляем сундук из комнаты
        if 'treasure_chest' in room_info['items']:
            room_info['items'].remove('treasure_chest')
        
        #заканчиваем игру
        print('\n В сундуке сокровище! Вы победили!')
        game_state['game_over'] = True
        return
    
    #если ключа нет - предлагаем ввести код (решив загадку)
    player_choice = player_actions.get_input('\n Сундук заперт. ... Ввести код? (yes/no): ')
    
    #если игрок сказал "да" - выводим загадку
    if player_choice == 'yes':
        treasure_puzzle = room_info['puzzle']
        puzzle_question, puzzle_answer = puzzle_info #присваиваем переменным загадку и ответ на неё + выводим условия загадки
        print('\n', puzzle_question)
        
        #получаем ответ от игрока
        player_answer = player_actions.get_input('Ваш ответ: ')
        
        #сверяем ответ игрока с изначально заложенным в загадку
        if player_answer.lower() == puzzle_answer.lower():
            print('\n Ваш код подошел!')
            
            #если ответ подошел - удаляем сундук
            if 'treasure_chest' in room_info['items']:
                room_info['items'].remove('treasure_chest')
                
            #заканчиваем игру
            print('\n В сундуке сокровище! Вы победили!')            
            game_state['game_over'] = True
        
        #если код не подошел - сообщаем об этом    
        else:
            print('\n Код не подошел.')
        
    #если игрок отказался вводить код        
    else:
        print('\n Вы отступаете от сундука.')
        
#функция помощи
def show_help():
    print("\nДоступные команды:")
    print("  go <direction>  - перейти в направлении (north/south/east/west)")
    print("  look            - осмотреть текущую комнату")
    print("  take <item>     - поднять предмет")
    print("  use <item>      - использовать предмет из инвентаря")
    print("  inventory       - показать инвентарь")
    print("  solve           - попытаться решить загадку в комнате")
    print("  quit            - выйти из игры")
    print("  help            - показать это сообщение")
        
    
    
