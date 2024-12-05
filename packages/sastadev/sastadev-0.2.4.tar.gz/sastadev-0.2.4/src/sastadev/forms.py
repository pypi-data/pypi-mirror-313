import os

from sastadev.constants import formsfolder, intreebanksfolder

formext = '.xlsx'


def getformfilename(infullname, suffix):
    base, infilename = os.path.split(infullname)
    (filebase, ext) = os.path.splitext(infilename)
    (core, lastfolder) = os.path.split(base)
    if lastfolder == intreebanksfolder:
        formname = os.path.join(core, formsfolder, filebase + suffix + formext)
    else:
        formname = base + suffix + formext
    return formname
