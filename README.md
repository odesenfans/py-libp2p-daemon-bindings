# py-libp2p-daemon-bindings

This is a fork of https://github.com/mhchia/py-libp2p-daemon-bindings targeting
with the new JavaScript libp2p daemon.
The Go daemon for which the original lib was created is now deprecated.
This is a work in progress, the first step is to make the lib compatible with the new
daemon and remove the dependency on py-libp2p as it is not maintained anymore either.

[![Build Status](https://circleci.com/gh/mhchia/py-libp2p-daemon-bindings/tree/master.svg?style=shield)](https://circleci.com/gh/mhchia/py-libp2p-daemon-bindings/tree/master)

> The [libp2p daemon](https://github.com/libp2p/js-libp2p-daemon) bindings for Python

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
