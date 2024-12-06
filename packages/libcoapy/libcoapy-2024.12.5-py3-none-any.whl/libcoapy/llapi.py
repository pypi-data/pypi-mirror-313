
import os, sys, enum
import ctypes as ct

verbosity = 0
initialized = False

class NullPointer(Exception):
	pass

class ctypes_enum_gen(enum.IntEnum):
	@classmethod
	def from_param(cls, param):
		return ct.c_int(param)
	
	@classmethod
	def get_ctype(cls):
		return ct.c_int
	
	def __str__(self):
		return self.name

coap_tls_library_t = ctypes_enum_gen("coap_tls_library_t", [
	"COAP_TLS_LIBRARY_NOTLS",
	"COAP_TLS_LIBRARY_TINYDTLS",
	"COAP_TLS_LIBRARY_OPENSSL",
	"COAP_TLS_LIBRARY_GNUTLS",
	"COAP_TLS_LIBRARY_MBEDTLS",
	"COAP_TLS_LIBRARY_WOLFSSL",
	], start=0)

coap_log_t = ctypes_enum_gen("coap_log_t", [
	"COAP_LOG_EMERG",
	"COAP_LOG_ALERT",
	"COAP_LOG_CRIT",
	"COAP_LOG_ERR",
	"COAP_LOG_WARN",
	"COAP_LOG_NOTICE",
	"COAP_LOG_INFO",
	"COAP_LOG_DEBUG",
	"COAP_LOG_OSCORE",
	"COAP_LOG_DTLS_BASE",
	], start=0)

coap_proto_t = ctypes_enum_gen("coap_proto_t", [
		"COAP_PROTO_NONE",
		"COAP_PROTO_UDP",
		"COAP_PROTO_DTLS",
		"COAP_PROTO_TCP",
		"COAP_PROTO_TLS",
		"COAP_PROTO_WS",
		"COAP_PROTO_WSS",
		"COAP_PROTO_LAST"
		], start=0)

coap_resolve_type_t = ctypes_enum_gen("coap_resolve_type_t", [
		"COAP_RESOLVE_TYPE_LOCAL",
		"COAP_RESOLVE_TYPE_REMOTE"
		], start=0)

coap_uri_scheme_t = ctypes_enum_gen("coap_uri_scheme_t", [
		"COAP_URI_SCHEME_COAP",
		"COAP_URI_SCHEME_COAPS",
		"COAP_URI_SCHEME_COAP_TCP",
		"COAP_URI_SCHEME_COAPS_TCP",
		"COAP_URI_SCHEME_HTTP",
		"COAP_URI_SCHEME_HTTPS",
		"COAP_URI_SCHEME_COAP_WS",
		"COAP_URI_SCHEME_COAPS_WS",
		"COAP_URI_SCHEME_LAST",
		], start=0)

coap_response_t = ctypes_enum_gen("coap_response_t", [
		"COAP_RESPONSE_FAIL",
		"COAP_RESPONSE_OK",
		], start=0)

coap_nack_reason_t = ctypes_enum_gen("coap_nack_reason_t", [
	"COAP_NACK_TOO_MANY_RETRIES",
	"COAP_NACK_NOT_DELIVERABLE",
	"COAP_NACK_RST",
	"COAP_NACK_TLS_FAILED",
	"COAP_NACK_ICMP_ISSUE",
	"COAP_NACK_BAD_RESPONSE",
	"COAP_NACK_TLS_LAYER_FAILED",
	"COAP_NACK_WS_LAYER_FAILED",
	"COAP_NACK_WS_FAILED",
	], start=0)

class coap_event_t(ctypes_enum_gen):
	COAP_EVENT_DTLS_CLOSED		= 0x0000
	COAP_EVENT_DTLS_CONNECTED	= 0x01DE
	COAP_EVENT_DTLS_RENEGOTIATE	= 0x01DF
	COAP_EVENT_DTLS_ERROR		= 0x0200
	
	COAP_EVENT_TCP_CONNECTED	= 0x1001
	COAP_EVENT_TCP_CLOSED		= 0x1002
	COAP_EVENT_TCP_FAILED		= 0x1003
	
	COAP_EVENT_SESSION_CONNECTED	= 0x2001
	COAP_EVENT_SESSION_CLOSED		= 0x2002
	COAP_EVENT_SESSION_FAILED		= 0x2003
	
	COAP_EVENT_PARTIAL_BLOCK	= 0x3001
	COAP_EVENT_XMIT_BLOCK_FAIL	= 0x3002
	
	COAP_EVENT_SERVER_SESSION_NEW = 0x4001
	
	COAP_EVENT_SERVER_SESSION_DEL = 0x4002
	
	COAP_EVENT_BAD_PACKET			= 0x5001
	COAP_EVENT_MSG_RETRANSMITTED	= 0x5002
	
	COAP_EVENT_OSCORE_DECRYPTION_FAILURE	= 0x6001
	COAP_EVENT_OSCORE_NOT_ENABLED		 	= 0x6002
	COAP_EVENT_OSCORE_NO_PROTECTED_PAYLOAD	= 0x6003
	COAP_EVENT_OSCORE_NO_SECURITY			= 0x6004
	COAP_EVENT_OSCORE_INTERNAL_ERROR		= 0x6005
	COAP_EVENT_OSCORE_DECODE_ERROR			= 0x6006
	
	COAP_EVENT_WS_PACKET_SIZE	= 0x7001
	COAP_EVENT_WS_CONNECTED		= 0x7002
	COAP_EVENT_WS_CLOSED		= 0x7003
	
	COAP_EVENT_KEEPALIVE_FAILURE = 0x8001

def COAP_SIGNALING_CODE(N): return ((int((N)/100) << 5) | (N)%100)

class coap_pdu_signaling_proto_t(ctypes_enum_gen):
	COAP_SIGNALING_CSM     = COAP_SIGNALING_CODE(701)
	COAP_SIGNALING_PING    = COAP_SIGNALING_CODE(702)
	COAP_SIGNALING_PONG    = COAP_SIGNALING_CODE(703)
	COAP_SIGNALING_RELEASE = COAP_SIGNALING_CODE(704)
	COAP_SIGNALING_ABORT   = COAP_SIGNALING_CODE(705)

