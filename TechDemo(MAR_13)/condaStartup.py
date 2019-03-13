import subprocess
import os

script = 'python3 ISSS.py'
cmd_dict = {
		'activate_env': 'activate_env_%s.sh' % 'CaptionWriter',
		'script': script,
		'conda_name': 'isis3',
		}
cmd = 'cp activate.sh {activate_env} && echo "{script}" >> {activate_env} && sh {activate_env} {conda_name}'.format(**cmd_dict)
env = {}
env.update(os.environ)
result = subprocess.run(cmd, shell=True, env=env)
