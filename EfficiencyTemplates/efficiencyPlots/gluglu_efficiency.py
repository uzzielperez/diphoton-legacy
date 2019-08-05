from __future__ import division
import ROOT
# from hep_plt.CMSlumi import CMS_lumi, set_CMS_lumi, CMS_Energy
from ROOT import *
import re
from array import array
from math import sin

import csv
# inputfile = 'RSG75.csv'
# inputfile = 'RSG125.csv'
inputfile = 'RSG75_AN.csv'
#inputfile = 'RSG125_AN.csv'
#inputfile = 'RSGdefault.csv'

inputfile = 'hh125goodAN.csv'
#inputfile = 'hh75goodAN.csv'
#inputfile = 'hh75tAN.csv'
#inputfile = 'hh75AN.csv'
#inputfile = 'hh125AN.csv'
#inputfile = 'hhcheckAN.csv'
#inputfile = 'hhdefault.csv'

# --- FUNCTION DEFINITIONS
# have to use a dict for the MC_total

MC_total_dict = {750: 100000,
                 1000: 100000,
                 1250: 100000,
                 1500: 100000,
                 1750: 100000,
                 2000: 100000,
                 2250: 98000,
                 2500: 96000,
                 3000: 100000,
                 3500: 100000,
                 4000: 100000,
                 4250: 100000,
                 4500: 100000,
                 4750: 96000,
                 5000: 100000,
                 }
def readCSV_eff(inputfile):
	M, isGood_frac, Ntotal, NisEBEB, NisbEorEb, MC_total = [], [], [], [], [], []
	with open(inputfile, mode='r') as infile:
	    csv_file = csv.DictReader(infile)
	    row_num = 0
 	    for line in csv_file:
        	dset, ntotal,= line['Sample'], line['Ntotal']
		NisGood, isGoodfrac = line['NisGood'], line['isGoodfrac']
		nEBEB = line['nEBEB']
		nEBEEorEEEB = line['nEBEEorEEEB']
		nEEEE = line['nEEEE']
		npTcut = line['npTcut']
		pattern = "GluGluSpin0ToGammaGamma_W_1p4_M_([^(]*)"

		print nEBEEorEEEB
		match = re.findall(pattern, dset)
		mass = int(match[0])
		M.append(mass)
		isGood_frac.append(double(isGoodfrac))
		Ntotal.append(int(ntotal))
		NisEBEB.append(int(nEBEB))
		NisbEorEb.append(int(nEBEEorEEEB))
		MC_total.append(MC_total_dict[mass])

	print NisbEorEb

	efficiency_isEBEB = array( 'd' )
	efficiency_isbEorEb = array( 'd')
	efficiency_tot = array('d')


	for ntotal, nb, neBoreB, e, mctotal in zip(Ntotal, NisEBEB, NisbEorEb, isGood_frac, MC_total):
		barrel_eff = nb*e/mctotal
    		endcap_barrel_eff = neBoreB*e/mctotal
   		total_eff = barrel_eff + endcap_barrel_eff
    		print neBoreB, e, mctotal, neBoreB*e/mctotal, barrel_eff, endcap_barrel_eff
  	        efficiency_isEBEB.append(barrel_eff)
	        efficiency_isbEorEb.append(endcap_barrel_eff)
    		efficiency_tot.append(total_eff)

	#print efficiency_isEBEB
	gROOT.SetBatch()
	e_barrel_dict = {}
	e_EBorBE_dict = {}
	e_total_dict = {}

	for m, e1, e2, et in zip(M, efficiency_isEBEB, efficiency_isbEorEb, efficiency_tot):
   		#print e2
		e_barrel_dict[m] = e1
    		e_EBorBE_dict[m] = e2
    		e_total_dict[m] = et

	n = len(M)

	mass, e_barrel, e_EBorBE, etotal = array( 'd' ), array( 'd' ), array( 'd' ), array( 'd' )
	M.sort()
	for mpt in M:
	    #print e_barrel_dict[mpt]
	    #print e_EBorBE_dict[mpt]
	    e_barrel.append(e_barrel_dict[mpt])
	    e_EBorBE.append(e_EBorBE_dict[mpt])
	    etotal.append(e_total_dict[mpt])
	    mass.append(mpt)

	return mass, e_barrel, e_EBorBE, etotal

