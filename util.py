import os
import os.path
import hashlib

_rootdir = '.'
_datadir = 'data'
_downdir = 'down'

def _get_hex(uid):
    md5 = hashlib.md5()
    md5.update(uid.encode())
    uid = md5.hexdigest()
    value = int(uid, 16)
    return value

def get_friends_file(uid):
    value = _get_hex(uid)
    return  "{1}{0}{2}{0}{3:X}.txt".format(os.sep, _rootdir, _datadir, value)

def get_group_file(uid):
    value = _get_hex(uid)
    return  "{1}{0}{2}{0}{3:X}-G.txt".format(os.sep, _rootdir, _datadir, value)

def init_dir():
    dir = "{1}{0}{2}".format(os.sep, _rootdir, _datadir)
    if not os.path.exists(dir):
        os.mkdir(dir)
    dir = "{1}{0}{2}".format(os.sep, _rootdir, _downdir)
    if not os.path.exists(dir):
        os.mkdir(dir)

def create_dir(groupname, nickname):
    dir = '{1}{0}{2}{0}{3}'.format(os.sep, _rootdir, _downdir, groupname)
    if not os.path.exists(dir):
        os.mkdir(dir)
    dir = '{1}{0}{2}'.format(os.sep, dir, nickname)
    if not os.path.exists(dir):
        os.mkdir(dir)
    return '{1}{0}{2}'.format(os.sep, groupname, nickname)

def get_down_fsname(username, fsname):
    dir = "{1}{0}{2}{0}{3}".format(os.sep, _rootdir, _downdir, username)
    if not os.path.exists(dir):
        os.mkdir(dir)
    return "{1}{0}{2}".format(os.sep, dir, fsname)

#to create dir automatically
init_dir()