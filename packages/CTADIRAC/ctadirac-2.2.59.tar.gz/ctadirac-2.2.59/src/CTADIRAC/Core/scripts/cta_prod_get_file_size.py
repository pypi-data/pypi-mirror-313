#!/usr/bin/env python

__RCSID__ = "$Id$"

# generic imports
from multiprocessing import Pool

# DIRAC imports
import DIRAC
from DIRAC import gLogger
from CTADIRAC.Core.Utilities.tool_box import read_inputs_from_file
from DIRAC.Core.Base.Script import Script

Script.setUsageMessage(
    """
Bulk get file size from a list of lfns
Usage:
   cta-prod-get-file-size [options] <ascii file with lfn list>
"""
)

Script.parseCommandLine(ignoreErrors=True)

from DIRAC.Resources.Catalog.FileCatalog import FileCatalog

fc = FileCatalog()


@Script()
def main():
    args = Script.getPositionalArgs()
    if len(args) > 0:
        infile = args[0]
    else:
        Script.showHelp()

    infileList = read_inputs_from_file(infile)
    p = Pool(1)
    p.map(getSize, infileList)


def getSize(lfn):
    res = fc.getFileSize(lfn)
    if not res["OK"]:
        gLogger.error("Failed to get size for lfn", lfn)
        return res["Message"]
    if lfn in res["Value"]["Successful"]:
        gLogger.notice(lfn + " " + str(res["Value"]["Successful"][lfn]))
    else:
        res = DIRAC.S_ERROR(f"Failed to get size for lfn {lfn}")
        gLogger.error(res["Message"])
        return res


if __name__ == "__main__":
    main()
