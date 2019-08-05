#!/usr/bin/python

import ROOT
from ROOT import TClass,TKey, TIter,TCanvas, TPad,TFile, TPaveText, TColor, TGaxis, TH1F, TPad, TH1D, TLegend
from ROOT import kBlack, kBlue, kRed, kGreen, kMagenta, kCyan, kOrange, kViolet, kSpring
from ROOT import kBlue, kOrange, kCyan, kRed, kMagenta, kGreen, kViolet, kSpring, kPink, kAzure
from ROOT import gBenchmark, gStyle, gROOT, gDirectory
#from legend import *
#from plotsHelpercomp import *
import re
from ROOT import TMath
import sys
import os

#cmssw_base = os.getenv("CMSSW_BASE")
#CMSlumiPath = '/uscms_data/d3/cuperez/CMSSW_8_0_25/src/scripts/pyroot'
#CMSlumiPath = cmssw_base + 'Analyses/pyroot'
#sys.path.append(CMSlumiPath)

from CMSlumi import CMS_lumi, set_CMS_lumi
import argparse
from LambdaUcalc import xsecRatio

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
intlumi = 137
# Draw Options
DrawAsHi = False
gStyle.SetOptStat(0)
	

def labelParser(sample):
	if "SM" in sample:
		pattern = "OUT([^(]*)_pT70_"
		match 	= re.findall(pattern, sample)
		label = match[0]
	if "GGJets" in sample:
		pattern = "OUT([^(]*)_M"
		match = re.findall(pattern, sample)
		label = match[0]
		#labelList.appen
	if "RSG" in sample:
		pattern = "OUT([^(]*)ravitonToGammaGamma_kMpl([^(]*)_M_([^(]*).root"
		match = re.fiindall(pattern, sample)
		#PH, kMpl, M = match[0]
		label = match[0]
	if "GluGlu" in sample:
		pattern = "OUT([^(]*)Spin0ToGammaGamma_W_([^(]*)_M_([^(]*).root"
		match = re.findall(pattern, sample)
		#PH,W, M  = match[0]
		label = match[0]
	if "ADD" in sample:
		if "KK" in sample:
			pattern = "OUT([^(]*)GravToGG_MS_([^(]*)_NED_([^(]*)_KK_([^(]*)_M"      
			match = re.findall(pattern, sample)
 			#PH, LambdaT, NED, KK = match[0]
			label = match[0]
			# Add Sherpa label tuple
			label = ("Sherpa",) + label
		else:
			pattern = "OUT([^(]*)GravToGG_NegInt_([^(]*)_LambdaT_([^(]*)_M"
			match = re.findall(pattern, sample)
			PH, NegInt, LambdaT = match[0]
			label = PH, NegInt, LambdaT, '500'
			if "mgg" in sample:
				mcut = "mgg_([^(]*).root"
				mcut = re.findall(mcut, sample)[0]
				PH, NegInt, LT = match[0]
				label = PH, NegInt, LT, mcut
	if "Unp" in sample:
		pattern = "OUT([^(]*)_spin([^(]*)_du([^(]*)_LU([^(]*)_pT([^(]*)_M"
		match = re.findall(pattern, sample)
		#labelList.append(match[0])
		PH, spin, du, LU, pT = match[0]
		label = PH, spin, du, LU, pT
	return label


def createHist(obj, sample, lumi=None):
	file1 = ROOT.TFile(sample, "READ")
	hist = file1.Get(obj)
	if lumi is not None:
		hist.Scale(lumi)
	hist.SetDirectory(0)
	return hist, labelParser(sample)

