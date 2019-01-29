import re
import itchat
from itchat.content import *
import util

MSGS = {
    10:'成功上线',
    11:'成功下线',
    12:'',
}

#helper functions
def get_group_name(itchat, groupname):
    chatrooms = itchat.get_chatrooms(update=True)
    for room in chatrooms:
        key = room['UserName']
        chatroom = itchat.update_chatroom(key)
        skey, value = chatroom['NickName'], chatroom['NickName'] or chatroom['RemarkName']
        if key == groupname:
            return skey
    #for
    return 'default'

def init(instance):
    def lc():
        print('login wechat')
    def ec():
        print('logoff wechat')
    instance.auto_login(hotReload=True, statusStorageDir='wiinstance.pkl', loginCallback=lc, exitCallback=ec)

    @instance.msg_register(PICTURE, isFriendChat=True, isGroupChat=True)
    @instance.msg_register(VIDEO, isFriendChat=True, isGroupChat=True)
    @instance.msg_register(RECORDING, isFriendChat=True, isGroupChat=True)
    @instance.msg_register(ATTACHMENT, isFriendChat=True, isGroupChat=True)
    def download_file(msg):
        fromuser = msg['FromUserName']
        if fromuser.find('@@')>=0:      #group msg
            nickname = msg['ActualNickName']
            groupname = get_group_name(instance, fromuser)
            key = util.create_dir(groupname, nickname)
        else:                           #personal msg
            friends = instance.search_friends(userName=fromuser)
            key = friends['NickName']
        fsname = util.get_down_fsname(key, msg['FileName'])
        msg['Text'](fsname)

    #download_file

def fini():
    pass

def main():
    try:
        instance = itchat.new_instance()
        init(instance)
        instance.send(msg = MSGS[10], toUserName = 'filehelper')
        instance.run()
    finally:
        instance.send(msg = MSGS[11], toUserName = 'filehelper')
    fini()

if __name__ == "__main__":
    main()