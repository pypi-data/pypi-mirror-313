#!/usr/bin/env python3

import glob
import itertools
import os
import shutil
import sys
from pathlib import Path

import htcondor
from bilby.core.sampler import get_sampler_class
from bilby.core.utils import logger
from bilby_pipe.utils import convert_string_to_dict, strip_quotes
from bilby_pipe.job_creation.nodes.analysis_node import touch_checkpoint_files
from htcondor import dags

from .parser import create_parser

MASS_MODELS = dict(
    a="gwpopulation.models.mass.power_law_primary_mass_ratio",
    b="gwpopulation.models.mass.power_law_primary_mass_ratio",
    c="SinglePeakSmoothedMassDistribution",
    d="BrokenPowerLawSmoothedMassDistribution",
    e="MultiPeakSmoothedMassDistribution",
    f="BrokenPowerLawPeakSmoothedMassDistribution",
)

REDSHIFT_MODELS = dict(
    powerlaw="gwpopulation.models.redshift.PowerLawRedshift",
    madaudickinson="gwpopulation.models.redshift.MadauDickinsonRedshift",
)


def relative_topdir(path: str, reference: str) -> str:
    """Returns the top-level directory name of a path relative
    to a reference
    """
    try:
        return str(Path(path).resolve().relative_to(reference))
    except ValueError as exc:
        exc.args = (f"cannot format {path} relative to {reference}",)
        raise


def transfer_container(path: str = None) -> bool:
    return path is not None and os.path.exists(path) and not path.startswith("/cvmfs")


def container_lines(args):
    if args.container is None:
        return dict()
    requirements = "HAS_SINGULARITY=?=True"
    if args.backend == "jax":
        requirements = f"({requirements}) && has_avx"
    config = {
        "MY.SingularityImage": f'"{args.container}"',
        "requirements": requirements,
        "transfer_executable": False,
    }
    return config


def create_base(kind, args, gpus=0):
    log_file = f"{args.log_dir}/population-{kind}-$(label)"
    memory = "8GB"
    if transfer_container(args.container):
        disk = "10GB"
    else:
        disk = "4GB"
    config = {
        "universe": "vanilla",
        "initialdir": os.environ["PWD"],
        "executable": getattr(args, f"{kind}_executable"),
        "output": f"{log_file}.out",
        "error": f"{log_file}.err",
        "log": f"{log_file}.log",
        "request_cpus": "1",
        "request_gpus": gpus,
        "request_memory": memory,
        "request_disk": disk,
        "accounting_group": args.accounting,
        "accounting_group_user": args.user,
        "notification": "error",
        "arguments": _arguments(args, kind).format(
            **{var: f"$({var})" for var in _VARIABLES[kind]}
        ),
        "checkpoint_exit_code": 130,
        "MY.flock_local": True,
    }
    if kind == "collection" or args.pool == "local":
        config["MY.DESIRED_Sites"] = '"none"'
    if args.backend == "jax":
        config["requirements"] = "has_avx"
    if gpus:
        config["require_gpus"] = args.require_gpus
    if kind == "summary":
        config["environment"] = f'CONDA_EXE={os.getenv("CONDA_EXE")}'
    config.update(container_lines(args))
    config.update(transfer_files(args, kind))
    job = htcondor.Submit(config)
    return job


