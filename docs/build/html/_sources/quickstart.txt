
VarEvents Quick Start
=====================

This guide is meant to be a basic user's guide to the ``VarEvents``
library. It can be downloaded and run in IPython Notebook in order to
provide an interactive tutorial. When running this document, always run
the code block in Environment Setup first.

This Notebook can be downloaded
`here <http://docs.automic.us/VarEvents/v1.0.0/VarEvents.ipynb>`__.

Environment Setup
-----------------

Let's start by importing the ``VarEvents`` library. The ``sleep`` and
``partial`` functions are also imported because we will be using them
later.

.. code:: python

    from functools import partial
    from time import sleep
    import VarEvents

Basic Usage
-----------

This section is a quick start to the ``VarEvents`` library. All the
basics are here, but it will by no means explain all the ins and outs of
the library.

Event Handling Functions
~~~~~~~~~~~~~~~~~~~~~~~~

Below is a basic example of an event handling funciton. This handler
function, ``change_fun``, will allow us to watch changes to our
variables. Handlers can perform any operation, but the ``VarEvents``
library will always pass the handler instance responsible for the
function firing as the first parameter. The only exception to this rule
is if the target function is a class method. In that case, the ``self``
parameter will still be correctly passed first, followed by the handler
instance. The details of the handler class will be covered more later.

.. code:: python

    def change_fun(e):
        print 'changed to', e.handles

Events
~~~~~~

The ``VarEvents`` library primarily creates individual variables that
are capable of firing different events. The possible events are stored
in a dictionary inside of the ``VarEvents`` module called ``Events``.
They keys of this dictionary provide all the names of events that can be
fired. The values of the dictionary contain conditional functions
defining when the events should be fired.

.. code:: python

    VarEvents.Events



.. parsed-literal::

    {'changed': <function VarEvents.<lambda>>,
     'decreased': <function VarEvents.<lambda>>,
     'increased': <function VarEvents.<lambda>>}



New events can be created by adding them to this dictionary. This
dictionary is shared amongst all the variables that are created from
this module so whenever a new event definition is added to this
dictionary, it may be used by any variable whether it has been created
yet or not. The lambda function in the dictionary is what defines when
the event should be fired and should accept two inputs (``old``,
``new``) and return a boolean output. An output of ``True`` indicates
that the event should fire. The code for the default events is below.

.. code:: python

    events = {'changed': lambda old, new: old != new,
              'increased': lambda old, new: old < new,
              'decreased': lambda old, new: old > new}

Below are a few examples of how new events can be created.

.. code:: python

    VarEvents.Events['toTrue'] = lambda old, new: bool(new) if (new != old) else False
    VarEvents.Events['toFalse'] = lambda old, new: not new if (new != old) else False
    
    # longer conditional function example
    import datetime
    def afternoon_changed(old, new):
        a = datetime.datetime.today()
        return a.hour > 11 and old != new
    VarEvents.Events['afternoonChanged'] = afternoon_changed

Event Variables
~~~~~~~~~~~~~~~

Alright, most of the basics are out of the way so let's get started.
We'll start off by creating an event handling function and an event
variable. Event variables are created with the ``Var`` class inside of
the ``VarEvents`` library. The required parameter when creating an
instance of this class is it's initial value. There are also inputs for
read only mode, blocking mode, and recursion mode. We'll talk about
those later.

.. code:: python

    def change_fun(e, name):
        print name, 'changed to', e.handles
    
    a = VarEvents.Var(5)

Now that we have the event variable, we tie handler functions to it by
using the ``subscribe`` method. The subscribe method takes two
parameters. The first is the event name, and the second is the function
that should be called. The function should take only one parameter, as
noted above, that will be the handler class. Since the function we
created also takes a parameter called name, we will use the partial
function to adapt the defined handler function to fit the required
scheme.

.. code:: python

    handler = a.subscribe('changed', partial(change_fun, name='a'))

The subscribe method returns an instance of the handler class. This can
be used to unsubscribe, resubscribe, and fire the handler. Additionally,
it contains the variable that calls the handler and the condition under
which the handler is called. For right now, don't worry too much about
this. We will cover it in a bit.

Now let's change the event variable and watch our new event get fired.
The event's value is changed by using the update method. When we fire
the event, the handler will be executed in a thread so as not to block
the main thread. This is the default behaviour. It can be changed, but
we'll talk about that in a minute. As an aside, I will be inserting some
random sleep statements into the sample code to do demonstrations while
not having to worry about threads conflicting with each other.

.. code:: python

    a.update(6)

