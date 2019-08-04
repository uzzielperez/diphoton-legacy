import ROOT
import time
import subprocess
import os
import argparse
import re
from string import Template
import sys

# Command line options
parser = argparse.ArgumentParser(description="cmsDriver")
parser.add_argument("-a", "--action", default="None", help="del for Delete. run for Run.")
parser.add_argument("-d", "--delete", action="store_true", help="del for Delete. run for Run.")
parser.add_argument("-r", "--run", action="store_true", help="del for Delete. run for Run.")
args = parser.parse_args()

action = args.action
# Timer
sw = ROOT.TStopwatch()
sw.Start()

DATASET = []

doSM          = False
doRSG         = True
doHeavyHiggs  = False


numevent = 10000

#Templates
class_Ctemp = "ClassDiphotonSigX.C"
class_htemp = "ClassDiphotonSigX.h"
run_analyzetemp = "analyze.C"

if doSM:
    #DATASET.append("/store/user/cuperez/DiPhotonAnalysis/ExoANDiphoton/GGJets_M-60To200_Pt-50_13TeV-sherpa/crab_GGJets_M-60To200_Pt-50_13TeV-sherpa__Fall17_PU2017-v1__MINIAODSIM/190304_071350/0000")
    #DATASET.append("/store/user/cuperez/DiPhotonAnalysis/ExoANDiphoton/GGJets_M-200To500_Pt-50_13TeV-sherpa/crab_GGJets_M-200To500_Pt-50_13TeV-sherpa__Fall17_PU2017-v1__MINIAODSIM/190304_071315/0000")
    DATASET.append("/store/user/cuperez/DiPhotonAnalysis/ExoANDiphoton/GGJets_M-500To1000_Pt-50_13TeV-sherpa/crab_GGJets_M-500To1000_Pt-50_13TeV-sherpa__Fall17_PU2017-v1__MINIAODSIM/190304_071326/0000")
    DATASET.append("/store/user/cuperez/DiPhotonAnalysis/ExoANDiphoton/GGJets_M-1000To2000_Pt-50_13TeV-sherpa/crab_GGJets_M-1000To2000_Pt-50_13TeV-sherpa__Fall17_PU2017-v1__MINIAODSIM/190304_071303/0000")
    DATASET.append("/store/user/cuperez/DiPhotonAnalysis/ExoANDiphoton/GGJets_M-2000To4000_Pt-50_13TeV-sherpa/crab_GGJets_M-2000To4000_Pt-50_13TeV-sherpa__Fall17_PU2017-v2__MINIAODSIM/190304_071408/0000")
    DATASET.append("/store/user/cuperez/DiPhotonAnalysis/ExoANDiphoton/GGJets_M-4000To6000_Pt-50_13TeV-sherpa/crab_GGJets_M-4000To6000_Pt-50_13TeV-sherpa__Fall17_PU2017-v2__MINIAODSIM/190304_071420/0000")
    DATASET.append("/store/user/cuperez/DiPhotonAnalysis/ExoANDiphoton/GGJets_M-6000To8000_Pt-50_13TeV-sherpa/crab_GGJets_M-6000To8000_Pt-50_13TeV-sherpa__Fall17_PU2017-v1__MINIAODSIM/190304_071338/0000")

    #DATASET.append("/store/user/cawest/GGJets_M-60To200_Pt-50_13TeV-sherpa/crab_GGJets_M-60To200_Pt-50_13TeV-sherpa__RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14/180531_184256/0000")
    #DATASET.append("/store/user/cawest/GGJets_M-200To500_Pt-50_13TeV-sherpa/crab_GGJets_M-200To500_Pt-50_13TeV-sherpa__RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v1/180531_184217/0000")
    #DATASET.append("/store/user/cawest/GGJets_M-500To1000_Pt-50_13TeV-sherpa/crab_GGJets_M-500To1000_Pt-50_13TeV-sherpa__RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v/180531_184235/0000")
    #DATASET.append("/store/user/cawest/GGJets_M-1000To2000_Pt-50_13TeV-sherpa/crab_GGJets_M-1000To2000_Pt-50_13TeV-sherpa__RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_/180531_184157/0000")
    #DATASET.append("/store/user/cawest/GGJets_M-2000To4000_Pt-50_13TeV-sherpa/crab_GGJets_M-2000To4000_Pt-50_13TeV-sherpa__Fall17_PU2017-v2__MINIAODSIM/190131_195335/0000")
    #DATASET.append("/store/user/cawest/GGJets_M-4000To6000_Pt-50_13TeV-sherpa/crab_GGJets_M-4000To6000_Pt-50_13TeV-sherpa__Fall17_PU2017-v2__MINIAODSIM/180925_195312/0000")
    #DATASET.append("/store/user/cawest/GGJets_M-6000To8000_Pt-50_13TeV-sherpa/crab_GGJets_M-6000To8000_Pt-50_13TeV-sherpa__RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_/180531_182940/0000")
    #DATASET.append("/store/user/cawest/GGJets_M-8000To13000_Pt-50_13TeV-sherpa/crab_GGJets_M-8000To13000_Pt-50_13TeV-sherpa__Fall17_PU2017-v1__MINIAODSIM/190131_195356/0000")
