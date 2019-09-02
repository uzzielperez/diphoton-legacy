#!/usr/bin/python

import ROOT
from ROOT import gBenchmark, gStyle, gROOT, gDirectory
import re
from hep_plt.Sensitivityfunctions import CalcSensitivityADD
from hep_plt.Plotfunctions import *
import argparse

# Command line options
parser = argparse.ArgumentParser(description="NonResonance")
parser.add_argument("-p", "--plot", action="store_true", help="Clean directory and delete copied files")
parser.add_argument("-s", "--sensitivity", action="store_true", help="Run os.system(cmd) to get CRAB files.")
args = parser.parse_args()

sw = ROOT.TStopwatch()
sw.Start()
gStyle.SetOptStat(0)


# To suppress canvas from popping up. Speeds up plots production.
gROOT.SetBatch()

doSM 	   = True

# ADD
doADD         = True
NI1_13        = False  #Pythia
doSherpa      = False

SM_m2000       = True
NI1_13_m2000   = True
doreADD        = False #Sherpa 
doreADDM2k     = True  #Sherpa


# Variables to Plot
kinematicsON = True
genON        = False
angularON    = True

isEBEB       = False

obj = []
if kinematicsON:
        obj.append("diphotonMinv")
#        obj.append("photon1Pt")
#        obj.append("photon2Pt")
#        obj.append("photon1Eta")
#        obj.append("photon2Eta")
#       	obj.append("photon1Phi")
#        obj.append("photon2Phi")
	if isEBEB:
		obj.append("diphotonMinvisEBEB")
if angularON:
        obj.append("chidiphoton")
        obj.append("diphotoncosthetastar")
	if isEBEB:
		obj.append("chidiphotonisEBEB")
		obj.append("diphotoncosthetastarisEBEB")
if genON:
        obj.append("gendiphotonMinv")
#        obj.append("genphoton1Pt")
#        obj.append("genphoton2Pt")
#        obj.append("genphoton1Eta")
#        obj.append("genphoton2Eta")
#        obj.append("genphoton1Phi")
#        obj.append("genphoton2Phi")
        if angularON:
                obj.append("genchidiphoton")
                obj.append("gendiphotoncosthetastar")


if doSM:
        DATASETSM = []
        if SM_m2000:
                DATASETSM.append("../NonResonanceTemplates/OUTGGJets_M_1000To2000_Pt_50mgg_2000.root")
                DATASETSM.append("../NonResonanceTemplates/OUTGGJets_M_4000To6000_Pt_50mgg_2000.root")
                DATASETSM.append("../NonResonanceTemplates/OUTGGJets_M_6000To8000_Pt_50mgg_2000.root")
                DATASETSM.append("../NonResonanceTemplates/OUTGGJets_M_2000To4000_Pt_50mgg_2000.root")
                DATASETSM.append("../NonResonanceTemplates/OUTGGJets_M_500To1000_Pt_50mgg_2000.root")
        else:
            # DATASETSM.append("../NonResonanceTemplates/OUTGGJets_M_60To200_Pt_50.root")
            # DATASETSM.append("../NonResonanceTemplates/OUTGGJets_M_200To500_Pt_50.root")
            DATASETSM.append("../NonResonanceTemplates/OUTGGJets_M_500To1000_Pt_50.root")
            DATASETSM.append("../NonResonanceTemplates/OUTGGJets_M_1000To2000_Pt_50.root")
            DATASETSM.append("../NonResonanceTemplates/OUTGGJets_M_2000To4000_Pt_50.root")
            DATASETSM.append("../NonResonanceTemplates/OUTGGJets_M_4000To6000_Pt_50.root")
            DATASETSM.append("../NonResonanceTemplates/OUTGGJets_M_6000To8000_Pt_50.root")
        varhistsm = [Stitch(DATASETSM, var) for var in obj]
