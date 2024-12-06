# Created by Alfred Ferrer Florensa
"""Contains objects for Command Line"""

import os
import sys
import subprocess
from cgecore.utils.savers_mixin import StringCreator


class ApplicationError(subprocess.CalledProcessError):
    """Raised when an application returns a non-zero exit status.
    The exit status will be stored in the returncode attribute, similarly
    the command line string used in the cmd attribute, and (if captured)
    stdout and stderr as strings.
    This exception is a subclass of subprocess.CalledProcessError.
    """

    def __init__(self, returncode, cmd, stdout="", stderr=""):
        """Initialize."""
        self.returncode = returncode
        self.cmd = cmd
        self.stdout = stdout
        self.stderr = stderr

    def __str__(self):
        """Format the error as a string."""
        # get first line of any stderr message
        try:
            msg = self.stderr.lstrip().split("\n", 1)[0].rstrip()
        except Exception:  # TODO, ValueError? AttributeError?
            msg = ""
        if msg:
            return """Non-zero return code %d from %r, with the error message:
                   %s""" % (
                   self.returncode,
                   self.cmd,
                   msg,
                   )
        else:
            return "Non-zero return code %d from %r" % (
                self.returncode, self.cmd)

    def __repr__(self):
        """Represent the error as a string."""
        return "ApplicationError(%i, %s, %s, %s)" % (
            self.returncode,
            self.cmd,
            self.stdout,
            self.stderr,
        )


class CommandResume(dict):

    def __init__(self, command, stdout="", stderr="", exec_name=None, key=None):

        if isinstance(command, str):
            self["command"] = command
        else:
            raise TypeError("Command should be a string")
        if isinstance(stdout, str):
            self["stdout"] = stdout
        else:
            raise TypeError("STDOUT should be a string")
        if isinstance(stderr, str):
            self["stderr"] = stderr
        else:
            raise TypeError("STDERR should be a string")
        self["parameters"] = dict()
        if exec_name is None:
            self["software_name"] = ""
        else:
            self["software_name"] = exec_name
            self.init_parameters(program_file=exec_name)

    def __str__(self):
        str_report = """Command:\n\t%s\nReturned STDERR\n%s\n
                          Returned STDOUT\n%s\n\n""" % (self["command"],
                                                        self["stderr"],
                                                        self["stdout"])
        return str_report

    def add_parameter(self, param, value):
        if param is None:
            raise ValueError("Parameter cannot be None")
        else:
            if value is None:
                value = True
            self["parameters"][param] = value

    def init_parameters(self, program_file):
        command_split = self["command"].split(program_file)
        if len(command_split) == 2 or len(command_split) == 1:
            param_split = command_split[-1].split()
            param = None
            value = None
            for str_param in param_split:
                if str_param.startswith("-"):
                    if param is not None:
                        self.add_parameter(param, value)
                    param = str_param
                else:
                    value = str_param
            if param is not None:
                self.add_parameter(param, value)
        else:
            self["parameters"] = None

    @staticmethod
    def get_unique_run_key(program, run_collection, key, delimiter=";;"):
        """
            Input:
                gene_key: None-unique key
                res_collection: Result object created by the cgelib package.
                minimum_key: Key prefix
                delimiter: String used as delimiter inside the returned key.
            Output:
                gene_key: Unique key (string)

            If gene_key is found in res_collection. Creates a unique key by
            appending a random string ton minimum_gene_key.
        """
        if "software_executions" in run_collection:
            v_num = len(run_collection["software_executions"]) + 1
            vrs_str = ("V{num}").format(num=v_num)
            if key is None:
                run_key = ("{program}{deli}run{vrs}"
                            .format(program=program, deli=delimiter,
                                    vrs=vrs_str))
            else:
                run_key = ("{program}{deli}run{vrs}{deli}{key}"
                            .format(program=program, deli=delimiter,
                                    vrs=vrs_str, key=key))
        else:
            run_key = ("{key}"
                       .format(key=key))
        return run_key

    @staticmethod
    def std_executable(cmdresume, json_report, key=None):
        cmdresume["type"] = "software_exec"
        run_key = CommandResume.get_unique_run_key(
                                        program=cmdresume["software_name"],
                                        run_collection=json_report,
                                        delimiter=";;", key=key)
        cmdresume["key"] = run_key


