import ROOT
from hep_plt.CMSlumi import CMS_lumi, set_CMS_lumi, CMS_Energy
from ROOT import *
import re
from array import array
from math import sin, sqrt

import csv
# have to use a dict for the MC_total

MC_total_dict = {750: 100000,
                 1250: 98000,
                 1500: 96000,
                 2500: 99000,
                 3000: 100000,
                 4250: 100000,
                 4500: 99026,
                 4750: 100000,
                 5000: 96000,
                 5750: 100000,
                 6000: 100000,
                 6500: 100000,
                 7000: 95002,
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
		#pattern = "GluGluSpin0ToGammaGamma_W_1p4_M_([^(]*)"
		pattern = "RSGravitonToGammaGamma_kMpl01_M_([^(]*)"

		match = re.findall(pattern, dset)
		mass = int(match[0])
		M.append(mass)
		isGood_frac.append(double(isGoodfrac))
		Ntotal.append(int(ntotal))
		NisEBEB.append(int(nEBEB))
		NisbEorEb.append(int(nEBEEorEEEB))
		MC_total.append(MC_total_dict[mass])


	efficiency_isEBEB = []
	efficiency_isbEorEb = []
	efficiency_tot = []

	for ntotal, nb, neBoreB, e, mctotal in zip(Ntotal, NisEBEB, NisbEorEb, isGood_frac, MC_total):
    		barrel_eff = nb*e/mctotal
    		endcap_barrel_eff = neBoreB*e/mctotal
   		total_eff = barrel_eff + endcap_barrel_eff
  	        efficiency_isEBEB.append(barrel_eff)
	        efficiency_isbEorEb.append(endcap_barrel_eff)
    		efficiency_tot.append(total_eff)


	gROOT.SetBatch()
	e_barrel_dict = {}
	e_EBorBE_dict = {}
	e_total_dict = {}

	for m, e1, e2, et in zip(M, efficiency_isEBEB, efficiency_isbEorEb, efficiency_tot):
   		e_barrel_dict[m] = e1
    		e_EBorBE_dict[m] = e2
    		e_total_dict[m] = et

	n = len(M)
	mass, e_barrel, e_EBorBE, etotal = array( 'd' ), array( 'd' ), array( 'd' ), array( 'd' )

	M.sort()
	for mpt in M:
	    e_barrel.append(e_barrel_dict[mpt])
	    e_EBorBE.append(e_EBorBE_dict[mpt])
	    etotal.append(e_total_dict[mpt])
	    mass.append(mpt)
	return mass, e_barrel, e_EBorBE, etotal

def createTGraphError(N, m, e, ex, ey, color, linestyl):
	umin, umax = 0.5, 1.4
	xmin, xmax = 750, 5000

	gr = ROOT.TGraphErrors(n, mass, e, ex, ey)
	gr.SetLineColor( color )
	gr.SetLineWidth( 2 )
	gr.SetMarkerColor( color )
	gr.SetMarkerStyle(2)
	gr.SetLineStyle( linestyl )
	#gr.SetMarkerStyle( 21 )
	gr.SetMinimum(0.2)
	gr.SetTitle(r' ')
	gr.GetXaxis().SetTitle( r'GluGluSpin0 m_X (GeV)' )
	#gr.GetXaxis().SetTitle( r'RSGraviton m_X (GeV)' )

	#gr.GetYaxis().SetTitle( r'#epsilon #times A' )
	gr.GetYaxis().SetTitle( r'#frac{(#epsilon #times A)_{pT125}}{(#epsilon #times A)_{pT75}}' )
	#gr.SetMinimum(0.2)
	gr.GetYaxis().SetRangeUser(umin, umax)
	gr.GetXaxis().SetRangeUser(xmin, xmax)

	return gr

def stddev(lst):
	mean = float(sum(lst)) / len(lst)
	return sqrt(sum((x - mean)**2 for x in lst) / len(lst))

def calcerror(data, mlist):
	Nlist = array('d', [MC_total_dict[n] for n in mlist] )
	stdev = stddev(data)
	error = array('d', [stdev/sqrt(N) for N in Nlist] )
	print error
	return error

# --- PROGRAM START ---
in1 = 'rsg_75.csv'
in2 = 'rsg_125.csv'

mass, e_barrel, e_EBorBE, etotal = readCSV_eff( in1 )
mass125, e125_barrel, e125_EBorBE, e125total = readCSV_eff( in2 )

e_t, e_eb, e_eborbe = array( 'd' ), array( 'd' ), array( 'd' )
for m, e1, e2, e1_b, e2_b, e1_e, e2_e in zip( mass,etotal, e125total, e_barrel, e125_barrel, e_EBorBE, e125_EBorBE ):
        #print m, e1, e2, e1_b, e2_b, e1_e, e2_e
	print e1, e2, e1/e2
        e_t.append(e2/e1)
        e_eb.append(e2_b/e1_b)
        e_eborbe.append(e2_e/e1_e)
n = len(mass)
# print e_t
# print e_eb
# print e_eborbe

err_t = calcerror(e_t, mass)
err_eb = calcerror(e_eb, mass)
err_eborbe = calcerror(e_eborbe, mass)
err_y = array('d', [0]*len(err_t))

r_eb = createTGraphError(n, mass, e_eb, err_eb, err_y,  2, linestyl=1)
r_eborbe = createTGraphError(n, mass, e_eborbe, err_eborbe, err_y, 4, linestyl=1)
r_t = createTGraphError(n, mass, e_t, err_t, err_y, 1, linestyl=1)


# r_eb = createTGraph(n, mass, e_eb, 2, linestyl=1)
# r_eborbe = createTGraph(n, mass, e_eborbe, 4, linestyl=1)
# r_t = createTGraph(n, mass, e_t, 1, linestyl=1)


c1 = ROOT.TCanvas("c1", "Efficiency vs M", 200, 10, 550, 200)
#c1.SetFillColor( 42 )
c1.SetGrid()
c1.cd()
pad1 = ROOT.TPad("pad1", "", 0, 0, 1, 1)
pad2 = ROOT.TPad("pad2", "", 0, 0, 1, 1)
pad3 = ROOT.TPad("pad3", "", 0, 0, 1, 1)
pad2.SetFillStyle(4000) # Make Transparent pad
pad2.SetFrameFillStyle(0)
pad3.SetFillStyle(4000) # Make Transparent pad
pad3.SetFrameFillStyle(0)

#mg = ROOT.TMultiGraph()

# Multipad solution
pad1.Draw()
pad1.cd()
r_eb.Draw(" APL ")
pad2.Draw()
pad2.cd()
r_eborbe.Draw( ' APL ' )
pad3.Draw()
pad3.cd()
r_t.Draw( ' APL ' )


leg = ROOT.TLegend(0.75, 0.55, 0.9, 0.85)
leg.SetBorderSize(0)
leg.SetFillColor(0)
leg.SetFillStyle(0)
leg.SetTextFont(42)
leg.SetTextSize(0.035)
#leg.SetHeader(r"#frac{#Gamma_{x}}{m_{x}} = 0.01")
leg.SetHeader(r"#tilde{#kappa} = 0.01")

leg.AddEntry(r_eb, "EBEB", "l")
leg.AddEntry(r_eborbe, "EBEE", "l")
leg.AddEntry(r_t, "Total", "l")

leg.Draw()

# set_CMS_lumi(c1, 4, 0, 137)
#CMS_Energy(c1, 0, E="13 TeV")
c1.Update()
#c1.GetFrame().SetFillColor(21)
#c1.GetFrame().SetBorderSize(12)
c1.Modified()
c1.Update()
c1.Draw()

c1.SaveAs("rsg_eff_err_ratio.pdf")
