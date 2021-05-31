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

from modules.openvas import OpenVAS
import modules.constant as constant

def main():
    """The main function

    """
    openvas = OpenVAS(
            constant.OPENVAS_API_URL,
            constant.OPENVAS_API_PORT,
            constant.OPENVAS_BASIC_AUTH_USER,
            constant.OPENVAS_BASIC_AUTH_PASS,
            constant.OPENVAS_USERNAME,
            constant.OPENVAS_PASSWORD)

    openvas.get_xml_reports()

if __name__ == "__main__":
    main()