def LabelMaker(obj, canvas, PeakParams=None):
	binSize = "125 GeV"
	if "Minv" in obj:
		canvas.SetLogy()
		xtitle = r"m_{#gamma#gamma}#scale[1.0]{(GeV)}"
	        ytitle = r"#scale[1.0]{Nevents/%s}" %(binSize)
		if PeakParams is None:
	   		xmin, xmax = 500, 13000
		else:
	        	ytitle = r"#scale[1.0]{Nevents}"
			W, M = PeakParams
			xmin, xmax = 500, int(M)+500
			if "001" not in W:
				xmin, xmax = 500,  int(M)+3000
		legpos = .55, 0.65, .80, .88
	if "Pt" in obj:
  		canvas.SetLogy()
  		xtitle = r"p_{T}#scale[1.0]{(GeV)}"
  		ytitle = r"#scale[1.0]{Nevents}"
  		xmin, xmax = 0, 10000
		if PeakParams is None:
	   		xmin, xmax = 500, 13000
		else:
			W, M = PeakParams
			xmin, xmax = 0, int(M)+500
			if "001" not in W:
				xmin, xmax = 0,  int(M)+2000
		legpos = .55, 0.65, .80, .88
  	if "chidiphoton" in obj:
      		xtitle = r"#Chi_{#gamma#gamma}"
     		ytitle = r"#scale[1.0]{Nevents}"
      		xmin, xmax = 1, 20
		legpos = .55, 0.68, .80, .88
  	if "costhetastar" in obj:
      		xtitle = r"cos#theta^{*}"
      		ytitle = r"#scale[1.0]{Nevents}"
      		xmin, xmax = -1, 1
        	#xpos1, ypos1, xpos2, ypos2 = .30, 0.30, .65, .50
        	legpos = .30, 0.50, .65, .70
  	if "Eta" in obj:
      		xtitle = r"#eta"
      		ytitle = r"#scale[1.0]{Nevents}"
      		xmin, xmax = -4, 4
		legpos = .55, 0.68, .80, .88
	if "Phi" in obj:
      		xtitle = r"#phi"
      		ytitle = r"#scale[1.0]{Nevents}"
      		xmin, xmax = -3.5, 3.5
		legpos = .65, 0.68, .80, .88
	canvas_and_labels = canvas, xtitle, ytitle, xmin, xmax, legpos
	return canvas_and_labels

def makeLegend(legpos, legendtitle=None):
	leg = TLegend(*legpos)
	leg.SetBorderSize(0)
        leg.SetFillColor(0)
       	leg.SetFillStyle(0)
        leg.SetTextFont(42)
        leg.SetTextSize(0.035)

	if legendtitle is None:
		return leg
	else:
		leg.SetHeader(legendtitle, "C")
		return leg

def CreateSMsty(histSM, lumi=None):
	#histSM.SetFillStyle(3144)
	histSM.SetFillColor(7)
	if lumi is not None:
		histSM.Scale(lumi)
	return histSM

