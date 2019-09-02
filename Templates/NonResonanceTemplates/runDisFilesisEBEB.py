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
#parser.add_argument("-a", "--action", default="None", help="del for Delete. run for Run.")
parser.add_argument("-d", "--delete", action="store_true", help="Clean directory and delete copied files")
parser.add_argument("-r", "--run", action="store_true", help="Run Analyze")
parser.add_argument("-c", "--cuts", default=None, help="Minv Cut")
#parser.add_argument("-r", "--run", action="store_true")
args = parser.parse_args()

#action = args.action
# Timer
sw = ROOT.TStopwatch()
sw.Start()

DATASET = []

doSM          = False
doADD         = False
doUnparticles = False

doSherpaADD   = False
doSherpaADDang = True

#runnumevent = 10000

#Templates
class_Ctemp = "ClassDiphotonSigX.C"
class_htemp = "ClassDiphotonSigX.h"
run_analyzetemp = "analyze.C"

if args.cuts is not None:
    class_Ctemp = "ClassAngCutsStudy.C"
    MinvCut     =  args.cuts# Basic cut is 500 GeV
    print "Applying invariant mass cut > %s" %(MinvCut)
    #if doSherpaADDang:
        #class_Ctemp = "ClassAngCutsStudySherpa.C"

if doSM:
    # DATASET.append("/store/user/cuperez/DiPhotonAnalysis/ExoANDiphoton/GGJets_M-60To200_Pt-50_13TeV-sherpa/crab_GGJets_M-60To200_Pt-50_13TeV-sherpa__Fall17_PU2017-v1__MINIAODSIM/190304_071350/0000")
    # DATASET.append("/store/user/cuperez/DiPhotonAnalysis/ExoANDiphoton/GGJets_M-200To500_Pt-50_13TeV-sherpa/crab_GGJets_M-200To500_Pt-50_13TeV-sherpa__Fall17_PU2017-v1__MINIAODSIM/190304_071315/0000")
    DATASET.append("/store/user/cuperez/DiPhotonAnalysis/ExoANDiphoton/GGJets_M-500To1000_Pt-50_13TeV-sherpa/crab_GGJets_M-500To1000_Pt-50_13TeV-sherpa__Fall17_PU2017-v1__MINIAODSIM/190304_071326/0000")
    DATASET.append("/store/user/cuperez/DiPhotonAnalysis/ExoANDiphoton/GGJets_M-1000To2000_Pt-50_13TeV-sherpa/crab_GGJets_M-1000To2000_Pt-50_13TeV-sherpa__Fall17_PU2017-v1__MINIAODSIM/190304_071303/0000")
    DATASET.append("/store/user/cuperez/DiPhotonAnalysis/ExoANDiphoton/GGJets_M-2000To4000_Pt-50_13TeV-sherpa/crab_GGJets_M-2000To4000_Pt-50_13TeV-sherpa__Fall17_PU2017-v2__MINIAODSIM/190304_071408/0000")
    DATASET.append("/store/user/cuperez/DiPhotonAnalysis/ExoANDiphoton/GGJets_M-4000To6000_Pt-50_13TeV-sherpa/crab_GGJets_M-4000To6000_Pt-50_13TeV-sherpa__Fall17_PU2017-v2__MINIAODSIM/190304_071420/0000")
    DATASET.append("/store/user/cuperez/DiPhotonAnalysis/ExoANDiphoton/GGJets_M-6000To8000_Pt-50_13TeV-sherpa/crab_GGJets_M-6000To8000_Pt-50_13TeV-sherpa__Fall17_PU2017-v1__MINIAODSIM/190304_071338/0000")

    # DATASET.append("/store/user/cawest/GGJets_M-60To200_Pt-50_13TeV-sherpa/crab_GGJets_M-60To200_Pt-50_13TeV-sherpa__RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14/180531_184256/0000")
    # DATASET.append("/store/user/cawest/GGJets_M-200To500_Pt-50_13TeV-sherpa/crab_GGJets_M-200To500_Pt-50_13TeV-sherpa__RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v1/180531_184217/0000")
    # DATASET.append("/store/user/cawest/GGJets_M-500To1000_Pt-50_13TeV-sherpa/crab_GGJets_M-500To1000_Pt-50_13TeV-sherpa__RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v/180531_184235/0000")
    # DATASET.append("/store/user/cawest/GGJets_M-1000To2000_Pt-50_13TeV-sherpa/crab_GGJets_M-1000To2000_Pt-50_13TeV-sherpa__RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_/180531_184157/0000")
    # DATASET.append("/store/user/cawest/GGJets_M-2000To4000_Pt-50_13TeV-sherpa/crab_GGJets_M-2000To4000_Pt-50_13TeV-sherpa__Fall17_PU2017-v2__MINIAODSIM/190131_195335/0000")
    # DATASET.append("/store/user/cawest/GGJets_M-4000To6000_Pt-50_13TeV-sherpa/crab_GGJets_M-4000To6000_Pt-50_13TeV-sherpa__Fall17_PU2017-v2__MINIAODSIM/180925_195312/0000")
    # DATASET.append("/store/user/cawest/GGJets_M-6000To8000_Pt-50_13TeV-sherpa/crab_GGJets_M-6000To8000_Pt-50_13TeV-sherpa__RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_/180531_182940/0000")
    # DATASET.append("/store/user/cawest/GGJets_M-8000To13000_Pt-50_13TeV-sherpa/crab_GGJets_M-8000To13000_Pt-50_13TeV-sherpa__Fall17_PU2017-v1__MINIAODSIM/190131_195356/0000")
