/* ZomboidNX: console-only diagnostics. Not Project Zomboid itself.
 * Written for libnx and the devkitPro switch application template.
 */
#include <switch.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv) {
    (void)argc;
    (void)argv;
    consoleInit(NULL);
    padConfigureInput(1, HidNpadStyleSet_NpadStandard);
    PadState pad;
    padInitializeDefault(&pad);

    int memory_tested = 0;
    int memory_ok = 0;
    int manifest_checked = 0;
    int manifest_present = 0;
    unsigned char *test_mem = NULL;

    while (appletMainLoop()) {
        padUpdate(&pad);
        u64 down = padGetButtonsDown(&pad);

        if (down & HidNpadButton_Plus) break;
        if (down & HidNpadButton_A) {
            free(test_mem);
            test_mem = malloc(16 * 1024 * 1024);
            memory_ok = (test_mem != NULL);
            memory_tested = 1;
            if (test_mem) {
                ((volatile unsigned char *)test_mem)[0] = 0xA5;
                ((volatile unsigned char *)test_mem)[16 * 1024 * 1024 - 1] = 0x5A;
            }
        }
        if (down & HidNpadButton_B) {
            FILE *f = fopen("sdmc:/switch/zomboidnx/game-manifest.txt", "rb");
            manifest_present = (f != NULL);
            manifest_checked = 1;
            if (f) fclose(f);
        }

        printf("\x1b[2J\x1b[1;1H");
        printf("ZomboidNX - feasibility diagnostic\n");
        printf("Nintendo Switch / Atmosphere / libnx\n\n");
        printf("Independent test application. Not the game.\n\n");
        printf("[A] Allocate and touch 16 MiB of RAM\n");
        printf("[B] Read-only check for optional SD manifest\n");
        printf("[+] Exit to hbmenu\n\n");
        printf("RAM test: %s\n", !memory_tested ? "not run" : (memory_ok ? "OK" : "FAILED"));
        printf("SD manifest: %s\n", !manifest_checked ? "not checked" : (manifest_present ? "found" : "not found"));
        consoleUpdate(NULL);
    }

    free(test_mem);
    consoleExit(NULL);
    return 0;
}
