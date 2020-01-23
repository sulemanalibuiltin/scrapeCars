import itertools
import json
import socket
import sys
from io import open as iopen
from multiprocessing import Pool
from pathlib import Path
from tqdm import tqdm

import requests

# put return n itmes at a time from an interable
def grouper(n, iterable):
    it = iter(iterable)
    while True:
        chunk = tuple(itertools.islice(it, n))
        if not chunk:
            return
        yield chunk

# download an image from a url
# return success/failure and the task to caller


def workFunc(task):

    try:
        socket.setdefaulttimeout(10)
        i = requests.get(task['url'])
    except:
        return((False, task))

    if i.status_code == requests.codes.ok:
        filename = '{0}'.format(task['filename'].replace(' ', '_'))
        f = iopen(filename, 'wb')
        f.write(i.content)
        f.close()
        return((True, task))
    else:
        return((False, task))


# read in tasking for files not already downloaded
def readTasking(fname, vehicle_type):
    taskList = list()
    tasking = open(fname, 'r')
    for task in tasking:
        task = task.strip()
        task = json.loads(task)
        task['filename'] = vehicle_type + 's/' + task['filename']
        myf = Path(task['filename'])
        if not myf.is_file():
            taskList.append(task)
    tasking.close()
    return taskList


def main(atOnce=1000):
    if len(sys.argv) < 2: 
        print 'include vehicle_type as arg (truck, car, or mpv)'
        return
    p = Pool()

    # file detailing what to download
    # each line should be of format:
    # fileType,color,make,odel,url,namehash
    vehicle_type = sys.argv[1]
    # fname = sys.argv[1]
    fname = vehicle_type+'s-dataset'

    # get listing of files to download
    taskList = readTasking(fname, vehicle_type)

    num_lines = len(taskList)
    print('processed {0} lines to download'.format(num_lines))
    print('tasking loaded')

    good = open(fname + '.good', 'w')
    bad = open(fname + '.bad', 'w')

    pbar = tqdm(total=num_lines)
    count = 0
    # do the downloads in batches
    for batch in grouper(atOnce, taskList):

        retval = p.map(workFunc, batch)

        for r, t in retval:
            if r:
                good.write(json.dumps(t) + '\n')
            else:
                bad.write(json.dumps(t) + '\n')
                
        good.flush()
        bad.flush()
        pbar.update(atOnce)

    pbar.close()
    good.close()
    bad.close()

if __name__ == '__main__':
    main(250)
