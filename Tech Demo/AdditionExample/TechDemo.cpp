#include <iostream>
#include <stdlib.h>

using namespace std;

int main(int argc, char** argsv)
   {
    if( argc == 1 )
       {
        cout << "\nThis program requires two integers given by command line"<< "\n";
        cout << "Aborting Function\n"<< endl;
        return 2;
       }
    else
       {


        int arg1 = atoi( argsv[1] );
        int arg2 = atoi( argsv[2] );
    
        cout<< "\n"<< arg1<< " + "<< arg2<< " = "<< (arg1 + arg2)<< endl;

        return (arg1 + arg2);
 
       } 
   }