if doRSG:
    DATASET.append('/store/user/cuperez/DiPhotonAnalysis/ExoANDiphoton/RSGravitonToGammaGamma_kMpl01_M_750_TuneCP2_13TeV_pythia8/crab_RSGravitonToGammaGamma_kMpl01_M_750_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAODSIM/190419_064210/0000')
    DATASET.append('/store/user/cuperez/DiPhotonAnalysis/ExoANDiphoton/RSGravitonToGammaGamma_kMpl01_M_1250_TuneCP2_13TeV_pythia8/crab_RSGravitonToGammaGamma_kMpl01_M_1250_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAODSIM/190222_083606/0000')
	  DATASET.append('/store/user/cuperez/DiPhotonAnalysis/ExoANDiphoton/RSGravitonToGammaGamma_kMpl01_M_1500_TuneCP2_13TeV_pythia8/crab_RSGravitonToGammaGamma_kMpl01_M_1500_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAODSIM/190222_083617/0000')
	  DATASET.append('/store/user/cuperez/DiPhotonAnalysis/ExoANDiphoton/RSGravitonToGammaGamma_kMpl01_M_2500_TuneCP2_13TeV_pythia8/crab_RSGravitonToGammaGamma_kMpl01_M_2500_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAODSIM/190222_083628/0000')
	  DATASET.append('/store/user/cuperez/DiPhotonAnalysis/ExoANDiphoton/RSGravitonToGammaGamma_kMpl01_M_3000_TuneCP2_13TeV_pythia8/crab_RSGravitonToGammaGamma_kMpl01_M_3000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAODSIM/190222_083639/0000')
	  DATASET.append('/store/user/cuperez/DiPhotonAnalysis/ExoANDiphoton/RSGravitonToGammaGamma_kMpl01_M_4250_TuneCP2_13TeV_pythia8/crab_RSGravitonToGammaGamma_kMpl01_M_4250_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAODSIM/190222_083653/0000')
	  DATASET.append('/store/user/cuperez/DiPhotonAnalysis/ExoANDiphoton/RSGravitonToGammaGamma_kMpl01_M_4500_TuneCP2_13TeV_pythia8/crab_RSGravitonToGammaGamma_kMpl01_M_4500_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAODSIM/190419_063803/0000')
	  DATASET.append('/store/user/cuperez/DiPhotonAnalysis/ExoANDiphoton/RSGravitonToGammaGamma_kMpl01_M_4750_TuneCP2_13TeV_pythia8/crab_RSGravitonToGammaGamma_kMpl01_M_4750_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAODSIM/190222_083715/0000')
	  DATASET.append('/store/user/cuperez/DiPhotonAnalysis/ExoANDiphoton/RSGravitonToGammaGamma_kMpl01_M_5000_TuneCP2_13TeV_pythia8/crab_RSGravitonToGammaGamma_kMpl01_M_5000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAODSIM/190222_083754/0000')
	  DATASET.append('/store/user/cuperez/DiPhotonAnalysis/ExoANDiphoton/RSGravitonToGammaGamma_kMpl01_M_5750_TuneCP2_13TeV_pythia8/crab_RSGravitonToGammaGamma_kMpl01_M_5750_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAODSIM/190222_083808/0000')
	  DATASET.append('/store/user/cuperez/DiPhotonAnalysis/ExoANDiphoton/RSGravitonToGammaGamma_kMpl01_M_6000_TuneCP2_13TeV_pythia8/crab_RSGravitonToGammaGamma_kMpl01_M_6000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAODSIM/190421_014743/0000')
	  DATASET.append('/store/user/cuperez/DiPhotonAnalysis/ExoANDiphoton/RSGravitonToGammaGamma_kMpl01_M_6500_TuneCP2_13TeV_pythia8/crab_RSGravitonToGammaGamma_kMpl01_M_6500_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAODSIM/190222_083831/0000')
	  DATASET.append('/store/user/cuperez/DiPhotonAnalysis/ExoANDiphoton/RSGravitonToGammaGamma_kMpl01_M_7000_TuneCP2_13TeV_pythia8/crab_RSGravitonToGammaGamma_kMpl01_M_7000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAODSIM/190419_064042/0000')

