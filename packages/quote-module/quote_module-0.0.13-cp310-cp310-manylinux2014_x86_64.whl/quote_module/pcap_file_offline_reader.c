#define _GNU_SOURCE
/* For sockaddr_in */
#include <netinet/in.h>
/* For socket functions */
#include <sys/socket.h>
#include <linux/unistd.h>
#include <sys/file.h>
#include <netinet/in.h>
#include <netinet/ip.h>
#include <net/if.h>
#include <netinet/if_ether.h>
#include <net/ethernet.h>
#include <netinet/tcp.h>
#define __FAVOR_BSD
#include <netinet/udp.h>
#include <arpa/inet.h>
#include <signal.h>

#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <errno.h>
#include <pcap.h>
#include <pcap/pcap.h>
#include <pcap/pcap-inttypes.h>
#include <sys/types.h>

#include <stdio.h>
#include <pthread.h>
#include <unistd.h>
#include <time.h>

#include "utils.h"

static pthread_t thread;

static callback_str_t global_callback = NULL;

static callback_quote_t global_offline_pcap_callback = NULL;

static void stock_quote_parser(const unsigned char *data,
                        unsigned int len,
                        void *arg,
                        const struct timeval *tv,
                        int category,
                        int format,
                        int version)
{
    struct quote_s quote;
    int offset = 0;
    int hour, minute, second, millisecond;
    unsigned char flag = 0;
    int status23, status24;
    int bool_odd = format == 23 ? 1 : 0;
    int vol_len = format == 23 ? 6 : 4;
    char last_c = ' ';

    memset(&quote, 0, sizeof(struct quote_s));
    // 股票代號
    // data[10-15]: 股票代號
    offset = 10;
    memset(quote.code_str, 0, sizeof(quote.code_str));
    memcpy(quote.code_str, &data[offset], 6);
    for(int i=0; i<6; i++) {
        if (quote.code_str[i] == ' ') {
            quote.code_str[i] = '\0';
            break;
        }
    }

#if 0
    // 我們不管認售權證
    last_c = quote.code_str[strlen(quote.code_str) - 1];
    if (last_c > '9') {
        return;
    }
#endif

    // data[16-21]: 撮合時間
    offset = 16;
    hour = convert_BCD(data[offset + 0]);
    minute = convert_BCD(data[offset + 1]);
    second = convert_BCD(data[offset + 2]);
    millisecond = convert_BCDs_len3_optimized(&data[offset + 3]);
    sprintf(quote.timestamp_str, "%.2d:%.2d:%.2d.%.6d", hour, minute, second, millisecond);

    quote.double_now_seconds = hour * 3600 + minute * 60 + second + millisecond / 1000000.0;


    // 揭示項目註記
    /*
        (1)以各別Bit 表示揭示項目（以二進位 BINARY 表示）
            Bit 7 （成交價、成交量）－ 0︰無成交價、成交量，不傳送
                                    1︰有成交價、成交量，而且傳送
            Bit 6-4（買進價、買進量）－ 000︰無買進價、買進量，不傳送
                                    001－101︰揭示買進價、買進量之傳送之檔位數（一至五檔以二進位BINARY 表示）
            Bit 3-1（賣出價、賣出量）－ 000︰無賣出價、賣出量，不傳送
                                    001－101︰揭示賣出價、賣出量之傳送之檔位數（一至五檔以二進位BINARY 表示）
            Bit 0 （最佳五檔價量） － 0︰揭示成交價量與最佳五檔買賣價量
                                1︰僅揭示成交價量、不揭示最佳五檔買賣價量
            說明：
                逐筆交易每筆委託撮合後，可能產生數個成交價量揭示，揭示最後一個成交價量時，
            同時揭露最佳五檔買賣價量，Bit 0 = 0。非最後一個成交價量揭示時，則僅揭示成交價量但
            不揭示最佳五檔，Bit 0 = 1。
        (2)每一揭示價欄位，長度為 5 Bytes；每一揭示量欄位，長度為 4 Bytes。
    */
    flag = data[22];
    // 漲跌停註記
    status23 = data[23];
    // 狀態註記
    /*
    Bit 7 試算狀態註記 0：一般揭示 1：試算揭示
    Bit 6 試算後延後開盤註記 0：否 1：是
    Bit 5 試算後延後收盤註記 0：否 1：是
    Bit 4 撮合方式註記 0：集合競價 1：逐筆撮合
    Bit 3 開盤註記 0：否 1：是
    Bit 2 收盤註記 0：否 1：是
    Bit 1-0 保留
    */
    status24 = data[24];
    if (status24 & 0x80) {
        quote.bool_simtrade = 1;
    }
    // 累計成交數量
    offset = 25;
    quote.volume_acc = convert_BCDs_len4_optimized(&data[offset]);

    // 從累計成交量之後開始
    if (bool_odd) {
        offset = 31;
    } else {
        offset = 29;
    }

    // 有成交價
    if (flag & 0x80) {
        quote.bool_close = 1;

        // 成交價
        quote.close_price = (double)convert_BCDs_len5_optimized(&data[offset]) / 10000;
        offset += 5;

        // 成交量
        quote.close_volume = vol_len == 4 ? convert_BCDs_len4_optimized(&data[offset]) : convert_BCDs_len6_optimized(&data[offset]); 
        offset += vol_len;

        // TODO: tick_type
    }
    /*
        Bit 0 （最佳五檔價量 0︰ 揭示成交價量與最佳五檔買賣價量
                           1︰ 僅揭示成交價量、不揭示最佳五檔買賣價量
        說明：
            逐筆交易每筆委託撮合後，可能產生數個成交價量揭示，揭示最後一個成交價量時，
        同時揭露最佳 五檔買賣價量， Bit 0 = 0。非最後一個成交價量揭示時，則僅揭示成交價量但
        不揭示最佳 五檔， Bit 0 = 1
    */
    if (flag & 1)   // 非最後一個成交價量揭示時
        quote.bool_continue = 1;
    // 五檔或三檔買進價量
    // 揭示項目註記
    memset(quote.bid_price, 0, sizeof(quote.bid_price));
    memset(quote.bid_volume, 0, sizeof(quote.bid_volume));

    quote.number_best_bid = (flag & 0b01110000) >> 4;

    for(int i=0; i<quote.number_best_bid; i++) {
        quote.bid_price[i] = (double) convert_BCDs_len5_optimized(&data[offset]) / 10000;
        offset += 5;
        quote.bid_volume[i] = (vol_len == 4) ? convert_BCDs_len4_optimized(&data[offset]) : convert_BCDs_len6_optimized(&data[offset]);
        offset += vol_len;
        quote.bool_bid_price = 1;
    }

    memset(quote.ask_price, 0, sizeof(quote.ask_price));
    memset(quote.ask_volume, 0, sizeof(quote.ask_volume));

    quote.number_best_ask = (flag & 0b00001110) >> 1;

    for(int i=0; i<quote.number_best_ask; i++) {
        quote.ask_price[i] = (double) convert_BCDs_len5_optimized(&data[offset]) / 10000;
        offset += 5;
        quote.ask_volume[i] = vol_len == 4 ? convert_BCDs_len4_optimized(&data[offset]) : convert_BCDs_len6_optimized(&data[offset]);
        offset += vol_len;
        quote.bool_ask_price = 1;
    }

#if 0
    //DumpHex(data, len);
    printf("%s code: %s, close: %.2f, VolSum: %d, Volume: %lld, [%.2f, %.2f, %.2f, %.2f, %.2f]/[%d, %d, %d, %d, %d] [%.2f, %.2f, %.2f, %.2f, %.2f]/[%d, %d, %d, %d, %d]\n",
           quote.timestamp_str, quote.code_str, quote.close_price, quote.volume_acc, quote.close_volume, 
           quote.ask_price[0], quote.ask_price[1], quote.ask_price[2], quote.ask_price[3], quote.ask_price[4],
           quote.ask_volume[0], quote.ask_volume[1], quote.ask_volume[2], quote.ask_volume[3], quote.ask_volume[4],
           quote.bid_price[0], quote.bid_price[1], quote.bid_price[2], quote.bid_price[3], quote.bid_price[4],
           quote.bid_volume[0], quote.bid_volume[1], quote.bid_volume[2], quote.bid_volume[3], quote.bid_volume[4]);
#endif


    if (global_offline_pcap_callback) {
        global_offline_pcap_callback(&quote);
    }
    if (global_mc_live_pcap_callback) {
        global_mc_live_pcap_callback(&quote);
    }
}



