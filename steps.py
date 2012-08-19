# -*- coding: utf-8 -*-
"""
This is the detailed description of my test case.
"""
# Generic step is a good place to start
# All you need then is to override some methods in it
from trytry.core.steps import GenericStep

# You would probably like to take advantage of LXC, a secure container
from trytry.core.utils.lxc import lxc_setup, lxc_teardown

__flow__ = {
    # class names in this module, which will be used as steps
    'steps': ['Step1', 'Step2'],
    # the name of LXC container template which will be used to set up
    # a base container for your user.
    'lxc_container': 'python',
    # Setup and teardown functions. You can define them as functions or,
    # exactly like steps, as strings within your module.
    # Function accept one parameter: an initialized Flow object
    'setup': lxc_setup,
    'teardown': lxc_teardown,
    # the name of your module
    'name': 'Simple Bash',
    # The short name of your module, will be used as a part of urls in tests
    'url': 'simple_bash',
    # Detailed description of your module
    'description': __doc__,
}


class MyGenericStep(GenericStep):
    prompt = u'# '

    def get_command(self, user_input):
        """
        This function, on a basis of user input, must return a tuple:

        ([list, of, commands, to, execute], "string with stdin")

        Some interpreters accept commands as command line arguments, then
        you should return user input as a part of command, like:

        ['bash', '-c', user_input]

        It's good that you usually shouldn't care about user import escaping.

        Some commands accept commands from stdin, then you must return just
        the list containing the interpreter name, and a line with user input.

        It's good, that if you use GenericStep, you shouldn't think much about
        restricting time limits, as well as shouldn't care about how command
        will be executed within the framework of the container. The return
        can be as easy as

        (['bash'], user_input)
        """
        return (['bash'], user_input)


class Step1(MyGenericStep):
    """
    This is the step task and description. You can use **markdown** here

    Minimalistic approach for module creation assumes that you only define
    a set of variables:

    prompt: prompt in the CLI interface
    expected_out: we wait for that output from the user. If output matches
                  with this string, user goes to the next step
    on_success_hint: the string which will be shown to user in case of success
    on_wrong_out_hint: the stdout of command return something else, then
                       this string will be displayed
    on_err_hint: this is the line which will be shown if something is returned
                 to commands stderr

    """
    name = "Step1"
    expected_out = "Hello World"
    on_success_hint = u'Well done!'
    on_wrong_out_hint = u"Let's try again!"


class Step2(MyGenericStep):
    """
    The execution and validation process follows two obvious passes:

    1) Execution. The result contains (out, err, returncode)
    2) Validation. A separate function is invoked, it accepts this triple, and
       return the dotdict object, containing following fields:

        'goto_next': True or False (depending on whether user has
                     successfully passed this step)
        'hint': text which will be shown as a comment to result of user
                command execution
        'ok_text': usually, the copy of stdout, but you are free to write
                   there whatever you want
        'err_text': usually, the copy of stderr, but you are free to write
                    there whatever you want

    Bearing that in mind, examine the code of this step
    """

    def analyze(self, out, err, returncode):
        from dotdict import dotdict
        ret = {
            'goto_next': False,
            'hint': None,
            'ok_text': out,
            'err_text': err,
        }
        if out == 'next':
            ret['goto_next'] = True
        else:
            ret['hint'] = 'Try to write a command which prints "next"'
        return dotdict(ret)