coap_log_t = ctypes_enum_gen("coap_log_t", [
	"COAP_LOG_EMERG",
	"COAP_LOG_ALERT",
	"COAP_LOG_CRIT",
	"COAP_LOG_ERR",
	"COAP_LOG_WARN",
	"COAP_LOG_NOTICE",
	"COAP_LOG_INFO",
	"COAP_LOG_DEBUG",
	"COAP_LOG_OSCORE",
	"COAP_LOG_DTLS_BASE",
	], start=0)

COAP_BLOCK_USE_LIBCOAP = 0x01
COAP_BLOCK_SINGLE_BODY = 0x02

COAP_OBSERVE_ESTABLISH = 0
COAP_OBSERVE_CANCEL    = 1

COAP_IO_WAIT    = 0
COAP_IO_NO_WAIT = ct.c_uint32(-1).value

class coap_request_t(ctypes_enum_gen):
	COAP_REQUEST_GET     = 1
	COAP_REQUEST_POST    = 2
	COAP_REQUEST_PUT     = 3
	COAP_REQUEST_DELETE  = 4
	COAP_REQUEST_FETCH   = 5
	COAP_REQUEST_PATCH   = 6
	COAP_REQUEST_IPATCH  = 7

COAP_OPTION_IF_MATCH       =  1
COAP_OPTION_URI_HOST       =  3
COAP_OPTION_ETAG           =  4
COAP_OPTION_IF_NONE_MATCH  =  5
COAP_OPTION_OBSERVE        =  6
COAP_OPTION_URI_PORT       =  7
COAP_OPTION_LOCATION_PATH  =  8
COAP_OPTION_URI_PATH       = 11
COAP_OPTION_CONTENT_FORMAT = 12
COAP_OPTION_CONTENT_TYPE   = COAP_OPTION_CONTENT_FORMAT
COAP_OPTION_MAXAGE         = 14
COAP_OPTION_URI_QUERY      = 15
COAP_OPTION_ACCEPT         = 17
COAP_OPTION_LOCATION_QUERY = 20
COAP_OPTION_PROXY_URI      = 35
COAP_OPTION_PROXY_SCHEME   = 39
COAP_OPTION_SIZE1          = 60

def COAP_RESPONSE_CODE(N): return (( int((N)/100) << 5) | (N)%100)

coap_pdu_type_t = ctypes_enum_gen("coap_pdu_type_t", [
	"COAP_MESSAGE_CON",
	"COAP_MESSAGE_NON",
	"COAP_MESSAGE_ACK",
	"COAP_MESSAGE_RST",
	], start=0)

class coap_pdu_code_t(ctypes_enum_gen):
	COAP_EMTPY_CODE = 0
	
	COAP_REQUEST_CODE_GET    = coap_request_t.COAP_REQUEST_GET
	COAP_REQUEST_CODE_POST   = coap_request_t.COAP_REQUEST_POST
	COAP_REQUEST_CODE_PUT    = coap_request_t.COAP_REQUEST_PUT
	COAP_REQUEST_CODE_DELETE = coap_request_t.COAP_REQUEST_DELETE
	COAP_REQUEST_CODE_FETCH  = coap_request_t.COAP_REQUEST_FETCH
	COAP_REQUEST_CODE_PATCH  = coap_request_t.COAP_REQUEST_PATCH
	COAP_REQUEST_CODE_IPATCH = coap_request_t.COAP_REQUEST_IPATCH
	
	COAP_RESPONSE_CODE_CREATED                    = COAP_RESPONSE_CODE(201)
	COAP_RESPONSE_CODE_DELETED                    = COAP_RESPONSE_CODE(202)
	COAP_RESPONSE_CODE_VALID                      = COAP_RESPONSE_CODE(203)
	COAP_RESPONSE_CODE_CHANGED                    = COAP_RESPONSE_CODE(204)
	COAP_RESPONSE_CODE_CONTENT                    = COAP_RESPONSE_CODE(205)
	COAP_RESPONSE_CODE_CONTINUE                   = COAP_RESPONSE_CODE(231)
	COAP_RESPONSE_CODE_BAD_REQUEST                = COAP_RESPONSE_CODE(400)
	COAP_RESPONSE_CODE_UNAUTHORIZED               = COAP_RESPONSE_CODE(401)
	COAP_RESPONSE_CODE_BAD_OPTION                 = COAP_RESPONSE_CODE(402)
	COAP_RESPONSE_CODE_FORBIDDEN                  = COAP_RESPONSE_CODE(403)
	COAP_RESPONSE_CODE_NOT_FOUND                  = COAP_RESPONSE_CODE(404)
	COAP_RESPONSE_CODE_NOT_ALLOWED                = COAP_RESPONSE_CODE(405)
	COAP_RESPONSE_CODE_NOT_ACCEPTABLE             = COAP_RESPONSE_CODE(406)
	COAP_RESPONSE_CODE_INCOMPLETE                 = COAP_RESPONSE_CODE(408)
	COAP_RESPONSE_CODE_CONFLICT                   = COAP_RESPONSE_CODE(409)
	COAP_RESPONSE_CODE_PRECONDITION_FAILED        = COAP_RESPONSE_CODE(412)
	COAP_RESPONSE_CODE_REQUEST_TOO_LARGE          = COAP_RESPONSE_CODE(413)
	COAP_RESPONSE_CODE_UNSUPPORTED_CONTENT_FORMAT = COAP_RESPONSE_CODE(415)
	COAP_RESPONSE_CODE_UNPROCESSABLE              = COAP_RESPONSE_CODE(422)
	COAP_RESPONSE_CODE_TOO_MANY_REQUESTS          = COAP_RESPONSE_CODE(429)
	COAP_RESPONSE_CODE_INTERNAL_ERROR             = COAP_RESPONSE_CODE(500)
	COAP_RESPONSE_CODE_NOT_IMPLEMENTED            = COAP_RESPONSE_CODE(501)
	COAP_RESPONSE_CODE_BAD_GATEWAY                = COAP_RESPONSE_CODE(502)
	COAP_RESPONSE_CODE_SERVICE_UNAVAILABLE        = COAP_RESPONSE_CODE(503)
	COAP_RESPONSE_CODE_GATEWAY_TIMEOUT            = COAP_RESPONSE_CODE(504)
	COAP_RESPONSE_CODE_PROXYING_NOT_SUPPORTED     = COAP_RESPONSE_CODE(505)
	COAP_RESPONSE_CODE_HOP_LIMIT_REACHED          = COAP_RESPONSE_CODE(508)

	COAP_SIGNALING_CODE_CSM                       = coap_pdu_signaling_proto_t.COAP_SIGNALING_CSM
	COAP_SIGNALING_CODE_PING                      = coap_pdu_signaling_proto_t.COAP_SIGNALING_PING
	COAP_SIGNALING_CODE_PONG                      = coap_pdu_signaling_proto_t.COAP_SIGNALING_PONG
	COAP_SIGNALING_CODE_RELEASE                   = coap_pdu_signaling_proto_t.COAP_SIGNALING_RELEASE
	COAP_SIGNALING_CODE_ABORT                     = coap_pdu_signaling_proto_t.COAP_SIGNALING_ABORT