if doADD:
    #DATASET.append('/store/user/cuperez/DiPhotonAnalysis/signal-2018/ADDGravToGG_NegInt-0_LambdaT-10000_M-2000To4000_TuneCP2_13TeV-pythia8/crab_ADDGravToGG_NegInt-0_LambdaT-10000_M-2000To4000_TuneCP2_13TeV-pythia8__Fall17_PU2017-v1__MINIAODSIM/190207_171204/0000')
    #DATASET.append('/store/user/cuperez/DiPhotonAnalysis/ExoANDiphoton/ADDGravToGG_NegInt-1_LambdaT-13000_M-500To1000_TuneCP2_13TeV-pythia8/crab_ADDGravToGG_NegInt-1_LambdaT-13000_M-500To1000_TuneCP2_13TeV-pythia8__Fall17_PU2017-v1__MINIAODSIM/190304_071943/0000')
    #DATASET.append('/store/user/cuperez/DiPhotonAnalysis/ExoANDiphoton/ADDGravToGG_NegInt-1_LambdaT-13000_M-1000To2000_TuneCP2_13TeV-pythia8/crab_ADDGravToGG_NegInt-1_LambdaT-13000_M-1000To2000_TuneCP2_13TeV-pythia8__Fall17_PU2017-v1__MINIAODSIM/190304_071907/0000')
    #DATASET.append('/store/user/cuperez/DiPhotonAnalysis/ExoANDiphoton/ADDGravToGG_NegInt-1_LambdaT-13000_M-2000To4000_TuneCP2_13TeV-pythia8/crab_ADDGravToGG_NegInt-1_LambdaT-13000_M-2000To4000_TuneCP2_13TeV-pythia8__Fall17_PU2017-v1__MINIAODSIM/190304_071921/0000')
    #DATASET.append('/store/user/cuperez/DiPhotonAnalysis/ExoANDiphoton/ADDGravToGG_NegInt-1_LambdaT-13000_M-4000To13000_TuneCP2_13TeV-pythia8/crab_ADDGravToGG_NegInt-1_LambdaT-13000_M-4000To13000_TuneCP2_13TeV-pythia8__Fall17_PU2017-v1__MINIAODSIM/190304_071932/0000')

    DATASET.append('/store/user/cuperez/DiPhotonAnalysis/ExoANDiphoton/ADDGravToGG_NegInt-1_LambdaT-10000_M-1000To2000_TuneCP2_13TeV-pythia8/crab_ADDGravToGG_NegInt-1_LambdaT-10000_M-1000To2000_TuneCP2_13TeV-pythia8__Fall17_PU2017-v1__MINIAODSIM/190319_071912/0000')
    DATASET.append('/store/user/cuperez/DiPhotonAnalysis/ExoANDiphoton/ADDGravToGG_NegInt-1_LambdaT-10000_M-2000To4000_TuneCP2_13TeV-pythia8/crab_ADDGravToGG_NegInt-1_LambdaT-10000_M-2000To4000_TuneCP2_13TeV-pythia8__Fall17_PU2017-v1__MINIAODSIM/190319_071922/0000')
    DATASET.append('/store/user/cuperez/DiPhotonAnalysis/ExoANDiphoton/ADDGravToGG_NegInt-1_LambdaT-10000_M-4000To10000_TuneCP2_13TeV-pythia8/crab_ADDGravToGG_NegInt-1_LambdaT-10000_M-4000To10000_TuneCP2_13TeV-pythia8__Fall17_PU2017-v1__MINIAODSIM/190319_071937/0000')
    DATASET.append('/store/user/cuperez/DiPhotonAnalysis/ExoANDiphoton/ADDGravToGG_NegInt-1_LambdaT-10000_M-500To1000_TuneCP2_13TeV-pythia8/crab_ADDGravToGG_NegInt-1_LambdaT-10000_M-500To1000_TuneCP2_13TeV-pythia8__Fall17_PU2017-v1__MINIAODSIM/190319_071947/0000')
    DATASET.append('/store/user/cuperez/DiPhotonAnalysis/ExoANDiphoton/ADDGravToGG_NegInt-1_LambdaT-6000_M-1000To2000_TuneCP2_13TeV-pythia8/crab_ADDGravToGG_NegInt-1_LambdaT-6000_M-1000To2000_TuneCP2_13TeV-pythia8__Fall17_PU2017-v1__MINIAODSIM/190319_071956/0000')
    DATASET.append('/store/user/cuperez/DiPhotonAnalysis/ExoANDiphoton/ADDGravToGG_NegInt-1_LambdaT-6000_M-2000To4000_TuneCP2_13TeV-pythia8/crab_ADDGravToGG_NegInt-1_LambdaT-6000_M-2000To4000_TuneCP2_13TeV-pythia8__Fall17_PU2017-v1__MINIAODSIM/190319_072009/0000')
    DATASET.append('/store/user/cuperez/DiPhotonAnalysis/ExoANDiphoton/ADDGravToGG_NegInt-1_LambdaT-6000_M-4000To6000_TuneCP2_13TeV-pythia8/crab_ADDGravToGG_NegInt-1_LambdaT-6000_M-4000To6000_TuneCP2_13TeV-pythia8__Fall17_PU2017-v1__MINIAODSIM/190319_072020/0000')
    DATASET.append('/store/user/cuperez/DiPhotonAnalysis/ExoANDiphoton/ADDGravToGG_NegInt-1_LambdaT-6000_M-500To1000_TuneCP2_13TeV-pythia8/crab_ADDGravToGG_NegInt-1_LambdaT-6000_M-500To1000_TuneCP2_13TeV-pythia8__Fall17_PU2017-v1__MINIAODSIM/190319_072030/0000')
    DATASET.append('/store/user/cuperez/DiPhotonAnalysis/ExoANDiphoton/ADDGravToGG_NegInt-1_LambdaT-8000_M-1000To2000_TuneCP2_13TeV-pythia8/crab_ADDGravToGG_NegInt-1_LambdaT-8000_M-1000To2000_TuneCP2_13TeV-pythia8__Fall17_PU2017-v1__MINIAODSIM/190319_072040/0000')
    DATASET.append('/store/user/cuperez/DiPhotonAnalysis/ExoANDiphoton/ADDGravToGG_NegInt-1_LambdaT-8000_M-2000To4000_TuneCP2_13TeV-pythia8/crab_ADDGravToGG_NegInt-1_LambdaT-8000_M-2000To4000_TuneCP2_13TeV-pythia8__Fall17_PU2017-v1__MINIAODSIM/190319_072050/0000')
    DATASET.append('/store/user/cuperez/DiPhotonAnalysis/ExoANDiphoton/ADDGravToGG_NegInt-1_LambdaT-8000_M-4000To8000_TuneCP2_13TeV-pythia8/crab_ADDGravToGG_NegInt-1_LambdaT-8000_M-4000To8000_TuneCP2_13TeV-pythia8__Fall17_PU2017-v1__MINIAODSIM/190319_072100/0000')
    DATASET.append('/store/user/cuperez/DiPhotonAnalysis/ExoANDiphoton/ADDGravToGG_NegInt-1_LambdaT-8000_M-500To1000_TuneCP2_13TeV-pythia8/crab_ADDGravToGG_NegInt-1_LambdaT-8000_M-500To1000_TuneCP2_13TeV-pythia8__Fall17_PU2017-v1__MINIAODSIM/190319_072110/0000')