if doHeavyHiggs:
    # Pre-List
    DATASET.append('/store/user/cuperez/DiPhotonAnalysis/ExoANDiphoton/GluGluSpin0ToGammaGamma_W_1p4_M_1000_TuneCP2_13TeV_pythia8/crab_GluGluSpin0ToGammaGamma_W_1p4_M_1000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAODSIM/190225_135154/0000')
    DATASET.append('/store/user/cuperez/DiPhotonAnalysis/ExoANDiphoton/GluGluSpin0ToGammaGamma_W_1p4_M_1500_TuneCP2_13TeV_pythia8/crab_GluGluSpin0ToGammaGamma_W_1p4_M_1500_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAODSIM/190425_032900/0000')
    DATASET.append('/store/user/cuperez/DiPhotonAnalysis/ExoANDiphoton/GluGluSpin0ToGammaGamma_W_1p4_M_1750_TuneCP2_13TeV_pythia8/crab_GluGluSpin0ToGammaGamma_W_1p4_M_1750_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAODSIM/190520_215311/0000')
    DATASET.append('/store/user/cuperez/DiPhotonAnalysis/ExoANDiphoton/GluGluSpin0ToGammaGamma_W_1p4_M_2000_TuneCP2_13TeV_pythia8/crab_GluGluSpin0ToGammaGamma_W_1p4_M_2000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAODSIM/190225_135231/0000')
    DATASET.append('/store/user/cuperez/DiPhotonAnalysis/ExoANDiphoton/GluGluSpin0ToGammaGamma_W_1p4_M_2250_TuneCP2_13TeV_pythia8/crab_GluGluSpin0ToGammaGamma_W_1p4_M_2250_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAODSIM/190225_135249/0000')
    DATASET.append('/store/user/cuperez/DiPhotonAnalysis/ExoANDiphoton/GluGluSpin0ToGammaGamma_W_1p4_M_2500_TuneCP2_13TeV_pythia8/crab_GluGluSpin0ToGammaGamma_W_1p4_M_2500_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAODSIM/190225_135300/0000')
    DATASET.append('/store/user/cuperez/DiPhotonAnalysis/ExoANDiphoton/GluGluSpin0ToGammaGamma_W_1p4_M_3000_TuneCP2_13TeV_pythia8/crab_GluGluSpin0ToGammaGamma_W_1p4_M_3000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAODSIM/190225_135312/0000')
    DATASET.append('/store/user/cuperez/DiPhotonAnalysis/ExoANDiphoton/GluGluSpin0ToGammaGamma_W_1p4_M_3500_TuneCP2_13TeV_pythia8/crab_GluGluSpin0ToGammaGamma_W_1p4_M_3500_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAODSIM/190520_221656/0000')
    DATASET.append('/store/user/cuperez/DiPhotonAnalysis/ExoANDiphoton/GluGluSpin0ToGammaGamma_W_1p4_M_4000_TuneCP2_13TeV_pythia8/crab_GluGluSpin0ToGammaGamma_W_1p4_M_4000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAODSIM/190225_135325/0000')
    DATASET.append('/store/user/cuperez/DiPhotonAnalysis/ExoANDiphoton/GluGluSpin0ToGammaGamma_W_1p4_M_4250_TuneCP2_13TeV_pythia8/crab_GluGluSpin0ToGammaGamma_W_1p4_M_4250_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAODSIM/190501_030502/0000')
    DATASET.append('/store/user/cuperez/DiPhotonAnalysis/ExoANDiphoton/GluGluSpin0ToGammaGamma_W_1p4_M_4500_TuneCP2_13TeV_pythia8/crab_GluGluSpin0ToGammaGamma_W_1p4_M_4500_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAODSIM/190501_030641/0000')
    DATASET.append('/store/user/cuperez/DiPhotonAnalysis/ExoANDiphoton/GluGluSpin0ToGammaGamma_W_1p4_M_4750_TuneCP2_13TeV_pythia8/crab_GluGluSpin0ToGammaGamma_W_1p4_M_4750_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAODSIM/190501_030758/0000')
    DATASET.append('/store/user/cuperez/DiPhotonAnalysis/ExoANDiphoton/GluGluSpin0ToGammaGamma_W_1p4_M_5000_TuneCP2_13TeV_pythia8/crab_GluGluSpin0ToGammaGamma_W_1p4_M_5000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAODSIM/190501_030915/0000')
    DATASET.append('/store/user/cuperez/DiPhotonAnalysis/ExoANDiphoton/GluGluSpin0ToGammaGamma_W_1p4_M_750_TuneCP2_13TeV_pythia8/crab_GluGluSpin0ToGammaGamma_W_1p4_M_750_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAODSIM/190501_031045/0000')

