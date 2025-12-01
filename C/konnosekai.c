#include<stdio.h>

#define JUDUL "Putrahaidaribad"
#define BILANGAN 100

int main() {
    int angka = 10;
    char huruf = 'A';
    float pecahan = 4.57324;

    printf("konstanta JUDUL adalah %s\n", JUDUL);
    printf("Konstanta BILANGAN adalah %i\n", BILANGAN);
    
    printf("variabel angka = %d\n", angka);
    printf("variabel huruf = %c\n", huruf);
    printf("variabel pecahan = %.2f\n", pecahan);
    
    return 0;
}