#define ${ClassDiphotonSignal}_cxx
#include "${ClassDiphotonSignal}.h"
#include <TH2.h>
#include <TStyle.h>
#include <TCanvas.h>

void ${ClassDiphotonSignal}::Loop()
{
   if (fChain == 0) return;

   Long64_t nentries = fChain->GetEntriesFast();
   //counters
   double Ntotal      = 0;
   int nDiphMinv   = 0;
   int netaCut     = 0;
   int isEBEB = 0;
   int isEBEEorEEEB = 0;
   int isEEEB = 0;
   int isEEEE = 0;
   double NisGood = 0;
   double efficiency = 0;
   int npTcut = 0;

   double pTCut = 75; // default analyzer 75

   cout << "pT: " << pTCut << endl;

   TString logfile = "LOG.csv";
   ofstream outfile;
   outfile.open(logfile, ios::app);

   TString pTeventLog = "pTeventlog.csv";
   ofstream pToutfile;
   pToutfile.open(pTeventLog, ios::app);


   // Event Loop
   Long64_t nbytes = 0, nb = 0;
   for (Long64_t jentry=0; jentry<nentries;jentry++) {
      Long64_t ientry = LoadTree(jentry);
      if (ientry < 0) break;
      nb = fChain->GetEntry(jentry);   nbytes += nb;
      //if (Cut(ientry) < 0) continue;
      Ntotal++;
      double weight = Event_weightAll;
      if(jentry%10000 == 0) cout << "Number of processed events: " << jentry << endl;
      // Only look at eventw with two true photons

      if ( isGood && (Photon1_pt > pTCut) && (Photon2_pt > pTCut))
      {
        NisGood = NisGood + 1;
        npTcut = npTcut + 1;
        pToutfile << "${nametag}" << "," << Event_run << "," << Event_evnum << "," << Photon1_pt << "," <<  Photon2_pt << "," << Diphoton_Minv << endl;

        if ((1.566 < std::abs(Photon1_eta) && std::abs(Photon1_eta) < 2.5) && (1.566 < std::abs(Photon2_eta) && std::abs(Photon2_eta) < 2.5)) isEEEE = isEEEE + 1;
        if  ((std::abs(Photon1_eta)<1.442) && (std::abs(Photon2_eta)<1.442)) isEBEB = isEBEB + 1; //
      	if (((std::abs(Photon1_eta)<1.442) && (1.566 < std::abs(Photon2_eta) && std::abs(Photon2_eta) < 2.5)) || ((1.566 < std::abs(Photon1_eta) && std::abs(Photon1_eta) < 2.5) && std::abs(Photon2_eta)<1.442)) isEBEEorEEEB = isEBEEorEEEB + 1;  
       }
   }
   efficiency = NisGood/Ntotal;

   cout << endl;
   cout << "Model point: " << "${nametag}" << endl;
   cout << "Total entries            : " << Ntotal    << " " << nentries << endl;
   cout << "pTCut: " << npTcut << endl;
   cout << "isGood : " << NisGood << endl;
   cout << "isEBEB  : " << isEBEB << endl;
   cout << "isEBEEorEEEB: " << isEBEEorEEEB << endl;
   cout << "isEEEE: " << isEEEE << endl;
   cout << "Efficiency: " << NisGood/Ntotal << endl;
   cout << endl;
   //outfile.open(logfile, ios::app);
   outfile << "${nametag}" << "," << Ntotal << "," << NisGood << "," << NisGood/Ntotal << "," <<  isEBEB << "," << isEBEEorEEEB <<  "," << isEEEE << "," << npTcut << endl;
   outfile.close();
}
