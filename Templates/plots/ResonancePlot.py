#!/usr/bin/python

import ROOT
from ROOT import gBenchmark, gStyle, gROOT, gDirectory
import re
# from hep_plt.Sensitivityfunctions import CalcSensitivity
from hep_plt.Plotfunctions import *

gStyle.SetOptStat(0)

# To suppress canvas from popping up. Speeds up plots production.
gROOT.SetBatch()

# Variables to Plot
kinematicsON = False
genON 	     = True
angularON    = False

# Plot Resonant Models
isRSG_model  = False
isHeavyHiggs = False
customList   = True

# Overlay Signal with Background
doSM   	     = False

# Width options: Narrower, comparable, wider than the detector resolution
W_narrow = True
W_medium = False
W_wider  = True


obj = []
if kinematicsON:
	obj.append("diphotonMinv")
	obj.append("photon1Pt")
	obj.append("photon2Pt")
	obj.append("photon1Eta")
	obj.append("photon2Eta")
	obj.append("photon1Phi")
	obj.append("photon2Phi")
if angularON:
	obj.append("chidiphoton")
	obj.append("diphotoncosthetastar")
if genON:
	obj.append("gendiphotonMinv")
	# obj.append("genphoton1Pt")
	# obj.append("genphoton2Pt")
	# obj.append("genphoton1Eta")
	# obj.append("genphoton2Eta")
	# obj.append("genphoton1Phi")
	# obj.append("genphoton2Phi")
	if angularON:
		obj.append("genchidiphoton")
		obj.append("gendiphotoncosthetastar")




DATASET = []
if customList:
	DATASET.append("../ResonanceTemplates/OUTRSGravitonToGammaGamma_kMpl001_M_5000.root")
	DATASET.append("../ResonanceTemplates/OUTRSGravitonToGammaGamma_kMpl01_M_750.root")
	DATASET.append("../ResonanceTemplates/OUTRSGravitonToGammaGamma_kMpl001_M_750.root")
	DATASET.append("../ResonanceTemplates/OUTRSGravitonToGammaGamma_kMpl02_M_5000.root")
	DATASET.append("../ResonanceTemplates/OUTRSGravitonToGammaGamma_kMpl01_M_5000.root")
	DATASET.append("../ResonanceTemplates/OUTRSGravitonToGammaGamma_kMpl02_M_750.root")
if W_narrow:
	if isRSG_model:
		DATASET.append("../ResonanceTemplates/OUTRSGravitonToGammaGamma_kMpl001_M_750.root")
if W_medium:
	if isRSG_model:
		DATASET.append("../ResonanceTemplates/OUTRSGravitonToGammaGamma_kMpl01_M_1250.root")
		DATASET.append("../ResonanceTemplates/OUTRSGravitonToGammaGamma_kMpl01_M_1500.root")
		DATASET.append("../ResonanceTemplates/OUTRSGravitonToGammaGamma_kMpl01_M_2500.root")
		DATASET.append("../ResonanceTemplates/OUTRSGravitonToGammaGamma_kMpl01_M_3000.root")
		DATASET.append("../ResonanceTemplates/OUTRSGravitonToGammaGamma_kMpl01_M_4250.root")
		DATASET.append("../ResonanceTemplates/OUTRSGravitonToGammaGamma_kMpl01_M_4750.root")
		DATASET.append("../ResonanceTemplates/OUTRSGravitonToGammaGamma_kMpl01_M_5000.root")
		DATASET.append("../ResonanceTemplates/OUTRSGravitonToGammaGamma_kMpl01_M_5750.root")
		DATASET.append("../ResonanceTemplates/OUTRSGravitonToGammaGamma_kMpl01_M_6000.root")
		DATASET.append("../ResonanceTemplates/OUTRSGravitonToGammaGamma_kMpl01_M_6500.root")
if W_wider:
	if isRSG_model:
		DATASET.append("../ResonanceTemplates/OUTRSGravitonToGammaGamma_kMpl02_M_1000.root")
		DATASET.append("../ResonanceTemplates/OUTRSGravitonToGammaGamma_kMpl02_M_1750.root")
		DATASET.append("../ResonanceTemplates/OUTRSGravitonToGammaGamma_kMpl02_M_2000.root")
		DATASET.append("../ResonanceTemplates/OUTRSGravitonToGammaGamma_kMpl02_M_2250.root")
		DATASET.append("../ResonanceTemplates/OUTRSGravitonToGammaGamma_kMpl02_M_2500.root")
		DATASET.append("../ResonanceTemplates/OUTRSGravitonToGammaGamma_kMpl02_M_3500.root")
		DATASET.append("../ResonanceTemplates/OUTRSGravitonToGammaGamma_kMpl02_M_5000.root")
		DATASET.append("../ResonanceTemplates/OUTRSGravitonToGammaGamma_kMpl02_M_5500.root")
		DATASET.append("../ResonanceTemplates/OUTRSGravitonToGammaGamma_kMpl02_M_5750.root")
		DATASET.append("../ResonanceTemplates/OUTRSGravitonToGammaGamma_kMpl02_M_7000.root")
		DATASET.append("../ResonanceTemplates/OUTRSGravitonToGammaGamma_kMpl02_M_750.root")
		DATASET.append("../ResonanceTemplates/OUTRSGravitonToGammaGamma_kMpl02_M_8000.root")

if doSM:
	DATASETSM = []
	DATASETSM.append("../ResonanceTemplates/OUTGGJets_M_60To200_Pt_50.root")
	DATASETSM.append("../ResonanceTemplates/OUTGGJets_M_200To500_Pt_50.root")
	DATASETSM.append("../ResonanceTemplates/OUTGGJets_M_500To1000_Pt_50.root")
	DATASETSM.append("../ResonanceTemplates/OUTGGJets_M_1000To2000_Pt_50.root")
	DATASETSM.append("../ResonanceTemplates/OUTGGJets_M_2000To4000_Pt_50.root")
	DATASETSM.append("../ResonanceTemplates/OUTGGJets_M_4000To6000_Pt_50.root")
	DATASETSM.append("../ResonanceTemplates/OUTGGJets_M_6000To8000_Pt_50.root")

for dset in DATASET:
	for var in obj:
		if doSM:
			print "Plotting %s of %s." %(var, dset)
   			SMhistlabeltuple = Stitch(DATASETSM, "%s" %(var))
			if "gen" in var:
				PlotResonance(var, dset, color=2, outputdir="make")
			else:
				PlotResonance(var, dset, color=2, outputdir="make", Background=SMhistlabeltuple)
		else:
			PlotResonance(var, dset, color=2, outputdir="make")