def createTGraph(N, m, e, color, linestyl):
	umin, umax = 0, 0.70
	xmin, xmax = 750, 5000

	gr = ROOT.TGraph(n, mass, e)
	gr.SetLineColor( color )
	gr.SetLineWidth( 2 )
	gr.SetMarkerColor( 4 )
	gr.SetLineStyle( linestyl )
	#gr.SetMarkerStyle( 21 )
	gr.SetMinimum(0.2)
	gr.SetTitle(r' ')
	gr.GetXaxis().SetTitle( r'GluGluSpin0 m_X (GeV)' )
	#gr.GetXaxis().SetTitle( r'RSGraviton m_X (GeV)' )
	gr.GetYaxis().SetTitle( r'#epsilon #times A' )
	#gr.SetMinimum(0.2)
	gr.GetYaxis().SetRangeUser(umin, umax)
	gr.GetXaxis().SetRangeUser(xmin, xmax)

	return gr

# --- PROGRAM START ---

in1 = 'gluglu_75.csv'
in2 = 'gluglu_125.csv'
#in2 = 'LOG.csv'

mass, e_barrel, e_EBorBE, etotal = readCSV_eff( in1 )
mass125, e125_barrel, e125_EBorBE, e125total = readCSV_eff( in2 )

print e_barrel
print e125_barrel

c1 = ROOT.TCanvas("c1", "Efficiency vs M", 200, 10, 550, 500)
#c1.SetFillColor( 42 )
#c1.SetGrid()
c1.cd()
pad1 = ROOT.TPad("pad1", "", 0, 0, 1, 1)
pad2 = ROOT.TPad("pad2", "", 0, 0, 1, 1)
pad3 = ROOT.TPad("pad3", "", 0, 0, 1, 1)
pad1_b = ROOT.TPad("pad1_b", "", 0, 0, 1, 1)
pad2_b = ROOT.TPad("pad2_b", "", 0, 0, 1, 1)
pad3_b = ROOT.TPad("pad3_b", "", 0, 0, 1, 1)
pad2.SetFillStyle(4000) # Make Transparent pad
pad2.SetFrameFillStyle(0)
pad3.SetFillStyle(4000) # Make Transparent pad
pad3.SetFrameFillStyle(0)
pad1_b.SetFillStyle(4000) # Make Transparent pad
pad1_b.SetFrameFillStyle(0)
pad2_b.SetFillStyle(4000) # Make Transparent pad
pad2_b.SetFrameFillStyle(0)
pad3_b.SetFillStyle(4000) # Make Transparent pad
pad3_b.SetFrameFillStyle(0)

#mg = ROOT.TMultiGraph()

n = len(mass)
n125 = len(mass125)
print mass
print mass125

print e_barrel
print e125_barrel
print "EEEE"
print e_EBorBE
print e125_EBorBE

gr = createTGraph(n, mass, e_barrel, 2, linestyl=2)
gr_eb = createTGraph(n, mass, e_EBorBE, 4, linestyl=2)
gr_t = createTGraph(n, mass, etotal, 1, linestyl=2)

gr125 = createTGraph(n125, mass125, e125_barrel, 2, linestyl=1)
gr_eb125 = createTGraph(n125, mass125, e125_EBorBE, 4, 1)
gr_t125 = createTGraph(n125, mass125, e125total, 1, 1 )

# Multipad solution
pad1.Draw()
pad1.cd()
gr.Draw(" APL ")
pad2.Draw()
pad2.cd()
gr_eb.Draw( ' APL ' )
pad3.Draw()
pad3.cd()
gr_t.Draw( ' APL ' )

pad1_b.Draw()
pad1_b.cd()
gr125.Draw( ' APL ')
pad2_b.Draw()
pad2_b.cd()
gr_eb125.Draw( ' APL ' )
pad3_b.Draw()
pad3_b.cd()
gr_t125.Draw( ' APL ' )


leg = ROOT.TLegend(0.65, 0.3, 0.9, 0.6)
leg.SetBorderSize(0)
leg.SetFillColor(0)
leg.SetFillStyle(0)
leg.SetTextFont(42)
leg.SetTextSize(0.035)
leg.SetHeader(r"#frac{#Gamma_{x}}{m_{x}} = 0.01")

leg.AddEntry(gr, "EBEB", "l")
leg.AddEntry(gr_eb, "EBEE", "l")
leg.AddEntry(gr_t, "Total", "l")
leg.AddEntry(gr125, "EBEB_125", "l")
leg.AddEntry(gr_eb125, "EBEE_125", "l")
leg.AddEntry(gr_t125, "Total_125", "l")

leg.Draw()

# set_CMS_lumi(c1, 4, 0, 137)
# CMS_Energy(c1, 0, E="13 TeV")
c1.Update()
#c1.GetFrame().SetFillColor(21)
#c1.GetFrame().SetBorderSize(12)
c1.Modified()
c1.Update()
c1.Draw()
tag = inputfile[3:-4] + "all"
c1.SaveAs("gluglu_eff.pdf")
