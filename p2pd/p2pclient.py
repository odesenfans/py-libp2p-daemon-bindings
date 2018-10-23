import socket
import sys

import base58

import multiaddr

from p2pd.config import (
    control_path,
    listen_path,
)
from p2pd.constants import (
    BUFFER_SIZE,
)
from p2pd.serialization import (
    PBReadWriter,
)

import p2pd.pb.p2pd_pb2 as p2pd_pb


class Multiaddr(multiaddr.Multiaddr):
    """Currently use `multiaddr.Multiaddr` as the backend.
    """

    def __init__(self, *, bytes_addr=None, string_addr=None):
        # e.g. maddr_bytes = b'\x04\x7f\x00\x00\x01\x06\xc2\xc9'
        if bytes_addr is not None:
            maddr_hex = bytes_addr.hex()  # '047f00000106c2c9'
            bytes_addr = maddr_hex.encode()
        super().__init__(bytes_addr=bytes_addr, string_addr=string_addr)

    def to_bytes(self):
        strange_bytes = super().to_bytes()  # b'047f00000106c2c9'
        maddr_hex = str(strange_bytes)[2:-1]  # '047f00000106c2c9'
        return bytes.fromhex(maddr_hex)

    def to_string(self):
        return multiaddr.codec.bytes_to_string(self._bytes)


class PeerID:
    _bytes = None

    def __init__(self, peer_id_bytes):
        self._bytes = peer_id_bytes

    def __repr__(self):
        return "<PeerID {}>".format(self.to_string()[2:10])

    def to_bytes(self):
        return self._bytes

    def to_string(self):
        return base58.b58encode(self._bytes).decode()

    @classmethod
    def from_string(cls, peer_id_string):
        peer_id_bytes = base58.b58decode(peer_id_string)
        pid = PeerID(peer_id_bytes)
        return pid


class ControlFailure(Exception):
    pass


def raise_if_failed(response):
    if response.type == p2pd_pb.Response.ERROR:
        raise ControlFailure(
            "connect failed. msg={}".format(
                response.error.msg,
            )
        )


class Client:
    control_path = None
    listen_path = None
    listener = None

    mutex_handlers = None
    handlers = None

    def __init__(self, control_path, listen_path):
        self.control_path = control_path
        self.listen_path = listen_path
        # TODO: handlers
        # TODO: listen sock

    def _new_control_conn(self):
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        # TODO: handle `socket.error`?
        s.connect(self.control_path)
        return s

    def identify(self):
        s = self._new_control_conn()
        rw = PBReadWriter(s)
        req = p2pd_pb.Request(type=p2pd_pb.Request.IDENTIFY)
        rw.write(req)

        resp = p2pd_pb.Response()
        rw.read(resp)
        raise_if_failed(resp)
        peer_id_bytes = resp.identify.id
        maddrs_bytes = resp.identify.addrs

        # TODO: PeerID, MultiAddr
        maddrs = []
        for maddr_bytes in maddrs_bytes:
            # addr is
            # maddr_str = str(maddr)[2:-1]
            # maddr_bytes_m = bytes.fromhex(maddr_str)
            maddr = Multiaddr(bytes_addr=maddr_bytes)
            assert maddr.to_bytes() == maddr_bytes
            maddrs.append(maddr)
        peer_id = PeerID(peer_id_bytes)

        s.close()

        return peer_id, maddrs

    def connect(self, peer_id, maddrs):
        s = self._new_control_conn()
        rwtor = PBReadWriter(s)
        maddrs_bytes = [i.to_bytes() for i in maddrs]
        connect_req = p2pd_pb.ConnectRequest(
            peer=peer_id.to_bytes(),
            addrs=maddrs_bytes,
        )
        req = p2pd_pb.Request(
            type=p2pd_pb.Request.CONNECT,
            connect=connect_req,
        )
        rwtor.write(req)
        resp = p2pd_pb.Response()
        rwtor.read(resp)
        raise_if_failed(resp)

        s.close()


def main():
    c = Client(control_path, listen_path)
    peer_id, maddrs = c.identify()
    print(peer_id, maddrs)
    maddrs = [Multiaddr(string_addr="/ip4/127.0.0.1/tcp/10000")]
    peer_id = PeerID.from_string("QmS5QmciTXXnCUCyxud5eWFenUMAmvAWSDa1c7dvdXRMZ7")
    c.connect(peer_id, maddrs)


if __name__ == "__main__":
    main()
