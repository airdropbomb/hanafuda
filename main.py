import os
import sys
import time
from colorama import init
from src.deeplchain import _clear, _banner, kng, mrh, bru, hju, pth, log, read_config, countdown_timer

config = read_config()
init(autoreset=True)

def run_grows():
    os.system('python src/grows.py')

def run_gardens():
    os.system('python src/gardens.py')

def run_hanafuda():
    os.system('python src/hanafuda.py')

def main():
    _clear()
    _banner()
    countdown_before_start = config.get('countdown_before_start', 10)
    while True:
        try:
            menu = f"""
 {hju}Select an option:
  {kng}1. Execute {pth}Grow {kng}Actions
  {kng}2. Execute {pth}Garden {kng}Actions
  {kng}3. Execute {pth}Deposit {kng}Actions
  {kng}4. Exit
            """
            print(menu)
            choice = input(" Enter your choice (1,2,3,4): ")

            if choice == '1':
                log(hju + f"Preparing your grow data!")
                countdown_timer(countdown_before_start)
                run_grows()
            elif choice == '2':
                log(hju + f"Preparing your garden data!")
                countdown_timer(countdown_before_start)
                run_gardens()
            elif choice == '3':
                log(hju + f"Preparing your deposit data!")
                time.sleep(2)
                run_hanafuda()
            elif choice == '4':
                break
            else:
                print("Invalid choice. Please try again.")
        except KeyboardInterrupt as e:
            sys.exit()

if __name__ == '__main__':
    main()