COAP_RESOURCE_FLAGS_RELEASE_URI = 0x1
COAP_RESOURCE_FLAGS_NOTIFY_NON  = 0x0
COAP_RESOURCE_FLAGS_NOTIFY_CON  = 0x2
COAP_RESOURCE_FLAGS_NOTIFY_NON_ALWAYS  = 0x4
COAP_RESOURCE_FLAGS_HAS_MCAST_SUPPORT  = 0x8 
COAP_RESOURCE_FLAGS_LIB_DIS_MCAST_DELAYS = 0x10
COAP_RESOURCE_FLAGS_LIB_ENA_MCAST_SUPPRESS_2_05 = 0x20
COAP_RESOURCE_FLAGS_LIB_ENA_MCAST_SUPPRESS_2_XX = 0x40
COAP_RESOURCE_FLAGS_LIB_DIS_MCAST_SUPPRESS_4_XX = 0x80
COAP_RESOURCE_FLAGS_LIB_DIS_MCAST_SUPPRESS_5_XX = 0x100
COAP_RESOURCE_FLAGS_MCAST_LIST = (
   COAP_RESOURCE_FLAGS_HAS_MCAST_SUPPORT |
   COAP_RESOURCE_FLAGS_LIB_DIS_MCAST_DELAYS |
   COAP_RESOURCE_FLAGS_LIB_ENA_MCAST_SUPPRESS_2_05 |
   COAP_RESOURCE_FLAGS_LIB_ENA_MCAST_SUPPRESS_2_XX |
   COAP_RESOURCE_FLAGS_LIB_DIS_MCAST_SUPPRESS_4_XX |
   COAP_RESOURCE_FLAGS_LIB_DIS_MCAST_SUPPRESS_5_XX)
 
COAP_RESOURCE_FLAGS_FORCE_SINGLE_BODY = 0x200
COAP_RESOURCE_FLAGS_OSCORE_ONLY       = 0x400
COAP_RESOURCE_HANDLE_WELLKNOWN_CORE   = 0x800

COAP_SOCKET_EMPTY        = 0x0000
COAP_SOCKET_NOT_EMPTY    = 0x0001
COAP_SOCKET_BOUND        = 0x0002
COAP_SOCKET_CONNECTED    = 0x0004
COAP_SOCKET_WANT_READ    = 0x0010
COAP_SOCKET_WANT_WRITE   = 0x0020
COAP_SOCKET_WANT_ACCEPT  = 0x0040
COAP_SOCKET_WANT_CONNECT = 0x0080
COAP_SOCKET_CAN_READ     = 0x0100
COAP_SOCKET_CAN_WRITE    = 0x0200
COAP_SOCKET_CAN_ACCEPT   = 0x0400
COAP_SOCKET_CAN_CONNECT  = 0x0800
COAP_SOCKET_MULTICAST    = 0x1000

coap_tid_t = ct.c_int
coap_mid_t = ct.c_int
coap_opt_t = ct.c_uint8
coap_tick_t = ct.c_uint64
coap_option_num_t = ct.c_uint16
coap_fd_t = ct.c_int
coap_socket_flags_t = ct.c_uint16

COAP_INVALID_MID = -1
COAP_INVALID_TID = COAP_INVALID_MID

class LStructure(ct.Structure):
	def __str__(self):
		return "<{}: {{{}}}>".format(
			self.__class__.__name__,
			", ".join(["{}: {}".format(
					f[0],
					str(getattr(self, f[0]))
				)
				for f in self._fields_])
			)
	
	# Looks like number types get converted to type "int". We have to use this
	# workaround to access the actual ctype of a field.
	# https://stackoverflow.com/questions/71802792/why-does-ctypes-c-int-completely-change-its-behaviour-when-put-into-ctypes-struc
	def ctype(self, field):
		ftype=None
		for fname, ftype in self._fields_:
			if fname == field:
				t = ftype
				break
		return ftype.from_buffer(self, getattr(self.__class__, field).offset)
	
	@classmethod
	def set_fields(cls, fields):
		cls._fields_ = [ (name, typ) for typ, name in fields ]

class coap_address_t(ct.Structure):
	pass

class coap_context_t(ct.Structure):
	pass

class coap_optlist_t(ct.Structure):
	pass

class coap_pdu_t(ct.Structure):
	pass

class coap_resource_t(ct.Structure):
	pass

class coap_session_t(ct.Structure):
	pass

def c_uint8_p_to_str(uint8p, length):
	b = ct.string_at(uint8p, length)
	try:
		return b.decode()
	except:
		return b

c_uint8_p = ct.POINTER(ct.c_uint8)

class coap_addr_info_t(ct.Structure):
	pass
coap_addr_info_t._fields_ = [
		("next", ct.POINTER(coap_addr_info_t)),
		("scheme", ct.c_int),
		("proto", ct.c_int),
		("addr", coap_address_t),
		]

class coap_fixed_point_t(LStructure):
	_fields_ = [("integer_part", ct.c_uint16), ("fractional_part", ct.c_uint16)]


class coap_string_t(LStructure):
	_fields_ = [("length", ct.c_size_t), ("s", c_uint8_p)]
	
	def __init__(self, value=None):
		super().__init__()
		
		if value:
			if isinstance(value, str):
				b = value.encode()
			else:
				b = value
			
			self.s = bytes2uint8p(b)
			self.length = ct.c_size_t(len(b))
	
	def __str__(self):
		return str(c_uint8_p_to_str(self.s, self.length))

