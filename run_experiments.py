"""CLI for running key experiments for this project."""
import os
import sys
import argparse
from src.basic_cv_experiment import fit_gm_cv


def get_argparser():
    """Constructs a basic CLI with a menu of available experiments."""
    arg_parser = argparse.ArgumentParser(description="Use this command line app "
            "to run key experiments.")
    arg_parser.add_argument("--gm5xcv", nargs=3, help=
            "Run 5x cross-validations on the GM cell line. First argument "
            "should be filepath of y-values; second argument should be "
            "filepath of xvalues; third argument should be filepath of "
            "motif priorities (to indicate which motifs were selected by "
            "LASSO.",
            metavar=('yvalues', 'xvalues', 'priority'))
    return arg_parser



def setup_logfile(project_path):
    """Checks for the existence of the logfile
    and sets it up if not already present."""
    logfile_path = os.path.join(project_path, "results",
                                "result_log.txt")

    if not os.path.exists(logfile_path):
        with open(logfile_path, "w+") as fhandle:
            fhandle.write("Model,dataset,splitnum,hparams,pearsonr,MAE,time\n")

    return logfile_path



if __name__ == "__main__":
    parser = get_argparser()
    home_dir = os.path.abspath(os.path.dirname(__file__))
    args = parser.parse_args()
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    if args.gm5xcv:
        logfile_path = setup_logfile(home_dir)
        fit_gm_cv(args.gm5xcv[0], args.gm5xcv[1], args.gm5xcv[2],
                  logfile_path)
