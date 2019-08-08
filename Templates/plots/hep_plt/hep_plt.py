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

def createHisto(obj, sample, lumi=None):
	file1 = ROOT.TFile(sample, "READ")
	hist = file1.Get(obj)
	if lumi is not None:
		hist.Scale(lumi)
	#hist.SetDirectory(0)
	return hist

def Resonance(obj, sample, color=None, outputdir=None, lumi=None):
    hist = createHisto(obj, sample)
    # h = hist.Clone("shaperhist")
    canvas = ROOT.TCanvas()
    hist.SetMarkerSize(0)
    hist.SetFillColor(kBlack)
    hist.SetFillStyle(3344)

    if color is None:
        h.SetLineColor(1)
    else:
        h.SetLineColor(color)

    # h.SetFillStyle(3244)
    # h.SetFillColor(kOrange-3)
    # h.GetYaxis().SetTitle(ytitle)
    # h.GetYaxis().SetTitleOffset(1.0)
    # h.GetYaxis().SetTitle(xtitle)
    # h.GetXaxis().SetTitle(xmin, xmax)
    h.Draw("hist, same")
    hist.Draw("same, E2")

    canvas.Update()
    canvas.Draw()
    label_dset = re.findall("OUT([^(]*).root", sample)

    if outputdir is None:
        canvas.SaveAs("%s.pdf" %(labeldset))
    else:
        if not os.path.exists(outputdir):
            os.mkdir(outputdir)
            os.chdir(outputdir)
            canvas.SaveAs("%s.pdf" %(labeldset))
            os.chdir("..")
