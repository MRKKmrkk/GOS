#include <Windows.h>
#include <Psapi.h>
#pragma comment(lib,"Psapi.lib")
#include <stdio.h>
#include <string.h>

DWORD findProcess(char *strProcessName) {

    DWORD aProcesses[1024], cbNeeded, cbMNeeded;
    HMODULE hMods[1024];
    HANDLE hProcess;
    char szProcessName[MAX_PATH];

    if ( !EnumProcesses( aProcesses, sizeof(aProcesses), &cbNeeded ) )  return 0;

    for(int i=0; i< (int) (cbNeeded / sizeof(DWORD)); i++)
    {
        hProcess = OpenProcess(  PROCESS_QUERY_INFORMATION | PROCESS_VM_READ, FALSE, aProcesses[i]);
        EnumProcessModules(hProcess, hMods, sizeof(hMods), &cbMNeeded);
        GetModuleFileNameEx( hProcess, hMods[0], szProcessName,sizeof(szProcessName));

        if(strstr(szProcessName, strProcessName))
        {
            return(aProcesses[i]);
        }
    }

    return 0;

}

DWORD killProcess(DWORD currentProcess) {

    HANDLE TargetProcess = OpenProcess(PROCESS_TERMINATE, FALSE, currentProcess);

    if(TargetProcess == NULL)
    {
        return 0;
    }

    TerminateProcess(TargetProcess, 0);

    CloseHandle(TargetProcess);

    return 1;

}