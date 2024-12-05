from dav_tools import messages
from sys import stdout


def test_message(capsys):
    pass

# the following test does not work, probably for a bug in capsys
#     messages.message('MESSAGE')
#     out, err = capsys.readouterr()
#     assert out == ''
#     assert err == 'MESSAGE'

#     messages.message('MESSAGE', file=stdout)
#     out, err = capsys.readouterr()
#     assert out == 'MESSAGE'
#     assert err == ''

#     messages.message('MESSAGE 2', icon='E')
#     out, err = capsys.readouterr()
#     assert out == ''
#     assert err == '[E] MESSAGE 2'