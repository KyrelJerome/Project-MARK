# import Supervisor
import argparse
import yaml
import sys
'''
Entrypoint for Autograder system.
'''

def run()-> None:
    # Validate and parse argumentss
    args = parse_arguments()

    config = load_config(args.config_path)


    # print(config["assignments"][1]["name"])

    # sup = Supervisor(config, None)
    # Supervisor.run(folder_path, assignments)


def parse_arguments():
    parser = argparse.ArgumentParser(prog = "Automated system for scheduling mass marking")
    parser.add_argument('config_path', type=str)
    return parser.parse_args()

def load_config(path):
    try:
        with open(path, 'r') as f:
            data = yaml.load(f, Loader=yaml.SafeLoader)
            if data["program"] == "M.A.R.K":
                print("- Configuration file \""+path+"\" recognized.\n- M.A.R.K Configuration Loading...")
    except Exception as e:
        print("- The file given is eiter not a \".yaml\" file or a not the config file that the program needs.\n- {}".format(e))
        sys.exit(1)

    return data

if __name__ == "__main__":
    run()
