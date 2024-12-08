#define _GNU_SOURCE
/* For sockaddr_in */
#include <netinet/in.h>
/* For socket functions */
#include <sys/socket.h>
#include <linux/unistd.h>
#include <sys/file.h>

#include <event2/event.h>
#include <arpa/inet.h>
#include <sys/signal.h>
#include <assert.h>
#include <unistd.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <errno.h>
#include <time.h>
#include <math.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <netinet/ip.h>
#include <net/if.h>
#include <netinet/if_ether.h>
#include <net/ethernet.h>
#include <netinet/tcp.h>
#define __FAVOR_BSD
#include <netinet/udp.h>
#include <arpa/inet.h>
#include <pcap.h>
//#include <sys/file.h>
#include <sys/stat.h>

#include <sys/ioctl.h>

#include <sys/resource.h>

#include <fcntl.h>

#include <stdio.h>
#include <pthread.h>
#include <unistd.h>
#include <jansson.h>
#include <time.h>

#include "utils.h"

static pthread_t thread;

callback_quote_t global_mc_live_pcap_callback = NULL;

typedef void (*quote_callback_t)(const unsigned char *data, unsigned int len, void *arg, const struct timeval *tv);

#define MAX_LINE 16384
struct fd_state {
    char buffer[MAX_LINE];
    struct in_addr mcast_ip;
    u_int16_t mcast_port;
    struct event *read_event;
    quote_callback_t callback;
    void *arg;

    char str_name[BUFSIZ];
    char str_mcast[BUFSIZ];
    char str_local[BUFSIZ];
    int int_mcast_port;
};

static void free_fd_state(struct fd_state *state)
{
    printf("state freed: %s %s:%d -> %s\n", state->str_name, state->str_mcast, state->int_mcast_port, state->str_local);
    event_free(state->read_event);
    free(state);
}

static void do_read(evutil_socket_t fd, short events, void *arg)
{
    struct fd_state *state = arg;
    unsigned char buf[BUFSIZ];
    struct sockaddr_in src_addr;
    socklen_t len;
    ssize_t result;
    struct timeval tv;

    result = recvfrom(fd, buf, sizeof(buf), 0, (struct sockaddr*)&src_addr, &len);
#if 0
    fprintf(stderr, "recv %zd from %s:%d", result, inet_ntoa(src_addr.sin_addr), ntohs(src_addr.sin_port));
    fprintf(stderr, " with mcast_channel %s:%d\n", inet_ntoa(state->mcast_ip), ntohs(state->mcast_port));
#endif

    if (result > 0) {
        gettimeofday(&tv, NULL);
        state->callback(buf, (int) result, state->arg, &tv);
    }

    if (result == 0) {
        free_fd_state(state);
    } else if (result < 0) {
        if (errno == EAGAIN) // XXXX use evutil macro
        {
            return;
        }
        perror("recv");
        free_fd_state(state);
    }
}

static struct fd_state * alloc_fd_state(struct event_base *base, evutil_socket_t fd)
{
    struct fd_state *state = malloc(sizeof(struct fd_state));
    if (!state)
        return NULL;
    state->read_event = event_new(base, fd, EV_READ|EV_PERSIST, do_read, state);
    if (!state->read_event) {
        free(state);
        return NULL;
    }
    return state;
}



