'Build a Docker image with automatic tag.'
from .projectinfo import ProjectInfo
import os

def main():
    info = ProjectInfo.seek('.')
    command = 'docker', 'build', '-t', info.config.docker.tag, info.projectdir
    os.execvp(command[0], command)

if '__main__' == __name__:
    main()