class coap_str_const_t(coap_string_t):
	pass

class coap_binary_t(coap_string_t):
	def __str__(self):
		return str([ "0x%02x" % (self.s[i]) for i in range(self.length)])

class coap_bin_const_t(coap_binary_t):
	pass

class coap_uri_t(LStructure):
	_fields_ = [
			("host", coap_str_const_t),
			("port", ct.c_uint16),
			("path", coap_str_const_t),
			("query", coap_str_const_t),
			("scheme", ct.c_int),
			]

class coap_dtls_spsk_info_t(LStructure):
	_fields_ = [
		("hint", coap_bin_const_t),
		("key", coap_bin_const_t),
		]

class coap_tls_version_t(LStructure):
	_fields_ = [
		("version", ct.c_uint64),
		("type", coap_tls_library_t.get_ctype()),
		("built_version", ct.c_uint64),
		]


# looks like ctypes does not support coap_response_t (enum) as return value
coap_response_handler_t = ct.CFUNCTYPE(ct.c_int, ct.POINTER(coap_session_t), ct.POINTER(coap_pdu_t), ct.POINTER(coap_pdu_t), coap_mid_t)
coap_release_large_data_t = ct.CFUNCTYPE(None, ct.POINTER(coap_session_t), ct.py_object)
coap_resource_release_userdata_handler_t = ct.CFUNCTYPE(None, ct.py_object)

coap_method_handler_t = ct.CFUNCTYPE(None, ct.POINTER(coap_resource_t), ct.POINTER(coap_session_t),
	ct.POINTER(coap_pdu_t), ct.POINTER(coap_string_t), ct.POINTER(coap_pdu_t));
coap_nack_handler_t = ct.CFUNCTYPE(None, ct.POINTER(coap_session_t), ct.POINTER(coap_pdu_t), coap_nack_reason_t.get_ctype(), coap_mid_t)
coap_ping_handler_t = ct.CFUNCTYPE(None, ct.POINTER(coap_session_t), ct.POINTER(coap_pdu_t), coap_mid_t)
coap_pong_handler_t = ct.CFUNCTYPE(None, ct.POINTER(coap_session_t), ct.POINTER(coap_pdu_t), coap_mid_t)
# get_ctype() to avoid "TypeError: cannot build parameter" message
coap_event_handler_t = ct.CFUNCTYPE(None, ct.POINTER(coap_session_t), coap_event_t.get_ctype())

# actually returns coap_dtls_spsk_info_t
coap_dtls_psk_sni_callback_t = ct.CFUNCTYPE(ct.c_void_p, ct.c_char_p, ct.POINTER(coap_session_t), ct.py_object)
# actually returns coap_bin_const_t
coap_dtls_id_callback_t = ct.CFUNCTYPE(ct.c_void_p, ct.POINTER(coap_bin_const_t), ct.POINTER(coap_session_t), ct.py_object)

COAP_DTLS_SPSK_SETUP_VERSION = 1

class coap_dtls_spsk_t(LStructure):
	_fields_ = [
		("version", ct.c_uint8),
		("reserved", ct.c_uint8 * 7),
		("validate_id_call_back", coap_dtls_id_callback_t),
		("id_call_back_arg", ct.py_object),
		("validate_sni_call_back", coap_dtls_psk_sni_callback_t),
		("sni_call_back_arg", ct.py_object),
		("psk_info", coap_dtls_spsk_info_t),
		]

class coap_dtls_cpsk_info_t(LStructure):
	_fields_ = [
		("hint", coap_bin_const_t),
		("key", coap_bin_const_t),
		]

# actually returns coap_dtls_cpsk_info_t
coap_dtls_ih_callback_t = ct.CFUNCTYPE(ct.c_void_p, ct.POINTER(coap_str_const_t), ct.POINTER(coap_session_t), ct.py_object)

COAP_DTLS_CPSK_SETUP_VERSION = 1

class coap_dtls_cpsk_t(LStructure):
	_fields_ = [
		("version", ct.c_uint8),
		("reserved", ct.c_uint8 * 7),
		("validate_ih_call_back", coap_dtls_ih_callback_t),
		("ih_call_back_arg", ct.py_object),
		("client_sni", ct.c_char_p),
		("psk_info", coap_dtls_cpsk_info_t),
		]

# we handle this as opaque type for now due to preprocessor conditions
class coap_socket_t(LStructure):
	pass
# #if defined(WITH_LWIP)
#   struct udp_pcb *pcb;
# #elif defined(WITH_CONTIKI)
#   struct uip_udp_conn *udp_conn;
#   coap_context_t *context;
# #else
#   coap_fd_t fd;
# #endif /* WITH_LWIP */
# #if defined(RIOT_VERSION)
#   gnrc_pktsnip_t *pkt; 
# #endif /* RIOT_VERSION */
#   coap_socket_flags_t flags; 
#   coap_session_t *session; 
# #if COAP_SERVER_SUPPORT
#   coap_endpoint_t *endpoint; 
# #endif /* COAP_SERVER_SUPPORT */
# #if COAP_CLIENT_SUPPORT
#   coap_address_t mcast_addr; 
# #endif /* COAP_CLIENT_SUPPORT */
#   coap_layer_func_t lfunc[COAP_LAYER_LAST];

class coap_endpoint_t(LStructure):
	pass
coap_endpoint_t.set_fields([
		(ct.POINTER(coap_endpoint_t), "next"),
		(ct.POINTER(coap_context_t), "context"),
		(coap_proto_t.get_ctype(), "proto"),
		(ct.c_uint16, "default_mtu"),
		(coap_socket_t, "sock"),
		(coap_address_t, "bind_addr"),
		(ct.POINTER(coap_session_t), "sessions"),
		])

class coap_socket_t(LStructure):
	_fields_ = [
		("fd", coap_fd_t),
		("flags", coap_socket_flags_t),
		("session", ct.POINTER(coap_session_t)),
		("endpoint", ct.POINTER(coap_endpoint_t)),
		]


COAP_OPT_FILTER_SHORT = 6
COAP_OPT_FILTER_LONG  = 2

class coap_opt_filter_t(LStructure):
	_fields_ = [
		("mask", ct.c_uint16),
		("long_opts", ct.c_uint16 * COAP_OPT_FILTER_LONG),
		("short_opts", ct.c_uint8 * COAP_OPT_FILTER_SHORT),
		]

