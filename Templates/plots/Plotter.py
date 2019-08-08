#!/usr/bin/python

import ROOT
from ROOT import gBenchmark, gStyle, gROOT, gDirectory
import re
# from hep_plt.Sensitivityfunctions import CalcSensitivity
from hep_plt.Plotfunctions import *
from hep_plt.hep_plt import *

gStyle.SetOptStat(0)

# To suppress canvas from popping up. Speeds up plots production.
gROOT.SetBatch()


obj = []
obj.append("gendiphotonMinv")

DATASET = []
DATASET.append("../ResonanceTemplates/OUTRSGravitonToGammaGamma_kMpl001_M_5000.root")
DATASET.append("../ResonanceTemplates/OUTRSGravitonToGammaGamma_kMpl01_M_750.root")
DATASET.append("../ResonanceTemplates/OUTRSGravitonToGammaGamma_kMpl001_M_750.root")
DATASET.append("../ResonanceTemplates/OUTRSGravitonToGammaGamma_kMpl02_M_5000.root")
DATASET.append("../ResonanceTemplates/OUTRSGravitonToGammaGamma_kMpl01_M_5000.root")
DATASET.append("../ResonanceTemplates/OUTRSGravitonToGammaGamma_kMpl02_M_750.root")

# for dset in DATASET:
# 	for o in obj:
# 		PlotResonance(o, dset, color=2, outputdir="make")
# 	# Resonance(obj, dset, color=2, outputdir="make")

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

def plot_resonance(obj, sample):
	file = ROOT.TFile(sample, "READ")
	hist = file.Get(obj)
	h = hist.Clone()
	canvas = ROOT.TCanvas()
	canvas.SetLogy()
	hist.SetMarkerSize(0)
	hist.SetFillColor(kBlack)
	hist.SetFillStyle(3344)
	h.SetFillStyle(3244)
	h.SetFillColor(kOrange-3)
	h.SetLineColor(kOrange+10)
	h.GetYaxis().SetTitleOffset(1.0)
	m0 = int(re.findall("M_([^(]*).root", sample)[0])
	h.GetXaxis().SetRangeUser(m0-2000, m0+2000)
	h.Draw("hist, same")
	hist.Draw("same, E2")

	label_dset = re.findall("OUT([^(]*).root", sample)[0]

	legpos = .55, 0.65, .80, .88
	legend = makeLegend(legpos)
	legend.AddEntry(h, "%s" %(label_dset.replace("RSGravitonToGammaGamma", "RSG")), "f")
	legend.Draw()

	canvas.Update()
	canvas.Draw()

	canvas.SaveAs("%s.pdf" %(label_dset))

for dset in DATASET:
	for o in obj:
		plot_resonance(o, dset)