class CommandLineBase:
    """Generic interface for constructing command line strings.
    This class shouldn't be called directly; it should be subclassed to
    provide an implementation for a specific application. You can set
    options when creating the wrapper object using keyword arguments - or
    later using their corresponding properties.
    """

    # TODO - Replace the above example since EMBOSS doesn't work properly
    # if installed into a folder with a space like "C:\Program Files\EMBOSS"
    #
    # Note the call example above is not a doctest as we can't handle EMBOSS
    # (or any other tool) being missing in the unit tests.

    parameters = None  # will be a list defined in subclasses

    allowed_attr = ["parameters", "program_name", "path_exec", "language"]


    def __init__(self, cmd, path_exec, language="binary", **kwargs):
        """Create a new instance of a command line wrapper object."""
        # Init method - should be subclassed!
        #
        # The subclass methods should look like this:
        #
        # def __init__(self, cmd="muscle", **kwargs):
        #     self.parameters = [...]
        #     CommandLineBase.__init__(self, cmd, **kwargs)
        #
        # i.e. There should have an optional argument "cmd" to set the location
        # of the executable (with a sensible default which should work if the
        # command is on the path on Unix), and keyword arguments.  It should
        # then define a list of parameters, all objects derived from the base
        # class _ArgumentBase.
        #
        # The keyword arguments should be any valid parameter name, and will
        # be used to set the associated parameter.
        self.program_name = cmd
        if language == "binary" or language == None:
            language_str = ""
        else:
            language_str = "%s " % language
        self.language = language_str
        if path_exec != "":
            if not os.path.isdir(path_exec):
                raise OSError("The path %s is not a directory. Point to the "
                              "directory where the executable is.")
            path_exec = path_exec + "/"
        self.path_exec = path_exec
        try:
            parameters = self.parameters
        except AttributeError:
            raise AttributeError(
                "Subclass should have defined self.parameters"
            ) from None
        # Create properties for each parameter at run time
        aliases = set()
        for p in parameters:
            if not p.names:
                if not isinstance(p, _StaticArgument):
                    raise TypeError("Expected %r to be of type _StaticArgument"
                                    % p)
                continue
            for name in p.names:
                if name in aliases:
                    raise ValueError("Parameter alias %s multiply defined"
                                     % name)
                aliases.add(name)
            name = p.names[-1]

            # Beware of binding-versus-assignment confusion issues
            def getter(name):
                return lambda x: x._get_parameter(name)

            def setter(name):
                return lambda x, value: x.set_parameter(name, value)

            def deleter(name):
                return lambda x: x._clear_parameter(name)

            doc = p.description
            if isinstance(p, _SwitchArgument):
                doc += (
                    "\n\nThis property controls the addition of the %s "
                    "switch, treat this property as a boolean." % p.names[0]
                )
            else:
                doc += (
                    "\n\nThis controls the addition of the %s parameter "
                    "and its associated value.  Set this property to the "
                    "argument value required." % p.names[0]
                )
            prop = property(getter(name), setter(name), deleter(name), doc)
            setattr(self.__class__, name, prop)  # magic!
        for key, value in kwargs.items():
            self.set_parameter(key, value)

    def _validate(self):
        """Make sure the required parameters have been set (PRIVATE).
        Check that incompatible paramters are not set.
        No return value - it either works or raises a ValueError.
        This is a separate method (called from __str__) so that subclasses may
        override it.
        """
        param_set = []
        for p in self.parameters:
            if(p.is_set):
                param_set.append(p.names[-1])
            # Check for missing required parameters:
            if p.is_required is True and not (p.is_set):
                if not (p.alter_options):
                    raise ValueError("Required parameter %s is not set."
                                     % p.names[-1])
                required_exists = 0
                for p_set in self.parameters:
                    if p_set.is_set and p_set.names[-1] in p.alter_options:
                        required_exists = 1
                        continue
                if not required_exists:
                    raise ValueError("Parameter %s is not set. Neither "
                                     "alternative parameters as %s."
                                     % (p.names[-1],
                                        ', '.join(p.alter_options)))
            # Check for incompatible paramters set
            if p.incompatible is not None and p.is_set:
                arg_incompatible = set(p.incompatible) & set(param_set)
                if arg_incompatible:
                    raise ValueError("Parameter '%s' is set, but the "
                                     "incompatible parameter '%s' has "
                                     "been also set."
                                     % (p.names[-1],
                                        ', '.join(arg_incompatible)))

    def __str__(self):
        """Make the commandline string with the currently set options.
        e.g.
        >>> from Bio.Emboss.Applications import WaterCommandline
        >>> cline = WaterCommandline(gapopen=10, gapextend=0.5)
        >>> cline.asequence = "asis:ACCCGGGCGCGGT"
        >>> cline.bsequence = "asis:ACCCGAGCGCGGT"
        >>> cline.outfile = "temp_water.txt"
        >>> print(cline)
        water -outfile=temp_water.txt -asequence=asis:ACCCGGGCGCGGT
                -bsequence=asis:ACCCGAGCGCGGT -gapopen=10 -gapextend=0.5
        >>> str(cline)
        'water -outfile=temp_water.txt -asequence=asis:ACCCGGGCGCGGT
                -bsequence=asis:ACCCGAGCGCGGT -gapopen=10 -gapextend=0.5'
        """
        self._validate()
        commandline = "%s%s%s " % (_escape_filename(self.language),
                                 _escape_filename(self.path_exec),
                                 _escape_filename(self.program_name))
        for parameter in self.parameters:
            if parameter.is_set:
                # This will include a trailing space:
                commandline += str(parameter)
        return commandline.strip()  # remove trailing space

    def __repr__(self):
        """Return a representation of the command line object for debugging.
        e.g.
        >>> from Bio.Emboss.Applications import WaterCommandline
        >>> cline = WaterCommandline(gapopen=10, gapextend=0.5)
        >>> cline.asequence = "asis:ACCCGGGCGCGGT"
        >>> cline.bsequence = "asis:ACCCGAGCGCGGT"
        >>> cline.outfile = "temp_water.txt"
        >>> print(cline)
        water -outfile=temp_water.txt -asequence=asis:ACCCGGGCGCGGT
                -bsequence=asis:ACCCGAGCGCGGT -gapopen=10 -gapextend=0.5
        >>> cline
        WaterCommandline(cmd='water', outfile='temp_water.txt',
                         asequence='asis:ACCCGGGCGCGGT',
                         bsequence='asis:ACCCGAGCGCGGT',
                         gapopen=10, gapextend=0.5)
        """
        if self.path_exec == "":
            answer = "%s(cmd=%r" % (self.__class__.__name__,
                                    self.program_name)
        else:
            answer = "%s(cmd=%r, path_executable=%r" % (self.__class__.__name__,
                                                        self.program_name,
                                                        self.path_exec)
        if self.language == "":
            answer = "%s" % answer
        else:
            answer = "%s, programming_language=%r" % (answer, self.language)
        for parameter in self.parameters:
            if parameter.is_set:
                if isinstance(parameter, _SwitchArgument):
                    answer += ", %s=True" % parameter.names[-1]
                else:
                    answer += ", %s=%r" % (parameter.names[-1],
                                           parameter.value)
        answer += ")"
        return answer

    def _get_parameter(self, name):
        """Get a commandline option value (PRIVATE)."""
        for parameter in self.parameters:
            if name in parameter.names:
                if isinstance(parameter, _SwitchArgument):
                    return parameter.is_set
                else:
                    if parameter.is_set:
                        return parameter.value
                    else:
                        if parameter.default is not None:
                            return str(parameter.default) + " (default)"
                        else:
                            raise ValueError("Option name %s is not set and"
                                             " does not have a default value."
                                             % name)
        raise ValueError("Option name %s was not found." % name)

    def _clear_parameter(self, name):
        """Reset or clear a commandline option value (PRIVATE)."""
        cleared_option = False
        for parameter in self.parameters:
            if name in parameter.names:
                parameter.value = None
                parameter.is_set = False
                cleared_option = True
        if not cleared_option:
            raise ValueError("Option name %s was not found." % name)

    def set_parameter(self, name, value=None):
        """Set a commandline option for a program (OBSOLETE).
        Every parameter is available via a property and as a named
        keyword when creating the instance. Using either of these is
        preferred to this legacy set_parameter method which is now
        OBSOLETE, and likely to be DEPRECATED and later REMOVED in
        future releases.
        """
        set_option = False
        for parameter in self.parameters:
            if name in parameter.names:
                if isinstance(parameter, _SwitchArgument):
                    if value is None:
                        import warnings

                        warnings.warn(
                            "For a switch type argument like %s, "
                            "we expect a boolean.  None is treated "
                            "as FALSE!" % parameter.names[-1]
                        )
                    parameter.is_set = bool(value)
                    set_option = True
                elif isinstance(parameter, _SwitchValueArgument):
                    if value is None:
                        import warnings

                        warnings.warn(
                            "For a switch type argument like %s, "
                            "we expect a boolean.  None is treated "
                            "as FALSE!" % parameter.names[-1]
                        )
                    elif isinstance(value, bool):
                        parameter.is_set = bool(value)
                    else:
                        self._check_value(value, name,
                                          parameter.checker_function)
                        parameter.value = value
                        parameter.is_set = True
                    set_option = True
                else:
                    if value is not None:
                        self._check_value(value, name,
                                          parameter.checker_function)
                        parameter.value = value
                    parameter.is_set = True
                    set_option = True
        if not set_option:
            param_lst = [str(x.names) for x in self.parameters]
            raise ValueError("""Argument with name '%s' was not found among
                             the different arguments for %s, which are: %s.
                             Use 'custom_args' if your argument is not in
                             the previous list.""" % (
                    name, self.program_name, ", ".join(param_lst)))

    def _check_value(self, value, name, check_function):
        """Check whether the given value is valid (PRIVATE).
        No return value - it either works or raises a ValueError.
        This uses the passed function 'check_function', which can either
        return a [0, 1] (bad, good) value or raise an error. Either way
        this function will raise an error if the value is not valid, or
        finish silently otherwise.
        """
        if check_function is not None:
            is_good = check_function(value)  # May raise an exception
            if is_good not in [0, 1, True, False]:
                raise ValueError(
                    "Result of check_function: %r is of an unexpected value"
                    % is_good
                )
            if not is_good:
                raise ValueError(
                    "Invalid parameter value %r for parameter %s"
                    % (value, name)
                )

    def __setattr__(self, name, value):
        """Set attribute name to value (PRIVATE).
        This code implements a workaround for a user interface issue.
        Without this __setattr__ attribute-based assignment of parameters
        will silently accept invalid parameters, leading to known instances
        of the user assuming that parameters for the application are set,
        when they are not.
        >>> from Bio.Emboss.Applications import WaterCommandline
        >>> cline = WaterCommandline(gapopen=10, gapextend=0.5, stdout=True)
        >>> cline.asequence = "a.fasta"
        >>> cline.bsequence = "b.fasta"
        >>> cline.csequence = "c.fasta"
        Traceback (most recent call last):
        ...
        ValueError: Option name csequence was not found.
        >>> print(cline)
        water -stdout -asequence=a.fasta -bsequence=b.fasta -gapopen=10
                -gapextend=0.5
        This workaround uses a whitelist of object attributes, and sets the
        object attribute list as normal, for these.  Other attributes are
        assumed to be parameters, and passed to the self.set_parameter method
        for validation and assignment.
        """
        if name in CommandLineBase.allowed_attr:  # Allowed attributes
            self.__dict__[name] = value
        else:
            self.set_parameter(name, value)  # treat as a parameter

    def __call__(self, stdin=None, stdout=True, stderr=True, cwd=None,
                 env=None):
        """Execute command, wait for it to finish, return (stdout, stderr).
        Runs the command line tool and waits for it to finish. If it returns
        a non-zero error level, an exception is raised. Otherwise two strings
        are returned containing stdout and stderr.
        The optional stdin argument should be a string of data which will be
        passed to the tool as standard input.
        The optional stdout and stderr argument may be filenames (string),
        but otherwise are treated as a booleans, and control if the output
        should be captured as strings (True, default), or ignored by sending
        it to /dev/null to avoid wasting memory (False). If sent to a file
        or ignored, then empty string(s) are returned.
        The optional cwd argument is a string giving the working directory
        to run the command from. See Python's subprocess module documentation
        for more details.
        The optional env argument is a dictionary setting the environment
        variables to be used in the new process. By default the current
        process' environment variables are used. See Python's subprocess
        module documentation for more details.
        Default example usage::
            from Bio.Emboss.Applications import WaterCommandline
            water_cmd = WaterCommandline(gapopen=10, gapextend=0.5,
                                         stdout=True, auto=True,
                                         asequence="a.fasta",
                                         bsequence="b.fasta")
            print("About to run: %s" % water_cmd)
            std_output, err_output = water_cmd()
        This functionality is similar to subprocess.check_output(). In general
        if you require more control over running the command, use subprocess
        directly.
        When the program called returns a non-zero error level, a custom
        ApplicationError exception is raised. This includes any stdout and
        stderr strings captured as attributes of the exception object, since
        they may be useful for diagnosing what went wrong.
        """
        if not stdout:
            stdout_arg = open(os.devnull, "w")
        elif isinstance(stdout, str):
            stdout_arg = open(stdout, "w")
        else:
            stdout_arg = subprocess.PIPE

        if not stderr:
            stderr_arg = open(os.devnull, "w")
        elif isinstance(stderr, str):
            if stdout == stderr:
                stderr_arg = stdout_arg  # Write both to the same file
            else:
                stderr_arg = open(stderr, "w")
        else:
            stderr_arg = subprocess.PIPE

        if sys.platform != "win32":
            use_shell = True
        else:
            win_ver = platform.win32_ver()[0]
            if win_ver in ["7", "8", "post2012Server", "10"]:
                use_shell = True
            else:
                use_shell = False
        child_process = subprocess.Popen(
            str(self),
            stdin=subprocess.PIPE,
            stdout=stdout_arg,
            stderr=stderr_arg,
            universal_newlines=True,
            cwd=cwd,
            env=env,
            shell=use_shell,
        )
        # Use .communicate as can get deadlocks with .wait(), see Bug 2804
        stdout_str, stderr_str = child_process.communicate(stdin)
        if not stdout:
            assert not stdout_str, stdout_str
        if not stderr:
            assert not stderr_str, stderr_str
        return_code = child_process.returncode

        # Particularly important to close handles on Jython and PyPy
        # (where garbage collection is less predictable) and on Windows
        # (where cannot delete files with an open handle):
        if not stdout or isinstance(stdout, str):
            # We opened /dev/null or a file
            stdout_arg.close()
        if not stderr or (isinstance(stderr, str) and stdout != stderr):
            # We opened /dev/null or a file
            stderr_arg.close()

        if return_code:
            raise ApplicationError(return_code, str(self), stdout_str,
                                   stderr_str)
        return stdout_str, stderr_str


