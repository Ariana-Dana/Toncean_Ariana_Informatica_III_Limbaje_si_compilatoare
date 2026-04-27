#include <stdio.h>
#include <stdbool.h>

int main() {
    int x;
    double y;
    bool ok;
    double t1;
    double t2;
    double t3;
    double t4;
    double t5;
    double t6;

    x = 10;
    t1 = x * 2;
    t2 = t1 + 5.5;
    y = t2;
    ok = true;
    t3 = y > 20;
    t4 = t3 && ok;
    if (t4) goto L1;
    goto L2;
L1:
    printf("%f\n", y);
L2:
L3:
    t5 = x < 15;
    if (t5) goto L4;
    goto L5;
L4:
    t6 = x + 1;
    x = t6;
    goto L3;
L5:
    return 0;
}