def transfer_files(args, kind):
    run_dir = relative_topdir(args.run_dir, os.environ["PWD"])
    ini_file = f"{run_dir}/{args.label}_config_complete.ini"
    data_dir = f"{run_dir}/data"
    result_dir = f"{run_dir}/result"
    model_files = list()
    for model_list in args.all_models.values():
        for model in model_list:
            if model.endswith(".json"):
                model_files.append(os.path.abspath(model))
    if args.source_files is not None:
        source_files = [os.path.abspath(fname) for fname in args.source_files]
    else:
        source_files = list()
    if kind == "summary":
        inputs = [ini_file]
        inputs.extend(
            [f"{run_dir}/result/{label}_result.hdf5" for label in args.labels]
        )
        outputs = [f"{run_dir}/summary"]
    elif kind == "collection":
        if args.vt_file is None:
            inputs = list()
        elif "*" in args.vt_file:
            inputs = glob.glob(args.vt_file)
        else:
            inputs = [args.vt_file]
        inputs += [ini_file, data_dir]
        outputs = [data_dir]
    elif kind == "analysis":
        inputs = [
            f"{data_dir}/{args.data_label}.pkl",
            f"{data_dir}/{args.data_label}_posterior_files.txt",
            os.path.abspath(args.prior_file),
            ini_file,
        ]
        if args.vt_file is not None:
            inputs.append(f"{data_dir}/injections.pkl")
        cls = get_sampler_class(args.sampler)
        files, dirs = cls.get_expected_outputs(outdir=result_dir, label="$(label)")
        inputs.extend(files)
        inputs.extend(dirs)
        inputs.extend(model_files)
        inputs.extend(source_files)
        outputs = [result_dir]
    elif kind == "format":
        inputs = [
            f"{result_dir}/$(label)_result.hdf5",
            f"{result_dir}/$(label)_samples.pkl",
            f"{data_dir}/event_data.json",
        ]
        if args.post_plots:
            spectrum_plots = [
                "mass",
                "magnitude",
                "orientation",
                "redshift",
                "chi_eff_chi_p",
            ]
            inputs.extend(
                [
                    f"{result_dir}/$(label)_{key}_data.h5"
                    for key in spectrum_plots
                    if key in args.all_models
                ]
            )
        if args.vt_file is not None:
            inputs.append(f"{data_dir}/injections.pkl")
        inputs.extend(model_files)
        inputs.extend(source_files)
        outputs = [
            f"{result_dir}/$(label)_full_posterior.hdf5",
            f"{result_dir}/$(label)_popsummary_result.h5",
        ]
    elif kind == "plot":
        inputs = [
            ini_file,
            f"{result_dir}/$(label)_result.hdf5",
            f"{result_dir}/$(label)_samples.pkl",
        ]
        if args.vt_file is not None:
            inputs.append(f"{data_dir}/injections.pkl")
        inputs.extend(model_files)
        inputs.extend(source_files)
        outputs = [result_dir]
    else:
        raise ValueError(f"Unknown job type: {kind}")
    if transfer_container(args.container):
        inputs.append(args.container)
    return dict(
        should_transfer_files="YES",
        transfer_input_files=f"{','.join(inputs)}",
        transfer_output_files=f"{','.join(outputs)}",
        when_to_transfer_output="ON_EXIT_OR_EVICT",
        preserve_relative_paths=True,
        stream_error=True,
        stream_output=True,
    )


def _arguments(args, kind):
    run_dir = relative_topdir(args.run_dir, os.environ["PWD"])
    ini_file = f"{run_dir}/{args.label}_config_complete.ini"
    data_dir = f"{run_dir}/data"
    result_dir = f"{run_dir}/result"
    if args.vt_file is not None:
        vt_file = f"{data_dir}/injections.pkl"
    else:
        vt_file = args.vt_file
    if kind == "analysis":
        arguments = (
            f"{ini_file} --run-dir {run_dir} --label {{label}} "
            f"{{models}} {{vt_models}} --vt-file {vt_file}"
        )
    elif kind == "collection":
        arguments = f"{ini_file} --run-dir {run_dir}"
    elif kind == "format":
        arguments = (
            f"--result-file {result_dir}/{{label}}_result.hdf5 "
            f"--n-samples {args.n_post_samples} --max-redshift {args.max_redshift} "
            f"--minimum-mass {args.minimum_mass} --maximum-mass {args.maximum_mass} "
            f"--injection-file {vt_file} "
            f"--filename {result_dir}/{{label}}_full_posterior.hdf5 "
            f"--samples-file {result_dir}/{{label}}_samples.pkl "
            f"--vt-ifar-threshold {args.vt_ifar_threshold} "
            f"--vt-snr-threshold {args.vt_snr_threshold} "
            f"--backend {args.backend} --cosmology {args.cosmology} "
            f"--make-popsummary-file {args.make_popsummary_file} "
            f"--popsummary-file {result_dir}/{{label}}_popsummary_result.h5 "
            f"--event-data-file {data_dir}/event_data.json "
        )
        if args.cosmo:
            arguments += f"--cosmo "
    elif kind == "plot":
        arguments = (
            f"{ini_file} --run-dir {run_dir} "
            f"--result-file {result_dir}/{{label}}_result.hdf5 "
            f"--samples {result_dir}/{{label}}_samples.pkl "
        )
    elif kind == "summary":
        result_files = " ".join(
            [f"{result_dir}/{label}_result.hdf5" for label in args.labels]
        )
        arguments = (
            f"--config {ini_file} --webdir {run_dir}/summary "
            f"--samples {result_files} --labels {' '.join(args.labels)}"
        )
    return arguments


