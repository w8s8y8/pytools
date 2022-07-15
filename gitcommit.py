# -*- coding: utf-8 -*-

import datetime
import time
import fileinput
import subprocess

def run(cmdline):
    process = subprocess.Popen(cmdline, stdout=subprocess.PIPE)
    last_line_not_empty = False
    while process.poll() is None:
        line = process.stdout.readline().strip().decode('UTF-8')
        line_not_empty = len(line) > 0
        if line_not_empty or last_line_not_empty:
            print(line)
        last_line_not_empty = line_not_empty

if __name__ == '__main__':
    file = fileinput.FileInput('message.txt', openhook=fileinput.hook_encoded('utf-8'))

    end, message  = [file.readline().strip(), file.readline().strip()]

    print(end)
    print(message)

    end = datetime.datetime.strptime(end, '%Y-%m-%d %H:%M:%S')

    seconds = (end - datetime.datetime.now()).total_seconds()

    if seconds > 0:
        time.sleep(seconds)
        run('git add message.txt')
        time.sleep(2)
        run(f'git commit -m \"{message}\"')
        time.sleep(2)
        run('git -c diff.mnemonicprefix=false -c core.quotepath=false --no-optional-locks push -v --tags origin master:master')
        time.sleep(10)
