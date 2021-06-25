import Supervisor
import argparse
import yaml
'''
Entrypoint for Autograder system.
'''

def run()-> None:
    # Validate and parse argumentss
    args = parse_arguments()

    config = load_config(args.config_path)

    sup = Supervisor(config, None)
    Supervisor.run(folder_path, assignments)


def parse_arguments():
    parser = argparse.ArgumentParser(
        prog = "Automated system for scheduling mass marking")
    parser.add_argument('config_path', metavar='c',
                        type=str, nargs='?', required=True)
    parser.add_argument('output_path', metavar='o',
                        type=str, nargs='?', required=True)
    return parser.parse_args()

def load_config(path):
    return yaml.load(path)

if __name__ == "__main__":
    run()