class _ArgumentBase:
    """A class to hold information about a parameter for a commandline.
    Do not use this directly, instead use one of the subclasses.
    """

    def __init__(self):
        raise NotImplementedError

    def __str__(self):
        raise NotImplementedError


class _ContentArgument(_ArgumentBase):
    """Represent an option that can be set for a program.
    This holds UNIXish options like --append=yes and -a yes,
    where a value (here "yes") is generally expected.
    For UNIXish options like -kimura in clustalw which don't
    take a value, use the _SwitchArgument object instead.
    Attributes:
     - names -- a list of string names (typically two entries) by which
       the parameter can be set via the legacy set_parameter method
       (eg ["-a", "--append", "append"]). The first name in list is used
       when building the command line. The last name in the list is a
       "human readable" name describing the option in one word. This
       must be a valid Python identifier as it is used as the property
       name and as a keyword argument, and should therefore follow PEP8
       naming.
     - description -- a description of the option. This is used as
       the property docstring.
     - filename -- True if this argument is a filename (or other argument
       that should be quoted) and should be automatically quoted if it
       contains spaces.
     - checker_function -- a reference to a function that will determine
       if a given value is valid for this parameter. This function can either
       raise an error when given a bad value, or return a [0, 1] decision on
       whether the value is correct.
     - equate -- should an equals sign be inserted if a value is used?
     - is_required -- a flag to indicate if the parameter must be set for
       the program to be run.
     - is_set -- if the parameter has been set
     - value -- the value of a parameter
    """

    def __init__(
        self,
        names,
        description,
        filename=False,
        checker_function=None,
        is_required=False,
        equate=False,
        required_options=None,
        alter_options=None,
        incompatible=None,
        allow_multiple=False,
        default=None
    ):
        self.names = names
        if not isinstance(description, str):
            raise TypeError("Should be a string: %r for %s" % (description, names[-1]))
        # Note 'filename' is for any string with spaces that needs quoting
        self.is_filename = filename
        self.checker_function = checker_function
        self.description = description
        self.equate = equate
        self.is_required = is_required
        self.is_set = False
        self.value = None
        self.required_options = required_options
        self.alter_options = alter_options
        self.incompatible = incompatible
        self.default = default
        self.allow_multiple = allow_multiple

    def __str__(self):
        """Return the value of this option for the commandline.
        Includes a trailing space.
        """
        # Note: Before equate was handled explicitly, the old
        # code would do either "--name " or "--name=value ",
        # or " -name " or " -name value ".  This choice is now
        # now made explicitly when setting up the option.
        if self.value is None:
            return "%s " % self.names[0]
        if isinstance(self.value, list):
            if self.allow_multiple:
                if self.is_filename:
                    v = " ".join(_escape_filename(val) for val in self.value) + " "
                else:
                    v = " '" + " ".join(self.value) + "' "
            else:
                raise TypeError("This argument cannot be a list")
        else:
            if self.is_filename:
                v = _escape_filename(self.value)
            else:
                v = str(self.value)
        if self.equate:
            return "%s=%s " % (self.names[0], v)
        else:
            return "%s %s " % (self.names[0], v)


