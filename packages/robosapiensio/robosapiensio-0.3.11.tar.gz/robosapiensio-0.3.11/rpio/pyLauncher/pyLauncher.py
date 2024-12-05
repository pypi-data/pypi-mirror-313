from rpio.utils.auxiliary import *
from subprocess import call


def launch(launchFile='launch.xml'):
    """Function to launch one or more python software component using a launch description file

        :param [launchFile]: [launch description file(XML)], defaults to [launch.xml]
        :type [launchFile]: [String](, optional)
        ...
        :return: [Functions returns nothing]
        :rtype: [None]
    """

    # 0. interpret launch file
    launchDescription = parse_launch_xml(file=launchFile,formalism="python")

    # 1. launch all commands at once
    execute_commands(extractCommands(launchDescription))

def launch_main(mainFile='main.py'):
    """Function to launch one or more python software component using a main file

        :param [mainFile]: [launch description file(XML)], defaults to [launch.xml]
        :type [mainFile]: [String](, optional)
        ...
        :return: [Functions returns nothing]
        :rtype: [None]
    """
    command = ["python", mainFile]
    call(command)

def launch_docker_compose(path='/'):
    """Function to launch one or more python software component using a docker compose file

            :param [path]: [path to the docker compose file for the given platform], defaults to [/]
            :type [path]: [String](, optional)
            ...
            :return: [Functions returns nothing]
            :rtype: [None]
        """
    cdCommand = ["cd", path]
    call(cdCommand)
    dockerCommand = ["docker compose up --build -d"]    #-d runs in detached mode
    call(dockerCommand)