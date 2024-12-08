

#ifndef __UTILS_C__
#define __UTILS_C__

int convert_BCD(const unsigned char bcd);
int convert_BCDs_len2_optimized(const unsigned char *ptr);
int convert_BCDs_len3_optimized(const unsigned char *ptr);
int convert_BCDs_len4_optimized(const unsigned char *ptr);
int convert_BCDs_len5_optimized(const unsigned char *ptr);
unsigned long long convert_BCDs_len6_optimized(const unsigned char *ptr);
unsigned char xor_data(const unsigned char *data, int len);

struct quote_s {
    char code_str[8];
    char timestamp_str[32];
    double close_price;
    int bool_close;
    unsigned long long close_volume;
    int volume_acc;
    double ask_price[5];
    int ask_volume[5];
    double bid_price[5];
    int bid_volume[5];
    int bool_continue;
    int bool_bid_price;
    int bool_ask_price;
    int bool_odd;
    int number_best_ask;
    int number_best_bid;
    int tick_type;
    int bool_simtrade;

    double double_now_seconds;
};

typedef void (*callback_str_t)(const char*);
typedef void (*callback_quote_t)(struct quote_s *);

void stock_quote_unpacker(const unsigned char *data,
                          unsigned int len,
                          void *arg,
                          const struct timeval *tv);

void future_quote_unpacker(const unsigned char *data,
                          unsigned int len,
                          void *arg,
                          const struct timeval *tv);

void DumpHex(const void* data, int size);

extern callback_quote_t global_mc_live_pcap_callback;

#endif // __UTILS_C__