def PlotResonance(obj, sample, color=None, outputdir=None, Background=None, lumi=None):
	hist, label = createHist(obj, sample)
	canvas = ROOT.TCanvas()
	PH, W, M= label
	if "RSG" in label:
		leglabel = r"kMpl-%s, M-%s" %(W, M)
		Plot_outFileName = "RSG_kMpl-%s_M-%s%s.pdf" %(W, M, obj)
		outputdir = "%s_kMpl-%s_M-%s" %(PH, W, M)
		modeltag = "RS Graviton"
	if "GluGlu" in label:
		 leglabel = r"HeavyHiggs_W=%s, M-%s" %(W, M)
		 Plot_outFileName = "HeavyHiggs_W%s_M-%s_%s.pdf" %(W, M, obj)
		 outputdir = "%s_W-%s_M-%s" %(PH, W, M)
		 modeltag = "Heavy Higgs"
	canvas, xtitle, ytitle, xmin, xmax, legpos = LabelMaker(obj, canvas, (W,M))
        #print leglabel, xmin, xmax
	if "gen" in obj:
		Plot_outFileName = "GEN" + Plot_outFileName

	#legpos = .55, 0.78, .80, .88
	legend = makeLegend(legpos, "#bf{Legend:} %s"  %(modeltag))
	h = hist.Clone("shaperhist")

	# Error Markers
	hist.SetMarkerSize(0)
	hist.SetFillColor(kBlack)
	hist.SetFillStyle(3344)

	if color is None:
		h.SetLineColor(1)
	else:
		h.SetLineColor(color)

	h.SetFillStyle(3244)
	h.SetFillColor(kOrange-3)

	# If Standard Model/Background given, reconfigure canvas to overlay S+B.
	if Background is not None:
		histSM, labelSM = Background
		histSM = CreateSMsty(histSM)
		ymax = max(histSM.GetMaximum(), hist.GetMaximum())
		ymax = ymax + ymax*(0.3)
		histSM.SetMaximum(ymax)
		histSM.GetXaxis().SetTitle(xtitle)
		histSM.GetXaxis().SetRangeUser(xmin, xmax)
		histSM.GetYaxis().SetTitle(ytitle)
		hist.GetYaxis().SetTitleOffset(1.0)
		if lumi is not None:
			histSM.Scale(lumi)
			histSM.SetMaximum(ymax*lumi)
			h.Scale(lumi)
			hist.Scale(lumi)
		histSM.Draw("hist, same")
		h.Draw("hist, same") #Redraw Shape
		hist.Draw("same, E2") #Keep same option, Draw Error
		#histSM.Draw("hist, same") #Redraw SM
		legend.AddEntry(histSM, "%s" %(labelSM), "f")
		Plot_outFileName = "SM_vs_"+ Plot_outFileName
	else:
		h.GetYaxis().SetTitle(ytitle)
		h.GetYaxis().SetTitleOffset(1.0)
		h.GetXaxis().SetTitle(xtitle)
		h.GetXaxis().SetRangeUser(xmin, xmax)
		h.Draw("hist, same") #Redraw Shape
		hist.Draw("same, E2") # Draw Error
	legend.AddEntry(h, "%s" %(leglabel), "f")
	legend.Draw()
	set_CMS_lumi(canvas, 4, 0, intlumi)
	if lumi is not None:
		set_CMS_lumi(canvas, 4, 11, lumi)
	canvas.Update()
	canvas.Draw()
	if outputdir is None:
		canvas.SaveAs(Plot_outFileName)
	else:
		# Rename outputdir with parameters
        	if not os.path.exists(outputdir):
            		os.mkdir(outputdir)
		os.chdir(outputdir)
            	canvas.SaveAs(Plot_outFileName)
		os.chdir("..")

def Stitch(toStitchList, obj):
    # Used for stitching non-resonant mass bins
    openFileList, labelList = [], []
    for data in toStitchList:
		label = labelParser(data)
		# Open ROOT files
        	openFileList.append(ROOT.TFile(data, "READ"))
    		labelList.append(label)

    # Get Histogram objects
    hists = []
    for openfile in openFileList:
	histo = openfile.Get(obj)
	histo.SetDirectory(0)
        hists.append(histo)

    # Stitching
    i = 1
    hist = hists[0].Clone("hist")
    #print type(histo), "this?"
    while i < len(hists):
        hist.Add(hists[i], 1.0)
        i = i + 1

    hist.SetDirectory(0)
    return hist, label

