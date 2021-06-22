import platform 
import subprocess

class IPDevice:
    #constructor
    def __init__(self, name, mac, ip) -> None:
        self.name = name
        self.mac = mac
        self.ip = ip
        self.active = 0

    def is_active(self):
        result = self.ping(self.ip)
        self.active = 1 if result else 0
        return result

    def ping(self, host):
        """
        Returns True if host (str) responds to a ping request.
        Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
        """

        # Option for the number of packets as a function of
        param = '-n' if platform.system().lower()=='windows' else '-c'

        # Building the command. Ex: "ping -c 1 google.com"
        command = ['ping', param, '1', host]

        response = subprocess.run(command, capture_output=True)

        return not 'Destination host unreachable' in str(response.stdout) and 'Lost = 0' in str(response.stdout)