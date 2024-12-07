Assorted process and subprocess management functions.

*Latest release 20241206*:
run(): accept new remote= and ssh_exe= parameters to support remote execution, default via @uses_cmd_options(ssh_exe).

Not to be confused with the excellent
(psutil)[https://pypi.org/project/psutil/] package.

## <a name="groupargv"></a>`groupargv(pre_argv, argv, post_argv=(), max_argv=None, encode=False)`

Distribute the array `argv` over multiple arrays
to fit within `MAX_ARGV`.
Return a list of argv lists.

Parameters:
* `pre_argv`: the sequence of leading arguments
* `argv`: the sequence of arguments to distribute; this may not be empty
* `post_argv`: optional, the sequence of trailing arguments
* `max_argv`: optional, the maximum length of each distributed
  argument list, default from `MAX_ARGV`: `131072`
* `encode`: default `False`.
  If true, encode the argv sequences into bytes for accurate tallying.
  If `encode` is a Boolean,
  encode the elements with their .encode() method.
  If `encode` is a `str`, encode the elements with their `.encode()`
  method with `encode` as the encoding name;
  otherwise presume that `encode` is a callable
  for encoding each element.

The returned argv arrays will contain the encoded element values.

## <a name="PidFileManager"></a>`PidFileManager(path, pid=None)`

Context manager for a pid file.

Parameters:
* `path`: the path to the process id file.
* `pid`: the process id to store in the pid file,
  default from `os.etpid`.

Writes the process id file at the start
and removes the process id file at the end.

## <a name="pipefrom"></a>`pipefrom(argv, *, quiet: bool, remote=None, ssh_exe, text=True, stdin=-3, **popen_kw)`

Pipe text (usually) from a command using `subprocess.Popen`.
Return the `Popen` object with `.stdout` as a pipe.

Parameters:
* `argv`: the command argument list
* `quiet`: optional flag, default `False`;
  if true, print the command to `stderr`
* `text`: optional flag, default `True`; passed to `Popen`.
* `stdin`: optional value for `Popen`'s `stdin`, default `DEVNULL`
Other keyword arguments are passed to `Popen`.

Note that `argv` is passed through `prep_argv` before use,
allowing direct invocation with conditional parts.
See the `prep_argv` function for details.

## <a name="pipeto"></a>`pipeto(argv, *, quiet: bool, remote=None, ssh_exe, **kw)`

Pipe text to a command.
Optionally trace invocation.
Return the Popen object with .stdin encoded as text.

Parameters:
* `argv`: the command argument list
* `trace`: if true (default `False`),
  if `trace` is `True`, recite invocation to stderr
  otherwise presume that `trace` is a stream
  to which to recite the invocation.

Other keyword arguments are passed to the `io.TextIOWrapper`
which wraps the command's input.

Note that `argv` is passed through `prep_argv` before use,
allowing direct invocation with conditional parts.
See the `prep_argv` function for details.

## <a name="prep_argv"></a>`prep_argv(*argv, ssh_exe, remote=None)`

A trite list comprehension to reduce an argument list `*argv`
to the entries which are not `None` or `False`
and to flatten other entries which are not strings.

This exists ease the construction of argument lists
with methods like this:

    >>> command_exe = 'hashindex'
    >>> hashname = 'sha1'
    >>> quiet = False
    >>> verbose = True
    >>> prep_argv(
    ...     command_exe,
    ...     quiet and '-q',
    ...     verbose and '-v',
    ...     hashname and ('-h', hashname),
    ... )
    ['hashindex', '-v', '-h', 'sha1']

where `verbose` is a `bool` governing the `-v` option
and `hashname` is either `str` to be passed with `-h hashname`
or `None` to omit the option.

If `remote` is not `None` it is taken to be a remote host on
which to run `argv`. This is done via the `ssh_exe` argument,
which defaults to the string `'ssh'`. The value of `ssh_exe`
is a command string parsed with `shlex.split`. A new `argv`
is computed as:

    [
        *shlex.split(ssh_exe),
        remote,
        '--',
        shlex.join(argv),
    ]

## <a name="print_argv"></a>`print_argv(*argv, indent='', subindent='  ', end='\n', file=None, fold=False, print=None)`

Print an indented possibly folded command line.

## <a name="remove_pidfile"></a>`remove_pidfile(path)`

Truncate and remove a pidfile, permissions permitting.

## <a name="run"></a>`run(argv, *, check=True, doit: bool, input=None, logger=None, print=None, quiet: bool, remote=None, ssh_exe=None, stdin=None, **subp_options)`

Run a command via `subprocess.run`.
Return the `CompletedProcess` result or `None` if `doit` is false.

Positional parameter:
* `argv`: the command line to run

Note that `argv` is passed through `prep_argv(argv,remote=remote,ssh_exe=ssh_exe)`
before use, allowing direct invocation with conditional parts.
See the `prep_argv` function for details.

Keyword parameters:
* `check`: passed to `subprocess.run`, default `True`;
  NB: _unlike_ the `subprocess.run` default, which is `False`
* `doit`: optional flag, default `True`;
  if false do not run the command and return `None`
* `input`: default `None`: alternative to `stdin`;
  passed to `subprocess.run`
* `logger`: optional logger, default `None`;
  if `True`, use `logging.getLogger()`;
  if not `None` or `False` trace using `print_argv`
* `quiet`: default `False`; if false, print the command and its output
* `remote`: optional remote target on which to run `argv`
* `ssh_exe`: optional command string for the remote shell
* `stdin`: standard input for the subprocess, default `subprocess.DEVNULL`;
  passed to `subprocess.run`

Other keyword parameters are passed to `subprocess.run`.

## <a name="signal_handler"></a>`signal_handler(sig, handler, call_previous=False)`

Context manager to push a new signal handler,
yielding the old handler,
restoring the old handler on exit.
If `call_previous` is true (default `False`)
also call the old handler after the new handler on receipt of the signal.

Parameters:
* `sig`: the `int` signal number to catch
* `handler`: the handler function to call with `(sig,frame)`
* `call_previous`: optional flag (default `False`);
  if true, also call the old handler (if any) after `handler`

## <a name="signal_handlers"></a>`signal_handlers(sig_hnds, call_previous=False, _stacked=None)`

Context manager to stack multiple signal handlers,
yielding a mapping of `sig`=>`old_handler`.

Parameters:
* `sig_hnds`: a mapping of `sig`=>`new_handler`
  or an iterable of `(sig,new_handler)` pairs
* `call_previous`: optional flag (default `False`), passed
  to `signal_handler()`

## <a name="stop"></a>`stop(pid, signum=<Signals.SIGTERM: 15>, wait=None, do_SIGKILL=False)`

Stop the process specified by `pid`, optionally await its demise.

Parameters:
* `pid`: process id.
  If `pid` is a string, treat as a process id file and read the
  process id from it.
* `signum`: the signal to send, default `signal.SIGTERM`.
* `wait`: whether to wait for the process, default `None`.
  If `None`, return `True` (signal delivered).
  If `0`, wait indefinitely until the process exits as tested by
  `os.kill(pid, 0)`.
  If greater than 0, wait up to `wait` seconds for the process to die;
  if it exits, return `True`, otherwise `False`;
* `do_SIGKILL`: if true (default `False`),
  send the process `signal.SIGKILL` as a final measure before return.

## <a name="write_pidfile"></a>`write_pidfile(path, pid=None)`

Write a process id to a pid file.

Parameters:
* `path`: the path to the pid file.
* `pid`: the process id to write, defautl from `os.getpid`.

# Release Log



*Release 20241206*:
run(): accept new remote= and ssh_exe= parameters to support remote execution, default via @uses_cmd_options(ssh_exe).

*Release 20241122*:
* print_argv: new print= parameter to provide a print() function, refactor to use print instead of file.write.
* run: new optional print parameter, plumb to print_argv.
* Use @uses_doit and @uses_quiet to provide the default quiet and doit states.

*Release 20240316*:
Fixed release upload artifacts.

*Release 20240211*:
* run: new optional input= parameter to presupply input data.
* New prep_argv(*argv) function to flatten and trim computes argv lists; use automatically in run(), pipeot(), pipefrom().

*Release 20231129*:
run(): default stdin=subprocess.DEVNULL.

*Release 20230612*:
* pipefrom: default stdin=DEVNULL.
* Make many parameters keyword only.

*Release 20221228*:
* signal_handlers: bugfix iteration of sig_hnds.
* Use cs.gimmicks instead of cs.logutils.
* Drop use of cs.upd, fixes circular import; users of run() may need to call "with Upd().above()" themselves.

*Release 20221118*:
run: do not print cp.stdout.

*Release 20220805*:
run: print trace to stderr.

*Release 20220626*:
run: default quiet=True.

*Release 20220606*:
* run: fold in the superior run() from cs.ebooks.
* pipefrom,pipeto: replace trace= with quiet= like run().
* print_argv: add an `end` parameter (used by pipefrom).

*Release 20220531*:
* New print_argv function for writing shell command lines out nicely.
* Bump requirements for cs.gimmicks.

*Release 20220504*:
signal_handlers: reshape try/except to avoid confusing traceback.

*Release 20220429*:
* New signal_handler(sig,handler,call_previous=False) context manager to push a signal handler.
* New signal_handlers() context manager to stack handlers for multiple signals.

*Release 20190101*:
Bugfix context manager cleanup. groupargv improvements.

*Release 20171112*:
Bugfix array length counting.

*Release 20171110*:
New function groupargv for breaking up argv lists to fit within the maximum argument limit; constant MAX_ARGV for the default limit.

*Release 20171031*:
run: accept optional pids parameter, a setlike collection of process ids.

*Release 20171018*:
run: replace `trace` parameter with `logger`, default None

*Release 20170908.1*:
remove dependency on cs.pfx

*Release 20170908*:
run: pass extra keyword arguments to subprocess.call

*Release 20170906.1*:
Add run, pipefrom and pipeto - were incorrectly in another module.

*Release 20170906*:
First PyPI release.