def OverlayHists(obj, histlist, labelList, tag=None, lumi=None, Background=None, Mrange=None):
	 # print labelList, histList
  	 canvas = ROOT.TCanvas()
	 canvas, xtitle, ytitle, xmin, xmax, legpos = LabelMaker(obj, canvas)
	 if "Minv" in obj and Mrange is not None:
		xmin, xmax = Mrange
 	 #leg = TLegend(legpos)
	 leg = makeLegend(legpos, legendtitle="#bf{Sensitivity Studies}")
	 colorlist = [kBlue, kRed, kViolet+3, kOrange+3,
 	 	      kMagenta, kGreen, kViolet, kSpring,
 		      kPink, kAzure, kOrange+8, kGreen+8,
 		      kRed+8, kViolet+8, kMagenta+5]
     	 labels, histClones, iset, icolor, i = [], [], 0, 0, 0
	 while i < len(histlist):
		 histClone = histlist[i].Clone("hist%s" %(str(i)))
		 histClones.append(histClone)
	         i = i + 1
	 i = 0
	 eventsmaxlist = []
	 for histclone in histClones:
		label = labelList[i]
		#print label
         	eventsmaxlist.append(histclone.GetMaximum())
      		if "SM" in label or "GGJets" in label:
	     		histSM = histclone
	      		histSM.SetFillStyle(3144)
	      		histSM.SetFillColor(7+i)
			if lumi is not None:
	      			histSM.Scale(lumi)
	     		if "SM" in label:
				leg.AddEntry(histSM, "%s" %(r"SM M_{gg} > 500 GeV"), "f")
			if "GGJets" in label:
				leg.AddEntry(histSM, "GGJets", "f")
			histSM.GetYaxis().SetTitle(ytitle)
	 		histSM.GetYaxis().SetTitleOffset(1.0)
	 		histSM.GetXaxis().SetTitle(xtitle)
	 		histSM.GetXaxis().SetRangeUser(xmin, xmax)
			if Background is not None:
				histSM.Draw("hist same")
			outName = "SM"	
		else:
			#histclone.SetLineColor(kRed)
	      		histclone.SetLineColor(colorlist[icolor])
	     		if lumi is not None:
				histclone.Scale(intlumi)
	      		histclone.GetXaxis().SetRangeUser(xmin, xmax)
			histclone.Draw(drawstyle)
			if "ADD" in label:
				if "Sherpa" in label:	
					Gen, PH, LambdaT, NED, KK = label
					LambdaU = str(round (float(LambdaT)/1000, 1))
					leglabel = r"#Lambda_{U}=%s, KK-%s" %(LambdaU, KK)
					leg.SetHeader("#bf{ADD Graviton to #gamma#gamma}", "C")
					outName = outName + "vsADD_LU%s_KK%s" %(LambdaU, KK) 
				else:
					PH, NegInt, LT, mgg = label
					LambdaT = str(round(float(LT)/1000 , 1) )
					if  NegInt is "1":
						NI = "Int+"
					if NegInt is "0":
						NI = "Int-"
					minvcut = str(round ( float(mgg)/1000, 1 ))
					leglabel = r"%s, #Lambda_{T}=%s, M>%s [TeV]" %(NI, LambdaT, minvcut)
					leg.SetHeader("#bf{ADD Graviton to #gamma#gamma}", "C")
					outName = outName + "vsADD_NegInt%s_LT%s" %(NegInt, LT)
				print outName 
			if "Unp" in label:
				PH, spin, du, LU, pT = label
	      			leglabel = r"#Lambda_{U}=%s, d_{u}=%s, spin-%s" %(LU, du, spin)
	 			outName = outName + "vsUnparticles_spin%s_du%s.pdf" %(spin, du)
   			leg.AddEntry(histclone, "%s" %(leglabel), "l")
     		i = i+1
   	        icolor = icolor + 1
	 
	 #print eventsmaxlist
	 ymax = max(eventsmaxlist)
	 ymax = ymax + ymax*(0.3)
  	 histSM.SetMaximum(ymax)
	 #histSM.SetMaximum(max(eventsmaxlist))
	 if lumi is not None:
		ymax = max(eventsmaxlist)*lumi
		ymax = ymax + 0.3*ymax
		histSM.SetMaximum(ymax)
	 	#histSM.SetMaximum(max(eventsmaxlist)*lumi)
	 
	 leg.Draw()
         if lumi is not None:
                #set_CMS_lumi(canvas, 4, 11, lumi)
	 	set_CMS_lumi(canvas, 4, 0, lumi)
	 if lumi is None:
	 	set_CMS_lumi(canvas, 4, 0, 1)
	 canvas.Update()
	 canvas.Draw()
	
	 if tag is not None:
		outName = tag + outName
		outputdir  = PH + tag
         	# Rename outputdir with parameters
         	if not os.path.exists(outputdir):
                	os.mkdir(outputdir)
                os.chdir(outputdir)
                canvas.SaveAs(outName+"V%s.pdf"%(obj))
                os.chdir("..") 
	 else:
	 	canvas.Print(outName+"V%s.pdf"%(obj))
	
