from selfreplicator.cli import cli
from selfreplicator import training
from selfreplicator.models import toy_model_stoichiometry

def main():
    args = cli.parse_args()
    if args.Selfreplicator_Module == "simulate":
        trainer=training.Trainer.from_json_config(args.input)
        trainer.save_path=args.output
        trainer.train()
        
if __name__ == "__main__":
    main()

# training.Trainer.from_json_config("/Users/parsaghadermarzi/Desktop/Academics/Projects/Selfrep/examples/config.json")