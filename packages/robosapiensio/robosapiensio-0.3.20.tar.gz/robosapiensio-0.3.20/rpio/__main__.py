# **********************************************************************************
# * Copyright (C) 2024-present Bert Van Acker (B.MKR) <bert.vanacker@uantwerpen.be>
# *
# * This file is part of the roboarch R&D project.
# *
# * RAP R&D concepts can not be copied and/or distributed without the express
# * permission of Bert Van Acker
# **********************************************************************************

import click

from rpio.commands.version import versionCmds
from rpio.commands.importer import importCmds
from rpio.commands.exporter import exportCmds
from rpio.commands.run import runCmds
from rpio.commands.build import buildCmds
from rpio.commands.package import packageCmds
from rpio.commands.deploy import deployCmds
from rpio.commands.transformations import transformationCmds
from rpio.commands.platform import platformCmds

cli=click.CommandCollection(sources=[versionCmds,packageCmds,transformationCmds,runCmds,buildCmds,deployCmds,platformCmds],help="robosapiensIO command line tool")


if __name__ == '__main__':
    cli()
