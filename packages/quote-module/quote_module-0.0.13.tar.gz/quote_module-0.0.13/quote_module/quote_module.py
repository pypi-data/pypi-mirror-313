import os
import ctypes
import sys
import json
from dataclasses import dataclass

# Load the shared library
lib_path = os.path.join(os.path.dirname(__file__), 'libquote_module.so')
quote_module = ctypes.CDLL(lib_path)




class QuoteS(ctypes.Structure):
    _fields_ = [
        ("_code_str", ctypes.c_char * 8),
        ("_timestamp_str", ctypes.c_char * 32),
        ("_close_price", ctypes.c_double),
        ("_bool_close", ctypes.c_int),
        ("_close_volume", ctypes.c_ulonglong),
        ("_volume_acc", ctypes.c_int),
        ("_ask_price", ctypes.c_double * 5),
        ("_ask_volume", ctypes.c_int * 5),
        ("_bid_price", ctypes.c_double * 5),
        ("_bid_volume", ctypes.c_int * 5),
        ("_bool_continue", ctypes.c_int),
        ("_bool_bid_price", ctypes.c_int),
        ("_bool_ask_price", ctypes.c_int),
        ("_bool_odd", ctypes.c_int),
        ("_number_best_ask", ctypes.c_int),
        ("_number_best_bid", ctypes.c_int),
        ("_tick_type", ctypes.c_int),
        ("_bool_simtrade", ctypes.c_int),
        ("_double_now_seconds", ctypes.c_double),

    ]

    class ArrayWrapper:
        def __init__(self, ctypes_array):
            self.ctypes_array = ctypes_array

        def __getitem__(self, index):
            return self.ctypes_array[index]

        def __setitem__(self, index, value):
            # Enforce type compatibility with the underlying ctypes array
            if isinstance(self.ctypes_array, ctypes.Array) and issubclass(self.ctypes_array._type_, (int, ctypes.c_int)):
                self.ctypes_array[index] = int(value)  # Convert to int if required
            elif isinstance(self.ctypes_array, ctypes.Array) and issubclass(self.ctypes_array._type_, (float, ctypes.c_double)):
                self.ctypes_array[index] = float(value)  # Convert to float if required
            else:
                self.ctypes_array[index] = value

        def __len__(self):
            return len(self.ctypes_array)

        def __repr__(self):
            return repr(list(self.ctypes_array))

        def copy(self):
            # Convert the ctypes array to a regular Python list
            return list(self.ctypes_array)


    def __str__(self):
        return f'{self.timestamp_str}, Code: {self.code_str} Close: {self.close_price} / {self.close_volume}, ' \
               f'Ask: ({self.ask_price[0]}, {self.ask_price[1]}, {self.ask_price[2]}, {self.ask_price[3]}, {self.ask_price[4]}) / ' \
               f'({self.ask_volume[0]}, {self.ask_volume[1]}, {self.ask_volume[2]}, {self.ask_volume[3]}, {self.ask_volume[4]}), ' \
               f'Bid: ({self.bid_price[0]}, {self.bid_price[1]}, {self.bid_price[2]}, {self.bid_price[3]}, {self.bid_price[4]}) / ' \
               f'({self.bid_volume[0]}, {self.bid_volume[1]}, {self.bid_volume[2]}, {self.bid_volume[3]}, {self.bid_volume[4]}), ' \
               f'Simtrade: {self.bool_simtrade}' if self._bool_close else \
               f'{self.timestamp_str}, ' \
               f'Ask: ({self.ask_price[0]}, {self.ask_price[1]}, {self.ask_price[2]}, {self.ask_price[3]}, {self.ask_price[4]}) / ' \
               f'({self.ask_volume[0]}, {self.ask_volume[1]}, {self.ask_volume[2]}, {self.ask_volume[3]}, {self.ask_volume[4]}), ' \
               f'Bid: ({self.bid_price[0]}, {self.bid_price[1]}, {self.bid_price[2]}, {self.bid_price[3]}, {self.bid_price[4]}) / ' \
               f'({self.bid_volume[0]}, {self.bid_volume[1]}, {self.bid_volume[2]}, {self.bid_volume[3]}, {self.bid_volume[4]}), ' \
               f'Simtrade: {self.bool_simtrade}, now_seconds: {self._double_now_seconds}'


    @property
    def code_str(self):
        return self._code_str.decode()

    @code_str.setter
    def code_str(self, value):
        self._code_str = value

    @property
    def timestamp_str(self):
        return self._timestamp_str.decode()

    @timestamp_str.setter
    def timestamp_str(self, value):
        self._timestamp_str = value

    @property
    def close_price(self):
        return self._close_price

    @close_price.setter
    def close_price(self, value):
        self._close_price = value

    @property
    def bool_close(self):
        return bool(self._bool_close)

    @bool_close.setter
    def bool_close(self, value):
        self._bool_close = value

    @property
    def close_volume(self):
        return self._close_volume

    @close_volume.setter
    def close_volume(self, value):
        self._close_volume = value

    @property
    def volume_acc(self):
        return self._volume_acc

    @volume_acc.setter
    def volume_acc(self, value):
        self._volume_acc = value

    @property
    def ask_price(self):
        return self.ArrayWrapper(self._ask_price)

    @ask_price.setter
    def ask_price(self, value):
        self._ask_price = value

    @property
    def ask_volume(self):
        return self.ArrayWrapper(self._ask_volume)

    @ask_volume.setter
    def ask_volume(self, value):
        self._ask_volume = value

    @property
    def bid_price(self):
        return self.ArrayWrapper(self._bid_price)

    @bid_price.setter
    def bid_price(self, value):
        self._bid_price = value

    @property
    def bid_volume(self):
        return self.ArrayWrapper(self._bid_volume)

    @bid_volume.setter
    def bid_volume(self, value):
        self._bid_volume = value

    @property
    def bool_continue(self):
        return bool(self._bool_continue)

    @bool_continue.setter
    def bool_continue(self, value):
        self._bool_continue = value

    @property
    def bool_bid_price(self):
        return bool(self._bool_bid_price)

    @bool_bid_price.setter
    def bool_bid_price(self, value):
        self._bool_bid_price = value

    @property
    def bool_ask_price(self):
        return bool(self._bool_ask_price)

    @bool_ask_price.setter
    def bool_ask_price(self, value):
        self._bool_ask_price = value

    @property
    def bool_odd(self):
        return bool(self._bool_odd)

    @bool_odd.setter
    def bool_odd(self, value):
        self._bool_odd = value

    @property
    def number_best_ask(self):
        return self._number_best_ask

    @number_best_ask.setter
    def number_best_ask(self, value):
        self._number_best_ask = value

    @property
    def number_best_bid(self):
        return self._number_best_bid

    @number_best_bid.setter
    def number_best_bid(self, value):
        self._number_best_bid = value

    @property
    def tick_type(self):
        return self._tick_type

    @tick_type.setter
    def tick_type(self, value):
        self._tick_type = value

    @property
    def bool_simtrade(self):
        return bool(self._bool_simtrade)

    @bool_simtrade.setter
    def bool_simtrade(self, value):
        self._bool_simtrade = value

    @property
    def double_now_seconds(self):
        return self._double_now_seconds 

    @double_now_seconds.setter
    def double_now_seconds(self, value):
        self._double_now_seconds = value