# Currently Editing
# Unedited
def PlotContinuous(obj, Background=None, Signal=None, color=None, outputdir=None, lumi=None):
  	 canvas = ROOT.TCanvas()
	 canvas, xtitle, ytitle, xmin, xmax, legpos = LabelMaker(obj, canvas)
	 leg = TLegend(legpos)
     	 colorlist = [kBlue, kOrange, kViolet+3, kRed,
	 	      kMagenta, kGreen, kViolet, kSpring,
		      kPink, kAzure, kOrange+8, kGreen+8,
		      kRed+8, kViolet+8, kMagenta+5]


	 # Checking if both Background and Signal Histograms given
	 if Background is not None:
		print "Overlaying Background and Signal"
		# Create Standard Model Background
		histSM, labelSM = Background
		histSM = CreateSMsty(histSM)
		histSM.GetXaxis().SetTitle(xtitle)
		histSM.GetXaxis().SetRangeUser(xmin, xmax)
		histSM.GetYaxis().SetTitle(ytitle)
		histSM.Draw("hist, same")
		Plot_outName = "SM"
		if Signal is not None:
			ymax = max(histSM.GetMaximum(), hist.GetMaximum())
			ymax = ymax + ymax*(0.3)
			histSM.SetMaximum(ymax)
			# Create Signal
			hist.GetYaxis().SetTitleOffset(1.0)
			# Overlay Background and Signal
			h.Draw("hist, same") #Redraw Shape
			hist.Draw("same, E2") #Keep same option, Draw Error
			## Create Plot_outFileName here
			Plot_outName = Plot_outName = "_vs_Signal"
			#legend.AddEntry(histSM, "%s" %(labelSM), "f")

	 elif Background is None:
		print "No Background given"
		if Signal is not None:
			print "Plotting Signal Only"
			h.GetYaxis().SetTitle(ytitle)
			h.GetYaxis().SetTitleOffset(1.0)
			h.GetXaxis().SetTitle(xtitle)
			h.GetXaxis().SetRangeUser(xmin, xmax)
			h.Draw("hist, same") #Redraw Shape
			hist.Draw("same, E2") # Draw Error
			legend.AddEntry(h, "%s" %(leglabel), "f")
			legend.Draw()
     	 canvas.Draw()

##### Unedited for Diphoton Studies
def OverlayDatasets(obj, DATASETS):
      uf = []
      for datafile in DATASETS:
	      uf.append(ROOT.TFile(datafile, "READ"))

      canvas = ROOT.TCanvas()
      uh = []
      bkgh = []

      for openfile in uf:
	      uh.append(openfile.Get(obj))

      canvas, xtitle, ytitle, xmin, xmax = LabelMaker(obj, canvas)
      # Legend Position
      xpos1, ypos1, xpos2, ypos2 = .55, 0.58, .80, .88
      if "costhetastar" in obj:
	xpos1, ypos1, xpos2, ypos2 = .30, 0.50, .65, .70

      #legendtitle = "#bf{Barrel-Barrel} Photons"
      leg = TLegend(xpos1, ypos1, xpos2, ypos2)

      colorlist = [kBlue, kOrange, kViolet+3, kRed, kMagenta, kGreen, kViolet, kSpring, kPink, kAzure, kOrange+8, kGreen+8, kRed+8, kViolet+8, kMagenta+5]
      labels = []
      histClones = []
      iset = 0
      icolor = 0
      i = 0

      while i < len(DATASETS):
	      histClone = uh[i].Clone("histdu%s" %(DATASETS[i]))
    	      histClones.append(histClone)
    	      i = i + 1

      j = 0
      eventsmaxlist = []
      for histclone in histClones:
	      eventsmaxlist.append(histclone.GetMaximum())
	      if "SM" in DATASETS[j]:

		      histSM = histclone
		      histSM.SetFillStyle(3144)
		      histSM.SetFillColor(7+j)
		      histSM.Scale(intlumi)
		      if "1000" in DATASETS[j]:
			      leg.AddEntry(histSM, "%s" %(r"SM M_{gg} > 1 TeV"), "f")
		      if "1500" in DATASETS[j]:
			      leg.AddEntry(histSM, "%s" %(r"SM M_{gg} > 1.5 TeV"), "f")
              	      if "2000" in DATASETS[j]:
 			      leg.AddEntry(histSM, "%s" %(r"SM M_{gg} > 2 TeV"), "f")
		      histSM.Draw("hist same")
	      else:
		      histclone.SetLineColor(colorlist[icolor])
		      histclone.Scale(intlumi)
		      histclone.Draw(drawstyle)
		      pattern = "../MINisEBEB/OUTUnp_spin([^(]*)_du([^(]*)_LU([^(]*)p0_m([^(]*)_pT([^(]*)_M([^(]*).root"
		      match = re.findall(pattern, DATASETS[j])
		      spinlabel, du, LambdaU, masscut, ptCut, massmin = match[0]
		      print match
		      leglabel = r"#Lambda_{U}=%s, d_{u}=%s, spin-%s" %(LambdaU, du, spinlabel)
    		      leg.AddEntry(histclone, "%s" %(leglabel), "l")
	      j = j+1
    	      icolor = icolor + 1

      print eventsmaxlist
      #legendtitle = "#bf{Renormalization Scale:} %s (%s)" %(LambdaU, "isEBEB")
      legendtitle = "#bf{Sensitivity Studies} (EB-EB)"
      leg.SetHeader(legendtitle, "C")
      leg.SetBorderSize(0)
      leg.SetFillColor(0)
      leg.SetFillStyle(0)
      leg.SetTextFont(42)
      leg.SetTextSize(0.035)

      histSM.SetMaximum(max(eventsmaxlist)*intlumi)
      histSM.GetYaxis().SetTitle(ytitle)
      histSM.GetYaxis().SetTitleOffset(1.0)
      histSM.GetXaxis().SetTitle(xtitle)
      histSM.GetXaxis().SetRangeUser(xmin, xmax)


      leg.Draw()
      set_CMS_lumi(canvas, 4, 11, intlumi)
      canvas.Update()
      canvas.Draw()
      canvas.Print("LOG%s_SMvsADD_%sfb-1_%s.pdf" %(intlumi, LambdaT, obj))

