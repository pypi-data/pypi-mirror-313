import argparse
from selfreplicator import __version__
cli = argparse.ArgumentParser(prog="SelfReplicator",
        description="SelfReplicator is a tool to simulate and visualize for the selfreplicator model.",
        epilog="Selfreplicator Chan Lab at Colorado State University.")
cli.add_argument("-v", "--version", action="version", version=f"{cli.prog} {__version__}")
cli.version = __version__
subparser=cli.add_subparsers(dest="Selfreplicator_Module", help='Selfreplicator Modules:')      
subparser.required = True
simulate=subparser.add_parser('simulate', help='Simulate the selfreplicator model.')
visualize=subparser.add_parser('visualize', help='Plot the selfreplicator model.')
simulate.add_argument("-i", "--input", type=str, help="The address to the json config file.",required=True)  
simulate.add_argument("-o", "--output", type=str, help="The address to save the output files.", required=True)
