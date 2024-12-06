#!/usr/bin/env bash

RUNDIR=prior
LOGDIR=$RUNDIR/logs
LABEL=simluation

RESULT_FILE=$RUNDIR/result/${LABEL}_result.json
SAMPLE_FILE=$RUNDIR/result/${LABEL}_samples.hdf5

touch empty.txt

gwpopulation_pipe_collection empty.txt\
  --run-dir $RUNDIR --log-dir $LOGDIR --label $LABEL --data-label $LABEL\
  --parameters mass_1 --parameters mass_ratio --parameters a_1 --parameters a_2 --parameters redshift --parameters cos_tilt_1 --parameters cos_tilt_2\
  --n-simulations 10 --samples-per-posterior 1000 --sample-from-prior True


gwpopulation_pipe_analysis empty.txt\
  --run-dir $RUNDIR --log-dir $LOGDIR --label $LABEL --data-label $LABEL\
  --prior-file test.prior --sampler pymultinest --sampler-kwargs "{nlive: 100}"\
  --enforce-minimum-neffective-per-event True\
  --vt-function ""

gwpopulation_pipe_plot empty.txt --run-dir $RUNDIR --result-file $RESULT_FILE --samples $SAMPLE_FILE

gwpopulation_pipe_to_common_format -r $RESULT_FILE -s $SAMPLE_FILE