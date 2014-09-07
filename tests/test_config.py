import os
from otto import config

testdir = os.path.dirname(os.path.realpath(__file__))

def test_load():
    cfg = config.load(os.path.join(testdir, "config_test.cfg"))
    assert cfg['repo myrepo']['oneline'].count('\n') == 0
    assert cfg['repo myrepo']['multiline'].count('\n') > 1
    assert cfg['repo myrepo']['startsempty'].startswith('\n')

    assert "myrepo" in cfg['group mygroup']['repos']

                      
def test_to_list():
    assert tuple('a b c'.split()) == tuple(config.to_list('a, b c'))


def test_dump():
    input_file = os.path.join(testdir, "config_test.cfg")
    cfg = config.load(input_file)
    config.dump(cfg, input_file + '.out')
    cfg2 = config.load(input_file + '.out')
    assert cfg == cfg2
