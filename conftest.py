import pytest, os, sys, pendulum, pyspeedtest, psutil
from pathlib import Path


def pytest_addoption(parser):
    """ Special function adds custom flags to pytest arg """
    parser.addini('env', help='valid envs include ()')
    parser.addoption("--repeat", action="store", help="enter an integer")
    parser.addoption("--env", action="store", help="enter an env ()")

def pytest_configure(config):
    """ Sets custom markers and calls setenv() function. Reads app ini file and adds values to test ini."""
    config.addinivalue_line(
        "markers",
        "single_run: mark test to only run once"
    )
    set_env(config)

def set_env(config):
    """ Sets our test env """
    global PYTEST_ENV
    valid_envs = {'valid', 'env', 'set'}
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
    global pytest_suite_info
    pytest_suite_info = {}
    pytest_suite_info['dir_path'] = Path(__file__).parent.absolute()
    pytest_suite_info['cwd'] = Path().absolute()
    # pytest_suite_info['suite_root_path'] = Config.rootpath
    # pytest_suite_info['suite_ini_file'] = Config.inipath
    pytest_suite_info['os'] = sys.platform
    pytest_suite_info['start_time'] = pendulum.now('America/Toronto')
    st = pyspeedtest.SpeedTest('www.speedtest.net')
    pytest_suite_info['ping'] = st.ping()

def specific_info():
    """ Information which may be useful to look at if we notice odd/inconsistent test results """
    global pytest_suite_info
    try:
        f = open(str(Path('test_logs/'+str(pytest_suite_info['start_time']))), 'w+') # Better if this was being stored on a shared drive
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
    global pytest_suite_info
    pytest_suite_info['end_time'] = pendulum.now('America/Toronto')
    for k, v in pytest_suite_info.items():
        print(k, v)
