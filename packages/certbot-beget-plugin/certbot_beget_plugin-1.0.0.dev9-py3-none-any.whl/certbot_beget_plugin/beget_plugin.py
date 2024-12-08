"""DNS Authenticator for Beget."""

import json
import logging
from typing import Any
from typing import Dict
from typing import List
from typing import Tuple
from typing import Optional

from certbot import errors
from certbot.plugins import dns_common
from certbot.plugins.dns_common import CredentialsConfiguration

from certbot import errors

import requests

logger = logging.getLogger(__name__)

BASE_API_URL = 'https://api.beget.com/api'

class Authenticator(dns_common.DNSAuthenticator):
    """DNS Authenticator for Beget

    This Authenticator uses the Beget API to fulfill a dns-01 challenge.
    """

    description = ('Obtain certificates using a DNS TXT record (if you are using Beget for '
                   'DNS).')
    ttl = 120

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.credentials: Optional[CredentialsConfiguration] = None
        self.client = {}


    @classmethod
    def add_parser_arguments(cls, add) -> None:
        super(Authenticator, cls).add_parser_arguments(add, default_propagation_seconds=120)
        add('credentials', help='Beget credentials INI file.')

    def more_info(self) -> str:
        return 'This plugin configures a DNS TXT record to respond to a dns-01 challenge using ' + \
               'the Beget API.'

    def _validate_credentials(self, credentials: CredentialsConfiguration) -> None:
        username = credentials.conf('username')
        password = credentials.conf('password')

        if not username or not password:
            raise errors.PluginError('It is necessary to set a beget_plugin_username and beget_plugin_password to access the Beget API')

    def _setup_credentials(self) -> None:
        self.credentials = self._configure_credentials(
            'credentials',
            'Beget credentials INI file',
            {
                'username': 'Beget API username',
                'password': 'Beget API password'
            },
            self._validate_credentials
        )

    def _perform(self, domain: str, validation_name: str, validation: str) -> None:
        self._get_beget_client().add_txt_record(domain, validation_name, validation, self.ttl)

    def _cleanup(self, domain: str, validation_name: str, validation: str) -> None:
        self._get_beget_client().del_txt_record(domain, validation_name, validation)

    def _get_beget_client(self) -> "BegetClient":
        if not self.credentials:
            raise errors.Error("Plugin has not been prepared.")
        
        if self.client == {}:
            self.client = BegetClient(self.credentials.conf('username'), self.credentials.conf('password'))

        return self.client