def bytes2uint8p(b, cast=c_uint8_p):
	if b is None:
		return None
	return ct.cast(ct.create_string_buffer(b), cast)

library_functions = [
	{ "name": "coap_startup", "restype": None },
	{ "name": "coap_cleanup", "restype": None },
	{ "name": "coap_package_version", "restype": ct.c_char_p },
	{ "name": "coap_string_tls_support", "restype": ct.c_char_p, "args": [ct.c_char_p, ct.c_size_t] },
	{ "name": "coap_string_tls_version", "restype": ct.c_char_p, "args": [ct.c_char_p, ct.c_size_t] },
	{ "name": "coap_get_tls_library_version", "restype": ct.POINTER(coap_tls_version_t) },
	{ "name": "coap_set_log_level", "args": [coap_log_t], "restype": None },
	{ "name": "coap_split_uri", "args": [ct.POINTER(ct.c_uint8), ct.c_size_t, ct.POINTER(coap_uri_t)] },
	{ "name": "coap_split_path", "args": [ct.c_char_p, ct.c_size_t, ct.c_char_p, ct.POINTER(ct.c_size_t)] },
	{ "name": "coap_new_context", "args": [ct.POINTER(coap_address_t)], "restype": ct.POINTER(coap_context_t) },
	{ "name": "coap_new_client_session", "args": [ct.POINTER(coap_context_t), ct.POINTER(coap_address_t), ct.POINTER(coap_address_t), coap_proto_t], "restype": ct.POINTER(coap_session_t) },
	{ "name": "coap_session_release", "args": [ct.POINTER(coap_session_t)], "restype": None },
	{ "name": "coap_resolve_address_info", "args": [
			ct.POINTER(coap_str_const_t),
			ct.c_uint16,
			ct.c_uint16,
			ct.c_uint16,
			ct.c_uint16,
			ct.c_int,
			ct.c_int,
			coap_resolve_type_t,
			],
		"restype": ct.POINTER(coap_addr_info_t)
		},
	{ "name": "coap_is_bcast", "args": [ct.POINTER(coap_address_t)] },
	{ "name": "coap_is_mcast", "args": [ct.POINTER(coap_address_t)] },
	{ "name": "coap_is_af_unix", "args": [ct.POINTER(coap_address_t)] },
	{ "name": "coap_free_address_info", "args": [ct.POINTER(coap_addr_info_t)], "restype": None },
	{ "name": "coap_pdu_init", "args": [ct.c_uint8, ct.c_uint8, ct.c_uint16, ct.c_size_t], "restype": ct.POINTER(coap_pdu_t) },
	{ "name": "coap_new_message_id", "args": [ct.POINTER(coap_session_t)], "restype": ct.c_uint16 },
	{ "name": "coap_session_max_pdu_size", "args": [ct.POINTER(coap_session_t)], "restype": ct.c_size_t },
	{ "name": "coap_send", "args": [ct.POINTER(coap_session_t), ct.POINTER(coap_pdu_t)], "restype": coap_mid_t, "res_error": COAP_INVALID_MID },
	
	{ "name": "coap_session_get_default_leisure", "args": [ct.POINTER(coap_session_t)], "restype": coap_fixed_point_t },
	{ "name": "coap_session_set_app_data", "args": { ct.POINTER(coap_session_t): "session", ct.py_object: "data"}, "restype": None },
	{ "name": "coap_session_get_app_data", "args": { ct.POINTER(coap_session_t): "session" }, "restype": ct.py_object },
	
	{ "name": "coap_register_request_handler", "args": {ct.POINTER(coap_resource_t): "resource", coap_request_t: "method", coap_method_handler_t: "handler"}, "restype": None },
	{ "name": "coap_register_response_handler", "args": {ct.POINTER(coap_context_t): "context", coap_response_handler_t: "handler"}, "restype": None },
	{ "name": "coap_register_nack_handler", "args": {ct.POINTER(coap_context_t): "context", coap_nack_handler_t: "handler"}, "restype": None },
	{ "name": "coap_register_ping_handler", "args": {ct.POINTER(coap_context_t): "context", coap_ping_handler_t: "handler"}, "restype": None },
	{ "name": "coap_register_pong_handler", "args": {ct.POINTER(coap_context_t): "context", coap_pong_handler_t: "handler"}, "restype": None },
	{ "name": "coap_register_event_handler", "args": {ct.POINTER(coap_context_t): "context", coap_event_handler_t: "handler"}, "restype": None },
	
	{ "name": "coap_register_handler", "args": { "resource": ct.POINTER(coap_resource_t), "method": ct.c_ubyte, "handler": coap_method_handler_t}, "restype": None},
	
	{ "name": "coap_context_set_block_mode", "args": { ct.POINTER(coap_context_t): "context", ct.c_uint8: "block_mode"}, "restype": None },
	{ "name": "coap_add_data_large_request", "args": [
			ct.POINTER(coap_session_t),
			ct.POINTER(coap_pdu_t),
			ct.c_size_t,
			ct.POINTER(ct.c_uint8),
			coap_release_large_data_t,
			ct.py_object,
			], "expect": 1},
	{ "name": "coap_add_data_large_response", "args": [
			ct.POINTER(coap_resource_t),
			ct.POINTER(coap_session_t),
			ct.POINTER(coap_pdu_t),
			ct.POINTER(coap_pdu_t),
			ct.POINTER(coap_string_t),
			ct.c_uint16,
			ct.c_int,
			ct.c_uint64,
			ct.c_size_t,
			ct.POINTER(ct.c_uint8),
			coap_release_large_data_t,
			ct.py_object,
			], "expect": 1},
	{ "name": "coap_get_data_large", "args": {
		"pdu": ct.POINTER(coap_pdu_t),
		"length": ct.POINTER(ct.c_size_t),
		"_data": ct.POINTER(ct.POINTER(ct.c_uint8)),
		"offset": ct.POINTER(ct.c_size_t),
		"total": ct.POINTER(ct.c_size_t),
		}, "expect": 1},
	
	{ "name": "coap_pdu_get_type", "args": [ct.POINTER(coap_pdu_t)], "restype": coap_pdu_type_t},
	{ "name": "coap_pdu_get_code", "args": [ct.POINTER(coap_pdu_t)], "restype": coap_pdu_code_t},
	{ "name": "coap_pdu_get_mid", "args": [ct.POINTER(coap_pdu_t)], "restype": coap_mid_t},
	{ "name": "coap_pdu_get_token", "args": [ct.POINTER(coap_pdu_t)], "restype": coap_bin_const_t},
	{ "name": "coap_pdu_duplicate", "args": {
			ct.POINTER(coap_pdu_t): "old_pdu",
			ct.POINTER(coap_session_t): "session",
			ct.c_size_t: "token_length",
			ct.POINTER(ct.c_uint8): "token",
			ct.POINTER(coap_opt_filter_t): "drop_options",
			},
		"restype": ct.POINTER(coap_pdu_t), },
	
	{ "name": "coap_new_optlist", "args": [ct.c_uint16, ct.c_size_t, ct.POINTER(ct.c_uint8)], "restype": ct.POINTER(coap_optlist_t) },
	{ "name": "coap_add_option", "args": [ct.POINTER(coap_pdu_t), ct.c_uint16, ct.c_size_t, ct.c_uint8], "restype": ct.c_size_t, "res_error": 0 },
	{ "name": "coap_insert_optlist", "args": [ct.POINTER(ct.POINTER(coap_optlist_t)), ct.POINTER(coap_optlist_t)], "expect": 1 },
	{ "name": "coap_delete_optlist", "args": [ct.POINTER(coap_optlist_t)], "restype": None },
	{ "name": "coap_opt_length", "args": [ct.POINTER(coap_opt_t)], "restype": ct.c_uint32 },
	{ "name": "coap_opt_value", "args": [ct.POINTER(coap_opt_t)], "restype": ct.POINTER(ct.c_uint8) },
	{ "name": "coap_opt_size", "args": [ct.POINTER(coap_opt_t)], "restype": ct.c_size_t },
	{ "name": "coap_encode_var_safe", "args": [ct.POINTER(ct.c_uint8), ct.c_size_t, ct.c_uint], "restype": ct.c_uint, "res_error": 0},
	{ "name": "coap_uri_into_options", "args": [
			ct.POINTER(coap_uri_t),
			ct.POINTER(coap_address_t),
			ct.POINTER(ct.POINTER(coap_optlist_t)),
			ct.c_int,
			ct.POINTER(ct.c_uint8),
			ct.c_size_t,
			]},
	{ "name": "coap_add_optlist_pdu", "args": [ct.POINTER(coap_pdu_t), ct.POINTER(ct.POINTER(coap_optlist_t))], "expect": 1 },
	{ "name": "coap_uri_into_optlist", "args": [
			ct.POINTER(coap_uri_t),
			ct.POINTER(coap_address_t),
			ct.POINTER(ct.POINTER(coap_optlist_t)),
			ct.c_int,
			]},
	{ "name": "coap_path_into_optlist", "args": [
			ct.POINTER(ct.c_uint8),
			ct.c_size_t,
			coap_option_num_t,
			ct.POINTER(ct.POINTER(coap_optlist_t)),
			]},
	{ "name": "coap_query_into_optlist", "args": [
			ct.POINTER(ct.c_uint8),
			ct.c_size_t,
			coap_option_num_t,
			ct.POINTER(ct.POINTER(coap_optlist_t)),
			]},
	
	
	{ "name": "coap_session_new_token", "args": [ct.POINTER(coap_session_t), ct.POINTER(ct.c_size_t), ct.POINTER(ct.c_uint8)], "restype": None },
	{ "name": "coap_add_token", "args": [ct.POINTER(coap_pdu_t), ct.c_size_t, ct.POINTER(ct.c_uint8)], "res_error": 0 },
	
	{ "name": "coap_address_init", "args": [ct.POINTER(coap_address_t)], "restype": None },
	{ "name": "coap_address_set_unix_domain", "args": [ct.POINTER(coap_address_t), ct.POINTER(ct.c_uint8), ct.c_size_t], "expect": 1 },
	
	{ "name": "coap_context_set_psk2", "args": [ct.POINTER(coap_context_t), ct.POINTER(coap_dtls_spsk_t)] },
	{ "name": "coap_new_client_session_psk2", "args": {
		"context": ct.POINTER(coap_context_t),
		"local_if": ct.POINTER(coap_address_t),
		"server": ct.POINTER(coap_address_t),
		"proto": coap_proto_t,
		"setup_data": ct.POINTER(coap_dtls_cpsk_t),
		},
		"restype": ct.POINTER(coap_session_t) },
	
	{ "name": "coap_io_process", "args": [ct.POINTER(coap_context_t), ct.c_uint32], "llapi_check": False },
	{ "name": "coap_io_prepare_epoll", "args": [ct.POINTER(coap_context_t), coap_tick_t], "restype": ct.c_uint },
	{ "name": "coap_context_get_coap_fd", "args": [ct.POINTER(coap_context_t)] },
	{ "name": "coap_ticks", "args": [ct.POINTER(coap_tick_t)], "restype": None },
	# TODO can we use fd_set from python?
	# { "name": "coap_io_process_with_fds", "args": {
	# 	ct.POINTER(coap_context_t): "ctx",
	# 	ct.c_uint32: "timeout_ms",
	# 	ct.c_int: "nfds",
	# 	fd_set *  	readfds,
	# 	fd_set *  	writefds,
	# 	fd_set *  	exceptfds 
	# 	}
	{ "name": "coap_io_prepare_io", "args": {
			ct.POINTER(coap_context_t): "ctx",
			ct.POINTER(ct.POINTER(coap_socket_t)): "sockets",
			ct.c_uint: "max_sockets",
			ct.POINTER(ct.c_uint): "num_sockets",
			coap_tick_t: "now",
			},
		"restype": ct.c_uint },
	{ "name": "coap_io_do_io", "args": {ct.POINTER(coap_context_t): "ctx", coap_tick_t: "now"}, "restype": None },
	
	{ "name": "coap_new_endpoint", "args": [ct.POINTER(coap_context_t), ct.POINTER(coap_address_t), coap_proto_t], "restype": ct.POINTER(coap_endpoint_t) },
	
	{ "name": "coap_resource_init", "args": {"uri_path": ct.POINTER(coap_str_const_t), "flags": ct.c_int}, "restype": ct.POINTER(coap_resource_t) },
	{ "name": "coap_resource_unknown_init", "args": {"put_handler": coap_method_handler_t}, "restype": ct.POINTER(coap_resource_t) },
	{ "name": "coap_resource_unknown_init2", "args": {"put_handler": coap_method_handler_t, "flags": ct.c_int}, "restype": ct.POINTER(coap_resource_t) },
	{ "name": "coap_resource_proxy_uri_init", "args": {"proxy_handler": coap_method_handler_t, "host_name_count": ct.c_size_t, "host_name_list": ct.POINTER(ct.c_char_p)}, "restype": ct.POINTER(coap_resource_t) },
	{ "name": "coap_resource_proxy_uri_init2", "args": {"proxy_handler": coap_method_handler_t, "host_name_count": ct.c_size_t, "host_name_list": ct.POINTER(ct.c_char_p), "flags": ct.c_int}, "restype": ct.POINTER(coap_resource_t) },
	{ "name": "coap_add_resource", "args": {"context": ct.POINTER(coap_context_t), "resource": ct.POINTER(coap_resource_t)}, "restype": None },
	{ "name": "coap_delete_resource", "args": {"context": ct.POINTER(coap_context_t), "resource": ct.POINTER(coap_resource_t)} },
	{ "name": "coap_resource_set_mode", "args": {"resource": ct.POINTER(coap_resource_t), "mode": ct.c_int}, "restype": None },
	{ "name": "coap_resource_set_userdata", "args": {"resource": ct.POINTER(coap_resource_t), "data": ct.py_object}, "restype": None },
	{ "name": "coap_resource_get_userdata", "args": {"resource": ct.POINTER(coap_resource_t)}, "restype": ct.py_object },
	{ "name": "coap_resource_release_userdata_handler", "args": {"context": ct.POINTER(coap_context_t), "callback": coap_resource_release_userdata_handler_t}, "restype": None },
	{ "name": "coap_resource_get_uri_path", "args": {"resource": ct.POINTER(coap_resource_t)}, "restype": ct.POINTER(coap_str_const_t) },
	
	{ "name": "coap_resource_set_get_observable", "args": {ct.POINTER(coap_resource_t): "resource", ct.c_int: "mode"}, "restype": None },
	{ "name": "coap_resource_notify_observers", "args": {ct.POINTER(coap_resource_t): "resource", ct.POINTER(coap_string_t): "query"} },
	{ "name": "coap_cancel_observe", "args": {ct.POINTER(coap_session_t): "session", ct.POINTER(coap_binary_t): "token", coap_pdu_type_t: "message_type"}, "res_error": 0 },
	
	{ "name": "coap_pdu_set_code", "args": {ct.POINTER(coap_pdu_t): "pdu", coap_pdu_code_t: "code"}, "restype": None },
	
	{ "name": "coap_make_str_const", "args": {ct.c_char_p: "string"}, "restype": ct.POINTER(coap_str_const_t) },
	{ "name": "coap_get_uri_path", "args": { ct.POINTER(coap_pdu_t): "pdu" }, "restype": ct.POINTER(coap_string_t)},
	
	{ "name": "coap_join_mcast_group_intf", "args": {ct.POINTER(coap_context_t): "context", ct.c_char_p: "groupname", ct.c_char_p: "ifname"} },
	{ "name": "coap_session_get_ifindex", "args": {ct.POINTER(coap_session_t): "session"}, "res_error": -1 },
	
	{ "name": "coap_session_get_addr_local", "args": {ct.POINTER(coap_session_t): "session"}, "restype": ct.POINTER(coap_address_t) },
	{ "name": "coap_session_get_addr_mcast", "args": {ct.POINTER(coap_session_t): "session"}, "restype": ct.POINTER(coap_address_t) },
	{ "name": "coap_session_get_addr_remote", "args": {ct.POINTER(coap_session_t): "session"}, "restype": ct.POINTER(coap_address_t) },
	
	{ "name": "coap_print_addr", "args": {ct.POINTER(coap_address_t): "address", ct.POINTER(ct.c_ubyte): "buffer", ct.c_size_t: "length" }, "restype": ct.c_size_t },
	{ "name": "coap_print_ip_addr", "args": {ct.POINTER(coap_address_t): "address", ct.POINTER(ct.c_ubyte): "buffer", ct.c_size_t: "length" }, "restype": ct.c_char_p },
	]