static int mcast_channel_fd_new(const char *str_name,
                                struct event_base *base,
                                struct in_addr mcast,
                                const char *str_mcast,
                                struct in_addr local,
                                const char *str_local,
                                u_int16_t mcast_port,
                                int int_mcast_port )
{
    evutil_socket_t nsock;
    struct sockaddr_in sin;
    int loop = 1;
    struct ip_mreq mreq;
    struct fd_state *state = NULL;

    mreq.imr_multiaddr = mcast;
    mreq.imr_interface = local;

    sin.sin_family = AF_INET;
    //sin.sin_addr.s_addr = inet_addr("192.168.56.126");
    sin.sin_addr.s_addr = 0;
    sin.sin_port = mcast_port;
    nsock = socket(AF_INET, SOCK_DGRAM, 0);
    evutil_make_socket_nonblocking(nsock);

    {
        int one = 1;
        setsockopt(nsock, SOL_SOCKET, SO_REUSEADDR, &one, sizeof(one));
    }

    if (bind(nsock, (struct sockaddr*)&sin, sizeof(sin)) < 0) {
        perror("bind");
        return -1;
    }
    if(setsockopt(nsock, IPPROTO_IP, IP_MULTICAST_LOOP, &loop, sizeof(loop)) < 0)
    {
        perror("setsocket():IP MULTICAST_LOOP");
        return -1;
    }

    if(setsockopt(nsock, IPPROTO_IP, IP_ADD_MEMBERSHIP, &mreq, sizeof(mreq)) < 0) {
        printf("%s setsockopt():IP ADD MEMBURSHIP\n",strerror(errno));
        return -1;
    }
    state = alloc_fd_state(base, nsock);
    if (state == NULL) {
        return 0;
    }
    state->mcast_ip = mreq.imr_multiaddr;
    state->mcast_port = mcast_port;
    // User defined data
    if (!strncmp(str_name, "TSE", 3)) {
        state->callback = stock_quote_unpacker;
    } else if (!strncmp(str_name, "OTC", 3)) {
        state->callback = stock_quote_unpacker;
    } else if (!strncmp(str_name, "FUT", 3)) {
        state->callback = future_quote_unpacker;
    } 
    state->arg = NULL;

    strcpy(state->str_name, str_name);
    strcpy(state->str_mcast, str_mcast);
    strcpy(state->str_local, str_local);
    state->int_mcast_port = int_mcast_port;
    event_add(state->read_event, NULL);
    return 0;
}


void *thread_mc_live_pcap_reader(void *str_mapping)
{
    json_t *root;
    json_error_t error;
    struct event_base *base;
    struct in_addr mcast;
    struct in_addr local;

    base = event_base_new();
    if (!base) {
        printf("event_base_new error. Exit..\n");
        return NULL;
    }

    root = json_loads(str_mapping, 0, &error);
    if (!root) {
        fprintf(stderr, "Error parsing JSON: %s\n", error.text);
        return NULL;
    }

    if (!json_is_array(root)) {
        fprintf(stderr, "Error: root is not an array\n");
        json_decref(root);
        return NULL;
    }

    size_t index;
    json_t *value;
    json_array_foreach(root, index, value) {
        const char *description = json_string_value(json_object_get(value, "description"));
        const char *multicast_address = json_string_value(json_object_get(value, "multicast_address"));
        int port = json_integer_value(json_object_get(value, "port"));
        const char *interface = json_string_value(json_object_get(value, "interface"));

        mcast.s_addr = inet_addr(multicast_address);
        local.s_addr = inet_addr(interface);

        printf("Description: %s\n", description);
        printf("Multicast Address: %s\n", multicast_address);
        printf("Port: %d\n", port);
        printf("Interface: %s\n", interface);
        printf("\n");

        mcast_channel_fd_new(description, 
                             base, 
                             mcast, 
                             multicast_address, 
                             local, 
                             interface, 
                             htons(port), 
                             port);
    }
    json_decref(root);
    event_base_dispatch(base);
    return NULL;
}

void set_mc_live_pcap_callback(callback_quote_t callback) {
    global_mc_live_pcap_callback = callback;
}


void start_mc_live_pcap_read(const char *str_mapping) {
    printf("%s:%d %s\n", __FUNCTION__, __LINE__, str_mapping);
    pthread_create(&thread, NULL, thread_mc_live_pcap_reader, (void *)str_mapping);
}

void stop_mc_live_pcap_read() {
    pthread_cancel(thread);
    pthread_join(thread, NULL);
}

