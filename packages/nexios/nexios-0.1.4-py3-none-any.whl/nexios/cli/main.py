import argparse
from nexios.cli.create_project import create_project_structure

def main():
    parser = argparse.ArgumentParser(prog="nexio")
    subparsers = parser.add_subparsers(dest="command")
    
    # 'create' subcommand
    create_parser = subparsers.add_parser('create', help="Create a new Nexio project")
    create_parser.add_argument('project_name', type=str, help="The name of the project to create")
    
    args = parser.parse_args()
    
    if args.command == "create":
        create_project_structure(args.project_name)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