void stock_quote_unpacker(const unsigned char *data,
                          unsigned int len,
                          void *arg,
                          const struct timeval *tv)
{
    int offset = 0;
    int data_len = 0;
    int category = 0;
    int format = 0;
    int version = 0;
    int serial_number = 0;
    static int last_serial_number_TSE = 0;
    static int last_serial_number_OTC = 0;
    unsigned target_format = 0;
    unsigned message_type = 0;
    while(len > 0) {
        offset = 0;
        if (data[0] != 0x1b) {
            return;
        }
        // 1, 2: Length
        offset = 1;
        data_len = convert_BCDs_len2_optimized(&data[offset]);
        if (data_len == 0)
            break;
        int ret = xor_data(&data[1], data_len - 1);
        if (ret != 7) {

        } else {
            // 3: category stock_code
            offset = 3;
            category = convert_BCD(data[offset]);
            // 4: format stock_code
            offset = 4;
            format = convert_BCD(data[offset]);
            // 5: version stock_code
            offset = 5;
            version = convert_BCD(data[offset]);
            // 6: Serial number
            offset = 6;
            serial_number = convert_BCDs_len4_optimized(&data[offset]);

            target_format = category * 10000 + format * 100 + version;
            message_type = category * 100 + format;
    #if 1
            if (message_type == 101 || message_type == 201) {

            } else if (message_type == 106 || message_type == 206) {
                // 格式六：集中市場普通股競價交易即時行情資訊
                // 格式六︰等價交易即時行情資訊
                stock_quote_parser(data, data_len, arg, tv, category, format, version);
            } else if (message_type == 117 || message_type == 217) {
                // 格式十七︰第二IP上櫃股票等價交易即時行情資訊
                // 格式十七：第二IP集中市場普通股競價交易即時行情資訊
                stock_quote_parser(data, data_len, arg, tv, category, format, version);
            } else if (message_type == 123 || message_type == 223) {
                // 格式二十三：集中市場盤中零股交易即時行情資訊
                // 格式二十三︰上櫃股票盤中零股交易即時行情資訊
                //stock_quote_parser(data, data_len, arg, tv, category, format, version);
            }
    #endif
        }
        len -= data_len;
        data += data_len;
    }

}


