from colorama import Fore

import os

def clear_console():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

class MenuAction(object):
    def __init__(self, title, func):
        self.title = title
        self.function = func

    def render_title(self):
        return self.title
    
    def run(self):
        if isinstance(self.function, ViewMenu):
            self.function.view()
        else:
            self.function()

class OptionAction(object):
    def __init__(self, args, title, action, args_names, choices=[], default_value=None, data_type=str, data_range=None):
        self.args = args
        self.title = title
        self.action = action
        self.value = default_value
        self.choices = choices
        self.args_names = args_names
        self.data_type = data_type
        self.data_range = data_range

    def render_title(self):
        if self.action in ['store_true', 'choice']:
            return f'{self.title} (selected: {Fore.YELLOW}{self.value}{Fore.RESET})'
        elif self.action == 'manual_input':
            return f'{self.title} (saved: {Fore.YELLOW}{self.value}{Fore.RESET})'
        elif self.action == 'bool_switch':
            if self.args[self.args_names.replace('-', '_')]:
                return f'{self.title} {Fore.GREEN}(enabled){Fore.RESET}'
            return f'{self.title} {Fore.RED}(disabled){Fore.RESET}'
        
    def run(self):
        if self.action == 'bool_switch':
            self.args[self.args_names.replace('-', '_')] = not self.args[self.args_names.replace('-', '_')]
            return True
        execution = True
        while True:
            clear_console()
            print(self.title+'\n')
            menu_items = []
            if self.choices != []:
                menu_items = self.choices
            else:
                menu_items = self.args_names
            if self.action != 'manual_input':
                for index in range(0, len(menu_items)):
                    menu_item = menu_items[index]
                    print(f'{index+1} - {menu_item}')
                print()
            try:
                if self.action == 'manual_input':
                    while True:
                        if self.data_range is not None:
                            print('Allowed values: '+str(self.data_range)+'\n')
                        self.value = input('>>> ').strip()
                        try:
                            self.value = self.data_type(self.value)
                            if self.data_range is not None:
                                if self.value not in self.data_range:
                                    raise
                            self.args[self.args_names.replace('-', '_')] = self.value # self.args_names is str
                            execution = False
                            break
                        except:
                            clear_console()
                            print(self.title+'\n')
                if not execution:
                    break
                index = int(input('>>> ').strip()) - 1
                self.value = menu_items[index]
                if index in range(0, len(menu_items)):
                    if self.action == 'store_true':
                        for args_name in self.args_names: # self.args_names is list
                            self.args[args_name.replace('-', '_')] = False
                        self.args[self.value.replace('-', '_')] = True # self.value == args_name
                    elif self.action == 'choice':
                        self.args[self.args_names.replace('-', '_')] = self.value # self.args_names is str
                    break
            except ValueError:
                pass

class ViewMenu(object):
    def __init__(self, title):
        self.title = title
        self.items = []
        self.execution = True

    def add_item(self, menu_action_object: MenuAction):
        self.items.append(menu_action_object)
    
    def view(self):
        self.execution = True
        while self.execution:
            clear_console()
            print(self.title+'\n')
            for item_index in range(0, len(self.items)):
                item = self.items[item_index]
                print(f'{item_index+1} - {item.render_title()}')
            print()
            try:
                selected_item_index = int(input('>>> ')) - 1
                if selected_item_index in range(0, len(self.items)):
                    self.items[selected_item_index].run()
            except ValueError:
                pass
    
    def close(self):
        self.execution = False