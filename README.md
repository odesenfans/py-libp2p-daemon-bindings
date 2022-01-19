# py-libp2p-daemon-bindings

[![Build Status](https://circleci.com/gh/mhchia/py-libp2p-daemon-bindings/tree/master.svg?style=shield)](https://circleci.com/gh/mhchia/py-libp2p-daemon-bindings/tree/master)

> The [libp2p daemon](https://github.com/libp2p/go-libp2p-daemon) bindings for Python

Have aligned with the go-client now!

## Supported methods

The following methods are supported by the library and are tested against jsp2pd 0.10.1.

- [x] `Identify`
- [x] `Connect`
- [x] `StreamOpen`
- [x] `StreamHandler` - Register
- [x] `StreamHandler` - Inbound stream
- [x] DHT ops - base functionalities
- [ ] Conn manager ops: unimplemented in jsp2pd
- [x] PubSub ops
- [ ] Peer Store