if doSherpaADDang:
    DATASET.append('/store/user/cuperez/DiPhotonAnalysis/ExoANDiphoton/ADDGravToGG_MS-10000_NED-4_KK-1_M-1000To2000_13TeV-sherpa/crab_ADDGravToGG_MS-10000_NED-4_KK-1_M-1000To2000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/190315_055305/0000')
    DATASET.append('/store/user/cuperez/DiPhotonAnalysis/ExoANDiphoton/ADDGravToGG_MS-10000_NED-4_KK-1_M-2000To4000_13TeV-sherpa/crab_ADDGravToGG_MS-10000_NED-4_KK-1_M-2000To4000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/190315_055324/0000')
    DATASET.append('/store/user/cuperez/DiPhotonAnalysis/ExoANDiphoton/ADDGravToGG_MS-10000_NED-4_KK-1_M-4000To10000_13TeV-sherpa/crab_ADDGravToGG_MS-10000_NED-4_KK-1_M-4000To10000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/190315_055335/0000')
    DATASET.append('/store/user/cuperez/DiPhotonAnalysis/ExoANDiphoton/ADDGravToGG_MS-10000_NED-4_KK-1_M-500To1000_13TeV-sherpa/crab_ADDGravToGG_MS-10000_NED-4_KK-1_M-500To1000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/190315_055346/0000')
    # DATASET.append('/store/user/cuperez/DiPhotonAnalysis/ExoANDiphoton/ADDGravToGG_MS-11000_NED-4_KK-1_M-1000To2000_13TeV-sherpa/crab_ADDGravToGG_MS-11000_NED-4_KK-1_M-1000To2000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/190315_055357/0000')
    # DATASET.append('/store/user/cuperez/DiPhotonAnalysis/ExoANDiphoton/ADDGravToGG_MS-11000_NED-4_KK-1_M-2000To4000_13TeV-sherpa/crab_ADDGravToGG_MS-11000_NED-4_KK-1_M-2000To4000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/190315_055408/0000')
    # DATASET.append('/store/user/cuperez/DiPhotonAnalysis/ExoANDiphoton/ADDGravToGG_MS-11000_NED-4_KK-1_M-4000To11000_13TeV-sherpa/crab_ADDGravToGG_MS-11000_NED-4_KK-1_M-4000To11000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/190315_055419/0000')
    # DATASET.append('/store/user/cuperez/DiPhotonAnalysis/ExoANDiphoton/ADDGravToGG_MS-11000_NED-4_KK-1_M-500To1000_13TeV-sherpa/crab_ADDGravToGG_MS-11000_NED-4_KK-1_M-500To1000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/190315_055429/0000')
    DATASET.append('/store/user/cuperez/DiPhotonAnalysis/ExoANDiphoton/ADDGravToGG_MS-6000_NED-4_KK-1_M-1000To2000_13TeV-sherpa/crab_ADDGravToGG_MS-6000_NED-4_KK-1_M-1000To2000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/190316_021039/0000')
    DATASET.append('/store/user/cuperez/DiPhotonAnalysis/ExoANDiphoton/ADDGravToGG_MS-6000_NED-4_KK-1_M-2000To4000_13TeV-sherpa/crab_ADDGravToGG_MS-6000_NED-4_KK-1_M-2000To4000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/190316_021500/0000')
    DATASET.append('/store/user/cuperez/DiPhotonAnalysis/ExoANDiphoton/ADDGravToGG_MS-6000_NED-4_KK-1_M-4000To6000_13TeV-sherpa/crab_ADDGravToGG_MS-6000_NED-4_KK-1_M-4000To6000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/190315_055019/0000')
    DATASET.append('/store/user/cuperez/DiPhotonAnalysis/ExoANDiphoton/ADDGravToGG_MS-6000_NED-4_KK-1_M-500To1000_13TeV-sherpa/crab_ADDGravToGG_MS-6000_NED-4_KK-1_M-500To1000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/190315_055030/0000')
    #  DATASET.append('/store/user/cuperez/DiPhotonAnalysis/ExoANDiphoton/ADDGravToGG_MS-7000_NED-4_KK-1_M-1000To2000_13TeV-sherpa/crab_ADDGravToGG_MS-7000_NED-4_KK-1_M-1000To2000_13TeV-sherpa__80XMniAODv2__MINIAODSIM')
    # DATASET.append('/store/user/cuperez/DiPhotonAnalysis/ExoANDiphoton/ADDGravToGG_MS-7000_NED-4_KK-1_M-2000To4000_13TeV-sherpa/crab_ADDGravToGG_MS-7000_NED-4_KK-1_M-2000To4000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/190315_055055/0000')
    # DATASET.append('/store/user/cuperez/DiPhotonAnalysis/ExoANDiphoton/ADDGravToGG_MS-7000_NED-4_KK-1_M-4000To7000_13TeV-sherpa/crab_ADDGravToGG_MS-7000_NED-4_KK-1_M-4000To7000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/190315_055107/0000')
    #  DATASET.append('/store/user/cuperez/DiPhotonAnalysis/ExoANDiphoton/ADDGravToGG_MS-7000_NED-4_KK-1_M-500To1000_13TeV-sherpa/crab_ADDGravToGG_MS-7000_NED-4_KK-1_M-500To1000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/190315_055123/0000')
    DATASET.append('/store/user/cuperez/DiPhotonAnalysis/ExoANDiphoton/ADDGravToGG_MS-8000_NED-4_KK-1_M-1000To2000_13TeV-sherpa/crab_ADDGravToGG_MS-8000_NED-4_KK-1_M-1000To2000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/190315_055136/0000')
    DATASET.append('/store/user/cuperez/DiPhotonAnalysis/ExoANDiphoton/ADDGravToGG_MS-8000_NED-4_KK-1_M-2000To4000_13TeV-sherpa/crab_ADDGravToGG_MS-8000_NED-4_KK-1_M-2000To4000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/190315_055147/0000')
    DATASET.append('/store/user/cuperez/DiPhotonAnalysis/ExoANDiphoton/ADDGravToGG_MS-8000_NED-4_KK-1_M-4000To8000_13TeV-sherpa/crab_ADDGravToGG_MS-8000_NED-4_KK-1_M-4000To8000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/190315_055158/0000')
    DATASET.append('/store/user/cuperez/DiPhotonAnalysis/ExoANDiphoton/ADDGravToGG_MS-8000_NED-4_KK-1_M-500To1000_13TeV-sherpa/crab_ADDGravToGG_MS-8000_NED-4_KK-1_M-500To1000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/190315_055209/0000')
    # DATASET.append('/store/user/cuperez/DiPhotonAnalysis/ExoANDiphoton/ADDGravToGG_MS-9000_NED-4_KK-1_M-1000To2000_13TeV-sherpa/crab_ADDGravToGG_MS-9000_NED-4_KK-1_M-1000To2000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/190315_055219/0000')
    # DATASET.append('/store/user/cuperez/DiPhotonAnalysis/ExoANDiphoton/ADDGravToGG_MS-9000_NED-4_KK-1_M-2000To4000_13TeV-sherpa/crab_ADDGravToGG_MS-9000_NED-4_KK-1_M-2000To4000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/190315_055232/0000')
    # DATASET.append('/store/user/cuperez/DiPhotonAnalysis/ExoANDiphoton/ADDGravToGG_MS-9000_NED-4_KK-1_M-4000To9000_13TeV-sherpa/crab_ADDGravToGG_MS-9000_NED-4_KK-1_M-4000To9000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/190315_055243/0000')
    # DATASET.append('/store/user/cuperez/DiPhotonAnalysis/ExoANDiphoton/ADDGravToGG_MS-9000_NED-4_KK-1_M-500To1000_13TeV-sherpa/crab_ADDGravToGG_MS-9000_NED-4_KK-1_M-500To1000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/190315_055254/0000')

