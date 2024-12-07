import subprocess as sub 

class CreateGitBranch():
    def __init__(self):
        pass

    def run():
        print('//////////////////////////////////////////////////////')
        print('Make sure you have a git repo')
        print('//////////////////////////////////////////////////////')
        GitBranchName = input('Enter your new git branch Name : ')
        sub.run(f'git branch {GitBranchName}')
        print(f'{GitBranchName} branch craeted')
        sub.run(f'git branch ')
        sub.run(f'git switch {GitBranchName}',shell=True)
        print(f'switch to {GitBranchName}',shell=True)

