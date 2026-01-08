import math

from labyrinth_game import constants, player_actions


#функция принмает словарь в качестве аргумента, получает из константы все данные
def describe_current_room(game_state):
    room_name = game_state['current_room']
    room_info = constants.ROOMS[room_name] #получаем всю информацию о комнате
    
    #ввёл разделитель, чтобы было удобнее выводить информацию
    division = '_' * 80 
    
    #теперь выводим её
    print(f'\n {division} \n {room_name.upper()}')
    
    #описание комнаты
    print(f'\n {division} \n {room_info["description"]}')
    
    #проверяем, не нулевое ли значение предметов. Если не нулевое - выводим.
    room_items = room_info['items']
    if room_items:
        print(f'\n {division} \n Заметные предметы: {", ".join(room_items)}')
    
    #выводим, какие выходы есть в комнате
    room_exits = room_info['exits'].keys()
    print(f'\n {division} \n Выходы: {", ".join(room_exits)}')
    
    #так же, как и с предметами, идет проверка на наличие загадки.
    room_puzzle = room_info['puzzle']
    if room_puzzle:
        print(f'\n {division} \n Здесь есть загадка (используйте команду solve).')

def solve_puzzle(game_state):
    room_name = game_state['current_room']
    room_info = constants.ROOMS[room_name] #получаем всю информацию о комнате
    
    #получаем информацию конкретно о загадке комнаты
    puzzle_info = room_info['puzzle'] 
    
    #проверим, есть ли вообще загадка
    if not puzzle_info:
        print('\n В этой комнате загадок нет')

        return #завершаем выполнение функции, если загадок нет
        
    #присваиваем переменным загадку и ответ на неё + выводим условия загадки
    puzzle_question, puzzle_answer = puzzle_info
    print(f'\n Комната содержит следующую загадку: \n {puzzle_question}')
    
    #получаем ответ игрока
    player_answer = player_actions.get_input('\n Ваш ответ на загадку: ')
    
    #т.к. я поменял структуру ответов на загадки в constants, 
    #тут теперь идет проверка по каждому элементу списка ответов
    if player_answer.lower() in [answer.lower() for answer in puzzle_answer]:
        print('\n Вы верно решили загадку! Поздравляем!!')
        room_info['puzzle'] = None
        
        if room_name == 'hall':
            print('\n Вы замечаете, что буквы надписи начали двигаться.')
            print('\n Они создали сообщение по центру: Ученье - свет. Неученье - тьма.')
        
        elif room_name == 'trap_room':
            print('\n Вы чудом избежали смертельного ранения')
            
        elif room_name == 'library':
            print('\n Получив правильный ответ, свиток засверкал')
            print('\n Ученье - свет. Неученье - тьма", промолвили вы')
            print('\n В инвентарь был добавлен ключ от сокровищницы. Знания - сила.')
            game_state['player_inventory'].append('treasure_key')
        
        elif room_name == 'torture_room':
            print('\n Вы решаете ещё раз осмотреть комнату.')
            print('\n Может быть, ответ "3" был секретом к чему-то большему?')
            print('\n Вы окидываете взглядом все инструменты и устройства.')
            print('\n Вам становится не по себе, и вы решаете поскорее уйти.')
            
        
        else:
            print('\n Загадка успешно решена, но изменений вы не заметили.')
            print('\n Зато потренировали мозг.')
    
    else:

        #если игрок ошибся в ответе в trap_room - запускаем trigger_trap()
        if room_name == 'trap_room':
            print('Вы оступились')
            trigger_trap(game_state)
        else:
            print('\n Неверно. Попробуйте снова.')
        
#логика победы    
def attempt_open_treasure(game_state):
    room_name = game_state['current_room']
    
    #получаем всю информацию о комнате
    room_info = constants.ROOMS[room_name]
    
    #получаем информацию конкретно о загадке комнаты
    puzzle_info = room_info['puzzle']
    
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
    player_choice = player_actions.get_input('\n Сундук заперт. Ввести код? (yes/no): ')
    
    #если игрок сказал "да" - выводим загадку
    if player_choice == 'yes':
               
        #присваиваем переменным загадку и ответ на неё
        puzzle_question, puzzle_answer = puzzle_info
        print('\n', puzzle_question)
        
        #получаем ответ от игрока
        player_answer = player_actions.get_input('Ваш ответ: ')
        
        #сверяем ответ игрока с изначально заложенным в загадку
        if player_answer.lower() in [answer.lower() for answer in puzzle_answer]:
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
def show_help(commands):
    for command, description in commands.items():
        print(f"  {command:<16} - {description}")



 #немного случайности в путешествии
def pseudo_random(seed, modulo):
    #возьмем синус от seed, умноженного на число с дробной частью
    sin_seed = math.sin(seed * 12.9898)
    
    #умножим его на другое рандомное число
    sin_seed_multi = sin_seed * 43758.5453
    
    #отбросим целую часть
    sin_seed_multi_fracture = sin_seed_multi - math.floor(sin_seed_multi)
    
    #умножим её на modulo
    final_value = sin_seed_multi_fracture * modulo
    
    #возвращаем целое число
    return int(final_value)

#ловушки повсюду
def trigger_trap(game_state):
    print('\n Ловушка активирована! Пол стал дрожать...')
    
    player_inventory = game_state['player_inventory']
    
    #смотрим, есть ли в инвентаре игрока предметы
    if player_inventory:
    
        #рандомно выбираем один предмет из инвентаря
        item_losing_process = pseudo_random(game_state['steps_taken'], 
                                            len(player_inventory))
        
        #игрок его теряет
        item_lost = player_inventory.pop(item_losing_process)
        
        print(f'\n Вы упали, ударились головой об пол и выронили {item_lost}.')
    
    #нет предметов - роллим урон
    else:
        damage_to_player_rng = pseudo_random(game_state['steps_taken'], 10)
        
        #неповезло - проигрыш
        if damage_to_player_rng < 3:
            print('\n Вы подскользнулись и ударились головой об пол.')
            game_state['game_over'] = True
        
        #повезло - можно играть дальше
        else:
            print('\n Вы чудом уцелели в этой тряске')
        

#случайности не случайны
def random_event(game_state):
    steps_taken = game_state['steps_taken']
    
    #если выпадает 0 - активируется одно событие из трех
    if pseudo_random(steps_taken, 10) == 0:
        scripted_event = pseudo_random(steps_taken, 3)
        print('\n Вы стали свидетелем необычного события.')
        
        #при этом событии в комнату добавляется монетка
        if scripted_event == 0:
            print('\n Вы видите на полу что-то блестящее.')
            room_items = constants.ROOMS[game_state['current_room']]['items']
            room_items.append('coin')
            
        #появляется нечто, которое можно отпугнуть мечом
        if scripted_event == 1:
            print('\n Вы слышите странный шорох.')
            if 'sword' in game_state['player_inventory']:
                print('\n Он стих довольно быстро, как только увидел ваш меч.')
                
        #если игрок находится в trap_room - потеряет предмет или получит урон    
        if scripted_event == 2:
            
            #присваиваем комнату
            player_in_trap_room = game_state['current_room'] == 'trap_room'
            
            #а также отсутствие факела
            player_has_no_torch = 'torch' not in game_state['player_inventory']
            
            if player_in_trap_room and player_has_no_torch:
                print('\n Всё вокруг вас вдруг затряслось!')
                trigger_trap(game_state)
                
    #если выпало что либо кроме 0 - ничего не происходит            
    else:
        return
        
    