class _SwitchValueArgument(_ArgumentBase):
    """Represent an optional argument switcht that can introduce a value for a
    program. This holds UNIXish options like -proxi in kma can either be
    included in the command string or ommitted; and when included, can have a
    value or not.
    Attributes:
     - names -- a list of string names (typically two entries) by which
       the parameter can be set via the legacy set_parameter method
       (eg ["-a", "--append", "append"]). The first name in list is used
       when building the command line. The last name in the list is a
       "human readable" name describing the option in one word. This
       must be a valid Python identifier as it is used as the property
       name and as a keyword argument, and should therefore follow PEP8
       naming.
     - description -- a description of the option. This is used as
       the property docstring.
     - filename -- True if this argument is a filename (or other argument
       that should be quoted) and should be automatically quoted if it
       contains spaces.
     - checker_function -- a reference to a function that will determine
       if a given value is valid for this parameter. This function can either
       raise an error when given a bad value, or return a [0, 1] decision on
       whether the value is correct.
     - equate -- should an equals sign be inserted if a value is used?
     - is_required -- a flag to indicate if the parameter must be set for
       the program to be run.
     - is_set -- if the parameter has been set
     - value -- the value of a parameter"""

    def __init__(
        self,
        names,
        description,
        filename=False,
        checker_function=None,
        is_required=False,
        equate=False,
        default=False,
        incompatible=None,
    ):
        self.names = names
        if not isinstance(description, str):
            raise TypeError("Should be a string: %r for %s" % (description,
                                                               names[-1]))
        # Note 'filename' is for any string with spaces that needs quoting
        self.is_filename = filename
        self.checker_function = checker_function
        self.description = description
        self.equate = equate
        self.is_required = is_required
        self.is_set = False
        self.value = None
        self.default = default
        self.incompatible = incompatible

    def __str__(self):
        """Return the value of this option for the commandline.
        Includes a trailing space.
        """
        # Note: Before equate was handled explicitly, the old
        # code would do either "--name " or "--name=value ",
        # or " -name " or " -name value ".  This choice is now
        # now made explicitly when setting up the option.
        if not self.is_set:
            return "%s False" % self.names[0]
        if self.value is None:
            return "%s " % (self.names[0])
        if self.is_filename:
            v = _escape_filename(self.value)
        else:
            v = str(self.value)
        if self.equate:
            return "%s=%s " % (self.names[0], v)
        else:
            return "%s %s " % (self.names[0], v)


