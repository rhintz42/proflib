proflib
=======

This is a library for adding helpul debugging/testing profiling to your
project.


Overview
--------
The basic concept is to make it as easy as possible to print out as much
helpful information as you deem necessary while debuggging, in an output that
helps you the most. You can give the variables you want to track, the variables
you don't care about, and many other settings to print out the data you want to
see. You can also customize how the data is printed out, so you can log output
to the console the way you want it seen, or even print your data to a file for
easy logs later.


Why We Build It
---------------
The purpose of this is to make it extremely easy to debug your code and create
tests. 


Why it's great for creating tests
--------------------------
You're able to see real data to mock out your tests with, so you don't have to
search through to see what variables may be valid to use as your mocks.


Installation
------------
First, install OutLib, a dependency for proflib
* pip install git+git://github.com/rhintz42/outlib.git#egg=outlib

Last, install ProfLib, which is the actual library
* pip install git+git://github.com/rhintz42/proflib.git#egg=proflib


How to Use
----------
Using this library is extremely easy, all you need to do is import the library
to your file and add the decorator above the function you wish to profile

Add this line to the top of the file that has the function you wish to profile:

    from proflib.lib.decorators import persistent_locals

Then, add the wrapper right above the function you wish to profile:

    @persistent_locals()


Example:

    from proflib.lib.decorators import persistent_locals

    @persistent_locals()
    def test_function(cool):
        return cool
