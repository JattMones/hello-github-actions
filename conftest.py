import pytest, os, sys, pendulum, pyspeedtest, psutil
from pathlib import Path

def pytest_addoption(parser):
    """ Special function adds custom flags to pytest arg """
    #parser.addoption("--multirun", action="store", default="1", help="enter a number")
    pass

def pytest_generate_tests(metafunc):
    """ Special function generates the tests with below configurations """
    pass
    #if metafunc.config.option.multirun == "1":
    #        pass
    #else:
    #    metafunc.fixturenames.append('tmp_ct')
    #    metafunc.parametrize('tmp_ct', range(int(metafunc.config.option.multirun)))

#@pytest.fixture(scope='session')
#def pytest_setup():
#    """ Example setup function, run once per test suite execution"""
#    pass

def general_info():
    """ Information we'd like to display with existing pytest output """
    global pytest_suite_info
    pytest_suite_info = {}
    pytest_suite_info['Path'] = os.path.dirname(os.path.realpath(__file__))
    pytest_suite_info['OS'] = sys.platform
    pytest_suite_info['StartTime'] = pendulum.now('America/Toronto')
    st = pyspeedtest.SpeedTest('www.speedtest.net')
    pytest_suite_info['Ping'] = st.ping()

def specific_info():
    """ Information which may be useful to look at if we notice odd/inconsistent test results """
    global pytest_suite_info
    try:
        f = open(str(Path('test_logs/'+str(pytest_suite_info['StartTime']))), 'w+') # Better if this was being stored on a shared drive
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
    pytest_suite_info['EndTime'] = pendulum.now('America/Toronto')
    for k, v in pytest_suite_info.items():
        print(k, v)