multicast_source_mapping = [
    {
        "description": "TSE 股票即時行情及證券基本料",
        "multicast_address": "224.0.100.100",
        "port": 10000,
    },
    {
        "description": "TSE 權證即時行情及證券基本料",
        "multicast_address": "224.2.100.100",
        "port": 10002,
    },
    {
        "description": "TSE 股票5秒行情快照及證券基本料",
        "multicast_address": "224.4.100.100",
        "port": 10004,
    },
    {
        "description": "TSE 其它資訊(統計、公告類資訊)",
        "multicast_address": "224.6.100.100",
        "port": 10006,
    },
    {
        "description": "TSE 盤中零股即時行情及盤中零股證券基本資料",
        "multicast_address": "224.8.100.100",
        "port": 10008,
    },
    {
        "description": "OTC 股票即時行情及證券基本料",
        "multicast_address": "224.0.30.30",
        "port": 3000,
    },
    {
        "description": "OTC 權證即時行情及證券基本料",
        "multicast_address": "224.2.30.30",
        "port": 3002,
    },
    {
        "description": "OTC 股票5秒行情快照及證券基本料",
        "multicast_address": "224.4.30.30",
        "port": 3004,
    },
    {
        "description": "OTC 其它資訊(統計、公告類資訊)",
        "multicast_address": "224.6.30.30",
        "port": 3006,
    },
    {
        "description": "OTC 盤中零股即時行情及盤中零股證券基本資料",
        "multicast_address": "224.8.30.30",
        "port": 3008,
    },
    # {
    #     "description": "FUT 一般交易選擇權資訊",
    #     "multicast_address": "225.0.30.30",
    #     "port": 3000,
    # },
    # {
    #     "description": "FUT 夜盤一般交易選擇權資訊",
    #     "multicast_address": "225.10.30.30",
    #     "port": 3000,
    # },
]

