#ifndef ISIS_COMMAND_LINE_TEST_C
#define ISIS_COMMAND_LINE_TEST_C

#include "isisCommandLineTest.h"

using namespace std;

int main()
   {
     int TestValue = 0;
        
    // try isis command 
    try
       {
        
        system("qview");
        throw TestValue;
       }
    catch(int errorCode)
       {
        cout << "qview failed\n";
       }
       
       // try main conda
    try
       {
        system("conda deactivate isis3");
        throw TestValue;
       }
    catch(int errorCode)
       {
        cout << "isis3 deactivation failed\n";
       }
      
    // try activating isis 
    try
       {
        system("$ conda deactivate");
        throw TestValue;
       }
    catch(int errorCode)
       {
        cout << "main didnt work\n";
       }
       
    
    return TestValue;
   }

#endif