for dset in DATASET:
    pattern = "store/user/cuperez/DiPhotonAnalysis/ExoANDiphoton/([^(]*)_TuneCP2_13TeV_pythia8/crab_"
    #pattern = "store/user/cuperez/DiPhotonAnalysis/signal-2018/([^(]*)_TuneCP2_13TeV_pythia8/crab_"
    if doSM:
        #pattern = "/store/user/cawest/([^(]*)_13TeV-sherpa/crab"
        pattern = "/store/user/cuperez/DiPhotonAnalysis/ExoANDiphoton/([^(]*)_13TeV-sherpa/crab"
    match = re.findall(pattern, dset)
    print match
    nametag   = match[0].replace('-', '_')
    classname = "Class_%s" %(nametag)
    an_func   = "analyze_%s" %(nametag)
    outfile   = "%s" %(nametag)

    # Template Replacements
    cmssw_base = os.getenv("CMSSW_BASE")
    rep = {'ClassDiphotonSignal': classname,
           "outputfile": outfile,
           "cmssw_base": cmssw_base,
           "eosdsetdir": dset,
	   "nametag": nametag,
           "analyzefunc": an_func,
           }

    #Read and replace template file
    C_src = Template(open(class_Ctemp).read())
    C_sub = C_src.substitute(rep)

    h_src = Template(open(class_htemp).read())
    h_sub = h_src.substitute(rep)

    an_src = Template(open(run_analyzetemp).read())
    an_sub = an_src.substitute(rep)

    #write to file
    outfile_C = open("%s.C" %(classname), "w+")
    outfile_C.write(C_sub)

    outfile_h = open("%s.h" %(classname), "w+")
    outfile_h.write(h_sub)

    outfile_an = open("analyze_%s.C" %(nametag), "w+")
    outfile_an.write(an_sub)

def RunAnalyze(file_list):
	for anFile in file_list:
		if anFile.startswith("analyze_") and anFile.endswith(".C"):
			root_cmd = "root -l -q %s" %(anFile)
			os.system(root_cmd)
def DelClassFiles(file_list):
    for classFile in file_list:
        if "Class_" in classFile:
            del_cmd = "rm %s" %(classFile)
            os.system(del_cmd)
        if "analyze_" in classFile:
            del_cmd = "rm %s" %(classFile)
            os.system(del_cmd)
        if "LOG" in classFile:
	    del_cmd = "rm %s" %(classFile)
            os.system(del_cmd)
    print "deleted auxilliary files"

if args.run:
    RunAnalyze(os.listdir('.'))
if args.delete:
    DelClassFiles(os.listdir('.'))

sw.Stop()
print "Real time: " + str(sw.RealTime() / 60.0) + " minutes"
print "CPU time:  " + str(sw.CpuTime() / 60.0) + " minutes"