CALLBACK_TYPE = ctypes.CFUNCTYPE(None, ctypes.POINTER(QuoteS))

#########################################
# Multicast quote reader 
#########################################

py_mc_live_pcap_callback = None

INTERFACE_IP_TSE = '10.175.2.17'  # COLO TSE
INTERFACE_IP_OTC = '10.175.1.17'  # COLO OTC
INTERFACE_IP_FUT = '10.71.17.74'  # 4 In 1


def py_mc_live_pcap_callback_wrapper(quote_ptr):
    if py_mc_live_pcap_callback:
        quote = quote_ptr.contents
        py_mc_live_pcap_callback(quote)


c_mc_live_pcap_callback = CALLBACK_TYPE(py_mc_live_pcap_callback_wrapper)

quote_module.start_mc_live_pcap_read.argtypes = [ctypes.c_char_p]
quote_module.stop_mc_live_pcap_read.argtypes = []
quote_module.set_mc_live_pcap_callback.argtypes = [CALLBACK_TYPE]


def set_mc_live_pcap_callback(callback):
    global py_mc_live_pcap_callback
    py_mc_live_pcap_callback = callback
    quote_module.set_mc_live_pcap_callback(c_mc_live_pcap_callback)


def start_mc_live_pcap_read(mapping=multicast_source_mapping):
    print(f'start_mc_live_pcap_read: {mapping}\n\n')
    source: dict
    for source in multicast_source_mapping:
        if source['description'].startswith('TSE'):
            source['interface'] = INTERFACE_IP_TSE
        elif source['description'].startswith('OTC'):
            source['interface'] = INTERFACE_IP_OTC
        if source['description'].startswith('FUT'):
            source['interface'] = INTERFACE_IP_FUT

    print(f'Replace values: {mapping}\n\n')

    quote_module.start_mc_live_pcap_read(ctypes.c_char_p(json.dumps(multicast_source_mapping).encode('utf-8')))

    print('after quote_module.start_mc_live_pcap_read\n\n')


def stop_mc_live_pcap_read():
    quote_module.stop_mc_live_pcap_read()


#########################################
# Offline pcap reader 
#########################################
py_offline_pcap_callback = None


def py_offline_pcap_callback_wrapper(quote_ptr):
    if py_offline_pcap_callback:
        quote = quote_ptr.contents
        py_offline_pcap_callback(quote)


c_offline_pcap_callback = CALLBACK_TYPE(py_offline_pcap_callback_wrapper)

quote_module.start_offline_pcap_read.argtypes = [ctypes.c_char_p]

quote_module.stop_offline_pcap_read.argtypes = []

quote_module.set_offline_pcap_callback.argtypes = [CALLBACK_TYPE]

quote_module.check_offline_pcap_read_ended.argtypes = []
quote_module.check_offline_pcap_read_ended.restype = ctypes.c_int


def set_offline_pcap_callback(callback):
    global py_offline_pcap_callback
    py_offline_pcap_callback = callback
    quote_module.set_offline_pcap_callback(c_offline_pcap_callback)


def start_offline_pcap_read(path_pcap):
    quote_module.start_offline_pcap_read(ctypes.c_char_p(path_pcap.encode('utf-8')))


def stop_offline_pcap_read():
    quote_module.stop_offline_pcap_read()


def check_offline_pcap_read_ended():
    return quote_module.check_offline_pcap_read_ended()


#########################################
# Dummy
#########################################
py_callback = None


def py_callback_wrapper(value):
    if py_callback:
        py_callback(value.decode('utf-8'))


c_callback = CALLBACK_TYPE(py_callback_wrapper)

quote_module.start_thread.argtypes = []
quote_module.stop_thread.argtypes = []
quote_module.set_callback.argtypes = [CALLBACK_TYPE]


def set_callback(callback):
    global py_callback
    py_callback = callback
    quote_module.set_callback(c_callback)


def start():
    quote_module.start_thread()


def stop():
    quote_module.stop_thread()
