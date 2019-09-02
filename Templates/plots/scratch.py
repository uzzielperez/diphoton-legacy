#!/usr/bin/python

import ROOT
from ROOT import gBenchmark, gStyle, gROOT, gDirectory
import re
from hep_plt.Sensitivityfunctions import *
from hep_plt.Plotfunctions import *
import argparse
import numpy as np


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

var = "chidiphoton"
#var = "diphotoncosthetastar"
#var = "diphotonMinv"

if doSM:
        DATASETSM = []
        DATASETSM.append("../NonResonanceTemplates/OUTGGJets_M_1000To2000_Pt_50mgg_2000.root")
       	DATASETSM.append("../NonResonanceTemplates/OUTGGJets_M_4000To6000_Pt_50mgg_2000.root")
        DATASETSM.append("../NonResonanceTemplates/OUTGGJets_M_6000To8000_Pt_50mgg_2000.root")
        DATASETSM.append("../NonResonanceTemplates/OUTGGJets_M_2000To4000_Pt_50mgg_2000.root")
        DATASETSM.append("../NonResonanceTemplates/OUTGGJets_M_500To1000_Pt_50mgg_2000.root")
	histSM, labelSM = Stitch(DATASETSM, var)
	
if doADD:
	signal = []
        DSETm2000 = []
        DSETm2000.append("../NonResonanceTemplates/OUTADDGravToGG_NegInt_1_LambdaT_13000_M_1000To2000mgg_2000.root")
        DSETm2000.append("../NonResonanceTemplates/OUTADDGravToGG_NegInt_1_LambdaT_13000_M_2000To4000mgg_2000.root")
       	DSETm2000.append("../NonResonanceTemplates/OUTADDGravToGG_NegInt_1_LambdaT_13000_M_4000To13000mgg_2000.root")
        DSETm2000.append("../NonResonanceTemplates/OUTADDGravToGG_NegInt_1_LambdaT_13000_M_500To1000mgg_2000.root")
	hist, label = Stitch(DSETm2000, var) 

hstack = [histSM, hist]
labell = [labelSM, label]

if "Minv" in var:
	xmin, xmax = 2000, 13000
if "chidiphoton" in var:
	xmin, xmax = 0, 20
if "costhetastar" in var:
	xmin, xmax = -1, 1

print label
b = GetIntegralfromRange(xmin, xmax, histSM)
sb = GetIntegralfromRange(xmin, xmax, hist)
print round(137*b,2)
print round(137*sb,2)

hstack = [histSM, hist]
labell = [labelSM, label]

CalcSensitivityADD(var, hstack, labell, lumi=137)
print "\n \n" 
#print "Maximizing S/B enhancement over chidiphoton range.."
print "Looping over range of cuts..."
print "When Signal yield is close to 95CL upper limit (last column), we have a better chance at exclusion."
xmaxL = np.arange(1,7, 1)
#print xmaxL
print "SR,   b,   sb,   s,  cl95  s-cl95" 
for xmax in xmaxL:
	b    = round(137*GetIntegralfromRange(xmin, xmax, histSM), 2)
	sb   = round(137*GetIntegralfromRange(xmin, xmax, hist), 2)
	s    = sb - b
	n_obs = int(b)
	cl95 = Calc95CLuplim(n_obs, s)
	delta = cl95-s   
	print xmin, "-", xmax, b, sb, s, cl95, delta


