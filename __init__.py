"""
VarEvents Module
    Handler Class
    Var Class
    Property Class

Copyright 2104 Humble Robot Development
               Humble.Robot.Development@gmail.com

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from copy import copy
from threading import Thread
from weakref import WeakKeyDictionary
from functools import partial

__ver__ = '0.1.1'
__author__ = 'Humble Robot Development'
__email__ = 'Humble.Robot.Development@gmail.com'
__date__ = 'February 2014'

Events = {'changed': lambda old, new: old != new,
          'increased': lambda old, new: old < new,
          'decreased': lambda old, new: old > new}


class Handler(object):

    def __init__(self, fun, handles, event, eid=None,
                 blocking=False, recursion=False):
        """ Handler(fun, handles, event, eid, blocking, recursion)
        Creates a Handler instance.
        fun - Handler function to run
        handles - Var instance to respond to
        event - String for name of event to respond to
        eid - Optional, ID of handler if subscribed
        blocking - Optional, Toggles Blocking Mode
        recursion - Optional, Toggle Recursive Mode
        """
        # store input
        self._fun = fun
        self.handles = handles
        self.event = event
        self._id = eid
        self._blocking = blocking
        self._recursion = recursion
        # initilize
        self._thread = None

    def __repr__(self):
        out = 'VarEvents.Handler(' + str(self._fun) + ', ' + \
            str(self.handles) + ', ' + self.event + ') '
        if self._id is not None:
            out += 'SUBSCRIBED '
        if self.running:
            out += 'RUNNING'
        return out

    def __del__(self):
        if self._id is not None:
            self.remove()

    def fire(self):
        """ fire(self)
        Fires the event as a thread
        """
        if self.blocking:
            self.run()
        elif self.recursion or not self.running:
            self._thread = Thread(target=self.run)
            self._thread.daemon = True
            self._thread.start()

    def run(self):
        """run(self)
        Runs the handler function
        """
        self._fun(self)
        self._thread = None

    @property
    def running(self):
        """ running
        Shows whether the handler is already running
        """
        return self._thread is not None

    @property
    def blocking(self):
        """ blocking
        Shows whether this handler will block the main thread
        """
        return self._blocking

    @blocking.setter
    def blocking(self, val):
        self._blocking = val

    @property
    def recursion(self):
        """ recursion
        Shows whether recursion is possible for this handler.
        Only possible when in non-blocking mode.
        """
        return self._recursion and not self._blocking

    @recursion.setter
    def recursion(self, val):
        self._recursion = val

    def unsubscribe(self):
        """ unsubscribe(self)
        Removes the handler's subscription
        """
        assert self._id is not None, 'Handler is not subscribed'
        self.handles.unsubscribe(self._id)
        self._id = None

    def subscribe(self):
        """ subscribe(self)
        Adds the handler's subscription
        """
        assert self._id is None, 'Handler is already subscribed'
        self.handles.subscribe(handler=self)


class Var(object):

    # basic special functions
    def __init__(self, init, readonly=False, blocking=False,
                 recursion=False, reporter=None):
        """ Var(init, readonly, blocking, recursion)
        Creates and instance of the Var class
        init - Initial value of the variable
        readonly - Optional, Toggles Read Only Mode
        blocking - Optional, Toggles Blocking Mode
        recursion - Optional, Toggles Recurison Mode
        """
        # initialize class
        global Events
        self.events = Events
        self._val = init
        self._handlers = []
        self.readonly = readonly
        self.blocking = blocking
        self.recursion = recursion
        self.reporter = reporter

    def __repr__(self):
        return 'Watched Variable: ' + self._val.__repr__()

    def __len__(self):
        return len(self._val)

    def __contains__(self, item):
        return item in self._val

    def __iter__(self):
        return self.__iter__()

    def __reversed__(self):
        return self.__reversed__()

    # attribute handling
    def __getattr__(self, name):
        return partial(self.__proxy__, fun=getattr(self._val, name))

    def __delattr__(self, name):
        self._val.__delattr__(name)

    def __dir__(self):
        return dir(self._val) + \
            ['events', 'update', 'subscribe', 'copy', '__fwd__', '__proxy__',
             'unsubscribe', '__get__', '__set__', 'recursion', 'readonly',
             'blocking']

    # string conversion
    def __str__(self):
        return str(self._val)

    def __unicode__(self):
        return unicode(self._val)

    # number conversion
    def __int__(self):
        return int(self._val)

    def __float__(self):
        return float(self._val)

    def __hex__(self):
        return hex(self._val)

    def __oct__(self):
        return oct(self._val)

    def __long__(self):
        return long(self._val)

    def __complex__(self):
        return complex(self._val)

    # truth testing
    def __nonzero__(self):
        return bool(self._val)

    # comparisons
    def __eq__(self, other):
        return self._val == other

    def __ne__(self, other):
        return self._val != other

    def __lt__(self, other):
        return self._val < other

    def __le__(self, other):
        return self._val <= other

    def __gt__(self, other):
        return self._val > other

    def __ge__(self, other):
        return self._val >= other

    # math functions
    def __add__(self, other):
        return self._val + other

    def __sub__(self, other):
        return self._val - other

    def __mul__(self, other):
        return self._val * other

    def __div__(self, other):
        return self._val / other

    def __truediv__(self, other):
        return self._val.__truediv__(other)

    def __floordiv__(self, other):
        return self._val // other

    def __mod__(self, other):
        return self._val % other

    def __divmod__(self, other):
        return divmod(self._val, other)

    def __pow__(self, *args):
        return self._val.__pow__(*args)

    def __lshift__(self, other):
        return self._val.__lshift__(other)

    def __rshift__(self, other):
        return self._val.__rshift__(other)

    def __and__(self, other):
        return self._val and other

    def __or__(self, other):
        return self._val or other

    def __xor__(self, other):
        return self._val ^ other

    # reversed math functions
    def __radd__(self, other):
        return self._val.__radd__(other)

    def __rsub__(self, other):
        return self._val.__rsub__(other)

    def __rmul__(self, other):
        return self._val.__rmul__(other)

    def __rdiv__(self, other):
        return self._val.__rdiv__(other)

    def __rtruediv__(self, other):
        return self._val.__rtruediv__(other)

    def __rfloordiv__(self, other):
        return self._val.__rfloordiv__(other)

    def __rmod__(self, other):
        return self._val.__rmod__(other)

    def __rdivmod__(self, other):
        return self._val.__rdivmod__(other)

    def __rpow__(self, *args):
        return self._val.__rpow__(*args)

    def __rlshift__(self, other):
        return self._val.__rlshift__(other)

    def __rrshift__(self, other):
        return self._val.__rrshift__(other)

    def __rand__(self, other):
        return self._val.__rand__(other)

    def _readonlyr__(self, other):
        return self._val._readonlyr__(other)

    def __rxor__(self, other):
        return self._val.__rxor__(other)

    # in-place math functions
    def __iadd__(self, other):
        self.update(self._val + other)
        return self

    def __isub__(self, other):
        self.update(self._val - other)
        return self

    def __imul__(self, other):
        self.update(self._val * other)
        return self

    def __idiv__(self, other):
        self.update(self._val / other)
        return self

    def __itruediv__(self, other):
        self.update(self._val.__truediv__(other))
        return self

    def __ifloordiv__(self, other):
        self.update(self._val // other)
        return self

    def __imod__(self, other):
        self.update(self._val % other)
        return self

    def __ipow__(self, *args):
        self.update(self._val.__pow__(*args))
        return self

    def __ilshift__(self, other):
        self.update(self._val.__lshift__(other))
        return self

    def __irshift__(self, other):
        self.update(self._val.__rshift__(other))
        return self

    def __iand__(self, other):
        self.update(self._val and other)
        return self

    def __ior__(self, other):
        self.update(self._val or other)
        return self

    def __ixor__(self, other):
        self.update(self._val ^ other)
        return self

    # unary operations
    def __neg__(self):
        return self._val.__neg__()

    def __pos__(self):
        return self._val.__pos__()

    def __invert__(self):
        return self._val.__invert__()

    def __abs__(self):
        return self._val.__abs__()

    # indices
    def __index__(self, *args):
        return self._val.__index__(*args)

    def __getitem__(self, key):
        return self._val[key]

    def __setitem__(self, key, value):
        val_copy = copy(self._val)
        val_copy[key] = value
        self.update(val_copy)

    def __delitem__(self, key):
        val_copy = copy(self._val)
        del val_copy[key]
        self.update(val_copy)

    # custom special functions
    def __fwd__(self, event):
        handlers = [h for h in self._handlers if
                    h is not None and h.event is event]
        for h in handlers:
            h.fire()

    def __proxy__(self, fun, *args, **kwargs):
        old = copy(self._val)
        out = fun(*args, **kwargs)
        self._checkEvents(old, self._val)
        return out

    # user functions
    def update(self, value, force=False, silent=False):
        """ update(self, value, force=False)
        Updates the value of the variable.
        Forwards events to handlers as
        appropriate.
        """
        # normalize input
        assert not self.readonly or force, 'This variable is read only'
        if isinstance(value, Var):  # this check is needed for inline math
            value = value._val      # functions when using Properties
        # update value in memory
        old = copy(self._val)
        self._val = value
        # call reporter if necessary
        if not silent and self.reporter is not None \
                and self.events['changed'](old, self._val):
            self.reporter(self._val)
        # call all other events
        self._checkEvents(old, self._val)

    def _checkEvents(self, old, new):
        for ename, econd in self.events.iteritems():
            if econd(old, new):
                self.__fwd__(ename)

    def subscribe(self, event=None, fun=None, handler=None):
        """subscribe(self, event=None, fun=None, handler=None)
        Subscribes a handler to an event.
        event and fun must be supplied if handler is not.
        If handler is supplied, event and fun will be ignored.
        """
        # create handler if neccessary
        if handler is None:
            assert fun is not None and event is not None, \
                'A function and event or a handler must be supplied'
            assert event in self.events.keys(), str(event) + \
                ' is not a valid event'
            handler = Handler(fun, self, event, blocking=self.blocking,
                              recursion=self.recursion)
        # subscribe the event
        self._handlers.append(handler)
        handler._id = len(self._handlers) - 1
        return handler

    def unsubscribe(self, eid):
        """unsubscribe(self, eid)
        Unsubscribes the handler with the given id
        """
        self._handlers[eid] = None

    def copy(self):
        """copy (self)
        Provides a duplicate of the current value
        """
        return copy(self._val)


class Property(object):

    # Special Thanks To:
    # http://nbviewer.ipython.org/urls/gist.github.com/
    #   ChrisBeaumont/5758381/raw/descriptor_writeup.ipynb

    def __init__(self, default, readonly=False,
                 blocking=False, recursion=False):
        self._default = default
        self.readonly = readonly
        self._blocking = blocking
        self._recursion = recursion
        self._data = WeakKeyDictionary()

    def __get__(self, instance, owner=None):
        try:
            return self._data[instance]
        except KeyError:
            self._data[instance] = Var(self._default, self.readonly,
                                       self._blocking, self._recursion)
            return self._data[instance]

    def __set__(self, instance, value):
        obj = self.__get__(instance)
        obj.update(value)
