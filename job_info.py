#
# quick attempt at colorizing job information from Slurm
# aspirations of making useful, console-based admin tools
#

import subprocess
import sys

class tcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_progress_bar(index, total, label=''):
    n_bar = 10  # Progress bar width
    progress = index / total
    sys.stdout.write(f"[{'=' * int(n_bar * progress):{n_bar}s}] {int(100 * progress)}%  {label}")
    sys.stdout.flush()
    
q_partition = 'batch'
slurm_cmd = 'sinfo --Format=All ' + ' --partition=' + q_partition
print("slurm_cmd = ", slurm_cmd)
p = subprocess.Popen(slurm_cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
output = p.stdout.read().decode()

# first row is keys
# each row after is data

rows = output.splitlines()

# strip all the whitespace from the first row which are the headers/keys
keys = []
for k in rows[0].split('|'):
  keys.append(k.strip())

headers = dict()
for i,h in enumerate(keys):
  headers[h] = i

for r in rows:
  # strip all whitespace from each item in the row
  node = []
  for k in r.split('|'):
    node.append(k.strip())

  hostname_string = ''

  # starts with 'down'

  if node[headers['STATE']].startswith('down'):
    hostname_string += tcolors.FAIL

  if node[headers['STATE']] == 'idle':
    hostname_string += tcolors.OKGREEN

  if node[headers['STATE']] == 'allocated':
    hostname_string += tcolors.OKBLUE

  if node[headers['STATE']] == 'mixed':
    hostname_string += tcolors.OKCYAN

  hostname_string += node[headers['HOSTNAMES']] + ' ' + node[headers['STATE']] + tcolors.ENDC

  print( hostname_string, node[headers['CPUS(A/I/O/T)']], node[headers['CPU_LOAD']], node[headers['FREE_MEM']] )

