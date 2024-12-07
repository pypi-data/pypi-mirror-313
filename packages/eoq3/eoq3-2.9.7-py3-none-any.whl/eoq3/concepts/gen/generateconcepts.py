'''
 script to create
 - conecepts.py
 - __init__.py
 
 Bjoern Annighoefer 2023
'''

import os

if __name__ == "__main__":
    os.system('python -m eoq3conceptsgen.generatefromconceptscli -i gen/concepts.py.mako -o concepts.py')
    os.system('python -m eoq3conceptsgen.generatefromconceptscli -i gen/__init__.py.mako -o __init__.py')
    
    