if doADD:
	signal = []
        if NI1_13:
	    tag = "NI1_13"
            DATASETS = []
            DATASETS.append("../NonResonanceTemplates/OUTADDGravToGG_NegInt_1_LambdaT_13000_M_1000To2000.root")
            DATASETS.append("../NonResonanceTemplates/OUTADDGravToGG_NegInt_1_LambdaT_13000_M_2000To4000.root")
            DATASETS.append("../NonResonanceTemplates/OUTADDGravToGG_NegInt_1_LambdaT_13000_M_4000To13000.root")
            DATASETS.append("../NonResonanceTemplates/OUTADDGravToGG_NegInt_1_LambdaT_13000_M_500To1000.root")
            vhist = [Stitch(DATASETS, var) for var in obj]
	    signal.append(vhist)
            #print len(varhist)
        if NI1_13_m2000:
            tag = "m2kNI1_13"
            DSETm2000 = []
            DSETm2000.append("../NonResonanceTemplates/OUTADDGravToGG_NegInt_1_LambdaT_13000_M_1000To2000mgg_2000.root")
            DSETm2000.append("../NonResonanceTemplates/OUTADDGravToGG_NegInt_1_LambdaT_13000_M_2000To4000mgg_2000.root")
            DSETm2000.append("../NonResonanceTemplates/OUTADDGravToGG_NegInt_1_LambdaT_13000_M_4000To13000mgg_2000.root")
            DSETm2000.append("../NonResonanceTemplates/OUTADDGravToGG_NegInt_1_LambdaT_13000_M_500To1000mgg_2000.root")
            # Stitch function returns stitched histogram and label - Tuple
	    vhist2 = [Stitch(DSETm2000, var) for var in obj]
	    signal.append(vhist2)
        if doreADD:
            DATASETS = []

            #DATASETS.append("../NonResonanceTemplates/OUTADDGravToGG_MS_6000_NED_4_KK_1_M_1000To2000.root")
            #DATASETS.append("../NonResonanceTemplates/OUTADDGravToGG_MS_6000_NED_4_KK_1_M_2000To4000.root")
            #DATASETS.append("../NonResonanceTemplates/OUTADDGravToGG_MS_6000_NED_4_KK_1_M_200To500.root")
            #DATASETS.append("../NonResonanceTemplates/OUTADDGravToGG_MS_6000_NED_4_KK_1_M_4000To6000.root")
            #DATASETS.append("../NonResonanceTemplates/OUTADDGravToGG_MS_6000_NED_4_KK_1_M_500To1000.root")
            #sig = [Stitch(DATASETS, var) for var in obj]
            #signal.append(sig)

            DATASETS = []

            DATASETS.append("../NonResonanceTemplates/OUTADDGravToGG_MS_8000_NED_4_KK_1_M_1000To2000.root")
            DATASETS.append("../NonResonanceTemplates/OUTADDGravToGG_MS_8000_NED_4_KK_1_M_2000To4000.root")
            DATASETS.append("../NonResonanceTemplates/OUTADDGravToGG_MS_8000_NED_4_KK_1_M_4000To8000.root")
            DATASETS.append("../NonResonanceTemplates/OUTADDGravToGG_MS_8000_NED_4_KK_1_M_500To1000.root")
            sig = [Stitch(DATASETS, var) for var in obj]
            signal.append(sig)

            DATASETS = []
            DATASETS.append("../NonResonanceTemplates/OUTADDGravToGG_MS_10000_NED_4_KK_1_M_2000To4000.root")
            DATASETS.append("../NonResonanceTemplates/OUTADDGravToGG_MS_10000_NED_4_KK_1_M_4000To10000.root")
            DATASETS.append("../NonResonanceTemplates/OUTADDGravToGG_MS_10000_NED_4_KK_1_M_500To1000.root")
            sig = [Stitch(DATASETS, var) for var in obj]
            signal.append(sig)
            DATASETS = []

            DATASETS.append("../NonResonanceTemplates/OUTADDGravToGG_MS_11000_NED_4_KK_1_M_1000To2000.root")
            DATASETS.append("../NonResonanceTemplates/OUTADDGravToGG_MS_11000_NED_4_KK_1_M_2000To4000.root")
            DATASETS.append("../NonResonanceTemplates/OUTADDGravToGG_MS_11000_NED_4_KK_1_M_4000To11000.root")
            sig = [Stitch(DATASETS, var) for var in obj]
            signal.append(sig)

        if doreADDM2k:
            DATASETS = []
            #DATASETS.append("../NonResonanceTemplates/OUTADDGravToGG_MS_6000_NED_4_KK_1_M_1000To2000.root")
            #DATASETS.append("../NonResonanceTemplates/OUTADDGravToGG_MS_6000_NED_4_KK_1_M_2000To4000.root")
            #DATASETS.append("../NonResonanceTemplates/OUTADDGravToGG_MS_6000_NED_4_KK_1_M_200To500.root")
            #DATASETS.append("../NonResonanceTemplates/OUTADDGravToGG_MS_6000_NED_4_KK_1_M_4000To6000.root")
            #DATASETS.append("../NonResonanceTemplates/OUTADDGravToGG_MS_6000_NED_4_KK_1_M_500To1000.root")
            #sig = [Stitch(DATASETS, var) for var in obj]
            #signal.append(sig)

            DATASETS = []
            DATASETS.append("../NonResonanceTemplates/OUTADDGravToGG_MS_8000_NED_4_KK_1_M_1000To2000mgg_2000_8000.root")
            DATASETS.append("../NonResonanceTemplates/OUTADDGravToGG_MS_8000_NED_4_KK_1_M_2000To4000mgg_2000_8000.root")
            DATASETS.append("../NonResonanceTemplates/OUTADDGravToGG_MS_8000_NED_4_KK_1_M_4000To8000mgg_2000_8000.root")
            #DATASETS.append("../NonResonanceTemplates/OUTADDGravToGG_MS_8000_NED_4_KK_1_M_500To1000mgg_2000_8000.root")
            sig = [Stitch(DATASETS, var) for var in obj]
            signal.append(sig)

            DATASETS = []
            DATASETS.append("../NonResonanceTemplates/OUTADDGravToGG_MS_10000_NED_4_KK_1_M_1000To2000mgg_2000_10000.root")
            DATASETS.append("../NonResonanceTemplates/OUTADDGravToGG_MS_10000_NED_4_KK_1_M_2000To4000mgg_2000_10000.root")
            DATASETS.append("../NonResonanceTemplates/OUTADDGravToGG_MS_10000_NED_4_KK_1_M_4000To10000mgg_2000_10000.root")
            #DATASETS.append("../NonResonanceTemplates/OUTADDGravToGG_MS_10000_NED_4_KK_1_M_500To1000mgg_2000_10000.root")
            sig = [Stitch(DATASETS, var) for var in obj]
            signal.append(sig)

            DATASETS = []
            DATASETS.append("../NonResonanceTemplates/OUTADDGravToGG_MS_11000_NED_4_KK_1_M_1000To2000mgg_2000_11000.root")
            DATASETS.append("../NonResonanceTemplates/OUTADDGravToGG_MS_11000_NED_4_KK_1_M_2000To4000mgg_2000_11000.root")
            DATASETS.append("../NonResonanceTemplates/OUTADDGravToGG_MS_11000_NED_4_KK_1_M_4000To11000mgg_2000_11000.root")
            #DATASETS.append("../OUTADDGravToGG_MS_11000_NED_4_KK_1_M_500To1000mgg_2000_11000.root")
            sig = [Stitch(DATASETS, var) for var in obj]
            signal.append(sig)



