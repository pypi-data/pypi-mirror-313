"""
This module allows a portion of an EMTDC simulation to be run
in a Python process.

Example::

    import mhi.cosim

    with mhi.cosim.cosimulation("config.cfg") as cosim:
       channel = cosim.channel(1)

       time = 0
       time_step = 0.001
       run_time = 1.0

       x = ...
       y = ...
       z = ...

       while time <= run_time:

           a = ...
           b = ...
           c = ...
           d = ...

           time += time_step
           channel.set_values(a, b, c, d)
           channel.send(time)

           if time <= run_time:
               x, y, z = channel.get_values(time)
"""

#===============================================================================
# Imports
#===============================================================================

from __future__ import annotations
import os
import sys
from contextlib import contextmanager
from typing import Dict, Iterable, List, Tuple

# Import the C extension module
from mhi.cosim._cosim import initialize_cfg, finalize, Error, Channel # pylint: disable=no-name-in-module


#===============================================================================
# Version Info
#===============================================================================

_VERSION = (1, 2, 1)

_TYPE = 'f0'
VERSION = '.'.join(map(str, _VERSION))
VERSION_HEX = int.from_bytes((*_VERSION, int(_TYPE, 16)), byteorder='big')


#===============================================================================
# Named Channel
#===============================================================================

class NamedChannel:
    """
    A communication channel with subchannels identified usings
    names instead of numeric indices.

    Parameters:
        channel_id (int): channel identifier
        recv_names: a sequence of strings such as ``['a', 'b']``.
            Alternatively, `recv_names` can be a single string with each
            name separated by whitespace and/or commas, for example
            ``'a b'`` or ``'a, b'``.
        send_names: a sequence of strings such as ``['x', 'y']``.
            Alternatively, `send_names` can be a single string with each
            name separated by whitespace and/or commas, for example
            ``'x y'`` or ``'x, y'``.

    The following code, using subchanel indices 0 & 1::

        with mhi.cosim.cosimulation(config_file) as cosim:
            channel = cosim.channel(1)

            time = 0.0
            time_step = 0.001
            run_time = 1.0

            r_speed = 0

            while time <= run_time:
                torque = ...
                wind_speed = ...

                time += time_step;

                channel.set_value(torque, 0)
                channel.set_value(wind_speed, 1)
                channel.send(time)

                if time <= run_time:
                    r_speed = channel.get_value(time, 0)

    could become::

        with mhi.cosim.cosimulation(config_file) as cosim:
            channel = cosim.named_channel(1, "r_speed", "torque, wind_speed")

            time = 0.0
            time_step = 0.001
            run_time = 1.0

            r_speed = 0

            while time <= run_time:
                channel.torque = ...
                channel.wind_speed = ...

                time += time_step;
                channel.send(time)

                if time <= run_time:
                    channel.get_values(time)
                    r_speed = channel.r_speed
    """

    _channel: Channel
    _recv_names: List[str]
    _send: Dict[str, int]

    def __init__(self, channel_id, recv_names, send_names):

        if isinstance(recv_names, str):
            recv_names = recv_names.replace(',', ' ').split()
        recv_names = tuple(map(str, recv_names))

        if isinstance(send_names, str):
            send_names = send_names.replace(',', ' ').split()
        send_names = tuple(map(str, send_names))

        names = recv_names + send_names
        if len(set(names)) < len(names):
            raise ValueError("All names must be unique")
        if not all(name.isidentifier() for name in names):
            raise ValueError("All names must be valid identifiers")
        if any(name.startswith('_') for name in names):
            raise ValueError("Names must not start with an underscore")

        ch = Channel(channel_id)
        if ch.recv_size != len(recv_names):
            raise ValueError(f"Expected {ch.recv_size} recv indices, "
                             f"got {len(recv_names)}")
        if ch.send_size != len(send_names):
            raise ValueError(f"Expected {ch.send_size} send indices, "
                             f"got {len(send_names)}")

        self.__dict__['_channel'] = ch
        self.__dict__['_recv_names'] = recv_names
        self.__dict__['_send'] = {val: idx for idx, val in enumerate(send_names)}
        self.__dict__.update((name, 0.0) for name in recv_names)


    def get_values(self, time: float) -> None:
        """
        Wait for simulation to reach ``time``, and update the named subchannels
        with the values received from the remote end.

        This function blocks until the remote end has reached and transmitted
        value for the given time.

        Parameters:
            time (float): next simulation time
        """

        values = self._channel.get_values(time)
        self.__dict__.update(zip(self._recv_names, values))

    def __setattr__(self, name, val):
        index = self._send.get(name, None)
        if index is None:
            raise AttributeError("No such attribute: " + name)
        self._channel.set_value(val, index)

    def send(self, time: float) -> None:
        """
        Send to the remote end stored subchannel values, indicating they are
        valid up to the given time.

        Parameters:
            time (float): time stored values are valid until.
        """

        self._channel.send(time)


#===============================================================================
# Cosimulation
#===============================================================================

class Cosimulation:
    """
    A shim class to support a `with` statement that returns an
    object that manages intialization and finalization of the cosimulation
    library.
    """

    def channel(self, channel_id: int) -> Channel:
        """
        Return a channel object identified by `channel_id`

        Parameters:
            channel_id (int): channel identifier
        """

        return Channel(channel_id)

    find_channel = channel

    def named_channel(self, channel_id: int, recv_names,
                      send_names) -> NamedChannel:
        """
        Return a channel object identified by `channel_id`,
        with the given named recv and send subchannels.

        Parameters:
            channel_id (int): channel identifier
            recv_names: a sequence of strings such as ``['a', 'b']``.
                Alternatively, `recv_names` can be a single string with each
                name separated by whitespace and/or commas, for example
                ``'a b'`` or ``'a, b'``.
            send_names: a sequence of strings such as ``['x', 'y']``.
                Alternatively, `send_names` can be a single string with each
                name separated by whitespace and/or commas, for example
                ``'x y'`` or ``'x, y'``.
        """

        return NamedChannel(channel_id, recv_names, send_names)


#===============================================================================
# Context Manager for cosimulation
#===============================================================================

@contextmanager
def cosimulation(config_file):
    """
    This function returns a context managed object suitable for use in
    a `with` statement.

    Parameters:
        config_file: the cosimulation configuration file.

    Instead of writing::

        try:
            mhi.cosim.initialize_cfg(config_file)
            channel = mhi.cosim.Channel(1)
            ...
        finally:
            mhi.cosim.finalize()

    A `with` statement may be used::

        with mhi.cosim.cosimulation(config_file) as cosim:
            channel = cosim.find_channel(1)
            ...
    """

    config_file = os.fspath(config_file)

    initialize_cfg(config_file)
    try:
        yield Cosimulation()
    finally:
        finalize()
