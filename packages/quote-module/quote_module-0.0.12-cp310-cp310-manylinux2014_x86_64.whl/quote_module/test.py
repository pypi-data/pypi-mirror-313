
import datetime
import time
import quote_module.quote_module as qm


def callback_pcap_read(quote: qm.QuoteS):
    pass
    # print(f'Symbol: {quote.code_str.decode()} {quote.close_price}')
    print(quote)


if False:
    qm.INTERFACE_IP_TSE = '10.175.2.17' 
    qm.INTERFACE_IP_OTC = '10.175.1.17' 
    qm.INTERFACE_IP_FUT = '10.71.17.74'
    qm.set_mc_live_pcap_callback(callback_pcap_read)
    qm.start_mc_live_pcap_read()


if True:
    qm.set_offline_pcap_callback(callback_pcap_read)
    qm.start_offline_pcap_read('/home/william/tcpdump/TSEOTC-2024-09-30.pcap')


while True:
    ret = qm.check_offline_pcap_read_ended()
    if ret != 0:
        break
    print(f'{datetime.datetime.now()} {ret}')
    time.sleep(1)