.. parsed-literal::

    a changed to 6


This might also be a good time to note that you can interact with the
event variable class in the same way you would the traditional class of
the value that is inside of it. In plain English, what this means, is
that all of the methods that you would expect to be available normally,
are still available. Allow me to demonstrate.

.. code:: python

    a.update('asdf')
    print a.upper()

.. parsed-literal::

    a changed to asdf
    ASDF


The method ``upper`` is actually a method of the string inside the event
variable. The ``Var`` class will automatically map all of the functions
of it's value. Long story short, this means that the experience of using
the ``VarEvents`` library should be fairly seemless. While we are on
this subject, here are some other cool things you can do.

.. code:: python

    a.update(1)
    sleep(0.5)
    a += 7

.. parsed-literal::

    a changed to 1
    a changed to 8


.. code:: python

    a.update([1, 0, 8 , 3, 9, 2, 4])
    sleep(0.5)
    a.sort()

.. parsed-literal::

    a changed to [1, 0, 8, 3, 9, 2, 4]
    a changed to [0, 1, 2, 3, 4, 8, 9]


Handler Class
~~~~~~~~~~~~~

Well, I said we would talk about the handler class, and there is no
better time than the present. This class is created automatically by the
event variable, but it could also be created manually. The class is
created with three required parameters: ``fun``, ``handles``, and
``event``. The ``fun`` parameter is the handler function, ``handles`` is
the event variable instance that launches the handler, and ``event`` is
the name of the event to which the handler responds. There are also
inputs for read only mode, blocking mode, and recursion mode, but those
will be covered later.

.. code:: python

    def change_fun(e, name):
        print name, 'changed to', e.handles
    
    a = VarEvents.Var(5)
    handler = a.subscribe('changed', partial(change_fun, name='a'))
    print repr(handler)

.. parsed-literal::

    VarEvents.Handler(<functools.partial object at 0x10f5d3ba8>, 5, changed) SUBSCRIBED 


The handler class has a few useful properties, they are printed below.
It is important to note that the ``running`` property may not be
accurate in recursive mode.

.. code:: python

    print 'handles:', repr(handler.handles)
    print 'event:', handler.event
    print 'recursion:', handler.recursion
    print 'blocking:', handler.blocking
    print 'running:', handler.running

.. parsed-literal::

    handles: Watched Variable: 5
    event: changed
    recursion: False
    blocking: False
    running: False


The handler class has four important methods: ``fire``, ``run``,
``unsubscribe``, and ``subscribe``. The method ``fire`` evaluates if and
how the handler should run and then runs it if necessary. This is what
gets called from inside the event variable. The method ``run`` executes
the handler function in the thread in which it is executed regardless of
anything else. These two methods should generally not be called
directly. The ``unsubscribe`` and ``subscribe`` methods will disable and
re-enable the handler calling respectively.

.. code:: python

    a.update(1)
    sleep(0.5)
    
    handler.unsubscribe()
    a.update(2)
    sleep(0.5)
    
    handler.subscribe()
    a.update(3)
    sleep(0.5)

.. parsed-literal::

    a changed to 1
    a changed to 3


Event Properties
~~~~~~~~~~~~~~~~

It is likely that you may want to use an event variable as a property
inside of a class. You could do this as expected by using the Var class,
or, alternatively, a class is provided that allows the user to create a
more traditional style property. This class is a Python Descriptor
class. For this reason, **it must be defined at the class level** and
not inside the ``__init__`` function. Seriously. If you put it inside
the ``__init__`` function, it will not work. This took me an
embarrassingly long time to figure out.

Properties are created with the ``Property`` class inside of the module.
The class takes four inputs: ``default``, ``readonly``, ``blocking``,
and ``recursion``. We will only cover ``default`` right now and the rest
later. This class automatically generates ``Var`` instances as they are
needed for different instances of their parent classes. This makes it
potentially less memory intensive than simply generating the ``Var``
instances inside the ``__init__`` funtion. Whatever value is given to
``default`` will be the initial value given to the instances of ``Var``.

In addition to being potentially less memory intensive, there is another
advantage to using event properties when possible. The near elimination
of the need for the ``update`` method. When an event property is used,
the value can be updated inline in the standard way. Below is an example
of an event property demonstrating this.

.. code:: python

    def change_fun(e, name):
        print name, 'changed to', e.handles
    
    class test_class(object):
        val = VarEvents.Property(-900)
        
    a = test_class()
    b = test_class()
    
    handler_a = a.val.subscribe('changed', partial(change_fun, name='a'))
    handler_b = b.val.subscribe('changed', partial(change_fun, name='b'))
    
    a.val = 6  # look ma, no update call
    b.val += 999

