import subprocess as sub  

class PythonPackageUpload():
    def __init__(self):
        pass

    def run():
        print('//////////////////////////////////////////////////////')
        print('Make sure you have a Python installed')
        print('Make sure you changed the version')
        print('Make sure you have twine downloaded ')
        print('               : pip install twine')
        print('//////////////////////////////////////////////////////')
        sub.run('python setup.py sdist bdist_wheel',shell=True)
        sub.run('python -m twine upload  dist/*',shell=True)
        