if sys.version_info < (3,):
	def to_bytes(x):
		return x
else:
	def to_bytes(s):
		if isinstance(s, str):
			return s.encode()
		else:
			return s

def setup_fct(fdict):
	ct_fct = getattr(libcoap, fdict["name"])
	
	if "args" in fdict:
		if isinstance(fdict["args"], list):
			args = fdict["args"]
		else:
			args = []
			for key, value in fdict["args"].items():
				if isinstance(key, str):
					args.append(value)
				else:
					args.append(key)
	else:
		args = None
	
	ct_fct.argtypes = args
	
	ct_fct.restype = fdict.get("restype", ct.c_int)
	# workaround if the function returns NULL
	if ct_fct.restype == ct.py_object:
		ct_fct.restype = ct.c_void_p
	
	fdict["ct_fct"] = ct_fct

def ct_call(fdict, *nargs, **kwargs):
	global initialized
	if not initialized:
		initialized = True
		coap_startup()
	
	if "ct_fct" not in fdict:
		setup_fct(fdict)
	
	ct_fct = fdict["ct_fct"]
	
	newargs = list()
	for i in range(len(nargs)):
		newargs += (to_bytes(nargs[i]), )
	
	if "args" in fdict:
		for i in range(len(nargs), len(fdict["args"])):
			newargs += (None, )
		
		if isinstance(fdict["args"], dict) and kwargs:
			for key, value in kwargs.items():
				i = 0
				for argtype, argname in fdict["args"].items():
					if argname == key:
						newargs[i] = value
						break
					i += 1
	
	res = ct_fct(*newargs)
	if fdict.get("restype", ct.c_int) == ct.py_object:
		if res:
			res = ct.cast(res, ct.py_object).value
		else:
			res = None
	
	if verbosity > 1:
		print(fdict["name"], newargs, "=", res)
	
	if kwargs.get("llapi_check", True):
		if fdict.get("expect", False):
			if res != fdict["expect"]:
				if fdict.get("restype", ct.c_int) in [ct.c_long, ct.c_int] and res < 0:
					raise OSError(-res, fdict["name"]+str(newargs)+" failed with: "+os.strerror(-res)+" ("+str(-res)+")")
				else:
					raise OSError(res, fdict["name"]+str(newargs)+" failed with: "+str(res)+" (!= "+str(fdict["expect"])+")")
		elif fdict.get("res_error", False):
			if res == fdict["res_error"]:
				raise OSError(res, fdict["name"]+str(newargs)+" failed with: "+str(res)+" (== "+str(fdict["res_error"])+")")
		elif fdict.get("restype", ct.c_int) in [ct.c_long, ct.c_int] and res < 0:
			raise OSError(-res, fdict["name"]+str(newargs)+" failed with: "+os.strerror(-res)+" ("+str(-res)+")")
		elif isinstance(res, ct._Pointer) and not res:
			raise NullPointer(fdict["name"]+str(newargs)+" returned NULL pointer")
	
	return res