class BegetClient:
    """
    Encapsulates all communication with the Beget API.
    """


    def __init__(self, username:str, password:str) -> None: 
        self.username = username
        self.password = password
        self.subdomainExistsBefore = False


    def add_txt_record(self, domain: str, record_name: str, record_content: str, record_ttl: int) -> None:
        """
        Add a TXT record using the supplied information.

        :param str domain: The domain to use to look up the Beget zone.
        :param str record_name: The record name (typically beginning with '_acme-challenge.').
        :param str record_content: The record content (typically the challenge validation).
        :param int record_ttl: The record TTL (number of seconds that the record may be cached).
        :raises certbot.errors.PluginError: if an error occurs communicating with the Beget API
        """

        domains = self._getDomains()

        actualDomain = None
        for d in domains:
            if domain.endswith(d[1]):
                actualDomain = d

        if not actualDomain:
            raise errors.PluginError('The specified domain could not be found in the list of domains on the Beget account')
        
        if not self._subdomainIsExist(record_name):
            self._addSubdomain(record_name.removesuffix('.' + actualDomain[1]), actualDomain[0])
        else:
            self.subdomainExistsBefore = True

        self._createTxtRecord(record_name, record_content, 10)


    def del_txt_record(self, domain: str, record_name: str, record_content: str) -> None:
        """
        Delete a TXT record using the supplied information.

        Note that both the record's name and content are used to ensure that similar records
        created concurrently (e.g., due to concurrent invocations of this plugin) are not deleted.

        Failures are logged, but not raised.

        :param str domain: The domain to use to look up the Beget zone.
        :param str record_name: The record name (typically beginning with '_acme-challenge.').
        :param str record_content: The record content (typically the challenge validation).
        """

        if self.subdomainExistsBefore:
            self._deleteTxtRecord(record_name, record_content)
        else:
            self._deleteSubdomain(record_name)


    def _createTxtRecord(self, record_name: str, record_content: str, priority: int) -> None:
        records = {}
        resp = self._fetchWithAuth('/dns/getData', data={'fqdn': record_name})
        if resp['status'] == 'success':
            records = resp['result']['records']
        else:
            raise errors.PluginError('Failed to get records for domain: ' + resp['errors'])
    
        newRecord = {
            'priority' : priority,
            'value' : record_content,
        }

        if 'TXT' in records:
            records['TXT'].append(newRecord)
        else:
            records['TXT'] = [newRecord]
        
        resp = self._fetchWithAuth('/dns/changeRecords', data={'fqdn': record_name, 'records': records})
        if resp['status'] != 'success':
            raise errors.PluginError('Failed to change records for domain: ' + resp['errors'])

    def _deleteTxtRecord(self, record_name: str, record_content: str) -> None:
        records = {}
        resp = self._fetchWithAuth('/dns/getData', data={'fqdn': record_name})
        if resp['status'] == 'success':
            records = resp['result']['records']
        else:
            raise errors.PluginError('Failed to get records for domain: ' + resp['errors'])

        if 'TXT' in records:
            records['TXT'] = [record for record in records['TXT'] if record['txtdata'] != record_content]
        if not records['TXT']:
            del records['TXT']

        resp = self._fetchWithAuth('/dns/changeRecords', data={'fqdn': record_name, 'records': records})
        if resp['status'] != 'success':
            raise errors.PluginError('Failed to change records for domain: ' + resp['errors'])

    def _subdomainIsExist(self, expected) -> bool:
        subdomains = self._getSubdomains()
        return any(sd[1] == expected for sd in subdomains)


    def _getDomains(self) -> List[Tuple[int, str]]:
        res: List[Tuple[int, str]] = []
        resp = self._fetchWithAuth('/domain/getList')
        if resp['status'] == 'success':
            for d in resp['result']:
                res.append((d['id'],d['fqdn']))

        return res


    def _getSubdomains(self) -> List[Tuple[int, str]]:
        res: List[Tuple[int, str]] = []
        resp = self._fetchWithAuth('/domain/getSubdomainList')
        if resp['status'] == 'success':
            for d in resp['result']:
                res.append((d['id'],d['fqdn']))

        return res


    def _addSubdomain(self, subdomain: str, domain_id: int) -> None:
        data = {
            'subdomain' : subdomain,
            'domain_id' : domain_id
        }
        resp = self._fetchWithAuth('/domain/addSubdomainVirtual', data=data)
        if resp['status'] != 'success':
            errors.PluginError('Failed to create record temporary subdomain _acme-challenge: {}'.format(resp['errors']))


    def _deleteSubdomain(self, subdomain: str) -> None:
        subdomains = self._getSubdomains()

        for sub in subdomains:
            if sub[1] == subdomain or sub[1] == 'www.'+subdomain:
                data = {
                    'id' : sub[0]
                }
                resp = self._fetchWithAuth('/domain/deleteSubdomain', data=data)
                if resp['status'] != 'success':
                    errors.PluginError('Failed to delete record temporary subdomain _acme-challenge: {}'.format(resp['errors']))


    def _fetchWithAuth(
        self,
        endpoint: str,
        method: str = 'GET',
        params: Optional[Dict[str, Any]] = {},
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Optional[Dict[str, Any]]:
        url = BASE_API_URL + endpoint
        
        params.update({
            'login': self.username,
            'passwd': self.password,
            'input_format': 'json',
            'output_format': 'json',
            'input_data': json.dumps(data) if data else None
        })

        if params['input_data'] is None:
            del params['input_data']

        try:
            response = requests.request(method, url, params=params, json=data, headers=headers)
            response.raise_for_status()
            responceJson = response.json()

            if responceJson['status'] == "error":
                raise errors.PluginError('Fetch error: {}'.format(responceJson['error_text']))

            return responceJson['answer']
        
        except requests.RequestException as e:
            print(f'Error fetching from {url}: {e}')
            return None

