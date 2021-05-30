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

from . import constant
import http.client
import logging
import requests
from requests.auth import HTTPBasicAuth
from requests.exceptions import HTTPError

class Helper:
    def __init__(self):
        self.logger = logging.getLogger('Helper_Class')
        self.logger.propagate = True
        
        if constant.DEBUG:
            self.logger.setLevel(logging.DEBUG)

    def _get_request(self, url: str, basic_auth: bool, params=dict(), headers=dict(), cookies=dict()):
        """Will send a GET request to the url parameter.

        :param url: the url where the request should go to
        :type url: str
        :param basic_auth: whether basic auth should be used or not
        :type basic_auth: bool
        :param params: parameters which should be used for GET request
        :type params: dict
        :param headers: the header which should be used
        :type headers: dict
        :returns: the content of the response
        :rtype: object
        """

        if constant.DEBUG:
            http.client.HTTPConnection.debuglevel = 1

        try:
            if params:
                if basic_auth:
                    r = requests.get(
                            url,
                            cookies=cookies,
                            headers=headers,
                            params=params,
                            auth=HTTPBasicAuth(
                                constant.OPENVAS_BASIC_AUTH_USER,
                                constant.OPENVAS_BASIC_AUTH_PASS
                            )
                        )
                else:
                    r = requests.get(
                            url,
                            cookies=cookies,
                            headers=headers,
                            params=params,
                        )

            else:
                if basic_auth:
                    r = requests.get(
                            url,
                            cookies=cookies,
                            headers=headers,
                            auth=HTTPBasicAuth(
                                constant.OPENVAS_BASIC_AUTH_USER,
                                constant.OPENVAS_BASIC_AUTH_PASS
                            )
                        )
                else:
                    r = requests.get(
                            url,
                            cookies=cookies,
                            headers=headers,
                        )
            r.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occured: {err}')
        else:
           return r

    def _post_request(self, url: str, basic_auth: bool, data=dict(), headers=dict()):
        """Will send a POST request to the url parameter.

        :param url: the url where the request should go to
        :type url: str
        :param basic_auth: whether basic auth should be used or not
        :type basic_auth: bool
        :param data: the data which should be send via POST
        :type data: dict
        :param headers: the header which should be used
        :type headers: dict
        :returns: the content of the response
        :rtype: object
        """

        if constant.DEBUG:
            http.client.HTTPConnection.debuglevel = 1

        try:
            if basic_auth:
                r = requests.post(
                        url,
                        headers=headers,
                        data=data,
                        auth=HTTPBasicAuth(
                            constant.OPENVAS_BASIC_AUTH_USER,
                            constant.OPENVAS_BASIC_AUTH_PASS
                        )
                    )
            else:
                r = requests.post(
                        url,
                        headers=headers,
                        data=data,
                    )

            r.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occured: {err}')
        else:
            return r
