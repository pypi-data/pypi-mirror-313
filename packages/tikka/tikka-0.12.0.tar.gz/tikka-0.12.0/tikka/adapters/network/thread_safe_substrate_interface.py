# Copyright 2021 Vincent Texier <vit@free.fr>
#
# This software is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import inspect
import logging
from queue import Queue
from threading import Thread

from substrateinterface import SubstrateInterface

methods_to_queue = {
    "query",
    "query_multi",
    "rpc_request",
    "compose_call",
    "create_storage_key",
    "submit_extrinsic",
    "create_signed_extrinsic",
    "get_constant",
    "get_payment_info",
}


class ThreadSafe(Thread):

    queue: Queue = Queue()

    def __init__(self, *args, **kwargs):
        """
        Init a SubstrateInterface client adapter instance as a thread

        :param args: Positional arguments
        :param kwargs: Keywords arguments
        """
        super().__init__(*args, **kwargs)

    def run(self):
        """
        Started asynchronously with Thread.start()

        :return:
        """
        while True:
            # print("loop...")
            call, args, kwargs, result = self.queue.get()
            result_ = None
            # print(call.__name__, args, kwargs)
            if call == "--close--":
                logging.debug("Close queue thread on substrate_interface")
                break
            if not args and not kwargs:
                try:
                    result_ = call()
                except Exception as exception:
                    logging.exception(exception)
                    result.put(exception)
            elif not args and kwargs:
                try:
                    result_ = call(**kwargs)
                except Exception as exception:
                    logging.error(call)
                    logging.error(args)
                    logging.error(kwargs)
                    # logging.exception(exception)
                    result.put(exception)

            elif args and not kwargs:
                try:
                    result_ = call(*args)
                except Exception as exception:
                    logging.error(call)
                    logging.error(args)
                    logging.error(kwargs)
                    # logging.exception(exception)
                    result.put(exception)
            elif args and kwargs:
                try:
                    result_ = call(*args, **kwargs)
                except Exception as exception:
                    logging.error(call)
                    logging.error(args)
                    logging.error(kwargs)
                    # logging.exception(exception)
                    result.put(exception)
            # print(call.__name__, " put result ", result_)
            result.put(result_)
            # print("reloop...")

        logging.debug("SubstrateInterface connection closed and thread terminated.")

    def close(self):
        """
        Close connection

        :return:
        """
        # Closing the connection
        self.queue.put(("--close--", (), {}, None))


def decorator_for_func(cls, orig_func):
    def decorator(*args, **kwargs):
        # print("caller=", inspect.stack()[1].filename)
        # add to queue only if called outside of substrate_interface module...
        if "/substrateinterface/" in inspect.stack()[1].filename:
            # print("skip decorator for ", orig_func.__name__, " from ", inspect.stack()[1].filename)
            return orig_func(*args, **kwargs)
        # print("Decorating wrapper called for method %s" % orig_func.__name__)
        result: Queue = Queue()
        args[0].thread.queue.put((orig_func, args or tuple(), kwargs or dict(), result))
        # print(cls.queue.get())
        # print('done calling %s' % orig_func.__name__)
        return_ = result.get()
        if isinstance(return_, Exception):
            raise return_
        return return_

    return decorator


def decorator_for_class(cls):
    for name, method in inspect.getmembers(cls):
        if name not in methods_to_queue:
            continue
        # print("Decorating function %s" % name)
        setattr(cls, name, decorator_for_func(cls, method))
    return cls


@decorator_for_class
class ThreadSafeSubstrateInterface(SubstrateInterface):
    """
    Override substrate_interface client class with a queue to be thread safe

    """

    def __init__(self, *args, **kwargs):
        """
        Init a SubstrateInterface client adapter instance as a thread

        :param args: Positional arguments
        :param kwargs: Keywords arguments
        """
        super().__init__(*args, **kwargs)
        self.thread = ThreadSafe()
        self.thread.start()

    def close(self):
        logging.debug("Close RPC connection thread")
        self.thread.close()