if doSherpaADD:
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-10000_NED-2_KK-1_M-1000To2000_13TeV-sherpa/crab_ADDGravToGG_MS-10000_NED-2_KK-1_M-1000To2000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_183351/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-10000_NED-2_KK-1_M-2000To4000_13TeV-sherpa/crab_ADDGravToGG_MS-10000_NED-2_KK-1_M-2000To4000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_183405/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-10000_NED-2_KK-1_M-4000To10000_13TeV-sherpa/crab_ADDGravToGG_MS-10000_NED-2_KK-1_M-4000To10000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_183419/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-10000_NED-2_KK-1_M-500To1000_13TeV-sherpa/crab_ADDGravToGG_MS-10000_NED-2_KK-1_M-500To1000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_183431/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-10000_NED-4_KK-1_M-1000To2000_13TeV-sherpa/crab_ADDGravToGG_MS-10000_NED-4_KK-1_M-1000To2000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_183443/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-10000_NED-4_KK-1_M-2000To4000_13TeV-sherpa/crab_ADDGravToGG_MS-10000_NED-4_KK-1_M-2000To4000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_183457/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-10000_NED-4_KK-1_M-4000To10000_13TeV-sherpa/crab_ADDGravToGG_MS-10000_NED-4_KK-1_M-4000To10000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_183514/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-10000_NED-4_KK-1_M-500To1000_13TeV-sherpa/crab_ADDGravToGG_MS-10000_NED-4_KK-1_M-500To1000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_183529/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-11000_NED-2_KK-1_M-1000To2000_13TeV-sherpa/crab_ADDGravToGG_MS-11000_NED-2_KK-1_M-1000To2000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_183544/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-11000_NED-2_KK-1_M-2000To4000_13TeV-sherpa/crab_ADDGravToGG_MS-11000_NED-2_KK-1_M-2000To4000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_183601/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-11000_NED-2_KK-1_M-500To1000_13TeV-sherpa/crab_ADDGravToGG_MS-11000_NED-2_KK-1_M-500To1000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_183635/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-11000_NED-4_KK-1_M-1000To2000_13TeV-sherpa/crab_ADDGravToGG_MS-11000_NED-4_KK-1_M-1000To2000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_183648/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-11000_NED-4_KK-1_M-2000To4000_13TeV-sherpa/crab_ADDGravToGG_MS-11000_NED-4_KK-1_M-2000To4000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_183705/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-11000_NED-4_KK-1_M-4000To11000_13TeV-sherpa/crab_ADDGravToGG_MS-11000_NED-4_KK-1_M-4000To11000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_183719/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-3000_NED-2_KK-1_M-1000To2000_13TeV-sherpa/crab_ADDGravToGG_MS-3000_NED-2_KK-1_M-1000To2000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_171210/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-3000_NED-2_KK-1_M-2000To3000_13TeV-sherpa/crab_ADDGravToGG_MS-3000_NED-2_KK-1_M-2000To3000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_180945/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-3000_NED-2_KK-1_M-500To1000_13TeV-sherpa/crab_ADDGravToGG_MS-3000_NED-2_KK-1_M-500To1000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_180957/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-3000_NED-2_KK-4_M-1000To2000_13TeV-sherpa/crab_ADDGravToGG_MS-3000_NED-2_KK-4_M-1000To2000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_181013/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-3000_NED-2_KK-4_M-2000To3000_13TeV-sherpa/crab_ADDGravToGG_MS-3000_NED-2_KK-4_M-2000To3000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_181027/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-3000_NED-2_KK-4_M-500To1000_13TeV-sherpa/crab_ADDGravToGG_MS-3000_NED-2_KK-4_M-500To1000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_181040/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-3000_NED-4_KK-1_M-1000To2000_13TeV-sherpa/crab_ADDGravToGG_MS-3000_NED-4_KK-1_M-1000To2000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_181057/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-3000_NED-4_KK-1_M-2000To3000_13TeV-sherpa/crab_ADDGravToGG_MS-3000_NED-4_KK-1_M-2000To3000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_181112/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-3000_NED-4_KK-1_M-200To500_13TeV-sherpa/crab_ADDGravToGG_MS-3000_NED-4_KK-1_M-200To500_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_181124/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-3000_NED-4_KK-1_M-500To1000_13TeV-sherpa/crab_ADDGravToGG_MS-3000_NED-4_KK-1_M-500To1000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_181138/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-3500_NED-2_KK-1_M-1000To2000_13TeV-sherpa/crab_ADDGravToGG_MS-3500_NED-2_KK-1_M-1000To2000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_181149/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-3500_NED-2_KK-1_M-2000To3500_13TeV-sherpa/crab_ADDGravToGG_MS-3500_NED-2_KK-1_M-2000To3500_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_181201/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-3500_NED-2_KK-1_M-500To1000_13TeV-sherpa/crab_ADDGravToGG_MS-3500_NED-2_KK-1_M-500To1000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_181217/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-3500_NED-2_KK-4_M-1000To2000_13TeV-sherpa/crab_ADDGravToGG_MS-3500_NED-2_KK-4_M-1000To2000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_181229/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-3500_NED-2_KK-4_M-2000To3500_13TeV-sherpa/crab_ADDGravToGG_MS-3500_NED-2_KK-4_M-2000To3500_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_181242/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-3500_NED-2_KK-4_M-500To1000_13TeV-sherpa/crab_ADDGravToGG_MS-3500_NED-2_KK-4_M-500To1000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_181254/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-3500_NED-4_KK-1_M-1000To2000_13TeV-sherpa/crab_ADDGravToGG_MS-3500_NED-4_KK-1_M-1000To2000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_181308/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-3500_NED-4_KK-1_M-2000To3500_13TeV-sherpa/crab_ADDGravToGG_MS-3500_NED-4_KK-1_M-2000To3500_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_181320/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-3500_NED-4_KK-1_M-200To500_13TeV-sherpa/crab_ADDGravToGG_MS-3500_NED-4_KK-1_M-200To500_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_181332/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-3500_NED-4_KK-1_M-500To1000_13TeV-sherpa/crab_ADDGravToGG_MS-3500_NED-4_KK-1_M-500To1000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/190206_183440/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-4000_NED-2_KK-1_M-1000To2000_13TeV-sherpa/crab_ADDGravToGG_MS-4000_NED-2_KK-1_M-1000To2000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_181358/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-4000_NED-2_KK-1_M-2000To4000_13TeV-sherpa/crab_ADDGravToGG_MS-4000_NED-2_KK-1_M-2000To4000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_181413/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-4000_NED-2_KK-1_M-500To1000_13TeV-sherpa/crab_ADDGravToGG_MS-4000_NED-2_KK-1_M-500To1000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_181424/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-4000_NED-2_KK-4_M-1000To2000_13TeV-sherpa/crab_ADDGravToGG_MS-4000_NED-2_KK-4_M-1000To2000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_181436/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-4000_NED-2_KK-4_M-2000To4000_13TeV-sherpa/crab_ADDGravToGG_MS-4000_NED-2_KK-4_M-2000To4000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_181449/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-4000_NED-2_KK-4_M-500To1000_13TeV-sherpa/crab_ADDGravToGG_MS-4000_NED-2_KK-4_M-500To1000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_181501/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-4000_NED-4_KK-1_M-1000To2000_13TeV-sherpa/crab_ADDGravToGG_MS-4000_NED-4_KK-1_M-1000To2000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_181518/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-4000_NED-4_KK-1_M-2000To4000_13TeV-sherpa/crab_ADDGravToGG_MS-4000_NED-4_KK-1_M-2000To4000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_181530/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-4000_NED-4_KK-1_M-200To500_13TeV-sherpa/crab_ADDGravToGG_MS-4000_NED-4_KK-1_M-200To500_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_181542/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-4000_NED-4_KK-1_M-500To1000_13TeV-sherpa/crab_ADDGravToGG_MS-4000_NED-4_KK-1_M-500To1000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_181556/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-4500_NED-2_KK-1_M-1000To2000_13TeV-sherpa/crab_ADDGravToGG_MS-4500_NED-2_KK-1_M-1000To2000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_181612/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-4500_NED-2_KK-1_M-2000To3000_13TeV-sherpa/crab_ADDGravToGG_MS-4500_NED-2_KK-1_M-2000To3000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_181623/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-4500_NED-2_KK-1_M-3000To4500_13TeV-sherpa/crab_ADDGravToGG_MS-4500_NED-2_KK-1_M-3000To4500_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_181635/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-4500_NED-2_KK-1_M-500To1000_13TeV-sherpa/crab_ADDGravToGG_MS-4500_NED-2_KK-1_M-500To1000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_181646/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-4500_NED-2_KK-4_M-1000To2000_13TeV-sherpa/crab_ADDGravToGG_MS-4500_NED-2_KK-4_M-1000To2000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_181700/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-4500_NED-2_KK-4_M-2000To3000_13TeV-sherpa/crab_ADDGravToGG_MS-4500_NED-2_KK-4_M-2000To3000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_181716/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-4500_NED-2_KK-4_M-3000To4500_13TeV-sherpa/crab_ADDGravToGG_MS-4500_NED-2_KK-4_M-3000To4500_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_181728/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-4500_NED-2_KK-4_M-500To1000_13TeV-sherpa/crab_ADDGravToGG_MS-4500_NED-2_KK-4_M-500To1000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_181740/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-4500_NED-4_KK-1_M-1000To2000_13TeV-sherpa/crab_ADDGravToGG_MS-4500_NED-4_KK-1_M-1000To2000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_181751/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-4500_NED-4_KK-1_M-2000To3000_13TeV-sherpa/crab_ADDGravToGG_MS-4500_NED-4_KK-1_M-2000To3000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_181809/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-4500_NED-4_KK-1_M-200To500_13TeV-sherpa/crab_ADDGravToGG_MS-4500_NED-4_KK-1_M-200To500_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_181821/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-4500_NED-4_KK-1_M-3000To4500_13TeV-sherpa/crab_ADDGravToGG_MS-4500_NED-4_KK-1_M-3000To4500_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_181832/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-4500_NED-4_KK-1_M-500To1000_13TeV-sherpa/crab_ADDGravToGG_MS-4500_NED-4_KK-1_M-500To1000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_181844/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-5000_NED-2_KK-1_M-1000To2000_13TeV-sherpa/crab_ADDGravToGG_MS-5000_NED-2_KK-1_M-1000To2000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_181855/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-5000_NED-2_KK-1_M-2000To3000_13TeV-sherpa/crab_ADDGravToGG_MS-5000_NED-2_KK-1_M-2000To3000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_181915/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-5000_NED-2_KK-1_M-500To1000_13TeV-sherpa/crab_ADDGravToGG_MS-5000_NED-2_KK-1_M-500To1000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_181939/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-5000_NED-2_KK-4_M-1000To2000_13TeV-sherpa/crab_ADDGravToGG_MS-5000_NED-2_KK-4_M-1000To2000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_181951/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-5000_NED-2_KK-4_M-2000To3000_13TeV-sherpa/crab_ADDGravToGG_MS-5000_NED-2_KK-4_M-2000To3000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_182007/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-5000_NED-2_KK-4_M-3000To5000_13TeV-sherpa/crab_ADDGravToGG_MS-5000_NED-2_KK-4_M-3000To5000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_182020/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-5000_NED-2_KK-4_M-500To1000_13TeV-sherpa/crab_ADDGravToGG_MS-5000_NED-2_KK-4_M-500To1000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_182033/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-5000_NED-4_KK-1_M-1000To2000_13TeV-sherpa/crab_ADDGravToGG_MS-5000_NED-4_KK-1_M-1000To2000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_182044/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-5000_NED-4_KK-1_M-2000To3000_13TeV-sherpa/crab_ADDGravToGG_MS-5000_NED-4_KK-1_M-2000To3000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_182057/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-5000_NED-4_KK-1_M-200To500_13TeV-sherpa/crab_ADDGravToGG_MS-5000_NED-4_KK-1_M-200To500_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_182112/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-5000_NED-4_KK-1_M-3000To5000_13TeV-sherpa/crab_ADDGravToGG_MS-5000_NED-4_KK-1_M-3000To5000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_182127/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-5000_NED-4_KK-1_M-500To1000_13TeV-sherpa/crab_ADDGravToGG_MS-5000_NED-4_KK-1_M-500To1000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_182140/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-5500_NED-2_KK-1_M-1000To2000_13TeV-sherpa/crab_ADDGravToGG_MS-5500_NED-2_KK-1_M-1000To2000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_182156/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-5500_NED-2_KK-1_M-2000To4000_13TeV-sherpa/crab_ADDGravToGG_MS-5500_NED-2_KK-1_M-2000To4000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_182218/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-5500_NED-2_KK-1_M-4000To5500_13TeV-sherpa/crab_ADDGravToGG_MS-5500_NED-2_KK-1_M-4000To5500_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_182236/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-5500_NED-2_KK-1_M-500To1000_13TeV-sherpa/crab_ADDGravToGG_MS-5500_NED-2_KK-1_M-500To1000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_182248/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-5500_NED-2_KK-4_M-1000To2000_13TeV-sherpa/crab_ADDGravToGG_MS-5500_NED-2_KK-4_M-1000To2000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_182300/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-5500_NED-2_KK-4_M-2000To4000_13TeV-sherpa/crab_ADDGravToGG_MS-5500_NED-2_KK-4_M-2000To4000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_182315/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-5500_NED-2_KK-4_M-4000To5500_13TeV-sherpa/crab_ADDGravToGG_MS-5500_NED-2_KK-4_M-4000To5500_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_182327/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-5500_NED-2_KK-4_M-500To1000_13TeV-sherpa/crab_ADDGravToGG_MS-5500_NED-2_KK-4_M-500To1000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_182341/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-5500_NED-4_KK-1_M-1000To2000_13TeV-sherpa/crab_ADDGravToGG_MS-5500_NED-4_KK-1_M-1000To2000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/190206_183406/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-5500_NED-4_KK-1_M-2000To4000_13TeV-sherpa/crab_ADDGravToGG_MS-5500_NED-4_KK-1_M-2000To4000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_182408/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-5500_NED-4_KK-1_M-200To500_13TeV-sherpa/crab_ADDGravToGG_MS-5500_NED-4_KK-1_M-200To500_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_182421/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-5500_NED-4_KK-1_M-4000To5500_13TeV-sherpa/crab_ADDGravToGG_MS-5500_NED-4_KK-1_M-4000To5500_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_182432/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-5500_NED-4_KK-1_M-500To1000_13TeV-sherpa/crab_ADDGravToGG_MS-5500_NED-4_KK-1_M-500To1000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_182447/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-6000_NED-2_KK-1_M-1000To2000_13TeV-sherpa/crab_ADDGravToGG_MS-6000_NED-2_KK-1_M-1000To2000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_182459/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-6000_NED-2_KK-1_M-2000To4000_13TeV-sherpa/crab_ADDGravToGG_MS-6000_NED-2_KK-1_M-2000To4000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_182515/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-6000_NED-2_KK-1_M-4000To6000_13TeV-sherpa/crab_ADDGravToGG_MS-6000_NED-2_KK-1_M-4000To6000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_182526/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-6000_NED-2_KK-1_M-500To1000_13TeV-sherpa/crab_ADDGravToGG_MS-6000_NED-2_KK-1_M-500To1000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_182538/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-6000_NED-2_KK-4_M-1000To2000_13TeV-sherpa/crab_ADDGravToGG_MS-6000_NED-2_KK-4_M-1000To2000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_182551/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-6000_NED-2_KK-4_M-2000To4000_13TeV-sherpa/crab_ADDGravToGG_MS-6000_NED-2_KK-4_M-2000To4000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_182608/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-6000_NED-2_KK-4_M-4000To6000_13TeV-sherpa/crab_ADDGravToGG_MS-6000_NED-2_KK-4_M-4000To6000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_182620/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-6000_NED-2_KK-4_M-500To1000_13TeV-sherpa/crab_ADDGravToGG_MS-6000_NED-2_KK-4_M-500To1000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_182632/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-6000_NED-4_KK-1_M-1000To2000_13TeV-sherpa/crab_ADDGravToGG_MS-6000_NED-4_KK-1_M-1000To2000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_182643/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-6000_NED-4_KK-1_M-2000To4000_13TeV-sherpa/crab_ADDGravToGG_MS-6000_NED-4_KK-1_M-2000To4000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_182658/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-6000_NED-4_KK-1_M-200To500_13TeV-sherpa/crab_ADDGravToGG_MS-6000_NED-4_KK-1_M-200To500_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_182714/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-6000_NED-4_KK-1_M-4000To6000_13TeV-sherpa/crab_ADDGravToGG_MS-6000_NED-4_KK-1_M-4000To6000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_182726/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-6000_NED-4_KK-1_M-500To1000_13TeV-sherpa/crab_ADDGravToGG_MS-6000_NED-4_KK-1_M-500To1000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_182739/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-7000_NED-2_KK-1_M-1000To2000_13TeV-sherpa/crab_ADDGravToGG_MS-7000_NED-2_KK-1_M-1000To2000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_182753/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-7000_NED-2_KK-1_M-2000To4000_13TeV-sherpa/crab_ADDGravToGG_MS-7000_NED-2_KK-1_M-2000To4000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_182810/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-7000_NED-2_KK-1_M-4000To7000_13TeV-sherpa/crab_ADDGravToGG_MS-7000_NED-2_KK-1_M-4000To7000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_182823/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-7000_NED-2_KK-1_M-500To1000_13TeV-sherpa/crab_ADDGravToGG_MS-7000_NED-2_KK-1_M-500To1000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_182836/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-7000_NED-4_KK-1_M-1000To2000_13TeV-sherpa/crab_ADDGravToGG_MS-7000_NED-4_KK-1_M-1000To2000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_182849/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-7000_NED-4_KK-1_M-2000To4000_13TeV-sherpa/crab_ADDGravToGG_MS-7000_NED-4_KK-1_M-2000To4000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_182902/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-7000_NED-4_KK-1_M-4000To7000_13TeV-sherpa/crab_ADDGravToGG_MS-7000_NED-4_KK-1_M-4000To7000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_182919/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-7000_NED-4_KK-1_M-500To1000_13TeV-sherpa/crab_ADDGravToGG_MS-7000_NED-4_KK-1_M-500To1000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_182933/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-8000_NED-2_KK-1_M-1000To2000_13TeV-sherpa/crab_ADDGravToGG_MS-8000_NED-2_KK-1_M-1000To2000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_182945/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-8000_NED-2_KK-1_M-2000To4000_13TeV-sherpa/crab_ADDGravToGG_MS-8000_NED-2_KK-1_M-2000To4000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_183000/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-8000_NED-2_KK-1_M-4000To8000_13TeV-sherpa/crab_ADDGravToGG_MS-8000_NED-2_KK-1_M-4000To8000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_183019/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-8000_NED-2_KK-1_M-500To1000_13TeV-sherpa/crab_ADDGravToGG_MS-8000_NED-2_KK-1_M-500To1000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_183036/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-8000_NED-4_KK-1_M-1000To2000_13TeV-sherpa/crab_ADDGravToGG_MS-8000_NED-4_KK-1_M-1000To2000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_183052/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-8000_NED-4_KK-1_M-2000To4000_13TeV-sherpa/crab_ADDGravToGG_MS-8000_NED-4_KK-1_M-2000To4000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_183107/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-8000_NED-4_KK-1_M-4000To8000_13TeV-sherpa/crab_ADDGravToGG_MS-8000_NED-4_KK-1_M-4000To8000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_183120/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-8000_NED-4_KK-1_M-500To1000_13TeV-sherpa/crab_ADDGravToGG_MS-8000_NED-4_KK-1_M-500To1000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_183134/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-9000_NED-2_KK-1_M-1000To2000_13TeV-sherpa/crab_ADDGravToGG_MS-9000_NED-2_KK-1_M-1000To2000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_183146/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-9000_NED-2_KK-1_M-2000To4000_13TeV-sherpa/crab_ADDGravToGG_MS-9000_NED-2_KK-1_M-2000To4000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_183159/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-9000_NED-2_KK-1_M-4000To9000_13TeV-sherpa/crab_ADDGravToGG_MS-9000_NED-2_KK-1_M-4000To9000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_183215/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-9000_NED-2_KK-1_M-500To1000_13TeV-sherpa/crab_ADDGravToGG_MS-9000_NED-2_KK-1_M-500To1000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_183227/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-9000_NED-4_KK-1_M-1000To2000_13TeV-sherpa/crab_ADDGravToGG_MS-9000_NED-4_KK-1_M-1000To2000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_183244/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-9000_NED-4_KK-1_M-2000To4000_13TeV-sherpa/crab_ADDGravToGG_MS-9000_NED-4_KK-1_M-2000To4000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_183302/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-9000_NED-4_KK-1_M-4000To9000_13TeV-sherpa/crab_ADDGravToGG_MS-9000_NED-4_KK-1_M-4000To9000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_183325/0000')
    DATASET.append('/store/user/cawest/ADDGravToGG_MS-9000_NED-4_KK-1_M-500To1000_13TeV-sherpa/crab_ADDGravToGG_MS-9000_NED-4_KK-1_M-500To1000_13TeV-sherpa__80XMiniAODv2__MINIAODSIM/181106_183337/0000')

