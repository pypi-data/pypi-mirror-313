from pypartpicker import Scraper
from components.gpu import *
from components.psu import *
from components.ram import *
from components.hdd import *
from components.ssd import *
from components.cpucooler import *
from components.cpu import *
from components.motherboard import *
from components.case import *


def populateJSON():

    pcpp = Scraper()

    saveCPUsToJSON(pcpp, 25)
    saveCasesToJSON(pcpp, 25)
    saveCPUCoolersToJSON(pcpp, 25)
    saveGPUsToJson(pcpp, 25)
    saveHDDsToJSON(pcpp, 25)
    saveMBsToJSON(pcpp, 25)
    savePSUsToJSON(pcpp, 25)
    saveRAMsToJSON(pcpp, 25)
    saveSSDsToJSON(pcpp, 25)