class _SwitchArgument(_ArgumentBase):
    """Represent an optional argument switch for a program.
    This holds UNIXish options like -kimura in clustalw which don't
    take a value, they are either included in the command string
    or omitted.
    Attributes:
     - names -- a list of string names (typically two entries) by which
       the parameter can be set via the legacy set_parameter method
       (eg ["-a", "--append", "append"]). The first name in list is used
       when building the command line. The last name in the list is a
       "human readable" name describing the option in one word. This
       must be a valid Python identifier as it is used as the property
       name and as a keyword argument, and should therefore follow PEP8
       naming.
     - description -- a description of the option. This is used as
       the property docstring.
     - is_set -- if the parameter has been set
     - no_run -- if the argument exits the program
    NOTE - There is no value attribute, see is_set instead,
    """

    def __init__(self, names, description, default=False, no_run=False,
                 incompatible=None):
        self.names = names
        self.description = description
        self.is_set = False
        self.is_required = False
        self.no_run = no_run
        self.default = default
        self.incompatible = incompatible

    def __str__(self):
        """Return the value of this option for the commandline.
        Includes a trailing space.
        """
        assert not hasattr(self, "value")
        if self.is_set:
            return "%s " % self.names[0]
        else:
            return ""


class _Argument(_ArgumentBase):
    """Represent an argument on a commandline.
    The names argument should be a list containing one string.
    This must be a valid Python identifier as it is used as the
    property name and as a keyword argument, and should therefore
    follow PEP8 naming.
    """

    def __init__(
        self,
        names,
        description,
        filename=False,
        checker_function=None,
        is_required=False,
    ):
        self.names = names
        if not isinstance(description, str):
            raise TypeError("Should be a string: %r for %s" % (description,
                                                               names[-1]))
        # Note 'filename' is for any string with spaces that needs quoting
        self.is_filename = filename
        self.checker_function = checker_function
        self.description = description
        self.is_required = is_required
        self.is_set = False
        self.value = None
        self.no_run = False

    def __str__(self):
        if self.value is None:
            return " "
        elif self.is_filename:
            return "%s " % _escape_filename(self.value)
        else:
            return "%s " % self.value


