#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#    openvas.py
#
#    Copyright (c) 2021 Simon Krenz
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; Applies version 2 of the License.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

__version__ = '0.1'
__author__ = 'Simon Krenz'

from .helper import Helper
from . import constant
from bs4 import BeautifulSoup
import logging

class OpenVAS:
    def __init__(self,
            hostname=None,
            port=None,
            basic_auth_user=None,
            basic_auth_pass=None,
            username=None,
            password=None):

        self.logger = logging.getLogger('OpenVAS_API')
        if constant.DEBUG:
            self.logger.setLevel(logging.DEBUG)
        if basic_auth_user is None or basic_auth_pass is None:
            raise Exception('[ERROR] Missing basic auth username or password.')
        if username is None or password is None:
            raise Exception('[ERROR] Missing username or password.')

        self.basename = hostname
        self.baseurl = f"https://{hostname}:{port}"
        self.basic_auth = True
        self.basic_auth_user = basic_auth_user
        self.basic_auth_pass = basic_auth_pass
        self.username = username
        self.password = password
        self.helper = Helper()
        self.xml_reports = dict()

        self.headers = {
            'Accept': constant.HEADER_ACCEPT,
            'Accept-Encoding': constant.HEADER_ACCEPT_ENCODING,
            'Accept-Language': constant.HEADER_ACCEPT_LANGUAGE,
            'Cache-Control': constant.HEADER_CACHE_CONTROL,
            'Connection': constant.HEADER_CONNECTION,
            'Content-Type': constant.HEADER_CONTENT_TYPE,
            'User-Agent': constant.HEADER_USER_AGENT,
            'X-Requested-With': constant.HEADER_X_REQUESTED_WITH,
        }

        self.login()
        self._get_report_format_ids()

    def _login_token(self):
        """Get the OpenVAS auth token and cookies and sets them to self 

        :returns: self.token and self.cookies
        """
        data = {
            'cmd': 'login',
            'login': self.username,
            'password': self.password,
        }
        
        token = self.helper._post_request(
                    self.basename,
                    self.basic_auth,
                    data, 
                    self.headers)

        if token.status_code == 200:
            xml_response = BeautifulSoup(token.content, 'lxml')
            self.token = xml_response.find('token').get_text()
            self.cookies = token.cookies.get_dict()
        else:
            raise Exception('[FAIL] Could not login to OpenVAS')

    def login(self):
        """Calls _login_token to set auth token and cookies

        """
        r = self._login_token()

    def _get_report_format_ids(self):
        """Retrieves existent report formats.

        """
        self.logger.info('[INFO] Retrieving all available OpenVAS report formats...')
        params = {
            'cmd': 'get_report_formats',
            'token': self.token,
        }

        url = self.basename + "/gmp"

        r = self.helper._get_request(
                url, 
                self.basic_auth, 
                params, 
                self.headers, 
                self.cookies)

        if r.status_code == 200:
            xml_response = BeautifulSoup(r.content, 'lxml')
            formats_xml = xml_response.find_all('report_format')
            for report in formats_xml:
                if report.findChild('name', recursive=False).text == 'XML':
                    self.xml_report_id = report.get('id')
                if report.findChild('name', recursive=False).text == 'CSV Results':
                    self.csv_report_id = report.get('id')
        else:
            raise Exception('[FAIL] Could not get report formats from OpenVAS')
        print(self.csv_report_id)

    def get_xml_reports(self):
        """Retrieves all existent XML based reports and lists them

        """
        self.logger.info('[INFO] Retrieving all existing OpenVAS reports...')
        params = {
            'cmd': 'get_reports',
            'token': self.token,
            'details': 0,
            'filter': 'sort-reverse=date first=1 rows=10'
        }
        url = self.basename + "/gmp"

        r = self.helper._get_request(
                url, 
                self.basic_auth, 
                params, 
                self.headers, 
                self.cookies)

        if r.status_code == 200:
            xml_response = BeautifulSoup(r.content, 'lxml')
            reports_xml = xml_response.find_all('report', {
                'extension':'xml', 
                'format_id': self.xml_report_id})
            for report in reports_xml:
                self.xml_reports[report.get('id')] = dict()
                self.xml_reports[report.get('id')] = {
                    'name': report.findChild('name', recursive=False).get_text(),
                    'hosts': report.findChild('hosts').get_text(),
                    'vulns': report.findChild('vulns').get_text(),
                    'high': report.findChild('hole').findChild('full').get_text(),
                    'medium': report.findChild('warning').findChild('full').get_text(),
                    'low': report.findChild('info').findChild('full').get_text(),
                    'log': report.findChild('log').findChild('full').get_text(),
                    'severity': report.findChild('severity').findChild('full').get_text(),
                }
        else:
            raise Exception('[FAIL] Could not get reports from OpenVAS')

    def get_report(self, report_id: str):
        """Retrieves a specific report by id

        """
        self.logger.info(f'[INFO] Retrieving OpenVAS report {report_id}...')
        params = {
            'cmd': 'get_report',
            'token': self.token,
            'report_id': report_id,
            'filter': 'apply_overrides=0 min_qod=70 autofp=0 levels=hml first=1 rows=0 sort-reverse=severity',
            'ignore_pagination': 1,
            'report_format_id': self.csv_report_id,
            'submit': 'Download',
        }