#print obj
mcuts = ['1000', '2000', '2500', '3000', '3500']
ipts, ivar = 0, 0 #signal[modelptindex][varindex][hist(0)/label(1)]
for var, sm in zip(obj, varhistsm):
	# New stack for each variable
	hstack, labels = [], []
	hstack.append(sm[0])
	labels.append(sm[1])
	for sig in signal:
		hstack.append(sig[ivar][0])
		labels.append(sig[ivar][1])
	#print labels
	ivar = ivar + 1

	# Plots
	if args.plot:
	       #OverlayHists(var, hstack, labels, tag=tag, lumi=137)
           OverlayHists(var, hstack, labels, tag="sherpa", lumi=137, Background="Y", Mrange=(2000,13000))

    	if args.sensitivity:
		if "Minv" in var or "chidiphoton" in var or "costhetastar" in var:
			#CalcSensitivityADD(var, hstack, labels, lumi=137, McutList=mcuts)
			#CalcSensitivityADD(var, hstack, labels, lumi=137)
            		CalcSensitivityADD(var, hstack, labels, lumi=137, McutList=['2000'], chiMax=3.0)

# Original
"""
for var, sm, sig in zip(obj, varhistsm, varhist):
    #print var, sm[1], sig[1]
    hstack = []
    hstack.append(sm[0])
    hstack.append(sig[0])
    labels = []
    labels.append(sm[1])
    labels.append(sig[1])

    OverlayHists(var, hstack, labels)
"""
