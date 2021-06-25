import Supervisor
import sys

'''
Entrypoint for Autograder system.
'''


def run():
    # Validate arguments
    if not has_valid_args():
        print("Please insert valid inputs.")
    # Parse inputs passed in
    # Validate folder strucuture
    config = None # TODO: IMPLEMENT
    # Validate inputs
    # Define assignments
    
    sup = Supervisor(config, None)
    Supervisor.run(folder_path, assignments)

def has_valid_args():


if __name__==  "__main__":
    run()