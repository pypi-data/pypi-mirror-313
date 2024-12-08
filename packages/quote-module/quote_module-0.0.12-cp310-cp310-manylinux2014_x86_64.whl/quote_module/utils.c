
#include <math.h>
#include <iconv.h>
#include <string.h>
#include <stdio.h>


int convert_BCD(const unsigned char byte)
{
    return ((byte >> 4) * 10) + (byte & 0xf);
}

int convert_BCDs_len2_optimized(const unsigned char *ptr)
{
    int bcd0 = ((ptr[0] >> 4) * 10) + (ptr[0] & 0xf);
    int bcd1 = ((ptr[1] >> 4) * 10) + (ptr[1] & 0xf);

    return (bcd0 * 100) + bcd1;
}

int convert_BCDs_len3_optimized(const unsigned char *ptr)
{
    int bcd0 = ((ptr[0] >> 4) * 10) + (ptr[0] & 0xf);
    int bcd1 = ((ptr[1] >> 4) * 10) + (ptr[1] & 0xf);
    int bcd2 = ((ptr[2] >> 4) * 10) + (ptr[2] & 0xf);

    return (bcd0 * 10000) + (bcd1 * 100) + bcd2;
}

int convert_BCDs_len4_optimized(const unsigned char *ptr)
{
    int bcd0 = ((ptr[0] >> 4) * 10) + (ptr[0] & 0xf);
    int bcd1 = ((ptr[1] >> 4) * 10) + (ptr[1] & 0xf);
    int bcd2 = ((ptr[2] >> 4) * 10) + (ptr[2] & 0xf);
    int bcd3 = ((ptr[3] >> 4) * 10) + (ptr[3] & 0xf);

    return (bcd0 * 1000000) + (bcd1 * 10000) + (bcd2 * 100) + bcd3;
}

int convert_BCDs_len5_optimized(const unsigned char *ptr)
{
    int bcd0 = ((ptr[0] >> 4) * 10) + (ptr[0] & 0xf);
    int bcd1 = ((ptr[1] >> 4) * 10) + (ptr[1] & 0xf);
    int bcd2 = ((ptr[2] >> 4) * 10) + (ptr[2] & 0xf);
    int bcd3 = ((ptr[3] >> 4) * 10) + (ptr[3] & 0xf);
    int bcd4 = ((ptr[4] >> 4) * 10) + (ptr[4] & 0xf);

    return (bcd0 * 100000000) + (bcd1 * 1000000) + (bcd2 * 10000) + (bcd3 * 100) + bcd4;
}

unsigned long long convert_BCDs_len6_optimized(const unsigned char *ptr)
{
    int bcd0 = ((ptr[0] >> 4) * 10) + (ptr[0] & 0xf);
    int bcd1 = ((ptr[1] >> 4) * 10) + (ptr[1] & 0xf);
    int bcd2 = ((ptr[2] >> 4) * 10) + (ptr[2] & 0xf);
    int bcd3 = ((ptr[3] >> 4) * 10) + (ptr[3] & 0xf);
    int bcd4 = ((ptr[4] >> 4) * 10) + (ptr[4] & 0xf);
    int bcd5 = ((ptr[5] >> 4) * 10) + (ptr[5] & 0xf);

    return (bcd0 * 10000000000) + (bcd1 * 100000000) + (bcd2 * 1000000) + (bcd3 * 10000) + (bcd4 * 100) + bcd5;
}

unsigned char xor_data(const unsigned char *data, int len)
{
    unsigned char result = 0;  // Initialize XOR result to 0

    for (int i = 0; i < len; i++) {
        result ^= data[i];  // XOR each byte with the result
    }

    return result;  // Return the final XOR result
}

void DumpHex(const void* data, int size)
{
    unsigned char ascii[17];
    size_t i = 0, j;
    ascii[16] = '\0';
    printf("%8.8lX: ", i);
    for (i = 0; i < size; ++i) {
        printf("%02X ", ((unsigned char*)data)[i]);
        if (((unsigned char*)data)[i] >= ' ' && ((unsigned char*)data)[i] <= '~') {
            ascii[i % 16] = ((unsigned char*)data)[i];
        } else {
            ascii[i % 16] = '.';
        }
        if ((i+1) % 8 == 0 || i+1 == size) {
            printf(" ");
            if ((i+1) % 16 == 0) {
                printf("|  %s \n%8.8lX: ", ascii, i);
            } else if (i+1 == size) {
                ascii[(i+1) % 16] = '\0';
                if ((i+1) % 16 <= 8) {
                    printf(" ");
                }
                for (j = (i+1) % 16; j < 16; ++j) {
                    printf("   ");
                }
                printf("|  %s \n", ascii);
            }
        }
    }
    printf("\n");
}