_VARIABLES = dict(
    analysis=["label", "models", "vt_models"],
    collection=list(),
    format=["label"],
    plot=["label"],
    summary=list(),
)


def check_user(user=None):
    if user is None:
        if "USER" in os.environ:
            user = os.environ.get["USER"]
        else:
            raise ValueError(
                "Argument 'user' must be provided or set in environment variables!"
            )
    return user


def make_submit_files(args):
    subfiles = ["analysis", "collection", "common_format"]
    if args.post_plots:
        subfiles.append("plot")
    if args.make_summary:
        subfiles.append("summary")

    uses_gpu = ["analysis", "common_format", "plot"]

    jobs = dict()
    for label in subfiles:
        if label in uses_gpu:
            gpus = args.request_gpu
        else:
            gpus = 0
        jobs[label] = create_base(label.split("_")[-1], args, gpus)
    return jobs


def update_args(args):
    args.user = check_user(user=args.user)
    args.accounting = "ligo.dev.o4.cbc.bayesianpopulations.parametric"
    args.run_dir = os.path.abspath(args.run_dir)
    args.log_dir = os.path.abspath(args.log_dir)
    args.request_gpu = int(args.request_gpu)

    args.all_models = convert_string_to_dict(args.all_models)
    if args.conda_env is not None:
        env_path = f"{args.conda_env}/bin"
    elif args.container is not None:
        env_path = ""
    else:
        env_path = shutil.which("gwpopulation_pipe").rsplit("/", maxsplit=1)[0]
    if not env_path.endswith("/"):
        env_path += "/"
    args.analysis_executable = f"{env_path}gwpopulation_pipe_analysis"
    args.collection_executable = f"{env_path}gwpopulation_pipe_collection"
    args.format_executable = f"{env_path}gwpopulation_pipe_to_common_format"
    args.plot_executable = f"{env_path}gwpopulation_pipe_plot"
    args.summary_executable = f"{env_path}summarypages"
    args.custom_plotting = (
        os.path.join(os.path.dirname(__file__), "pesummary_plot.py"),
    )
    args.condor_dir = os.path.join(args.run_dir, "submit")
    args.result_dir = os.path.join(args.run_dir, "result")
    args.summary_dir = os.path.join(args.run_dir, "summary")
    args.data_dir = os.path.join(args.run_dir, "data")


def create_directories(args):
    for directory in [
        args.run_dir,
        args.log_dir,
        args.condor_dir,
        args.result_dir,
        args.data_dir,
        args.summary_dir,
    ]:
        if not os.path.isdir(directory):
            os.mkdir(directory)
        elif not os.path.isdir(directory):
            raise IOError(f"{directory} exists and is not a directory.")

    if os.path.isdir(args.existing_data_directory):
        os.rmdir(args.data_dir)
        os.symlink(
            os.path.abspath(args.existing_data_directory),
            os.path.abspath(args.data_dir),
        )
        do_collection = False
    else:
        do_collection = True
    return do_collection


def reduce_name(value):
    if value.endswith(".json"):
        value = value[:-5]
    return value.split(".")[-1]


def write_bash_file(variables, args, bash_file):
    bash_str = "#! /bin/bash\n\n"
    bash_str += f"echo 'Moving to {os.environ['PWD']}'\n"
    bash_str += f"cd {os.environ['PWD']}\n\n"
    if "collection" in variables:
        bash_str += f"{args.collection_executable} {_arguments(args, 'collection')}\n\n"
    for avar, pvar, fvar in zip(
        variables["analysis"], variables["plot"], variables["common_format"]
    ):
        bash_str += f"{args.analysis_executable} {_arguments(args, 'analysis').format(**avar)}\n\n"
        bash_str += (
            f"{args.plot_executable} {_arguments(args, 'plot').format(**pvar)}\n\n"
        )
        bash_str += (
            f"{args.format_executable} {_arguments(args, 'format').format(**fvar)}\n\n"
        )
    if "summary" in variables:
        bash_str += f"{args.summary_executable} {_arguments(args, 'summary')}\n\n"
    bash_str += "cd -\n"
    with open(bash_file, "w") as ff:
        ff.write(bash_str)