class _ArgumentList(_Argument):
    """Represent a variable list of arguments on a command line, e.g. multiple
    filenames."""

    # TODO - Option to require at least one value? e.g. min/max count?

    def __str__(self):
        if not isinstance(self.value, list):
            raise TypeError("Arguments should be a list")
        if not self.value:
            raise ValueError("Requires at least one filename")
        # A trailing space is required so that parameters following the last filename
        # do not appear merged.
        # e.g.:  samtools cat in1.bam in2.bam-o out.sam  [without trailing space][Incorrect]
        #        samtools cat in1.bam in2.bam -o out.sam  [with trailing space][Correct]
        if self.is_filename:
            return " ".join(_escape_filename(v) for v in self.value) + " "
        else:
            return " ".join(self.value) + " "


class _StaticArgument(_ArgumentBase):
    """Represent a static (read only) argument on a commandline.
    This is not intended to be exposed as a named argument or
    property of a command line wrapper object.
    """

    def __init__(self, value):
        self.names = []
        self.is_required = False
        self.is_set = True
        self.value = value

    def __str__(self):
        return "%s " % self.value


def _escape_filename(filename):
    """Escape filenames with spaces by adding quotes (PRIVATE).
    Note this will not add quotes if they are already included:
    >>> print((_escape_filename('example with spaces')))
    "example with spaces"
    >>> print((_escape_filename('"example with spaces"')))
    "example with spaces"
    >>> print((_escape_filename(1)))
    1
    Note the function is more generic than the name suggests, since it
    is used to add quotes around any string arguments containing spaces.
    """

    if not isinstance(filename, str):
        # for example the NCBI BLAST+ -outfmt argument can be an integer
        return filename
    if " " not in filename:
        return filename
    # We'll just quote it - works on Windows, Mac OS X etc
    if filename.startswith('"') and filename.endswith('"'):
        # Its already quoted
        return filename
    else:
        return '"%s"' % filename


def _test():
    """Run the Bio.Application module's doctests (PRIVATE)."""
    import doctest

    doctest.testmod(verbose=1)


if __name__ == "__main__":
    # Run the doctests
    _test()