def createRatio(h1, h2):
    h3 = h1.Clone("h3")
    h3.SetLineColor(kBlack)
    h3.SetMarkerStyle(21)
    h3.SetTitle("RATIO")
    #h3.SetMinimum(0.8)
    #h3.SetMaximum(2.5)
    # Set up plot for markers and errors
    h3.Sumw2()
    h3.SetStats(0)
    h3.Divide(h2)

    # Adjust y-axis settings
    y = h3.GetYaxis()
    y.SetTitle("ratio %s/%s" %(h1, h2))
    #y.SetTitleOffset(4.55)
    #y = h3.GetYaxis()
    #y.SetTitle("ratio h1/h2 ")
    y.SetNdivisions(505)
    y.SetTitleSize(20)
    y.SetTitleFont(43)
    y.SetTitleOffset(1.55)
    y.SetLabelFont(43)
    y.SetLabelSize(15)

    # Adjust x-axis settings
    x = h3.GetXaxis()
    x.SetTitleSize(40)
    x.SetTitleFont(43)
    x.SetTitleOffset(10.0)
    x.SetLabelFont(43)
    x.SetLabelSize(15)

    # return ratiohist
    return h3

def createCanvasPads():
    c = TCanvas("c", "canvas", 800, 800)
    # Upper histogram plot is pad1
    pad1 = TPad("pad1", "pad1", 0, 0.3, 1, 1.0)
    pad1.SetBottomMargin(0)  # joins upper and lower plot
    #pad1.SetGridx()
    pad1.SetLogy()
    pad1.Draw()
    # Lower ratio plot is pad2
    c.cd()  # returns to main canvas before defining pad2
    pad2 = TPad("pad2", "pad2", 0, 0.05, 1, 0.3)
    pad2.SetTopMargin(0)  # joins upper and lower plot
    pad2.SetBottomMargin(0.2)
    pad2.SetGridy()
    #pad2.SetGridx()
    pad2.Draw()

    return c, pad1, pad2

