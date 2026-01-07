#функция отображения инвентаря, принимает аргумент - словарь
def show_inventory(game_state):
    player_inventory = game_state['player_inventory'] #присваеваем переменной инвентарь
    
    #проверяем его наполнение
    if player_inventory: 
        print(f'\n {division_str * 50} \n В инвентаре следующие предметы: {', '.join(player_inventory)}.')
    else:
        print('Ваш инвентарь пуст')
        
        
def get_input(prompt="> "):
    try:
        player_command = input(prompt).lower()
        return player_command
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit" 
    