def make_dag(args):
    update_args(args)
    do_collection = create_directories(args)

    all_variables = dict()
    if do_collection:
        all_variables["collection"] = [dict(label=args.label)]

    run_dir = relative_topdir(args.run_dir, os.environ["PWD"])

    job_names = list()
    result_files = list()

    all_variables["analysis"] = list()
    all_variables["plot"] = list()
    all_variables["common_format"] = list()

    for values in itertools.product(*args.all_models.values()):
        models = dict(zip(args.all_models.keys(), values))
        prior_name = "_".join(
            [f"{key}_{reduce_name(value)}" for key, value in models.items()]
        )
        job_name = f"{args.label}_{prior_name}"
        job_names.append(job_name)
        result_files.append(f"{run_dir}/result/{job_name}_result.hdf5")

        if models.get("mass", None) in MASS_MODELS:
            models["mass"] = MASS_MODELS[models["mass"]]
        if models.get("redshift", None) in REDSHIFT_MODELS:
            models["redshift"] = REDSHIFT_MODELS[models["redshift"]]
        vt_models = dict()
        for key in models:
            if key in args.vt_parameters:
                vt_models[key] = models[key]
        for key in args.vt_parameters:
            if key not in models:
                logger.error(
                    f"VT parameter {key} not in models. Names in vt-parameters must be in models."
                )
        if len(vt_models) == 0:
            vt_models = {key: models[key] for key in ["mass", "redshift"]}

        models = "--models " + " --models ".join(
            [f"{key}:{value}" for key, value in models.items()]
        )
        vt_models = "--vt-models " + " --vt-models ".join(
            [f"{key}:{value}" for key, value in vt_models.items()]
        )

        all_variables["analysis"].append(
            dict(label=job_name, models=models, vt_models=vt_models)
        )
        touch_checkpoint_files(
            directory=args.result_dir,
            label=job_name,
            sampler=args.sampler,
            result_format="hdf5",
        )

        all_variables["plot"].append(dict(label=job_name))
        all_variables["common_format"].append(dict(label=job_name))

    args.labels = job_names

    if args.make_summary:
        all_variables["summary"] = [dict()]

    def layer_kwargs(kind):
        return dict(
            name=f"{args.condor_dir}/{kind}",
            submit_description=jobs[kind],
            vars=all_variables[kind],
        )

    dag = dags.DAG()
    jobs = make_submit_files(args)
    if do_collection:
        collection_layer = dag.layer(**layer_kwargs("collection"))
        next_layer = collection_layer.child_layer
    else:
        next_layer = dag.layer
    analysis_layer = next_layer(**layer_kwargs("analysis"))
    edges = dict(plot=dags.OneToOne(), common_format=dags.OneToOne(), summary=None)
    if args.post_plots:
        plot_layer = analysis_layer.child_layer(
            edge=edges["plot"], **layer_kwargs("plot")
        )
        plot_layer.child_layer(
            edge=edges["common_format"], **layer_kwargs("common_format")
        )
    else:
        analysis_layer.child_layer(
            edge=edges["common_format"], **layer_kwargs("common_format")
        )
    if args.make_summary:
        analysis_layer.child_layer(edge=edges["summary"], **layer_kwargs("summary"))

    bash_file = f"{args.condor_dir}/{args.label}.sh"
    dag_file = f"{args.condor_dir}/{args.label}.dag"

    dags.write_dag(dag, args.condor_dir, dag_file_name=f"{args.label}.dag")
    write_bash_file(all_variables, args, bash_file)

    print(f"dag file written to {dag_file}")
    print(f"shell script written to {bash_file}")
    print(f"Now run condor_submit_dag {dag_file}")


def main():
    parser = create_parser()
    args, _ = parser.parse_known_args(sys.argv[1:])

    complete_ini_file = f"{args.run_dir}/{args.label}_config_complete.ini"
    make_dag(args)
    parser.write_to_file(
        filename=complete_ini_file,
        args=args,
        overwrite=True,
        include_description=False,
    )
    with open(complete_ini_file, "r") as ff:
        content = ff.readlines()
    for ii, line in enumerate(content):
        content[ii] = strip_quotes(line)
    with open(complete_ini_file, "w") as ff:
        ff.writelines(content)
