""" Test Suite Configuration:
Key Functions:
`pytest_generate_tests(metafunc)` works to generate our tests with specific 'fixtures' or arangements/inputs (ie. run all tests 5 times)
`pytest_addoption` works to set-up our custom flags and test config values found in the .ini file
`pytest_configure` is responsible for reading config/.ini vars and setting them to be used by the suite (use of helper functions may be useful here for suites with many configuration areas)

GLOBAL VARIABLES:
PYTEST_ENV - global var holds the env our test suite should be run in
PYTEST_SUITE_INFO - global var holds info related to running our test (time, os, connectivity, etc.)

THINGS TO CONSIDER:
Logging & console output?
- Ideally we would remove the PYTEST_SUITE_INFO dict and have it's conntents be info level logs that are printed at the beginning with pytest standard output
- ^ We should consider using a with statement so that pytest doesn't print all INFO related logs that could occur
- Consider using the `record_testsuite_property("ARCH", "PPC")` to add the specific logging we want to be captured in a file.
Hooks vs. Fixtures vs. helper functions?
- Hooks are directly related to test configuration, because of this we should consider using hooks over fixtures in this conftest file
- ^ ie. use the two separate set-up and tear-down hooks rather than our combined set_up_tear_down fixture
- Helper functions should be used to group code, but again we should try to use the pre-defined hooks (or perhaps create custom hooks) rather than use many helper fucntions and fixtures
Fixtures vs Gloabl Vars?
- Fixtures do provide a space separate from the global name space
- However, if a fixture is simply setting a single value/var to be used (and not completing some task/process), global vars may be a simpler way for our tests to access/be passed these values
Flags to use when running?
- depends on how we design our output
-^ Ideally we get rid of print statements to report and are able to use logging (no need for -s or -rP flags)
- On debuggign failures, -rx flag should be added to print captured output from failed tests while debugging.
- `--verbose` may be useful for noobies using pytest, as it gives a non-abbreviated output format.
- `--resultlog=path` should be used if we configure our `specific_info` to be recorded with `record_testsuite_property()`


"""
import pytest, os, sys, pendulum, pyspeedtest, psutil
from pathlib import Path


def pytest_addoption(parser):
    """ Special function adds custom flags to pytest arg """
    parser.addini('env', help='sets the env for our test suite')
    parser.addini('valid_envs', help='defines valid envs for our test suite')
    parser.addini('browser', help='sets browser for our test suite (all, chrome, firefox, safari)')
    parser.addini('username', help='sets the username for our test suite (used for logins/requests)')
    parser.addini('password', help='sets the password for our test suite (used for logins/requests)')
    parser.addoption("--repeat", action="store", help="enter an integer")
    parser.addoption("--env", action="store", help="enter an env ()")

def pytest_configure(config):
    """ Sets custom markers and calls setenv() function. Reads app ini file and adds values to test ini."""
    config.addinivalue_line(
        "markers",
        "single_run: mark test to only run once"
    )#TODO Should we consider just adding this directly to .ini
    set_env(config)

def set_env(config):
    """ Sets our test env """
    global PYTEST_ENV
    valid_envs = config.getini('valid_envs')
    cmd_env = config.getoption("--env") # Commandline env var
    if cmd_env is not None:
        if cmd_env:
            print("test env set in terminal")
            PYTEST_ENV = cmd_env
    elif 'PYTEST_ENV' in os.environ and os.environ['PYTEST_ENV'] in valid_envs: # Platform Env variable setting test env var
            print(f"test env set to `{os.environ['PYTEST_ENV']}` in env var")
            PYTEST_ENV = os.environ['PYTEST_ENV']
    else:
        env = config.getini('env') # Checking .ini for env var, setting to default otherwise
        if env != '' and env in valid_envs:
            print(f'Using `{env}` value as env')
        else:
            print('Default env set to') #TODO set from app ini file as default

def pytest_generate_tests(metafunc):
    """ Special function generates the tests with below configurations """
    pass
    #if metafunc.config.option.repeat is not None:
    #   count = int(metafunc.config.option.repeat)
    #   if not request.node.get_closest_marker("single_run"):
    #       metafunc.fixturenames.append('tmp_ct')
    #       metafunc.parametrize('tmp_ct', range(int(metafunc.config.option.multirun)))

def get_ini(key, config):
    """ Returns value at given key (if the key exists) in the ini"""
    try:
        return config.getini(str(key))
    except: #TODO add key not found error
        #Throw warning
        return None

def general_info():
    """ Information we'd like to display with existing pytest output """
    global PYTEST_SUITE_INFO
    PYTEST_SUITE_INFO = {}
    PYTEST_SUITE_INFO['dir_path'] = Path(__file__).parent.absolute()
    PYTEST_SUITE_INFO['cwd'] = Path().absolute()
    # PYTEST_SUITE_INFO['suite_root_path'] = Config.rootpath
    # PYTEST_SUITE_INFO['suite_ini_file'] = Config.inipath
    PYTEST_SUITE_INFO['os'] = sys.platform
    PYTEST_SUITE_INFO['start_time'] = pendulum.now('America/Toronto')
    st = pyspeedtest.SpeedTest('www.speedtest.net')
    PYTEST_SUITE_INFO['ping'] = st.ping()

def specific_info():
    """ Information which may be useful to look at if we notice odd/inconsistent test results """
    #TODO consider using
    global PYTEST_SUITE_INFO
    try:
        f = open(str(Path('test_logs/'+str(PYTEST_SUITE_INFO['start_time']))), 'w+') # Better if this was being stored on a shared drive
        content = ''
    # content = psutil.....
    #measures things like memory, cpu, connectivity type, etc.
    # We can also add some of these to our info dict if we'd like
    #...
        f.write(content)
        f.close()
    except FileNotFoundError:
        # Github actions doesn't have test_logs directory
        pass

@pytest.fixture(autouse=True, scope='session')
def setup_teardown():
    """ Example setup & teardown function, run once per test suite execution"""
    general_info()
    specific_info()
    yield #---- Start Teardown ----
    global PYTEST_SUITE_INFO
    PYTEST_SUITE_INFO['end_time'] = pendulum.now('America/Toronto')
    for k, v in PYTEST_SUITE_INFO.items():
        print(k, v)
