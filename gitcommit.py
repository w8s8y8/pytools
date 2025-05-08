# -*- coding: utf-8 -*-

import datetime
import time
import codecs
import subprocess

def runcommand(cmdline):
    process = subprocess.Popen(cmdline, stdout=subprocess.PIPE)
    last_line_not_empty = False
    while process.poll() is None:
        line = process.stdout.readline().strip().decode('UTF-8')
        line_not_empty = len(line) > 0
        if line_not_empty or last_line_not_empty:
            print(line)
        last_line_not_empty = line_not_empty


if __name__ == '__main__':
    with codecs.open('gitmessage.txt', 'r', encoding='utf-8') as fp:
        timestamp = fp.readline().strip()
        message  = fp.readline().strip()

    print(timestamp)
    print(message)

    end = datetime.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
    timestamp = timestamp.replace(' ', 'T')

    seconds = (end - datetime.datetime.now()).total_seconds()

    if seconds > 2:
        time.sleep(seconds - 2)
        runcommand('git add gitmessage.txt')
        time.sleep(2)
        runcommand(f'git commit -m \"{message}\" --date="{timestamp}"')
        time.sleep(2)
        runcommand('git -c diff.mnemonicprefix=false -c core.quotepath=false --no-optional-locks push -v --tags origin master:master')
        time.sleep(10)