void future_quote_unpacker(const unsigned char *data,
                          unsigned int len,
                          void *arg,
                          const struct timeval *tv)
{

}


static void offline_pcap_handler_function(u_char *userData,
        const struct pcap_pkthdr *pkthdr,
        const u_char *packet)
{
    const struct ether_header *etherHeader;
    const struct ip *ipHeader;
    const struct udphdr *udpHeader;
    char source_IP[INET_ADDRSTRLEN];
    char dest_IP[INET_ADDRSTRLEN];
    u_int source_port, dest_port;
    u_char *data;
    int len;

    (*((unsigned int *)userData))++;

    etherHeader = (struct ether_header *)packet;
    if (ntohs(etherHeader->ether_type) != ETHERTYPE_IP) {
        return;
    }

    ipHeader = (struct ip *)(packet + sizeof(struct ether_header));
    inet_ntop(AF_INET, &(ipHeader->ip_src), source_IP, INET_ADDRSTRLEN);
    inet_ntop(AF_INET, &(ipHeader->ip_dst), dest_IP, INET_ADDRSTRLEN);
    if (ipHeader->ip_p == IPPROTO_TCP)
        return;
    udpHeader = (struct udphdr *)(packet + sizeof(struct ether_header) + sizeof(struct ip));
    source_port = ntohs(udpHeader->uh_sport);
    dest_port = ntohs(udpHeader->uh_dport);

    data = (u_char *) (udpHeader + 1);
    len = pkthdr->len - ((char *)data - (char *)packet);
    stock_quote_unpacker(data, len, NULL, &pkthdr->ts);
}

static char g_filename[BUFSIZ];

void *thread_pcap_file_offline_reader(void *filename_offline_pcap)
{
    pcap_t *fpcap;
    char errbuf[BUFSIZ];
    time_t start, end;
    unsigned int total_packets = 0;
    if (filename_offline_pcap == NULL) {
        printf("You didn't specify the offline pcap file\n");
        return NULL;

    }
    fpcap = pcap_open_offline_with_tstamp_precision(g_filename, PCAP_TSTAMP_PRECISION_NANO, errbuf);
    if (fpcap == NULL) {
        printf("Open %s failed", (char *)g_filename);
        return 0;
    }
    time(&start);
    if (pcap_loop(fpcap, 0, offline_pcap_handler_function, (void *)&total_packets)) {
        printf("pcap_loop() failed: %s\n", pcap_geterr(fpcap));
    }
    time(&end);
    pcap_close(fpcap);
    printf("Total %d packets processed. %f\n", total_packets, difftime(end, start));
    return NULL;
}

void set_offline_pcap_callback(callback_quote_t callback) {
    global_offline_pcap_callback = callback;
}


void start_offline_pcap_read(const char *path_pcap) {
    strcpy(g_filename, path_pcap);
    pthread_create(&thread, NULL, thread_pcap_file_offline_reader, (void *)path_pcap);
}

void stop_offline_pcap_read() {
    pthread_cancel(thread);
    pthread_join(thread, NULL);
}



void* thread_func(void* arg) {
    char buffer[100];
    while (1) {
        time_t now = time(NULL);
        struct tm* t = localtime(&now);
        strftime(buffer, sizeof(buffer), "%Y-%m-%d %H:%M:%S", t);
        if (global_callback) {
            global_callback(buffer);
        }
        sleep(1);
    }
    return NULL;
}

void start_thread() {
    pthread_create(&thread, NULL, thread_func, NULL);
}

void stop_thread() {
    pthread_cancel(thread);
    pthread_join(thread, NULL);
}

void set_callback(callback_str_t callback) {
    global_callback = callback;
}

int check_offline_pcap_read_ended() {
    //return pthread_kill(thread, 0);
    int res = pthread_tryjoin_np(thread, NULL);
    if (res == 0) {
        // Thread has terminated
        return 1;
    } else if (res == EBUSY) {
        // Thread is still running
        return 0;
    } else {
        // An error occurred
        return -1;
    }
}

