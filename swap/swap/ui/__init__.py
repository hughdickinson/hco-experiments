################################################################
"""
    An interface to interact with our utilities from the command line.
    Makes it easier to repeated run SWAP under different conditions.

    UI:
        Container for all the different interfaces

    Interface:
        A construct that manages options and determines the right action

    SWAPInterface:
        An interface for interacting with SWAP

    RocInterface:
        An interface to generate roc curves from multiple SWAP exports
"""

from swap.control import Control
import swap.config as config
import swap.plots as plots
import swap.app.caesar_app as caesar

from swap.utils.scores import ScoreExport
from swap.swap import SWAP

from swap.ui.ui import UI
from swap.ui.scores import RocInterface, ScoresInterface
from swap.ui.swap import SWAPInterface
from swap.ui.caesar import CaesarInterface

import pickle
import argparse
import os
import sys
import csv

import logging
logger = logging.getLogger(__name__)

__author__ = "Michael Laraia"


def run(*interfaces):
    """
        Run the interface

        Args:
            interface: Custom interface subclass to use
    """
    ui = UI()
    RocInterface(ui)
    SWAPInterface(ui)
    ScoresInterface(ui)
    CaesarInterface(ui)

    for interface in interfaces:
        interface()

    ui.run()


if __name__ == "__main__":
    # run()
    pass