.. parsed-literal::

    a changed to 6
    b changed to 99


Run Modes
---------

Read Only Mode, Recursive Mode, and Blocking Mode. We are finally going
to talk about them.

Read Only Mode
~~~~~~~~~~~~~~

Sometimes you may be creating a library where you will have parameters
that you don't want the end user to edit. This is where Read Only Mode
comes in. All variables in Read Only Mode may still be edited, but it
has to be forced. This is done by using the ``force`` parameter in the
``update`` method.

.. code:: python

    def change_fun(e, name):
        print name, 'changed to', e.handles
    
    a = VarEvents.Var(5, readonly=True)
    handler = a.subscribe('changed', partial(change_fun, name='a'))
    
    try:
        a.update(6)
    except AssertionError:
        print 'Oops!'
        
    a.update(6, force=True)
    sleep(0.1)

.. parsed-literal::

    Oops!
    a changed to 6


I'll quickly make a note here, that in order to update the value of a
read only property in a class, you must still use the ``update`` method
with the ``force`` parameter set.

.. code:: python

    def change_fun(e, name):
        print name, 'changed to', e.handles
    
    class test_class(object):
        val = VarEvents.Property(0, readonly=True)
        
    a = test_class()
    handler = a.val.subscribe('changed', partial(change_fun, name='a'))
    
    try:
        a.val = 6
    except AssertionError:
        print 'Oops!'
        
    a.val.update(999, force=True)
    sleep(0.1)

.. parsed-literal::

    Oops!
    a changed to 999


This doesn't make it impossible for the end user to edit a read only
variable, but it makes the end user take an additional step. This should
be enough to stop the user from accidentally interferring with a read
only variable while still allowing them to do so if they absolutely
want.

Read Only Mode can be activated by toggling the ``readonly`` parameter
to ``True`` when instanciating either a ``Var`` or ``Property`` class.
It can also be changed in the ``Var`` class by changing the property
called ``readonly``.

Recursive Mode
~~~~~~~~~~~~~~

By default, ``VarEvents`` runs in Non-Recursive Mode. Put simply, this
means that each handler instance is limited to only one running thread
at a time. This is done in order to prevent sticky situations with
accidental recursion. The following examples demonstrate why this is a
good thing. The first example runs in the default Non-Recursive Mode and
executes correctly.

.. code:: python

    def countdown(e):
        print 'Countdown Started:'
        while e.handles > 0:
            print e.handles
            sleep(1)
            e.handles -= 1
            
    a = VarEvents.Var(0)
    handler = a.subscribe('changed', countdown)
    a.update(5)
    sleep(5)

.. parsed-literal::

    Countdown Started:
    5
    4
    3
    2
    1


If more than one instance of the handler is allowed to run at a time,
then each time the variable is decremented, a new thread of the handler
function would run. Some users may argue that the automatic recursion
could have allowed the while loop to be removed, and that would be true.
However, I felt that this would generally create more obfusicated
spaghetti code, so, as a design choice, I turned it off by default.
Below is the same code with recursion turned on.

.. code:: python

    def countdown(e):
        print 'Countdown Started:'
        while e.handles > 0:
            print e.handles
            sleep(1)
            e.handles -= 1
            
    a = VarEvents.Var(0, recursion=True)
    handler = a.subscribe('changed', countdown)
    a.update(5)
    sleep(5)

.. parsed-literal::

    Countdown Started:
    5
    Countdown Started:
    4
    4
    3
    Countdown Started:
    3
    Countdown Started:
    2
    2
    Countdown Started:
    Countdown Started:
    Countdown Started:
    Countdown Started:


Woah, ok, that was worse. Just for the sake of conversation, let's fix
that code so it is safe for recursion.

.. code:: python

    def countdown(e):
        if e.handles > 0:
            print e.handles
            sleep(1)
            e.handles -= 1
            
    a = VarEvents.Var(0, recursion=True)
    handler = a.subscribe('changed', countdown)
    print 'Countdown Started:'
    a.update(5)
    sleep(5)

.. parsed-literal::

    Countdown Started:
    5
    4
    3
    2
    1


So the code can be made safe for recursion, and there is nothing wrong
with it. I just personally feel that the first example more clear than
the latter. If you need recursion for your project, its available.
However, if you don't need it, I would suggest not using it.

