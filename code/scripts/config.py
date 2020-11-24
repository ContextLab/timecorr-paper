import os
import socket

config = dict()

config['template'] = 'run_job.sh'

# ====== MODIFY ONLY THE CODE BETWEEN THESE LINES ======
if (socket.gethostname() == 'Lucys-MacBook-Pro-3.local') or (socket.gethostname() == 'vertex.kiewit.dartmouth.edu') or \
        (socket.gethostname() == 'vertex.local')or (socket.gethostname() == 'vpn-two-factor-general-230-141-43.dartmouth.edu'):
    config['datadir'] = '/Users/lucyowen/Desktop/timecorr_env/timecorr_paper/pieman/data'
    config['workingdir'] = '/Users/lucyowen/Desktop/timecorr_env/timecorr_paper/pieman'
    config['startdir'] = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))  # directory to start the job in
    config['template'] = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'run_job_local.sh')
else:
    config['datadir'] = '/dartfs/rc/lab/D/DBIC/CDL/f002s72/timecorr_paper/pieman/data'
    config['workingdir'] = '/dartfs/rc/lab/D/DBIC/CDL/f002s72/timecorr_paper/pieman'
    config['startdir'] = '/dartfs/rc/lab/D/DBIC/CDL/f002s72'
    config['template'] = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'run_job.sh')

# job creation options
config['scriptdir'] = os.path.join(config['workingdir'], 'scripts')
config['lockdir'] = os.path.join(config['workingdir'], 'locks')
config['resultsdir'] = os.path.join(config['workingdir'], 'results')

# runtime options
config['jobname'] = "timecorr_analysis"  # default job name
config['q'] = "default"  # options: default, testing, largeq
config['nnodes'] = 1  # how many nodes to use for this one job
config['ppn'] = 4  # how many processors to use for this one job (assume 4GB of RAM per processor)
config['walltime'] = '3:00:00'  # maximum runtime, in h:MM:SS
#config['startdir'] = '/ihome/lowen/repos/supereeg/examples'  # directory to start the job in
config['cmd_wrapper'] = "python3"  # replace with actual command wrapper (e.g. matlab, python, etc.)
config['modules'] = "(\"python/3.6\")"  # separate each module with a space and enclose in (escaped) double quotes
# ====== MODIFY ONLY THE CODE BETWEEN THESE LINES ======