def createSignalOnly(obj, sample1, sample2):
        file1 = ROOT.TFile(sample1, "READ")
        file2 = ROOT.TFile(sample2, "READ")
        hdata = file1.Get(obj)
        hist2 = file2.Get(obj)

        hdata.Scale(intlumi)
        hist2.Scale(intlumi)
	hsigonly = hist2.Clone("Signal+B")
	hsigonly.Add(hdata, -1)
	b = hdata.Integral()

        s = hsigonly.Integral() #already scaled
    	pattern = "OUTUnp_spin([^(]*)_du([^(]*)_LU([^(]*)p0_m([^(]*)_pT([^(]*)_M([^(]*).root"
        match = re.findall(pattern, sample2)
	spin, du, LU, mCut, pTcut, massmin = match[0]
        #print intlumi, "fb-1; LU, du, spin, Mcut: ", LU, du, spin, massmin, ";b: ", b, "; s: ", s, "; sb:", hist2.Integral(), "; P(b, s+b): ", TMath.Poisson(b, s+b)

	h3 = hsigonly.Clone("hsigonly")
	h3.SetDirectory(0)
	#h3.GetBinContent(bin)
	#print h3.GetBinContent(88)
	#print h3.GetBinContent(5)
        #AddDirectory(kFALSE)
        #print "hsigonly type", type(hsigonly), type(hdata), type(hsigonly)
	return h3, match[0]

def addToLegend(leg, hist, match):
        #LU, du, spin, massmin = match
        spin, du, LU, mCut, pTcut, massmin = match
	leglabel = r"#Lambda_{U}=%s, d_{u}=%s, spin-%s" %(LU, du, spin)
        leg.AddEntry(hist, "%s" %(leglabel), "l")

	return leg

def PlotRatio(h1, h2, labels1, labels2):
	c, pad1, pad2 = createCanvasPads()
    	#pad1.SetLogy()
	pad1.cd()
	h1.SetLineColor(kRed)
	h2.SetLineColor(kBlue)
	h1.Draw()
	x1 = h1.GetXaxis()
	y1 = h1.GetYaxis()
	ytitle = r"#scale[1.0]{Events/600GeV}"
	y1.SetTitle(ytitle)
	#x1.SetRangeUser(2000, 4000)
	h2.Draw("same")
        xpos1, ypos1, xpos2, ypos2 = .55, 0.58, .80, .88
	leg = makeLegend()
	leg = addToLegend(leg, h1, labels1)
        leg = addToLegend(leg, h2, labels2)
        leg.Draw()
        spin1, du1, LU1, mCut1, pTcut1, massmin1 = labels1
        spin2, du2, LU2, mCut2, pTcut2, massmin2 = labels2
	pad2.cd()
	hRatio = createRatio(h1, h2)
    	hRatio.Fit("pol0")
    	hRatio.GetFunction("pol0").SetLineColor(kRed)
    	stats = hRatio.FindObject("stats")
	if not stats:
		#continue
		stats.__class__ = ROOT.TPaveStats
    	#gStyle.SetOptFit(1111)
	#hRatio.GetXaxis().SetRangeUser(xmin, xmax)
	y = hRatio.GetYaxis()
	y.SetRangeUser(0, 10)
	y.SetTitle("Ratio")
	y.SetTitleSize(20)
	y.SetTitleFont(43)
	x = hRatio.GetXaxis()
	#x.SetRangeUser(2000, 4000)

        hRatio.Draw("ep")
	print "Theoretical ratio: ", xsecRatio(float(du1.replace("p",".")), float(LU1), float(LU2)), 1.00/xsecRatio(float(du1.replace("p",".")), float(LU1), float(LU2))
        c.Print("Ratio%s_%svs%s.pdf" %(du1, LU1, LU2))

