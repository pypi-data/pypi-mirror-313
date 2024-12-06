import os
import shutil
from argparse import ArgumentParser

from bilby.core.utils import logger
from bilby_pipe.parser import StoreBoolean

from .create_injections import create_injections
from .main import check_user

TEMPLATE = """################################################################################
## Generic arguments
################################################################################

label=pp_test_{idx}
run-dir=.
log-dir=logs/{idx}
user={user}
prior-dir=prior_files
vt-model=""
request-gpu={gpu}

################################################################################
## Analysis models
################################################################################

mass-models=[{mass}]
magnitude-models=[{magnitude}]
tilt-models=[{orientation}]
redshift-models=[dummy]

################################################################################
## Data collection arguments
################################################################################

data-label=pp_test_{idx}
injection-file={injection_file}
injection-index={idx}
n-simulations={n_simulation}
sample-from-prior={sample_from_prior}
plot=False

################################################################################
## Post arguments
################################################################################

post-plots=False
make-summary=False
"""


def setup_pp_test():
    parser = ArgumentParser()
    parser.add_argument(
        "--run-dir", default="pp_test", help="Directory to run the test in."
    )
    parser.add_argument("--prior-file", help="Prior file to generate samples from.")
    parser.add_argument(
        "--user", help="albert.einstein style user name.", default=None, type=str
    )
    parser.add_argument(
        "--n-simulation", type=int, default=100, help="Number of jobs to run."
    )
    parser.add_argument(
        "--n-events", type=int, default=40, help="Number of events to simulate per run."
    )
    parser.add_argument(
        "--sample-from-prior",
        action=StoreBoolean,
        help="Simulate posteriors from prior.",
    )
    parser.add_argument(
        "--mass-model",
        choices=["a", "b", "c", "d"],
        default="c",
        help="Mass model to use.",
    )
    parser.add_argument(
        "--magnitude-model",
        choices=["iid", "ind"],
        default="ind",
        help="Spin magnitude model to use.",
    )
    parser.add_argument(
        "--orientation-model",
        choices=["iid", "ind"],
        default="ind",
        help="Spin orientation model to use.",
    )
    parser.add_argument(
        "--submit",
        default=False,
        action=StoreBoolean,
        help="Whether to submit to condor.",
    )
    parser.add_argument(
        "--request-gpu",
        default=False,
        action=StoreBoolean,
        help="Whether to use a GPU for the relevant jobs.",
    )
    args = parser.parse_args()
    args.user = check_user(user=args.user)

    if not os.path.exists(args.run_dir):
        os.mkdir(args.run_dir)

    samples = create_injections(
        prior_file=args.prior_file, n_simulation=args.n_simulation
    )
    injection_file = os.path.abspath(
        os.path.join(args.run_dir, "injection_values.json")
    )
    samples.to_json(injection_file)

    bash_script = f"cd {args.run_dir}\n"
    total_dag = ""
    for ii in range(args.n_simulation):
        config_text = TEMPLATE.format(
            injection_file=injection_file,
            idx=ii,
            user=args.user,
            run_dir=args.run_dir,
            n_simulation=args.n_events,
            gpu=args.request_gpu,
            sample_from_prior=args.sample_from_prior,
            mass=args.mass_model,
            magnitude=args.magnitude_model,
            orientation=args.orientation_model,
        )
        config_filename = os.path.join(args.run_dir, f"config_{ii}.ini")
        with open(config_filename, "w") as ff:
            ff.write(config_text)
        bash_script += f"gwpopulation_pipe config_{ii}.ini\n"
        temp_dag_file = os.path.abspath(
            os.path.join(args.run_dir, "submit", f"pp_test_{ii}.dag")
        )
        total_dag += f"SUBDAG EXTERNAL pp_test_{ii} {temp_dag_file} DIR .\n"
        total_dag += f"RETRY pp_test_{ii} 0\n"

    bash_script += "cd -\n"

    multidag_file = os.path.join(os.path.abspath(args.run_dir), "multidag.dag")
    run_file = os.path.join(os.path.abspath(args.run_dir), "run.sh")

    bash_script += f"condor_submit_dag {multidag_file}\n"

    with open(multidag_file, "w") as ff:
        ff.write(total_dag)

    with open(run_file, "w") as ff:
        ff.write(bash_script)

    with open(os.path.join(args.run_dir, "post.sh"), "w") as ff:
        ff.write(f"bilby_pipe_pp_test .")

    for sub_dir in ["prior_files", "logs"]:
        if not os.path.exists(os.path.join(args.run_dir, sub_dir)):
            os.mkdir(os.path.join(args.run_dir, sub_dir))

    shutil.copy(args.prior_file, os.path.join(args.run_dir, "prior_files"))

    command = f"bash {run_file}"
    if args.submit:
        os.system(command=command)
    else:
        logger.info(f"Now run\n$ {command}")


def main():
    pass
