from colorama import Fore, init as colorama_init

import decimal
import platform
import sys

colorama_init()

class ProgressBarStyle:
    def __init__(self, advance_char='█', empty_advance_char='▓', progressbar_length=30):
        self.advance_char = advance_char
        self.empty_advance_char = empty_advance_char
        self.progressbar_length = progressbar_length

DEFAULT_STYLE = ProgressBarStyle()
DEFAULT_RICH_STYLE = ProgressBarStyle(f'{Fore.GREEN}━{Fore.RESET}', f'{Fore.LIGHTBLACK_EX}━{Fore.RESET}', 41)
CLASSIC_STYLE = ProgressBarStyle(f'{Fore.GREEN}█{Fore.RESET}', f'{Fore.LIGHTBLACK_EX}▓{Fore.RESET}')
DRACULA_STYLE = ProgressBarStyle(f'{Fore.RED}█{Fore.RESET}', f'{Fore.LIGHTRED_EX}▓{Fore.RESET}')
GIRL_STYLE    = ProgressBarStyle(f'{Fore.LIGHTMAGENTA_EX}█{Fore.RESET}', f'{Fore.MAGENTA}▓{Fore.RESET}')
DARK_STYLE    = ProgressBarStyle(f'{Fore.LIGHTBLACK_EX}█{Fore.RESET}', ' ')
RAINBOW_STYLE = ProgressBarStyle(f'{Fore.RED}█{Fore.CYAN}█{Fore.YELLOW}█{Fore.GREEN}█{Fore.BLUE}█{Fore.MAGENTA}█{Fore.RESET}', '', 10)

class ProgressBar:
    def __init__(self, total, description: str, progress_bar_style=DEFAULT_STYLE):
        self.advance = 0
        self.total = total
        self.description = description
        self.progressbar_length = progress_bar_style.progressbar_length
        self.advance_char = progress_bar_style.advance_char
        self.empty_advance_char = progress_bar_style.empty_advance_char
        self.advance_char_coef = round(self.total/self.progressbar_length, 2)

    @property
    def is_finished(self):
        return self.advance == self.total
    
    def force_finish(self):
        self.advance = self.total

    def render(self):
        if self.is_finished:
            advance_char_count = self.progressbar_length
        else:
            advance_char_count = int(self.advance/self.advance_char_coef)
        advance_percent = round(decimal.Decimal(self.advance/self.total), 2)*100
        if platform.release() == '7' and sys.platform.startswith('win'): # disable rendering for windows 7 (cmd.exe does not support ASCII control characters)
            pass
        else:
            print(f'{self.description}{self.advance_char*advance_char_count}{self.empty_advance_char*(self.progressbar_length-advance_char_count)} {advance_percent}%')
            print('\033[F', end='')
            if self.is_finished:
                print()
            
    def update(self, count):
        self.advance += count