def OverlayResonances(obj, DATASET, legpos, xrange):
	uf = []
	for datafile in DATASET:
		uf.append(ROOT.TFile(datafile, "READ"))

	canvas = ROOT.TCanvas()
	#canvas.SetLogy()
	uh = []

	for openfile in uf:
		uh.append(openfile.Get(obj))
		#uh1 = uf1.Get(obj)

	xtitle = r"m_{#gamma#gamma}#scale[1.0]{(GeV)}"
	ytitle = r"#scale[0.8]{weighted events}"

	xmin, xmax = xrange
	uh[0].GetYaxis().SetTitle(ytitle)
	uh[0].GetYaxis().SetTitleOffset(1.0)
	uh[0].GetXaxis().SetTitle(xtitle)
	#uh[0].GetYaxis().SetRangeUser(10**-5, max(eventsmaxlist))
	uh[0].GetXaxis().SetRangeUser(xmin, xmax)

	legEntry = []
	xpos1, ypos1, xpos2, ypos2 = legpos
	leg = TLegend(xpos1, ypos1, xpos2, ypos2)
	leg.SetBorderSize(0)
	leg.SetFillColor(0)
	leg.SetFillStyle(0)
	leg.SetTextFont(42)
	leg.SetTextSize(0.035)

	i = 0

	for hist in uh:
		hist.SetLineColor(i+1)
		if i == 9:
			hist.SetLineColor(46)
			#hist.SetLineStyle(9)
			#hist.SetFillColor(48)
		hist.Draw("hist, same")
		if "RSG" in DATASET[i]:
			pattern = "OUTRSGravitonToGammaGamma_kMpl([^(]*)_M_([^(]*).root"
		if "GluGlu" in DATASET[i]:
			pattern = "OUTGluGluSpin0ToGammaGamma_W_([^(]*)_M_([^(]*).root"
		match = re.findall(pattern, DATASET[i])
		W, M = match[0]
		if "RSG" in DATASET[i]:
			label = "RSG_kMpl-%s_M-%s" %(W, M)
		if "GluGlu" in DATASET[i]:
			label = "HeavyHiggs_W-%s_M-%s" %(W, M)

		Plot_outFileName = "%s.pdf" %(label)
		print label
		leg.AddEntry(hist, "%s" %(label), "l")
		i = i + 1

	leg.Draw()
	set_CMS_lumi(canvas, 4, 11, "1")
	canvas.Update()
	canvas.Draw()
	canvas.Print(Plot_outFileName)


def OverlayResonances(obj, DATASET, legpos, xrange):
	uf = []
	for datafile in DATASET:
		uf.append(ROOT.TFile(datafile, "READ"))

	canvas = ROOT.TCanvas()
	#canvas.SetLogy()
	uh = []

	for openfile in uf:
		uh.append(openfile.Get(obj))
		#uh1 = uf1.Get(obj)

	xtitle = r"m_{#gamma#gamma}#scale[1.0]{(GeV)}"
	ytitle = r"#scale[0.8]{weighted events}"

	xmin, xmax = xrange
	uh[0].GetYaxis().SetTitle(ytitle)
	uh[0].GetYaxis().SetTitleOffset(1.0)
	uh[0].GetXaxis().SetTitle(xtitle)
	#uh[0].GetYaxis().SetRangeUser(10**-5, max(eventsmaxlist))
	uh[0].GetXaxis().SetRangeUser(xmin, xmax)

	legEntry = []
	xpos1, ypos1, xpos2, ypos2 = legpos
	leg = TLegend(xpos1, ypos1, xpos2, ypos2)
	leg.SetBorderSize(0)
	leg.SetFillColor(0)
	leg.SetFillStyle(0)
	leg.SetTextFont(42)
	leg.SetTextSize(0.035)

	i = 0

	for hist in uh:
		hist.SetLineColor(i+1)
		if i == 9:
			hist.SetLineColor(46)
			#hist.SetLineStyle(9)
			#hist.SetFillColor(48)
		hist.Draw("hist, same")
		if "RSG" in DATASET[i]:
			pattern = "OUTRSGravitonToGammaGamma_kMpl([^(]*)_M_([^(]*).root"
		if "GluGlu" in DATASET[i]:
			pattern = "OUTGluGluSpin0ToGammaGamma_W_([^(]*)_M_([^(]*).root"
		match = re.findall(pattern, DATASET[i])
		W, M = match[0]
		if "RSG" in DATASET[i]:
			label = "RSG_kMpl-%s_M-%s" %(W, M)
		if "GluGlu" in DATASET[i]:
			label = "HeavyHiggs_W-%s_M-%s" %(W, M)

		Plot_outFileName = "%s.pdf" %(label)
		print label
		leg.AddEntry(hist, "%s" %(label), "l")
		i = i + 1

	leg.Draw()
	set_CMS_lumi(canvas, 4, 11, "1")
	canvas.Update()
	canvas.Draw()
	canvas.Print(Plot_outFileName)
