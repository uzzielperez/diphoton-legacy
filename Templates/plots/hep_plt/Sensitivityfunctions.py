#!/usr/bin/python

import ROOT
from ROOT import TClass,TKey, TIter,TCanvas, TPad,TFile, TPaveText, TColor, TGaxis, TH1F, TPad, TH1D, TLegend
#from ROOT import kBlack, kBlue, kRed, kGreen, kMagenta, kCyan, kOrange, kViolet, kSpring
from ROOT import kBlue, kOrange, kCyan, kRed, kMagenta, kGreen, kViolet, kSpring, kPink, kAzure
from ROOT import gBenchmark, gStyle, gROOT, gDirectory
from ROOT import TMath
#from legend import *
#from plotsHelpercomp import *
import re

import sys
CMSlumiPath = '/uscms_data/d3/cuperez/CMSSW_8_0_25/src/scripts/pyroot'
sys.path.append(CMSlumiPath)
from CMSlumi import CMS_lumi, set_CMS_lumi
import argparse
import numpy as np
#import scipy.stats.distributions
#from scipy.stats import poisson
import math
sw = ROOT.TStopwatch()
sw.Start()

LambdaT = "ALL"
SMPythia8 = True
SM = False
ADD = True

tag = "b"
zoom = False
#drawstyle = "hist, same"
drawstyle = "same"
#intlumi = 35.9
# Draw Options
DrawAsHi = False
gStyle.SetOptStat(0)

# https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.poisson.html
def poisson_probability(actual, mean):

    # naive:   math.exp(-mean) * mean**actual / factorial(actual)
    return   math.exp(-mean) * mean**actual / math.factorial(actual)

def GetIntegralfromRange(xmin, xmax, hist):
    x = hist.GetXaxis()
    bmin = x.FindBin(xmin)
    bmax = x.FindBin(xmax)
    integral = hist.Integral(bmin, bmax)
    return integral

def Calc95CLuplim(n_obs, s):
	n_obs = int(n_obs)
	tail = 0.05/2.0
	upperlim95CL = ROOT.MathMore.chisquared_quantile(1-tail, 2*(n_obs+1))/2
	#SigCLs95upperlim = CLs95upperlim - n_obs
	return round(upperlim95CL,2)

def RangeByVar(obj, mcut=None, xMin=None, xMax=None, chiMin=None, chiMax=None, label=None):
	if "Minv" in obj:
		xmin, xmax = 500, 13000
		if mcut is not None:
			xmin = int(mcut) 
		if label is not None and "Sherpa" in label:
			xmax = xMax
		if xMin is not None:
			xmin = xMin
		if xMax is not None:
			xmax = xMax
	if "chidiphoton" in obj:
		xmin, xmax = 0, 20
		if chiMin is not None:
			xmin = float(chiMin)
		if chiMax is not None:
			xmax = float(chiMax) 
	if "diphotoncosthetastar" in obj:
		xmin, xmax = -1, 1
	return xmin, xmax 

def CalcSensitivityADD(obj, DATASET, labels, lumi=None, McutList=None, chiMax=None):
	f = open("ADDsensitivity_log.csv", "w+")
	
	histClones, Mcuts = [], []
	
	for dset, label in zip(DATASET, labels):
		if "SM" in label or "GGJets" in label:
			taglabel = label
			#Mcuts.append('500')
		elif "ADD" in label:
			if "Sherpa" in label:	
				Gen, PH, LambdaT, NED, KK = label
				LambdaU = str(round (float(LambdaT)/1000, 1))
				taglabel = "ADDSherpaLU%sKK%s" %(LambdaU, KK)
				Mcuts.append('500')
			else:
				PH, NegInt, LT, mgg = label 
				taglabel = taglabel + "mgg%s" %(mgg) 		
				Mcuts.append(mgg)
		histClone = dset.Clone("hist_%s" %(taglabel))
		histClones.append(histClone)

	b, splusb, modelPt, IntRange = [], [], [], []	
	
	if McutList is not None:	
		Mcuts = McutList	
		
	print "Variable: ", obj 
	print "Model Point, mcut, B, S+B, S, S 95CL uplim, Signal Region"
	header = "Model Point,mcut,B,S+B,S,S95CL,Signal Region\n"
	f.write(header)
	for histclone, label in zip(histClones, labels):
		if "GGJets" in label:
			histSM = histclone
			if lumi is not None:
				histSM.Scale(lumi)
			for mcut in Mcuts:
				xmin, xmax = RangeByVar(obj, mcut)
				b = GetIntegralfromRange(xmin, xmax, histSM)
				#b.append(bkg)
				IntRange.append("%s-%s" %(str(xmin), str(xmax)))
			#print b
		if "ADD" in label:
			if lumi is not None:
				histclone.Scale(lumi)
			for mcut in Mcuts:
				#print label
				xmin, xmax = RangeByVar(obj, mcut)	
				if "Sherpa" in label:	
					Gen, PH, LU, NED, KK = label	
							
					xmin, xmax = RangeByVar(obj, mcut, xMax=int(LU), chiMax=chiMax, label="Sherpa")	
					b = GetIntegralfromRange(xmin, xmax, histSM) 	
					LU = round(float(LU)/1000, 1)	
					lbel = "NED%sLU%sKK%s" %(NED, LU, KK)
					modelPt.append(lbel)
					r = "%s-%s" %(str(xmin), str(xmax))
				else:
					PH, NegInt, LT, mgg = label
					LT = round(float(LT)/1000, 1) 
					lbel = "NI%sLT%s" %(NegInt, LT) 
					modelPt.append(lbel)
					r = "%s-%s" %(str(xmin), str(xmax))	
				sb = GetIntegralfromRange(xmin, xmax, histclone) 
				splusb.append(sb)
				s = sb - b 
				cl95 = Calc95CLuplim(b, s)
				b    = round(b, 1)
				sb   = round(sb, 1)
				s    = round(s, 1)
				cl95 = round(cl95, 1)
			print lbel, mcut, b, sb, s, cl95, r 
			yieldsInfo = "%s,%s,%s,%s,%s,%s,%s\n" %(lbel, mcut, b, sb, s, cl95, r) 
			f.write(yieldsInfo)

