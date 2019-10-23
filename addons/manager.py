import subprocess
import time
import os

from addons.log import log_action

class ServerManager:
    def __init__(self):
        self.memoryValue = '2G'
        self.serverFilePath = os.path.join(os.getcwd(), "server/server.jar")
        self.startCommand = f'java -Xms{self.memoryValue} -Xmx{self.memoryValue} -jar {self.serverFilePath} nogui java'

    def is_running(self):
        try:
            process = subprocess.check_output('screen -ls | grep minecraft', shell=True)
            return True if process.decode().split('\t')[1].split('.')[1] == 'minecraft' else False
        except subprocess.CalledProcessError:
            return False

    def execute_server_command(self, command):
        return os.system(f"screen -S minecraft -X stuff '{command}\015'")

    def run_web_panel(self):
        pass

    def start(self):
        os.chdir('server')
        if self.is_running():
                print('Server is already enabled!')
        else:
            if not os.path.isfile(self.serverFilePath):
                log_action('ERROR', 'Server file not exist!')
            else:
                process = subprocess.Popen(f"screen -dmS minecraft {self.startCommand}", shell=True)
                os.chdir('..')
                log_action('INFO', f'{self.memoryValue} | Server succesfull started!')

    def restart(self):
        os.chdir('server')
        if self.is_running():
            self.execute_server_command('say Serwer will be restarted in 5seconds')
            time.sleep(5)
            self.execute_server_command('save-all')
            self.execute_server_command('stop')
            subprocess.Popen(f"screen -dmS minecraft {self.startCommand}", shell=True)
            os.chdir('..')
            log_action('INFO', 'Server restarted!')
        else: print('Server is not enabled!')

    def stop(self):
        if self.is_running():
            self.execute_server_command('say Serwer will disabled in 5seconds!')
            time.sleep(5)
            self.execute_server_command('save-all')
            self.execute_server_command('stop')
            log_action('STOP', 'Server stopped!')
        else: print('Server is not enabled!')

