## qecore - Library of tools

[![Build Status](https://img.shields.io/gitlab/pipeline/dogtail/qecore)](https://gitlab.com/dogtail/qecore/-/pipelines) [![PyPI Version](https://img.shields.io/pypi/v/qecore)](https://pypi.org/project/qecore/)

Qecore is a Library of Tools designed to complement our automation stack with all that is required.

## Usage
### The `qecore-headless` script.
- The name `headless` in the name is historical, it is a session configuration script that runs our automation stack.
- This script provides a way to start a new session in ssh connected machine.
- It serves only for remote usage, using it locally will not end well. It is designed for fast GDM start and stop with user autologin.
- This script will start GDM and make a few changes to the system to enable start of an automation suite in wanted configuration, for example:
  - `qecore-headless "behave -kt automated_test"` - This script takes an argument of a script to run.
    - In this case we run `automated_test` via behave. Bash is the default - in bash we can start behave on our own.
  - `qecore-headless --session-type xorg` - Start X11 session.
  - `qecore-headless --session-type wayland` - Start Wayland session.
  - `qecore-headless --session-desktop gnome` - Change desktop to GNOME.
  - `qecore-headless --session-desktop gnome-classic` - Change desktop to GNOME Classic.
  - `qecore-headless --display` - Set a DISPLAY number for the session, default is `:0`.
  - `qecore-headless --dont-start` - Do not start GDM.
  - `qecore-headless --dont-kill` - Do not kill GDM.
  - `qecore-headless --restart` - Restart running GDM
  - `qecore-headless --keep X` - Keep GDM alive for X tests, restart it after.
  - `qecore-headless --keep-max` - Keep GDM alive for as long as possible when testing - restart on test fail.
  - `qecore-headless --force` - Force will check configuration match and fails if for example X11 is started instead of Wayland.
  - `qecore-headless --debug` - Sets environment variable for dogtail, upon which dogtail will be logged.
  - `qecore-headless --no-color` - No colors for headless output.
  - `qecore-headless --virtual-monitors X` - Experimental option to enable virtual monitors for multi-monitor setup testing.
  - `qecore-headless --help` - for more information.

You can of course combine any of these together, if it makes sense.

### Usage with `behave`.

The `behave` expected structure is very simple, we adjust it a bit for better readability:
```
features
├── environment.py
├── scenarios
|   └── main.feature
└── steps
    └── steps.py
```

The main file that `qecore` interacts with is `environment.py`.
#### `behave` has a few hooks that we can use to start our automation stack - lets look at `before_all`


```python
from qecore.sandbox import TestSandbox

def before_all(context) -> None:
    """
    This function will be run once in every 'behave' command called.
    """

    # This is the most important part, initiation of TestSandbox.
    # Most of the setup happens in this class.
    context.sandbox = TestSandbox("gnome-terminal", context=context)

    # To define an application for testing, use `get_application` from sandbox.
    # If application is not installed as rpm but as a flatpak user can use `get_flatpak`
    # Attention: Do not define gnome-shell as an application.
    # The gnome-shell accessibility tree is available for you in `context.sandbox.shell`
    context.terminal = context.sandbox.get_application(
        name="gnome-terminal",
        a11y_app_name="gnome-terminal-server",
        desktop_file_name="org.gnome.Terminal.desktop",
    )
    # To modify the application with some functionality or work around some issues.
    # Most of the time no changes should be needed.
    context.terminal.exit_shortcut = "<Ctrl><Shift><Q>"
```

#### Let's look at `before_scenario` next.

The `before_scenario` will take care of every setup we need, to modify the execution, change the [TestSandbox attributes](https://dogtail.gitlab.io/qecore/_modules/sandbox.html#TestSandbox.__init__) after initiating the class.

All the attributes are set to values that were proven over the years of development. Some corner cases always exist though, so everything is customizable/hackable to enable a large variety of options.

```python
def before_scenario(context, scenario) -> None:
    """
    This function will be run before every scenario in 'behave' command called.
    """
    context.sandbox.before_scenario(context, scenario)
```

To see everything it does, you can look at [before_scenario](https://dogtail.gitlab.io/qecore/_modules/sandbox.html#TestSandbox.before_scenario) implementation in documentation page.

#### And a final part `after_scenario`.

The `after_scenario` will take care of teardown. It will take care of anything that was set in `before_scenario` like stopping videos, fetching logs for our reports, uploading data to our HTML logs and closing any application started so that the session is cleared for the next test.

```python
def after_scenario(context, scenario) -> None:
    """
    This function will be run after every scenario in 'behave' command called.
    """
    context.sandbox.after_scenario(context, scenario)
```

To see everything it does, you can look at [after_scenario](https://dogtail.gitlab.io/qecore/_modules/sandbox.html#TestSandbox.after_scenario) implementation in documentation page.

In the [full example](https://gitlab.com/dogtail/qecore/-/blob/master/templates/environment.py) you can also see try/except usage. That is for recovery. Some issues can be fixed while running. We also need a way to end gracefully so that our data is loaded to the HTML page and not thrown away in case of a problem.


#### Working in `steps.py`.

After the setup in `environment.py` we can now start working on our automation in `steps.py`

The setup is important for two reasons.
- Now the test has all machine setup available through the sandbox, so they can query attributes or use sandbox methods that are very useful for testing.
  - `context.sandbox.<attribute>`
  - `context.sandbox.<method>`
- Users now do not have to start the applications and load accessibility tree to use, as they were defined in `environment.py`
  - In `main.feature` users can now use for example `* Start application "terminal" via "command"`
    - Application will start.
    - Load its accessibility tree.
    - Mark the application for cleanup after the test.
    - In `steps.py` users now have `context.terminal.instance` which is accessibility tree root of `gnome-terminal-server` so any `dogtail` query to `Atspi` will now work and automation can begin.


## Environment variables.

There is a lot of options we have to modify our runs without the need to change python code.

- `RICH_TRACEBACK=true behave...` - to enable rich Traceback for debugging of issues.
- `AUTORETRY=X behave...` - give an automation test X tries to pass before it is marked as a FAIL.
  - This option is also available as a `tag` in feature files `@autoretry=X`
- `STABILITY=X behave...` - run an automation test X times and every try has to pass for it to be marked as a PASS.
  - This option is also available as a `tag` in feature files `@stability=X`
- `QECORE_EMBED_ALL=true behave...` - all available data is embedded even if the suite PASSED (We do not embed on PASS by default).
- `QECORE_NO_CACHE=true behave...` - do not keep cache and regenerate files.
- `LOGGING=true behave...` - enables logging, this is a very verbose log about `qecore` execution.
- `PRODUCTION=false behave...` - disables all embedding, video recording, screenshot capture.
- `BACKTRACE=true behave...` - enables backtrace fetching from coredumpctl list.

You are able to use multiple variables, if the combination makes sense, together.

## Hacking.

From everything that I showed here, everything is customizable to some degree.

I implemented most the methods in a way that changing how they operate is done easily from `environment.py`

In case you need some specific change, look through the code and you should be able to identify what needs to be done (everything is in one place really, `sandbox`, `before_scenario`, `after_scenario`, that's it, everything else is called from there)


## This project was featured in Fedora Magazine:
  - https://fedoramagazine.org/automation-through-accessibility/
  - Full technical solution of our team's (Red Hat DesktopQE) automation stack https://modehnal.github.io/


### Execute unit tests

NOTE: This need to be updated for Fedora 40 and newer and RHEL-10 and newer.

Execute the tests (from the project root directory) on machine with dogtail:

```bash
rm -f /tmp/qecore_version_status.txt
rm -f dist/*.whl
python3 -m build
python3 -m pip install --force-reinstall --upgrade dist/qecore*.whl
sudo -u test scripts/qecore-headless "behave -f html-pretty -o /tmp/report_qecore.html -f plain tests/features"
```

You can use `-f pretty` instead of `-f plain` to get colored output.

The standard output should not contain any python traceback, produced HTML should be complete (after first scenario there is `Status`).