Recursive Mode can be activated by toggling the ``recursion`` parameter
to ``True`` when instanciating a ``Var``, ``Property``, or ``Handler``
class. It can also be changed in either the ``Var`` or ``Handler`` class
by changing the property called ``recursion``.

Blocking Mode
~~~~~~~~~~~~~

By default, ``VarEvents`` runs in Non-Blocking Mode. In Non-Blocking
Mode, a thread is spawned every time an event function is run so as to
not block the main thread. However, Non-Blocking Mode has some
surprising properties. It is important to note that if the variable is
updated outside of the handler, it will also be updated inside of the
handler. This can be rectified by running the handler in Blocking Mode,
but that solution may not always be appropriate. In order to prevent
this, a method called copy is available on each of the event variables.
Let's explore this.

.. code:: python

    # let's first see where this can go wrong
    def wait_and_print(e):
        sleep(1)
        print e.handles
    
    a = VarEvents.Var(0)
    a.subscribe('changed', wait_and_print)
    
    a.update(5)
    a.update(10)
    sleep(2)

.. parsed-literal::

    10


It may seem like the first event is being skipped, however, the event is
still being fired on the first change. Because the event is allowed to
run a seperate thread, the second change happens before the handler
prints the value. This results in the second value being printed. Let's
look at what happens when we turn on Blocking Mode.

.. code:: python

    # blocking mode turned on this time
    def wait_and_print(e):
        sleep(1)
        print e.handles
    
    a = VarEvents.Var(0, blocking=True)
    a.subscribe('changed', wait_and_print)
    
    a.update(5)
    a.update(10)

.. parsed-literal::

    5
    10


There we go, now that just makes so much more sense. Why doesn't this
dumb library just do this by default? That would make so much more
sense! Well, as before, design choice. Generally speaking, your handlers
will probably take much longer to run and if they are run in a seperate
thread as oppsed to the main thread, the rest of your application can
continue to run. This is generally desireable. If you would like to keep
the handlers in Non-Blocking Mode, but ignore automatic updates, the
``copy`` method is available.

.. code:: python

    # using the copy method
    def wait_and_print(e):
        val = e.handles.copy()
        sleep(1)
        print 'Value was', val
        print 'Value is now', e.handles
    
    a = VarEvents.Var(0)
    a.subscribe('changed', wait_and_print)
    
    a.update(5)
    a.update(10)
    sleep(2)

.. parsed-literal::

    Value was 5
    Value is now 10


Hopefully that clears up more confusion than it causes.

Blocking Mode can be activated by toggling the ``blocking`` parameter to
``True`` when instanciating a ``Var``, ``Property``, or ``Handler``
class. It can also be changed in either the ``Var`` or ``Handler`` class
by changing the property called ``blocking``.

Other Important Notes
---------------------

This section contains other random thoughts and warnings that I thought
of while typing the rest of this document. Hopefully this section can
eliminate some common frustrations.

Overwriting an Event Variable
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

I wanted to take a second to demonstrate the importance of the
``update`` method in event variables. Take a look at this example.

.. code:: python

    def change_fun(e, name):
        print name, 'changed to', e.handles
    
    a = VarEvents.Var(5)
    handler = a.subscribe('changed', partial(change_fun, name='a'))
    
    print repr(a)
    a.update(6)
    sleep(0.1)
    print repr(a)
    a = 7
    print repr(a)

.. parsed-literal::

    Watched Variable: 5
    a changed to 6
    Watched Variable: 6
    7


In that example, the first expected event is fired, but not the second.
This is because the ``a = 7`` line indicates to the Python interpreter
to change the variable ``a`` to an instance of ``int`` that equals
``7``. This is very different from updating that value stored inside the
``Val`` instance and is also why the ``repr`` string changes in the
above example. Event properties inside of classes are able to intercept
the set action raised by Python (with Descripter special functions) such
that when they are inside the class, the update function is not
required. However, if they are copied outside of the class, the update
function is again required. This next example demonstrates that.

.. code:: python

    def change_fun(e, name):
        print name, 'changed to', str(e.handles)
    
    class test_class(object):
        val = VarEvents.Property(0)
        
    a = test_class()
    handler = a.val.subscribe('changed', partial(change_fun, name='a'))
    
    print repr(a.val)
    a.val = 6
    print repr(a.val)
    val_a = a.val
    print repr(val_a)
    val_a.update(7)
    print repr(val_a)
    val_a = 8
    print repr(val_a)

.. parsed-literal::

    Watched Variable: 0
    a changed to 6
    Watched Variable: 6
    Watched Variable: 6
    a changed to 7
    Watched Variable: 7
    8

