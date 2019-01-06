
import re
import datetime
import time

intervals = (
    ('w', 604800),  # 60 * 60 * 24 * 7
    ('d', 86400),    # 60 * 60 * 24
    ('h', 3600),    # 60 * 60
    ('min', 60),
    ('sec', 1),
    )

def display_time(seconds, granularity=2):
    result = []

    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append("{} {}".format(str(int(value)), name))
    return ', '.join(result[:granularity])


def howlong():

    # Open the file with read only permit
    total_seconds = 0
    try:
        f = open('ledlog.txt', 'r')
        line = f.readline()
        look_for_on = True
        tic = 0
        toc = 0
        while line:
            print(line)

            if look_for_on:
                m = re.match( r'On\s+-\s+(\d{4}-.*)', line, re.M|re.I)
                if m:
                    print "Found ON time", m.group(1)
                    tic = time.mktime(time.strptime(m.group(1),"%Y-%m-%d %H:%M:%S"))
                    print tic
                    look_for_on = False
            else:
                m = re.match( r'Off\s+-\s+(\d{4}-.*)', line, re.M|re.I)
                if m:
                    print "Found OFF time : ", m.group(1)
                    toc = time.mktime(time.strptime(m.group(1),"%Y-%m-%d %H:%M:%S"))
                    print toc
                    diff = toc - tic
                    total_seconds += diff
                    look_for_on = True

            line = f.readline()
        f.close()
    except:
        pass

    z = [{"uptime": str(display_time(total_seconds))}]
    return z

print howlong()

