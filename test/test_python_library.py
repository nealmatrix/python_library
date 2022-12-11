import os
import sys

# Insert feed_handlers path
test_path = sys.path[0]
python_library_path = os.path.dirname(test_path)
sys.path.insert(0, python_library_path)

from configobj import ConfigObj

# ==================== Test Const ====================
class Test:
    BASIC = 'BASIC'
    SLACK = 'SLACK'

test = Test.SLACK
print(f'test python library: {test}')

# ==================== Initialize ====================
cfg = ConfigObj('test/test_python_library.cfg', interpolation = False)

# ==================== Test ====================
if test == Test.BASIC:
    pass

elif test == Test.SLACK:
    from neal_python_library.utils import SlackReporter

    slack_reporter = SlackReporter(cfg)
    slack_reporter.report(subject = 'test subject cat', text = 'test text')

