# **********************************************************************************
# * Copyright (C) 2024-present Bert Van Acker (B.MKR) <bert.vanacker@uantwerpen.be>
# *
# * This file is part of the roboarch R&D project.
# *
# * RAP R&D concepts can not be copied and/or distributed without the express
# * permission of Bert Van Acker
# **********************************************************************************

import click
from rpio import __version__


@click.group()
@click.pass_context
def versionCmds():
    pass

@versionCmds.command()
def version():
    """Display the current version."""
    version = __version__
    click.echo("rpio v"+version)