ssl_libs = [None, "openssl", "gnutls"]
tags = [".so.3", ".so", ".dll"]
versions = [None, "3"]

libnames = []
for ssl_lib in ssl_libs:
	for tag in tags:
		for version in versions:
			name = "libcoap"
			if version:
				name += "-"+version
			if ssl_lib:
				name += "-"+ssl_lib
			if tag:
				name += tag
			
			libnames.append(name)

if os.environ.get("LIBCOAPY_LIB", None):
	libnames.insert(0, os.environ.get("LIBCOAPY_LIB"))

libcoap = None
for libname in libnames:
	try:
		libcoap = ct.CDLL(libname)
	except:
		continue
	else:
		break

if libcoap is None:
	raise Exception("could not find libcoap library")

#libc = ct.CDLL('libc.so.6')
#libc.free.args = [ct.c_void_p]

resolve_immediately = False

for fdict in library_functions:
	if getattr(libcoap, fdict["name"], None) is None:
		if verbosity > 0:
			print(f["name"], "not found in library")
		continue
	
	if resolve_immediately:
		setup_fct(fdict)
	
	# we need the function generator to avoid issues due to late binding
	def function_generator(fdict=fdict):
		def dyn_fct(*nargs, **kwargs):
			return ct_call(fdict, *nargs, **kwargs)
		return dyn_fct
	
	if hasattr(sys.modules[__name__], fdict["name"]):
		print("duplicate function", fdict["name"], file=sys.stderr)
	
	setattr(sys.modules[__name__], fdict["name"], function_generator(fdict))

