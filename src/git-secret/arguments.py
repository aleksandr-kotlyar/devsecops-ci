import os
import getopt
from dataclasses import dataclass
from config import Config


@dataclass
class Arguments():
    verbose: bool = False
    help: bool = False
    target_dir: str = None
    branch: str = None
    commit_range: str = None
    config: Config = None

    @staticmethod
    def helptext():
        return "USAGE: python main.py --target-dir=/path/to/your/code [--verbose] [--commit-range=rev1..rev2]"

    @staticmethod
    def parse(args):
        config_filename = None
        result = Arguments()
        try:
            opts, args = getopt.getopt(args,
                                       "hv=",
                                       ["help",
                                        "verbose=",
                                        "conf-file=",
                                        "target-dir=",
                                        "commit-range="])
        except getopt.GetoptError as e:
            print(e)
            return None
        for o, a in opts:
            if o in ("-v", "--verbose"):
                result.verbose = (a != "no")
            elif o in ("-h", "--help"):
                result.help = True
            elif o in ("--conf-file"):
                config_filename = a
            elif o in ("--target-dir"):
                result.target_dir = a
            elif o in ("--commit-range"):
                result.commit_range = a if a else None

        if result.target_dir:
            if not config_filename:
                config_filename = ".devsecops-ci"
            conf_file = os.path.join(result.target_dir, config_filename)
            result.config = Config.load(conf_file)

        if result.config is None:
            result.config = Config()

        return result
