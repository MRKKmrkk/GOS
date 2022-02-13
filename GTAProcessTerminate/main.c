#include <Windows.h>
#pragma comment(lib,"Psapi.lib")
#include <stdio.h>
#include "win_util.h"

int main() {

    DWORD currentProcess = findProcess("gta5.exe");
    int code = killProcess(currentProcess);

    return code;

}
