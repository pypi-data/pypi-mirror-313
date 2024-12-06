# -*- coding: utf-8 -*-
# The source code in this file is covered by the CC0 v1.0 license.
# full license text: https://creativecommons.org/publicdomain/zero/1.0/
# SPDX-License-Identifier: CC0
# written by: Felix Schwarz (2019)

from blinker import Namespace


__all__ = [
    'connect_signals',
    'disconnect_signals',
    'SignalRegistry',
]

def connect_signals(signal_map, signal_registry):
    connected_signals = []
    for signal_name, signal_handler in signal_map.items():
        signal = signal_registry.signal(signal_name)
        signal.connect(signal_handler)
        ref_item = (signal_name, signal_handler)
        connected_signals.append(ref_item)
    return connected_signals

def disconnect_signals(connected_signals, signal_registry):
    for signal_name, signal_handler in connected_signals:
        signal = signal_registry.signal(signal_name)
        signal.disconnect(signal_handler)


class SignalRegistry(object):
    def __init__(self, blinker_namespace=None):
        if blinker_namespace is None:
            blinker_namespace = Namespace()
        self.namespace = blinker_namespace

    @property
    def signal(self):
        return self.namespace.signal

    def connect(self, signal_name, handler):
        signal = self.signal(signal_name)
        signal.connect(handler)

    def disconnect(self, signal_name, handler):
        signal = self.signal(signal_name)
        signal.disconnect(handler)

    def has_receivers(self, signal_name):
        signal_ = self.signal(signal_name)
        nr_receivers = len(signal_.receivers)
        return (nr_receivers > 0)

    def call_plugin(self, signal_name, log=None, sender=None, signal_kwargs=None):
        return self.call_plugins(
            signal_name,
            log                    = log,
            sender                 = sender,
            signal_kwargs          = signal_kwargs,
            expect_single_result   = True,
            expect_single_receiver = True,
        )

    def call_plugins(self, signal_name, log=None, sender=None, signal_kwargs=None, expect_single_receiver=False, expect_single_result=False):
        if not self.has_receivers(signal_name):
            if log:
                log.warning('no receivers for signal %r', signal_name)
            return None
        signal_ = self.signal(signal_name)
        nr_receivers = len(signal_.receivers)
        has_multiple_receivers = nr_receivers > 1
        if has_multiple_receivers and expect_single_receiver:
            if log:
                log.error('%d receivers for signal %r', nr_receivers, signal_name)
            # fail fast so this error will be noticed in case the user did not pass a logger
            return None

        signal_results = self._send(signal_, sender=sender, signal_kwargs=signal_kwargs)

        if not expect_single_result:
            return signal_results
        results = []
        for signal_result in signal_results:
            result = signal_result[1]
            if result is not None:
                results.append(signal_result)
        if len(results) > 1:
            raise ValueError('%d results returned after emitting signal %r' % (len(results), signal_name))
        elif len(results) == 1:
            single_result = results[0]
            result_value = single_result[1]
            return result_value
        # all receivers return "None" -> does not matter which "None" we return
        return None

    def _send(self, signal_, sender=None, signal_kwargs=None):
        sender = (sender,) if sender else ()
        if signal_kwargs is None:
            signal_kwargs = {}
        return signal_.send(*sender, **signal_kwargs)

    def send(self, signal_name, sender=None, signal_kwargs=None):
        signal_ = self.signal(signal_name)
        self._send(signal_, sender=sender, signal_kwargs=signal_kwargs)

