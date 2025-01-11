# this script is for using the invesitgation of the LRA linear resonat actuator 

import argparse

def frequency_range():
    pass



def play_sound():
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Investigate LRA frequency and sound')
    
    parser.add_argument("--mode",
                       type=str, 
                       required=True,
                       choices=['frequency', 'sound'],
                       help="Mode to run: frequency or sound investigation")
    
    args = parser.parse_args()
    
    if args.mode == 'frequency':
        frequency_range()
    elif args.mode == 'sound':
        play_sound()