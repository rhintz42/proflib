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
To install ProfLib you'll have to issue 2 commands from the terminal

    pip install git+git://github.com/rhintz42/outlib.git#egg=outlib
    pip install git+git://github.com/rhintz42/proflib.git#egg=proflib

OutLib is a dependency for ProfLib hosted on github


How to Use
----------
Using this library is extremely easy, all you need to do is import the library
to your file and add the decorator above the function you wish to profile

Add this line to the top of the file that has the function you wish to profile:

    from proflib.lib.decorators import prof

Then, add the wrapper right above the function you wish to profile:

    @prof()


Example:

    from proflib.lib.decorators import prof

    @prof()
    def test_function(cool):
        return cool





MORE COMPLICATED STUFF
======================
If you want to do more complicated stuff with this library, go for it! Here
are some guided suggestions


Local Installation
------------------
If you'd like to hack on this library, feel free to! Here are steps to download
and use this library locally:

Create a new python virtual environment

    virtualenv proflib

Go into the new folder created

    cd proflib

Activate your Environment

    source bin/activate

Create a source folder

    mkdir src

Go into the src folder

    cd src

Git clone the repository

    git clone https://github.com/rhintz42/proflib.git

Go into the new folder

    cd proflib

Install all the dependencies and create the egg-file

    python setup.py develop

Install all the test dependencies

    pip install -r test-requirements.txt

Everything should be installed for this project, but now you need to install
this library in your project. Goto the virtual environment of the project you
want to use this library in and activate that environment. Then, go back to
the proflib folder and type this command

    python setup.py develop

This will install proflib in the site-packages folder in that python
environment, so you can now change code in your proflib directory, and it will
affect that project!


How to Run The Tests
--------------------
If you hack on this locally (Which you definitely should!), you should run and
add tests! To run the tests, first install the necessary dependencies (If you
haven't done so already):

    pip install -r test-requirements.txt

After that, just run this command and your tests should run

    py.test


How to Add Tests
----------------
To add tests, just go into the correct folder and add tests!

To add Unit Tests, goto this folder:

    proflib/tests/unit/

If you want to add a Unit Test to a model, goto this folder:

    proflib/tests/unit/models

Try to follow the naming convention of

    test_<file_name_of_thing_testing>.py

And try to look at a few tests to see the conventions used for tests


How to Make This Library a Dependency for your Python Project
-------------------------------------------------------------
If you have a standard python project that has a setup.py file, it's easy to
make proflib be one of its dependencies. Just follow these steps:

First, add a new array "github_dependencies" above the "setup" method, and
add 'git+git://github.com/rhintz42/proflib.git#egg=proflib' to the array

    github_dependencies = [
        'git+git://github.com/rhintz42/proflib.git#egg=proflib'
    ]

Next, add the library to your 'requires' array

    requires = [
        # The ... signifies all the other packages you require
        ...,
        'proflib'
    ]

Last, add the kwarg 'dependency_links=github_dependcies,' to your setup method

    setup(name='<your_project>',
          ...,
          dependency_links=github_dependencies,
          ...,
          )

