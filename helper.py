#coding=utf-8
import re

def parse_task(idx, line, tasks):
    key, items, msg, target = "","","",""

    line = line.strip()
    pos = line.find('#')
    if pos>=0:
        line = line[:pos]
    if len(line) == 0: 
        return key

    #target and msg check: ensure we have 2 parts
    target_pos, msg_pos = line.find('target'), line.find('msg')
    if target_pos<0 or msg_pos<0:
        info = "Invalid line @ {} : {}".format(idx, line)
        print(info) 
        return key

    #time format check : ensure we have 5 parts
    end_pos = target_pos if target_pos < msg_pos else msg_pos
    #use re to remove extra space char
    items = re.split('\s+',line[:end_pos - 1])
    if len(items)<5 :
        info = "Invalid time @ {} : {}".format(idx, line)
        print(info)
        return key

    if end_pos == target_pos:
        target, msg = line[target_pos:msg_pos - 1], line[msg_pos:]
    else:
        msg, target = line[msg_pos:target_pos - 1], line[target_pos:]
    msg, target = msg.split('='), target.split('=')
    if len(msg)<2 or len(target)<2:
        info = "Invalid msg or target @ {} : {}".format(idx, line)
        print(info)
        return key

    msg, target = msg[1].strip(), target[1].strip()
    key = hash("@".join(items))
    if key not in tasks.keys():
        tasks[key] = [items, []]
    tasks[key][1].append([target, msg])
        
    return key

def load_tasks(fsname="tasks.txt"):
    '''load tasks from file fsname default "tasks.txt"
    each task lies on exactly one line, as crontab format
    {minute} {hour} {day-of-month} {month} {day-of-week} {target=...} {msg=...}
    any #... following content will be omited
    '''
    with open(fsname, encoding="utf-8") as handler:
        lines = handler.readlines()
    # construct tasks
    tasks = {}
    for idx,line in enumerate(lines,1):
        key = parse_task(idx, line, tasks)
        if key == "": continue
    #for
    return tasks

def parse_list(instr):
    if instr == '*':
        result = None
        return result
    if instr.find('-') > 0:
        parts = instr.split('-')
        result = range(int(parts[0]), int(parts[1])+1)
        return result
    if instr.find(',') > 0:
        parts = instr.split(',')
        result = []
        for part in parts:
            result.append(int(part))
        return result
    else:
        result = [int(instr)]
        return result

def parse_part(instr):
    pos = instr.find('/')
    if pos > 0:
        x = parse_list(instr[:pos])
        e_x = int(instr[pos+1:])
    else:  # no '/'
        x = parse_list(instr)
        e_x = None
    return x, e_x

def get_tasks_min_period(tasks):
    # value = 1 means every * run once
    minute, hour, day, month, week = 0, [], 0, 1, 1 
    e_minute, e_hour, e_day, e_month, e_week = 60,1,1,1,1
    for key, [timestr, msgs] in tasks.items():
        print(timestr, msgs)
        #minute part
        minute, e_minute = parse_part(timestr[0])
        #hour
        hour, e_hour = parse_part(timestr[1])
        #days
        day, e_day = parse_part(timestr[2])
        #months
        month, e_month = parse_part(timestr[3])
        #weekday
        week, e_week = parse_part(timestr[4])
        info = "{}/{} {}/{} {}/{} {}/{} {}/{}".format(minute, e_minute, hour, e_hour, day, e_day, month, e_month, week, e_week)
        print(info)
    #for
    return 5 # on every 5 minutes running

def remove_tasks(tasks, id):
    if 1<=id<=len(tasks):
        for idx, (key,[timestr, msgs]) in enumerate(tasks.items(),1):
            if idx == id: break
        
        if len(msgs) == 1:
            del tasks[key]
        else :
            msgs.pop()
        return True
    else:
        return False


def format_tasks(tasks):
    result = ""
    for idx, (key, [timestr, msgs]) in enumerate(tasks.items(),1):
        result += "{}: {} {}\n".format(idx, timestr, msgs)
    return result

def test_load_tasks():
    tasks = load_tasks()
    #print(tasks)
    get_tasks_min_period(tasks)
    msgs = format_tasks(tasks)
    print(msgs)

def test_parse_task(line):
    line = ""
    key, items, msg, target = parse_task(line)
    print(key, items, msg, target)

if __name__ == "__main__":
    test_load_tasks()