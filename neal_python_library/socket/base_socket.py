import struct
import socket
from configobj import ConfigObj

from socket import error as socket_error

from ttcommon.dataaccess.cfg_const import CfgCommonSection, CfgFields
from ttcommon.utils.socket.socket_const import SocketConst

class BaseSocket:
    def __init__(self, cfg: ConfigObj):
        self._name = self.__class__.__name__
        self._cfg = cfg
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('Socket Created')

        socket_cfg = self._cfg[CfgCommonSection.SOCKET]
        self._socket_host = socket_cfg[CfgFields.SOCKET_HOST]
        self._socket_port = int(socket_cfg[CfgFields.SOCKET_PORT])

    def __del__(self):
        self._socket.close()
        print('Socket Closed')

    # ==================== send msg ==================== 
    @staticmethod
    def send_msg(socket: socket.socket, msg: bytes):
        msg_with_length_prefix = struct.pack(SocketConst.MSG_LENGTH_FORMAT_STRING, len(msg)) + msg

        try:
            socket.sendall(msg_with_length_prefix)
        except socket_error as e:
            print('Send Failed: error({})'.format(e))

    # ==================== receive msg ====================
    @staticmethod
    def _recv_n_bytes(socket: socket.socket, n):
        data = bytearray()
        
        while len(data) < n:
            packet = socket.recv(n - len(data))
            if not packet:
                return None
            data.extend(packet)

        return data
    
    @staticmethod
    def recv_msg(socket: socket.socket):
        msg_length_format_string = SocketConst.MSG_LENGTH_FORMAT_STRING
        msg_length_size = struct.calcsize(msg_length_format_string)
        msg_length_bytes = BaseSocket._recv_n_bytes(socket, msg_length_size)
        
        if not msg_length_bytes:
            return None
        
        msg_length_int = struct.unpack(msg_length_format_string, msg_length_bytes)[0]
        msg = BaseSocket._recv_n_bytes(socket, msg_length_int)

        return msg
