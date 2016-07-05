# Command base
from django.core.management.base import BaseCommand

# All models for testing
from modules.models import Platform, CableModule, TestResult

# Paramiko for simple device SSH
import paramiko

# pprint for easy view
from pprint import pprint

# Date for checking dates
from datetime import date

# Logging
import logging
log = logging.getLogger('cables_db')

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('device_name', help='The current device being used for testing.')
        parser.add_argument('--start_port_num', help='Test modules start at this port number.')
        parser.add_argument('--device_ip', help='The IP address for a device if it can not use hostname.')
        parser.add_argument('--end_port_num', help='Test modules end at this port number.')

    def _find_cable_module(self, ethtool_dict):
        try:
            found_module = CableModule.objects.get(pin_number__exact=ethtool_dict['vendor_pn'], serial_number__exact=ethtool_dict['vendor_sn'])
        except CableModules.DoesNotExist as e:
            pass
        except CableModules.MultipleObjectsReturned as e:
            # If multiple objects are returned, the query went very poorly, for now pass error up
            raise e

        return found_module

    def _load_ethtool_data(self, ethtool_data_out):
        # ethtool dict
        eth_dict = {}

        # Split the lines
        for ethtool_line in ethtool_data_out.splitlines():
            key, value = ethtool_line.split(':', 1)

            # Strip white space on both
            key = key.strip()
            value = value.strip()

            # Replace the spaces in key with _ and lower
            key = key.replace(' ', '_').lower()
            
            eth_dict[key] = value
        return eth_dict

    def _start_ssh_connection(self, hostname, user='root', passw='cn321'):
        # Create SSH client
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(hostname, username=user, password=passw)

    def _device_sudo_command(self, command):
        ssh_stdin, ssh_stdout, ssh_stderr = self.ssh.exec_command(command)
        return ssh_stdout.read()

    def _get_speed_used(self, port_num):
        speed_used = self._device_sudo_command('ethtool swp{0} | grep -i speed'.format(port_num))

        speed_used = speed_used.split(':')[1]
        speed_used = speed_used.strip()
       
        # Remove the Mb/s piece
        speed_used = speed_used.replace('Mb/s', '')

        # Convert to int and divide by 1000
        return (int(speed_used)/1000)

    def _already_tested(self, platform, cable_module):
        # Check if this module, for this platform, was already tested TODAY
        try:
            temp_test_result = TestResult.objects.get(platform=platform, module=cable_module, date_tested=date.today())
        except TestResult.DoesNotExist:
            return False
        
        return True

    def handle(self, *args, **options):
        # Load the device in question SSH and platform from platform DB
        platform_model = options['device_name'].rsplit('-', 1)[0] # This removes the '-0X' number from end

        try:
            platform = Platform.objects.get(platform_name__exact=platform_model)
        except Platform.DoesNotExist:
            # Exit out early
            pass
    
        # Create SSH client, use device IP if for some reason hostname is known not working (moon rack device)
        if options['device_ip']:
            self._start_ssh_connection(options['device_ip'])
        else:
            self._start_ssh_connection(options['device_name'])

        # For each port, load a test result 
        for port_num in range(int(options['start_port_num']), int(options['end_port_num'])):
            # Call 'ethtool -m' to find what is being used in the port, only need vendor info
            ethtool_out = self._device_sudo_command('ethtool -m swp{0} | grep -i vendor'.format(port_num))

            # Load all the data into a dictonary
            ethtool_data_dict = self._load_ethtool_data(ethtool_out)

            # Find the module in the current cable DB, if it can't be found skip
            try:
                cable_module_tested = self._find_cable_module(ethtool_data_dict)
            except CableModules.MultipleObjectsReturned:
                # Can't load this module, log it and move on
                log.info("Could not load module in swp{0}".format(port_num))   
                continue

            # Is there already a test result for this module
            if self._already_tested(platform, cable_module_tested):
                log.info('{0} was already tested, skipping.'.format(cable_module_tested))
                continue

            # Get the current speed of the module 
            speed_tested = self._get_speed_used(port_num)

            # Ask user is QSA was used
            qsa_used = raw_input('{0} QSA Used? '.format(cable_module_tested))

            if qsa_used.lower() == 'yes':
                qsa_used_bool = True
            else:
                qsa_used_bool = False

            # Ask user if module pass/fail
            pass_or_fail = raw_input('{0} Pass or Fail? '.format(cable_module_tested))
            pass_or_fail = pass_or_fail.upper() # Always uppercase  
            if pass_or_fail == 'FAIL':
                bug_id_url = raw_input('Please enter the URL of the bug-id for this module: ')
            else:
                bug_id_url = None

            # Create test result
            new_test_result = TestResult(platform=platform, module=cable_module_tested, test_passed=pass_or_fail, speed=speed_tested, qsa_used=qsa_used_bool, bug_id=bug_id_url)

            print(new_test_result)
            
            is_good = raw_input('Does above result look good? ')
            if is_good.lower() == 'yes' or is_good.lower() == 'y':
                new_test_result.save()
            else:
                log.info('Test result was not good, not saving.')