print "Creating files..."
for dset in DATASET:
    #pattern = "/store/user/cawest/([^(]*)_13TeV-sherpa/crab"
    pattern = "/store/user/cuperez/DiPhotonAnalysis/ExoANDiphoton/([^(]*)_13TeV-sherpa/crab"
    if doADD:
        #pattern = "store/user/cuperez/DiPhotonAnalysis/signal-2018/([^(]*)_TuneCP2_13TeV-pythia8/crab_"
        pattern = "store/user/cuperez/DiPhotonAnalysis/ExoANDiphoton/([^(]*)_TuneCP2_13TeV-pythia8/crab_"
    if doSherpaADD:
        pattern = "/store/user/cawest/([^(]*)_13TeV-sherpa/crab_"

    match = re.findall(pattern, dset)
    #print match
    nametag   = match[0].replace('-', '_')

    setMmax = False
    #if doSherpaADDang:
        #pttn =  "ADDGravToGG_MS-([^(]*)_NED"
        #newmatch = re.findall(pttn, match[0])
        #Mmax = newmatch[0]
        #setMmax = True

    if args.cuts is not None:
        nametag = nametag + "mgg_"+str(MinvCut)
        if setMmax:
            nametag = nametag + "_%s" %(Mmax)

    print nametag
    classname = "Class_%s" %(nametag)
    an_func   = "analyze_%s" %(nametag)
    outfile   = "%s" %(nametag)

    # Template Replacements
    cmssw_base = os.getenv("CMSSW_BASE")
    rep = {'ClassDiphotonSignal': classname,
           "outputfile": outfile,
           "cmssw_base": cmssw_base,
           "eosdsetdir": dset,
           "analyzefunc": an_func,
           }
    if args.cuts is not None:
        rep['MinvCut'] = MinvCut
        if setMmax:
            rep['Mmax'] = Mmax

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
    print "deleted auxilliary files"

if args.run:
    RunAnalyze(os.listdir('.'))
if args.delete:
    DelClassFiles(os.listdir('.'))

sw.Stop()
print "Real time: " + str(sw.RealTime() / 60.0) + " minutes"
print "CPU time:  " + str(sw.CpuTime() / 60.0) + " minutes"