def CalcSensitivityUnp(obj, DATASET, intlumi, labelList):
	if labelList is None:
		# The inputs are root files instead of histograms 
        	uf = []
        	for datafile in DATASET:
           		 uf.append(ROOT.TFile(datafile, "READ"))
       		uh = []
       		for openfile in uf:
            		uh.append(openfile.Get(obj))
        	i, iset, histClones = 0, 0, []
         	while i < len(DATASET):
                	histClone = uh[i].Clone("histdu%s" %(DATASET[i]))
                	histClones.append(histClone)
                	i = i + 1
         	sig = []
         	j = 0
         	for histclone in histClones:
                	if "SM" in DATASET[j] or "GGJets" in DATASET[j]: 
          	      		histSM = histclone
          	      		histSM.Scale(intlumi)
          	      		b = histSM.Integral()
          	      		print "b = ", b
           	 	else:
                      		pattern = "OUTUnp_spin([^(]*)_du([^(]*)_LU([^(]*)p0_m([^(]*)_pT([^(]*)_M([^(]*).root"
          	      		match = re.findall(pattern, DATASET[j])
          	      		spin, du, LU, mCut, pTcut, massmin = match[0]
          	      		#print "prescaled: ", histclone.Integral(), " ", histclone.GetEntries()
          	     		histclone.Scale(intlumi)
          	      		#print histclone.Integral(), " ", histclone.GetEntries()
          	      		splusb = histclone.Integral()
          	      		sig.append(splusb)
                      		n_obs = int(b)
                      		tail = 0.05/2.0
          	      		s = splusb - b
          	      		CLs95upperlim = ROOT.MathMore.chisquared_quantile(1-tail, 2*(n_obs+1))/2
                      		SCLs95upperlim = CLs95upperlim - n_obs
                      		print intlumi,  "fb-1; LU, du, massmin= ", LU, du, massmin, ";b: ", b, "; s:", s, "; s+b: ", splusb, "95CLsupperlim(S+B and S):", CLs95upperlim, SCLs95upperlim #"; P(b, s+b): ", TMath.Poisson(b, splusb)
            			j = j+1
	else:
		f = open("sensitivity_log.csv", "w+")
		# DATASETS are already histogram objects
		i, histClones, clonelabels = 0, [], []
		while i < len(DATASET):
			label = labelList[i][0]
			if "SM" in label or "GGJets" in label:
				taglabel = "SM"
			else:
				if "Unp" in label:
					PH, spin, du, LU, pT = label
					taglabel = "spin%s_du%s_LU%s" %(spin, du, LU)
					#leglabel = r"#Lambda_{U}=%s, d_{u}=%s, spin-%s" %(LU, du, spin)
					#('Unp', '0', '1p9', '2000', '70')
				if "ADD" in label:
					minv = False
					if len(label) ==3:
						PH, NegInt, LT = label
					else:
						PH, NegInt, LT, mgg = label
						minv = True
					taglabel = PH + NegInt + "_" + LT
					if minv:
						taglabel = taglabel + "mgg%s" %(mgg)	 
					
			histClone = DATASET[i].Clone("hist_%s" %(taglabel))
			histClones.append(histClone)
			clonelabels.append(taglabel)
			i = i + 1
		i = 0
		if "ADD" in PH:
			header = "Label, intlumi, B, S+B, S, 95CLsUpperLim, Sig95CLsUpperLim \n"
		if "Unp" in PH: 
			header = "intlumi, spin, du, LambdaU, B, S+B, S, 95CLsUpperLim, Sig95CLsUpperLim \n"
		print header[:-1]
		f.write(header)
		for histclone in histClones:
			if "SM" in clonelabels[i] or "GGJets" in clonelabels[i]:
				histSM = histclone
				histSM.Scale(intlumi)
				b = GetIntegralfromRange(2000, 13000, histSM)
				#print "b = ", b
				#f.write("B = %s" %(str(b)))
			else:
				PH, spin, du, LU, pT = labelList[i][0]
				histclone.Scale(intlumi)
				splusb = GetIntegralfromRange(2000, 13000, histclone)
				n_obs = int(b)
				tail = 0.05/2.0
				s = splusb - b
				CLs95upperlim = ROOT.MathMore.chisquared_quantile(1-tail, 2*(n_obs+1))/2
	 			SigCLs95upperlim = CLs95upperlim - n_obs
				yields_info = "%s, %s, %s, %s, %s, %s, %s, %s, %s \n" %(str(intlumi), str(spin), str(du), str(LU), str(b), str(splusb), str(s), str(CLs95upperlim), str(SigCLs95upperlim))
				print yields_info[:-1]
				f.write(yields_info)
				#print intlumi,  "fb-1; LU, du= ", LU, du, ";b: ", b, "; s:", s, "; s+b: ", splusb, "95CLsupperlim(S+B and S):", CLs95upperlim, SCLs95upperlim #"; P(b, s+b): ", TMath.Poisson(b, splusb)
            		i = i + 1
		f.close()
