#include "${ClassDiphotonSignal}.C"
#include <iostream>
#include "TStopwatch.h"
using namespace std;

int ${analyzefunc}(){
        // start stopwatch
	TStopwatch sw;
	sw.Start();

	${ClassDiphotonSignal} t;
        t.Loop();

	// stop stopwatch
	sw.Stop();
	cout << "Real Time: " << sw.RealTime()/60.0 << " minutes" << endl;
	cout << "CPU Time: " << sw.CpuTime()/60.0 << " minutes" << endl;
	return 0;

}