if __name__ == "__main__":
	coap_startup()
	
	if len(sys.argv) < 2:
		uri_str = b"coap://localhost/.well-known/core"
	else:
		uri_str = sys.argv[1].encode()
	uri_t = coap_uri_t()
	
	coap_split_uri(ct.cast(ct.c_char_p(uri_str), c_uint8_p), len(uri_str), ct.byref(uri_t))
	
	ctx = coap_new_context(None);
	
	coap_context_set_block_mode(ctx, COAP_BLOCK_USE_LIBCOAP | COAP_BLOCK_SINGLE_BODY);
	
	import socket
	addr_info = coap_resolve_address_info(ct.byref(uri_t.host), uri_t.port, uri_t.port, uri_t.port, uri_t.port,
		socket.AF_UNSPEC, 1 << uri_t.scheme, coap_resolve_type_t.COAP_RESOLVE_TYPE_REMOTE);
	if not addr_info:
		print("cannot resolve", uri_str)
		sys.exit(1)
	
	dst = addr_info.contents.addr
	is_mcast = coap_is_mcast(ct.byref(dst));
	
	session = coap_new_client_session(ctx, None, ct.byref(dst), coap_proto_t.COAP_PROTO_UDP)
	
	have_response = 0
	def my_resp_handler(session, pdu_sent, pdu_recv, mid):
		global have_response
		have_response = 1;
		
		code = coap_pdu_get_code(pdu_recv)
		if code != coap_pdu_code_t.COAP_RESPONSE_CODE_CONTENT:
			print("unexpected result", coap_pdu_code_t(code).name)
			return coap_response_t.COAP_RESPONSE_OK;
		
		size = ct.c_size_t()
		databuf = ct.POINTER(ct.c_uint8)()
		offset = ct.c_size_t()
		total = ct.c_size_t()
		if coap_get_data_large(pdu_recv, ct.byref(size), ct.byref(databuf), ct.byref(offset), ct.byref(total)):
			import string
			
			print(size.value, end=" - ")
			for i in range(size.value):
				print("%02x" % databuf[i], end=" ")
			print(" - ", end="")
			for i in range(size.value):
				if chr(databuf[i]) in string.printable:
					print("%c" % databuf[i], end="")
				else:
					print(" ", end="")
			print()
		else:
			print("no data")
		
		return coap_response_t.COAP_RESPONSE_OK
	
	# we need to prevent this obj from being garbage collected or python/ctypes will segfault
	handler_obj = coap_response_handler_t(my_resp_handler)
	coap_register_response_handler(ctx, handler_obj)
	
	pdu = coap_pdu_init(COAP_MESSAGE_CON,
			coap_pdu_code_t.COAP_REQUEST_CODE_GET,
			coap_new_message_id(session),
			coap_session_max_pdu_size(session));
	
	optlist = ct.POINTER(coap_optlist_t)()
	scratch_t = ct.c_uint8 * 100
	scratch = scratch_t()
	coap_uri_into_options(ct.byref(uri_t), ct.byref(dst), ct.byref(optlist), 1, scratch, ct.sizeof(scratch))
	
	coap_add_optlist_pdu(pdu, ct.byref(optlist))
	
	mid = coap_send(session, pdu)
	if mid == COAP_INVALID_MID:
		print("coap_send() failed")
		sys.exit(1)
	
	wait_ms = (coap_session_get_default_leisure(session).integer_part + 1) * 1000;
	while have_response == 0 or is_mcast:
		res = coap_io_process(ctx, 1000);
		if res >= 0:
			if wait_ms > 0:
				if res >= wait_ms:
					print("timeout\n")
					break;
				else:
					wait_ms -= res
	
	coap_free_address_info(addr_info)
	
	coap_cleanup()
