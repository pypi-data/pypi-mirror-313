import bilby
import gwpopulation
import wcosmo
import numpy as np
from bilby_pipe.bilbyargparser import BilbyArgParser
from bilby_pipe.parser import StoreBoolean
from bilby_pipe.utils import noneint, nonestr


def create_parser():
    from ._version import __version__

    parser = BilbyArgParser(
        usage=__doc__, ignore_unknown_config_file_keys=False, allow_abbrev=False
    )
    parser.add("ini", type=str, is_config_file=True, help="Configuration ini file")
    parser.add("-v", "--verbose", action="store_true", help="Verbose output")
    parser.add(
        "--version",
        action="version",
        version="%(prog)s={version}\nbilby={bilby_version}\ngwpopulation={gwpopulation_version}".format(
            version=__version__,
            bilby_version=bilby.__version__,
            gwpopulation_version=gwpopulation.__version__,
        ),
    )

    base_parser = parser.add_argument_group(
        title="Generic arguments", description="Generic arguments"
    )

    base_parser.add_argument(
        "--run-dir",
        type=str,
        default="outdir",
        help="Output directory for posterior samples",
    )
    base_parser.add_argument(
        "--log-dir",
        type=str,
        default="logs",
        help="Output directory for writing log files",
    )
    base_parser.add_argument("--label", type=str, default="label", help="Run label")
    base_parser.add_argument("--user", type=str, help="User name", default=None)
    base_parser.add_argument(
        "--vt-file",
        type=nonestr,
        default=None,
        help="File to load VT data from or a glob string matching multiple files to combine.",
    )
    base_parser.add_argument(
        "--vt-ifar-threshold",
        type=float,
        default=1,
        help="IFAR threshold for resampling injections",
    )
    base_parser.add_argument(
        "--vt-snr-threshold",
        type=float,
        default=11,
        help="IFAR threshold for resampling injections. "
        "This is only used for O1/O2 injections",
    )
    base_parser.add_argument(
        "--vt-function",
        type=str,
        default="injection_resampling_vt",
        help="Function to generate selection function from.",
    )
    base_parser.add_argument(
        "--prior-file",
        type=str,
        help="Prior file containing priors for all considered parameters",
    )
    base_parser.add_argument(
        "--request-gpu",
        default=0,
        help="Whether to request a GPU for the relevant jobs.",
    )
    base_parser.add_argument(
        "--require-gpus",
        default='DeviceName=="GeForce GTX 1050 Ti"',
        type=str,
        help="The GPU requirements to pass for HTCondor.",
    )
    base_parser.add_argument(
        "--backend",
        default="jax",
        choices=gwpopulation.backend.SUPPORTED_BACKENDS,
        type=str,
        help="The backend to use for the analysis, default is jax",
    )
    base_parser.add_argument(
        "--cosmo",
        action=StoreBoolean,
        default=False,
        help="Whether to fit cosmological parameters.",
    )
    base_parser.add_argument(
        "--cosmology",
        type=str,
        default="Planck15_LAL",
        help=(
            "Cosmology to use for the analysis, this should be one of "
            f"{', '.join(wcosmo.available.keys())}, Planck15_LAL. Some of these are "
            "fixed pre-defined cosmologies while others are parameterized "
            "cosmologies. If a parameterized cosmology is used the parameters relevant"
            " parameters should be included in the prior specification."
        ),
    )
    base_parser.add_argument(
        "--container",
        type=nonestr,
        default=None,
        help="The path to the singularity image to use",
    )
    base_parser.add_argument(
        "--conda-env", type=nonestr, default=None, help="The conda environment to use"
    )
    base_parser.add_argument(
        "--pool",
        type=str,
        choices=["osg", "local"],
        default="osg",
        help="Which HTCondor pool to submit to, if osg, the local pool is also allowed",
    )

    model_parser = parser.add_argument_group(
        title="Analysis models", description="Analysis models"
    )
    model_parser.add_argument(
        "--all-models", type=str, help="All models to use, formatted as a json string"
    )
    model_parser.add_argument(
        "--source-files",
        action="append",
        help=(
            "Files containing source models to use for user-defined models. "
            "These files are transferred to the execute node when using the "
            "HTCondor file transfer mechanism. If the job is being run "
            "locally the file should be in the users PYTHONPATH."
        ),
    )

    collection_parser = parser.add_argument_group(
        title="Data collection arguments", description="Data collection arguments"
    )
    collection_parser.add_argument(
        "--existing-data-directory",
        type=str,
        default="/fail",
        help="Directory containing existing data",
    )
    collection_parser.add_argument(
        "--parameters",
        action="append",
        help=(
            "Parameters that are fit with the model. "
            "These are the parameters that will be extracted from the posterior samples "
            "and should follow Bilby naming conventions with the exception that all masses "
            "are assumed to be in the source frame. Here is a list of parameters for which "
            "prior factors will be properly accounted. "
            "mass_1: source frame primary mass, mass_2: source frame secondary mass, "
            "mass_1_detector: detector frame primary mass, mass_2_detector: detector frame secondary mass, "
            "chirp_mass: source frame chirp mass, chirp_mass_detector: detector frame chirp mass,"
            "mass_ratio: mass ratio, redshift: redshift, luminosity_distance: luminosity distance,"
            "a_1: primary spin magnitude, a_2: secondary spin magnitude, cos_tilt_1: "
            "cosine primary spin tilt, cos_tilt_2: cosine secondary spin tilt, "
            "chi_1: aligned primary spin, chi_2: aligned secondary spin."
            "Any other parameters will be assumed to have a flat prior."
            "These parameters are also used to set the fiducial prior values. "
            "No redundancy checks are performed so users should be careful to not "
            "include unused parameters as that may have unintended consequences."
        ),
    )
    collection_parser.add_argument(
        "--ignore", action="append", help="Events to ignore."
    )
    collection_parser.add_argument(
        "--sample-regex", type=str, help="Pattern to match for sample files"
    )
    collection_parser.add_argument(
        "--preferred-labels",
        action="append",
        help="Run labels to search for in sample files",
    )
    collection_parser.add_argument(
        "--plot",
        default=True,
        action=StoreBoolean,
        help="Whether to generate diagnostic plots",
    )
    collection_parser.add_argument(
        "--n-simulations", type=noneint, help="Number of posteriors to simulate"
    )
    collection_parser.add_argument(
        "--samples-per-posterior",
        type=int,
        default=int(1e6),
        help="Number of samples per posterior. If larger than the number of samples in the shortest posterior dataset, will ignore this input.",
    )
    collection_parser.add_argument(
        "--collection-seed",
        type=noneint,
        help="Seed for the downsampling of the posteriors for each event. For reproducibility.",
    )
    collection_parser.add_argument(
        "--data-label", default="posteriors", help="Label for data product."
    )
    collection_parser.add_argument(
        "--distance-prior",
        default="comoving",
        type=str,
        help=(
            "Distance prior format, e.g., euclidean, comoving. 'euclidean' assumes the distance prior goes "
            "like D^2. 'comoving' assumes sources are uniformly distributed in the comoving frame using "
            "the Planck15_LAL cosmology. Can be in the format of a dict with the same keys as the sample-regex"
        ),
    )

    collection_parser.add_argument(
        "--mass-prior",
        default="flat-detector",
        type=str,
        help=(
            "Mass prior used during the initial sampling, must match one of the following options. "
            "\n 'flat-detector': Flat in detector frame primary and secondary masses. "
            "\n 'chirp-mass': Flat in detector frame chirp mass and mass ratio. "
            "\n 'flat-detector-components': Flat in detector frame primary and secondary masses. "
            "This is the default for LVK samples and the same as the deprecated 'flat-detector' option. "
            "\n 'flat-source-components': Flat in source frame primary and secondary masses. "
            "\n 'flat-detector-chirp-mass-ratio': Flat in detector frame chirp mass and mass ratio. "
            "This is the same as the deprecated 'chirp-mass' option. Can be in the format of a dict with the same keys as the sample-regex"
        ),
    )
    collection_parser.add_argument(
        "--spin-prior",
        default="component",
        type=str,
        help=(
            "Spin prior, the only supported spin prior assumes the spins are isotropically distributed "
            "with a flat prior on the magnitude. Can be in the format of a dict with the same keys as the sample-regex."
        ),
    )

    analysis_parser = parser.add_argument_group(
        title="Arguments describing analysis jobs", description="Analysis arguments"
    )
    analysis_parser.add_argument(
        "--max-redshift",
        default=2.3,
        type=float,
        help="The maximum redshift considered, this should match the injections.",
    )
    analysis_parser.add_argument(
        "--minimum-mass",
        default=2,
        type=float,
        help="The minimum mass considered, this should match the injections "
        "and is important for smoothed mass models.",
    )
    analysis_parser.add_argument(
        "--maximum-mass",
        default=100,
        type=float,
        help="The maximum mass considered, this should match the injections "
        "and is important for smoothed mass models.",
    )
    analysis_parser.add_argument(
        "--sampler",
        default="dynesty",
        type=str,
        help="The sampler to use, the default is dynesty",
    )
    analysis_parser.add_argument(
        "--sampler-kwargs",
        type=str,
        default="Default",
        help=(
            "Dictionary of sampler-kwargs to pass in, e.g., {nlive: 1000} OR "
            "pass pre-defined set of sampler-kwargs {Default, FastTest}"
        ),
    )
    analysis_parser.add_argument(
        "--vt-parameters",
        action="append",
        help=(
            "Which parameters to include in the VT estimate, should be some "
            "combination of mass, redshift, spin parameters, see the '--parameters' "
            "option for more details."
        ),
    )
    analysis_parser.add_argument(
        "--enforce-minimum-neffective-per-event",
        action=StoreBoolean,
        default=True,
        help=(
            "Require that all Monte Carlo integrals for the single event "
            "marignalizaed likleihoods have at least as many effective samples"
            " as the number of events."
        ),
    )

    analysis_parser.add_argument(
        "--maximum-uncertainty",
        type=float,
        default=np.inf,
        help=(
            "Require that all log likelihood evaluations have an uncertainty (standard deviation) less than"
            " this value. It is not recommended to use with the '--enforce-minimum-neffective-per-event' option."
            "See Talbot and Golomb (2023) arxiv:2304.06138"
        ),
    )
    analysis_parser.add_argument(
        "--periodic-restart-time",
        type=noneint,
        default=None,
        help=(
            "The periodic restart time for running on HTCondor, this should be set when using the "
            "HTCondor file transfer system to avoid losing progress on eviction. "
            "See https://computing.docs.ligo.org/guide/htcondor/checkpointing/ for more details."
        ),
    )

    injection_parser = parser.add_argument_group(
        title="Arguments describing injections", description="Injection arguments"
    )
    injection_parser.add_argument(
        "--injection-file",
        default=None,
        type=nonestr,
        help="JSON file containing population parameters, should be pandas readable.",
    )
    injection_parser.add_argument(
        "--injection-index", type=noneint, help="Index in injection file to use."
    )
    injection_parser.add_argument(
        "--sample-from-prior",
        action=StoreBoolean,
        help="Simulate posteriors from prior.",
    )

    post_parser = parser.add_argument_group(
        title="Post processing arguments", description="Post arguments"
    )
    post_parser.add_argument(
        "--post-plots",
        action=StoreBoolean,
        default=True,
        help="Whether to make post-processing plots.",
    )
    post_parser.add_argument(
        "--make-summary",
        action=StoreBoolean,
        default=True,
        help="Whether to make a summary page.",
    )
    post_parser.add_argument(
        "--n-post-samples",
        default=5000,
        type=int,
        help="Number of samples to use in the common format script",
    )
    post_parser.add_argument(
        "--make-popsummary-file",
        action=StoreBoolean,
        default=True,
        help="Whether to make a summary result file in popsummary format.",
    )

    return parser
