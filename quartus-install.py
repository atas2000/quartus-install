#!/usr/bin/env python3
#-
# SPDX-License-Identifier: BSD-2-Clause
#
# Copyright (c) 2018 A. Theodore Markettos
# All rights reserved.
#
# This software was developed by SRI International and the University of
# Cambridge Computer Laboratory (Department of Computer Science and
# Technology) under DARPA contract HR0011-18-C-0016 ("ECATS"), as part of the
# DARPA SSITH research programme.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.
#

"""
Download and install Quartus Prime software on remote servers that don't have a web browser or GUI
"""

default_parallel = 16

fpga_key = {
    'a2' : 'arria',
    'a5' : 'arriav',
    'a10': 'arria10',
    'a5gz': 'arriavgz',
    'c4' : 'cyclone',
    'c5' : 'cyclonev',
    'c10lp' : 'cyclone10lp',
    'm2' : 'max',
    'm10' : 'max10',
    's4' : 'stratixiv',
    's5' : 'stratixv'
    }


def generate_pro_url(quartus_version, minor_version, revision):
    base_url = "https://download.altera.com/akdlm/software/acdsinst/"
    full_version = "%s.%s.%s" % (quartus_version, minor_version, revision)
    version_url = "%s/%s/%s/ib_installers" % (base_url, quartus_version, revision)
    pro_urls = {}
    if quartus_version >= '19.3':
        pro_urls.update( { "setup" : "%s/QuartusProSetup-%s-windows.exe" % (version_url, full_version) } )
        pro_urls.update( { "setup_part2" : "%s/QuartusProSetup-part2-%s-windows.exe" % (version_url, full_version) } )
    else:
        pro_urls.update( { "setup" : "%s/QuartusProSetup-%s-windows.exe" % (version_url, full_version) } )

    if quartus_version >= '19.2':
        pro_urls.update( { "modelsim_part1" : "%s/ModelSimProSetup-%s-windows.exe" % (version_url, full_version) } )
        pro_urls.update( { "modelsim_part2" : "%s/ModelSimProSetup-part2-%s-windows.exe" % (version_url, full_version) } )
    else:
        pro_urls.update( { "modelsim_" : "%s/ModelSimProSetup-%s-windows.exe" % (version_url, full_version) } )

    if quartus_version == '19.2':
        pro_urls.update( { "modelsim_part2" : "%s/modelsim-part2-%s-windows.qdz" % (version_url, full_version) } )

    if quartus_version >= '20.1':
        pro_urls.update( { "agilex" : "%s/agilex-%s.qdz" % (version_url, full_version) } )
    if quartus_version >= '20.3':
        pro_urls.update( { "diamondmesa" : "%s/diamondmesa-%s.qdz" % (version_url, full_version) } )
        pro_urls.update( { "setup_part2" : "%s/quartus_part2-%s.qdz" % (version_url, full_version) } )
    pro_urls.update( { "a10" : "%s/arria10-%s.qdz" % (version_url, full_version) } )
    pro_urls.update( { "c10gx" : "%s/cyclone10gx-%s.qdz" % (version_url, full_version) } )
    pro_urls.update( { "s10" : "%s/stratix10-%s.qdz" % (version_url, full_version) } )
    return pro_urls

def generate_std_url(quartus_version, minor_version, revision, edition):
    base_url="https://download.altera.com/akdlm/software/acdsinst/"
    version_url = "%s/%s%s/%s/ib_installers" % (base_url, quartus_version, edition, revision)
    full_version = "%s.%s.%s" % (quartus_version, minor_version, revision)
    urls = {}
    urls.update( { "setup" : "%s/QuartusSetup-%s-windows.exe" % (version_url, full_version) } )
    urls.update( { "modelsim" : "%s/ModelSimSetup-%s-windows.exe" % (version_url, full_version) } )
    for part in [1,2,3]:
        urls.update( { "a10_part%d" % (part) : "%s/arria10_part%d-%s.qdz" % (version_url, part, full_version) } )
    fpgas = fpga_key
    if 'a10' in fpgas:
        del fpgas['a10']
    for fpga in list(fpgas.keys()):
        urls.update( { fpga : "%s/%s-%s.qdz" % (version_url, fpga_key[fpga], full_version) } )
    return urls

# generate some URLs based on the regular pattern
quartus_url_203pro = generate_pro_url('20.3', '0', '158')
quartus_url_202pro = generate_pro_url('20.2', '0', '50')
quartus_url_201pro = generate_pro_url('20.1', '0', '177')
quartus_url_194pro = generate_pro_url('19.4', '0', '64')
quartus_url_193pro = generate_pro_url('19.3', '0', '222')
quartus_url_192pro = generate_pro_url('19.2', '0', '57')

quartus_url_2011std = generate_std_url('20.1', '1', '720', 'std.1')
quartus_url_201std = generate_std_url('20.1', '0', '711', 'std')
quartus_url_191std = generate_std_url('19.1', '0', '670', 'std')

# some files weren't updated in this patch release
for part in ["a5", "a10_part1", "a10_part2", "a10_part3", "a5gz"] :
    quartus_url_2011std[part] = quartus_url_201std[part]
quartus_url_2011std['setup'] = "https://download.altera.com/akdlm/software/acdsinst/20.1std.1/720/ib_installers/QuartusSetup-20.1.1.720-windows.exe"


# Lite have a different installer but the same device files
quartus_url_2011lite = dict(quartus_url_2011std)
quartus_url_2011lite['setup'] = "https://download.altera.com/akdlm/software/acdsinst/20.1std.1/720/ib_installers/QuartusLiteSetup-20.1.1.720-windows.exe"
quartus_url_201lite = dict(quartus_url_201std)
quartus_url_201lite['setup'] = "https://download.altera.com/akdlm/software/acdsinst/20.1std/711/ib_installers/QuartusLiteSetup-20.1.0.711-windows.exe"
quartus_url_191lite = dict(quartus_url_191std)
quartus_url_191lite['setup'] = "https://download.altera.com/akdlm/software/acdsinst/19.1std/670/ib_installers/QuartusLiteSetup-19.1.0.670-windows.exe"




# older versions, where each has sufficient quirks not to fit the pattern

quartus_url_191pro = {
    'setup' : 'https://download.altera.com/akdlm/software/acdsinst/19.1/240/ib_installers/QuartusProSetup-19.1.0.240-windows.exe',
    'modelsim_part1' : 'https://download.altera.com/akdlm/software/acdsinst/19.1/240/ib_installers/ModelSimProSetup-19.1.0.240-windows.exe',
    'modelsim_part2' : 'https://download.altera.com/akdlm/software/acdsinst/19.1/240/ib_installers/modelsim-part2-19.1.0.240-windows.qdz',
    'a10' : 'https://download.altera.com/akdlm/software/acdsinst/19.1/240/ib_installers/arria10-19.1.0.240.qdz',
    'c10gx' : 'https://download.altera.com/akdlm/software/acdsinst/19.1/240/ib_installers/cyclone10gx-19.1.0.240.qdz',
    's10' : 'https://download.altera.com/akdlm/software/acdsinst/19.1/240/ib_installers/stratix10-19.1.0.240.qdz',
    'patch_0.03' : 'https://www.intel.com/content/dam/altera-www/global/en_US/support/knowledge-center/components/2019/quartus-19.1-0.03-windows.exe'
}

quartus_url_181pro = {
    'setup' : 'https://download.altera.com/akdlm/software/acdsinst/18.1/222/ib_installers/QuartusProSetup-18.1.0.222-windows.exe',
    'modelsim_part1' : 'https://download.altera.com/akdlm/software/acdsinst/18.1/222/ib_installers/ModelSimProSetup-18.1.0.222-windows.exe',
    'modelsim_part2' : 'https://download.altera.com/akdlm/software/acdsinst/18.1/222/ib_installers/modelsim-part2-18.1.0.222-windows.qdz',
    'a10' : 'https://download.altera.com/akdlm/software/acdsinst/18.1/222/ib_installers/arria10-18.1.0.222.qdz',
    'c10gx' : 'https://download.altera.com/akdlm/software/acdsinst/18.1/222/ib_installers/cyclone10gx-18.1.0.222.qdz',
    's10' : 'https://download.altera.com/akdlm/software/acdsinst/18.1/222/ib_installers/stratix10-18.1.0.222.qdz'
}

quartus_url_181std = {
    'setup' : 'https://download.altera.com/akdlm/software/acdsinst/18.1std/625/ib_installers/QuartusSetup-18.1.0.625-windows.exe',
	'modelsim' : 'https://download.altera.com/akdlm/software/acdsinst/18.1std/625/ib_installers/ModelSimSetup-18.1.0.625-windows.exe',
	'c4' : 'https://download.altera.com/akdlm/software/acdsinst/18.1std/625/ib_installers/cyclone-18.1.0.625.qdz',
	'a5gz' : 'https://download.altera.com/akdlm/software/acdsinst/18.1std/625/ib_installers/arriavgz-18.1.0.625.qdz',
	'a5' : 'https://download.altera.com/akdlm/software/acdsinst/18.1std/625/ib_installers/arriav-18.1.0.625.qdz',
	'a10_part1' : 'https://download.altera.com/akdlm/software/acdsinst/18.1std/625/ib_installers/arria10_part1-18.1.0.625.qdz',
	'a10_part2' : 'https://download.altera.com/akdlm/software/acdsinst/18.1std/625/ib_installers/arria10_part2-18.1.0.625.qdz',
	'a10_part3' : 'https://download.altera.com/akdlm/software/acdsinst/18.1std/625/ib_installers/arria10_part3-18.1.0.625.qdz',
	'a2' : 'https://download.altera.com/akdlm/software/acdsinst/18.1std/625/ib_installers/arria-18.1.0.625.qdz',
	'c10lp' : 'https://download.altera.com/akdlm/software/acdsinst/18.1std/625/ib_installers/cyclone10lp-18.1.0.625.qdz',
	'c5' : 'https://download.altera.com/akdlm/software/acdsinst/18.1std/625/ib_installers/cyclonev-18.1.0.625.qdz',
	's4' : 'https://download.altera.com/akdlm/software/acdsinst/18.1std/625/ib_installers/stratixiv-18.1.0.625.qdz',
	's5' : 'https://download.altera.com/akdlm/software/acdsinst/18.1std/625/ib_installers/stratixv-18.1.0.625.qdz',
	'm10' : 'https://download.altera.com/akdlm/software/acdsinst/18.1std/625/ib_installers/max10-18.1.0.625.qdz',
	'm2' : 'https://download.altera.com/akdlm/software/acdsinst/18.1std/625/ib_installers/max-18.1.0.625.qdz',
	'opencl' : 'https://download.altera.com/akdlm/software/acdsinst/18.1std/625/ib_installers/AOCLSetup-18.1.0.625-windows.exe',
	'eds' : 'https://download.altera.com/akdlm/software/acdsinst/18.1std/625/ib_installers/SoCEDSSetup-18.1.0.625-windows.exe',
        'update_1': 'https://download.altera.com/akdlm/software/acdsinst/18.1std.1/646/update/QuartusSetup-18.1.1.646-windows.exe'
        }

quartus_url_181lite = dict(quartus_url_181std)
quartus_url_181lite['setup'] = "https://download.altera.com/akdlm/software/acdsinst/18.1std/625/ib_installers/QuartusLiteSetup-18.1.0.625-windows.exe"
quartus_url_181lite['a2'] = "https://download.altera.com/akdlm/software/acdsinst/18.1std/625/ib_installers/arria_lite-18.1.0.625.qdz"


quartus_url_171std = {
    'setup' : 'https://download.altera.com/akdlm/software/acdsinst/17.1std/590/ib_installers/QuartusSetup-17.1.0.590-windows.exe',
    'modelsim' : "https://download.altera.com/akdlm/software/acdsinst/17.1std/590/ib_installers/ModelSimSetup-17.1.0.590-windows.exe",
    'a2' : "https://download.altera.com/akdlm/software/acdsinst/17.1std/590/ib_installers/arria-17.1.0.590.qdz",
    'a10_part1' : "https://download.altera.com/akdlm/software/acdsinst/17.1std/590/ib_installers/arria10_part1-17.1.0.590.qdz",
    'a10_part2' : "https://download.altera.com/akdlm/software/acdsinst/17.1std/590/ib_installers/arria10_part2-17.1.0.590.qdz",
    'a10_part3' : "https://download.altera.com/akdlm/software/acdsinst/17.1std/590/ib_installers/arria10_part3-17.1.0.590.qdz",
    's4' : "https://download.altera.com/akdlm/software/acdsinst/17.1std/590/ib_installers/stratixiv-17.1.0.590.qdz",
    's5' : "https://download.altera.com/akdlm/software/acdsinst/17.1std/590/ib_installers/stratixv-17.1.0.590.qdz",
    'c10lp' : "https://download.altera.com/akdlm/software/acdsinst/17.1std/590/ib_installers/arriav-17.1.0.590.qdz",
    'c5' : "https://download.altera.com/akdlm/software/acdsinst/17.1std/590/ib_installers/cyclonev-17.1.0.590.qdz",
    'c4' : "https://download.altera.com/akdlm/software/acdsinst/17.1std/590/ib_installers/cyclone-17.1.0.590.qdz",
    'a5' : "https://download.altera.com/akdlm/software/acdsinst/17.1std/590/ib_installers/arriav-17.1.0.590.qdz",
    'a5gz' : "https://download.altera.com/akdlm/software/acdsinst/17.1std/590/ib_installers/arriav-17.1.0.590.qdz",
    'm5' : "https://download.altera.com/akdlm/software/acdsinst/17.1std/590/ib_installers/arriav-17.1.0.590.qdz",
    'm10' : "https://download.altera.com/akdlm/software/acdsinst/17.1std/590/ib_installers/arriav-17.1.0.590.qdz",
    'update_1' : "https://download.altera.com/akdlm/software/acdsinst/17.1std.1/593/update/QuartusSetup-17.1.1.593-windows.exe",
    'dsp' : 'https://download.altera.com/akdlm/software/acdsinst/17.1std/590/ib_installers/DSPBuilderSetup-17.1.0.590-windows.exe',
    'opencl' : 'https://download.altera.com/akdlm/software/acdsinst/17.1std/590/ib_installers/AOCLSetup-17.1.0.590-windows.exe',
    'eds' : 'https://download.altera.com/akdlm/software/acdsinst/17.1std/590/ib_installers/SoCEDSSetup-17.1.0.590-windows.exe'
}

quartus_url_171pro = {
    'setup' : "https://download.altera.com/akdlm/software/acdsinst/17.1/240/ib_installers/QuartusProSetup-17.1.0.240-windows.exe",
    'modelsim' : "https://download.altera.com/akdlm/software/acdsinst/17.1/240/ib_installers/QuartusProSetup-17.1.0.240-windows.exe",
    'a10_part1' : "https://download.altera.com/akdlm/software/acdsinst/17.1/240/ib_installers/arria10_part1-17.1.0.240.qdz",
    'a10_part2' : "https://download.altera.com/akdlm/software/acdsinst/17.1/240/ib_installers/arria10_part2-17.1.0.240.qdz",
    'a10_part3' : "https://download.altera.com/akdlm/software/acdsinst/17.1/240/ib_installers/arria10_part3-17.1.0.240.qdz",
    'c10gx_part1' : "https://download.altera.com/akdlm/software/acdsinst/17.1/240/ib_installers/cyclone10gx_part1-17.1.0.240.qdz",
    'c10gx_part2' : "https://download.altera.com/akdlm/software/acdsinst/17.1/240/ib_installers/cyclone10gx_part2-17.1.0.240.qdz",
    's10_part1' : "https://download.altera.com/akdlm/software/acdsinst/17.1/240/ib_installers/stratix10_part1-17.1.0.240.qdz",
    's10_part2' : "https://download.altera.com/akdlm/software/acdsinst/17.1/240/ib_installers/stratix10_part2-17.1.0.240.qdz",
    's10_part3' : "https://download.altera.com/akdlm/software/acdsinst/17.1/240/ib_installers/stratix10_part3-17.1.0.240.qdz",
    'update_1' : "https://download.altera.com/akdlm/software/acdsinst/17.1.2/304/update/QuartusProSetup-17.1.2.304-windows.exe"
}

quartus_url_180pro = {
    'setup' : 'https://download.altera.com/akdlm/software/acdsinst/18.0/219/ib_installers/QuartusProSetup-18.0.0.219-windows.exe',
    'a10_part1' : "https://download.altera.com/akdlm/software/acdsinst/18.0/219/ib_installers/arria10-18.0.0.219.qdz",
    'c10gx_part1' : "https://download.altera.com/akdlm/software/acdsinst/18.0/219/ib_installers/cyclone10gx-18.0.0.219.qdz",
    's10_part1' : "https://download.altera.com/akdlm/software/acdsinst/18.0/219/ib_installers/stratix10-18.0.0.219.qdz",
    'update_1': "https://download.altera.com/akdlm/software/acdsinst/18.0.1/261/update/QuartusProSetup-18.0.1.261-windows.exe"
}


quartus_url_180std = {
    'setup' : "https://download.altera.com/akdlm/software/acdsinst/18.0std/614/ib_installers/QuartusSetup-18.0.0.614-windows.exe",
    'a2' : "https://download.altera.com/akdlm/software/acdsinst/18.0std/614/ib_installers/arria-18.0.0.614.qdz",
    'a10_part1' : "https://download.altera.com/akdlm/software/acdsinst/18.0std/614/ib_installers/arria10_part1-18.0.0.614.qdz",
    'a10_part2' : "https://download.altera.com/akdlm/software/acdsinst/18.0std/614/ib_installers/arria10_part2-18.0.0.614.qdz",
    'a10_part3' : "https://download.altera.com/akdlm/software/acdsinst/18.0std/614/ib_installers/arria10_part3-18.0.0.614.qdz",
    'a5': "https://download.altera.com/akdlm/software/acdsinst/18.0std/614/ib_installers/arriav-18.0.0.614.qdz",
    'a5gz' : "https://download.altera.com/akdlm/software/acdsinst/18.0std/614/ib_installers/arriavgz-18.0.0.614.qdz",
    'c4': "https://download.altera.com/akdlm/software/acdsinst/18.0std/614/ib_installers/cyclone-18.0.0.614.qdz",
    'c10lp' : "https://download.altera.com/akdlm/software/acdsinst/18.0std/614/ib_installers/cyclone10lp-18.0.0.614.qdz",
    'c5' : "https://download.altera.com/akdlm/software/acdsinst/18.0std/614/ib_installers/cyclonev-18.0.0.614.qdz",
    'm5': "https://download.altera.com/akdlm/software/acdsinst/18.0std/614/ib_installers/max-18.0.0.614.qdz",
    'm10' : "https://download.altera.com/akdlm/software/acdsinst/18.0std/614/ib_installers/max10-18.0.0.614.qdz",
    's4' : "https://download.altera.com/akdlm/software/acdsinst/18.0std/614/ib_installers/stratixiv-18.0.0.614.qdz",
    's5': "https://download.altera.com/akdlm/software/acdsinst/18.0std/614/ib_installers/stratixv-18.0.0.614.qdz"
}

quartus_url_180lite = dict(quartus_url_180std)
quartus_url_180lite['setup'] = 'https://download.altera.com/akdlm/software/acdsinst/18.0std/614/ib_installers/QuartusLiteSetup-18.0.0.614-windows.exe'

quartus_url_170pro = {
    'setup' : "https://download.altera.com/akdlm/software/acdsinst/17.0/290/ib_installers/QuartusProSetup-17.0.0.290-windows.exe",
    'a10_part1' : "https://download.altera.com/akdlm/software/acdsinst/17.0/290/ib_installers/arria10_part1-17.0.0.290.qdz",
    'a10_part2' : "https://download.altera.com/akdlm/software/acdsinst/17.0/290/ib_installers/arria10_part2-17.0.0.290.qdz",
    'a10_part3' : "https://download.altera.com/akdlm/software/acdsinst/17.0/290/ib_installers/arria10_part3-17.0.0.290.qdz",
    'c10gx_part1' : "https://download.altera.com/akdlm/software/acdsinst/17.0/290/ib_installers/cyclone10gx_part1-17.0.0.290.qdz",
    'c10gx_part2' : "https://download.altera.com/akdlm/software/acdsinst/17.0/290/ib_installers/cyclone10gx_part2-17.0.0.290.qdz"
}

quartus_url_170std = {
    'setup' : "https://download.altera.com/akdlm/software/acdsinst/17.0std/595/ib_installers/QuartusSetup-17.0.0.595-windows.exe",
    'a2' : "https://download.altera.com/akdlm/software/acdsinst/17.0std/595/ib_installers/arria-17.0.0.595.qdz",
    'a10_part1' : "https://download.altera.com/akdlm/software/acdsinst/17.0std/595/ib_installers/arria10_part1-17.0.0.595.qdz",
    'a10_part2' : "https://download.altera.com/akdlm/software/acdsinst/17.0std/595/ib_installers/arria10_part2-17.0.0.595.qdz",
    'a10_part3' : "https://download.altera.com/akdlm/software/acdsinst/17.0std/595/ib_installers/arria10_part3-17.0.0.595.qdz",
    'a5' : "https://download.altera.com/akdlm/software/acdsinst/17.0std/595/ib_installers/arriav-17.0.0.595.qdz",
    'c4' : "https://download.altera.com/akdlm/software/acdsinst/17.0std/595/ib_installers/cyclone-17.0.0.595.qdz",
    'c10lp' : "https://download.altera.com/akdlm/software/acdsinst/17.0std/595/ib_installers/cyclone10lp-17.0.0.595.qdz",
    'c5' : "https://download.altera.com/akdlm/software/acdsinst/17.0std/595/ib_installers/cyclonev-17.0.0.595.qdz",
    'm5' : "https://download.altera.com/akdlm/software/acdsinst/17.0std/595/ib_installers/max-17.0.0.595.qdz",
    'm10' : "https://download.altera.com/akdlm/software/acdsinst/17.0std/595/ib_installers/max10-17.0.0.595.qdz",
    's4' : "https://download.altera.com/akdlm/software/acdsinst/17.0std/595/ib_installers/stratixiv-17.0.0.595.qdz",
    's5' : "https://download.altera.com/akdlm/software/acdsinst/17.0std/595/ib_installers/stratixv-17.0.0.595.qdz",
}

quartus_url_161std = {
    'setup' : "https://download.altera.com/akdlm/software/acdsinst/16.1/196/ib_installers/QuartusSetup-16.1.0.196-windows.exe",
    'a2' : "https://download.altera.com/akdlm/software/acdsinst/16.1/196/ib_installers/arria-16.1.0.196.qdz",
    'a10_part1' : "https://download.altera.com/akdlm/software/acdsinst/16.1/196/ib_installers/arria10_part1-16.1.0.196.qdz",
    'a10_part2' : "https://download.altera.com/akdlm/software/acdsinst/16.1/196/ib_installers/arria10_part2-16.1.0.196.qdz",
    'a10_part3' : "https://download.altera.com/akdlm/software/acdsinst/16.1/196/ib_installers/arria10_part3-16.1.0.196.qdz",
    'a5' : "https://download.altera.com/akdlm/software/acdsinst/16.1/196/ib_installers/arriav-16.1.0.196.qdz",
    'c4' : "https://download.altera.com/akdlm/software/acdsinst/16.1/196/ib_installers/cyclone-16.1.0.196.qdz",
    'm2' : "https://download.altera.com/akdlm/software/acdsinst/16.1/196/ib_installers/max-16.1.0.196.qdz",
    'm10' : "https://download.altera.com/akdlm/software/acdsinst/16.1/196/ib_installers/max10-16.1.0.196.qdz",
    's4' : "https://download.altera.com/akdlm/software/acdsinst/16.1/196/ib_installers/stratixiv-16.1.0.196.qdz",
    's5' : "https://download.altera.com/akdlm/software/acdsinst/16.1/196/ib_installers/stratixv-16.1.0.196.qdz"
    
}

quartus_url_171lite = dict(quartus_url_171std)
quartus_url_171lite['setup'] = "https://download.altera.com/akdlm/software/acdsinst/17.1std/590/ib_installers/QuartusLiteSetup-17.1.0.590-windows.exe"


quartus_url_160std = {
	'setup' : 'https://download.altera.com/akdlm/software/acdsinst/16.0/211/ib_installers/QuartusSetup-16.0.0.211-windows.exe',
	'modelsim' : 'https://download.altera.com/akdlm/software/acdsinst/16.0/211/ib_installers/ModelSimSetup-16.0.0.211-windows.exe',
	'a2' : 'https://download.altera.com/akdlm/software/acdsinst/16.0/211/ib_installers/arria-16.0.0.211.qdz',
	'a10_part1' : 'https://download.altera.com/akdlm/software/acdsinst/16.0/211/ib_installers/arria10_part1-16.0.0.211.qdz',
	'a10_part2' : 'https://download.altera.com/akdlm/software/acdsinst/16.0/211/ib_installers/arria10_part2-16.0.0.211.qdz',
	'a10_part3' : 'https://download.altera.com/akdlm/software/acdsinst/16.0/211/ib_installers/arria10_part3-16.0.0.211.qdz',
	'a5' : 'https://download.altera.com/akdlm/software/acdsinst/16.0/211/ib_installers/arriav-16.0.0.211.qdz',
	'a5gz' : 'https://download.altera.com/akdlm/software/acdsinst/16.0/211/ib_installers/arriavgz-16.0.0.211.qdz',
	'c4' : 'https://download.altera.com/akdlm/software/acdsinst/16.0/211/ib_installers/cyclone-16.0.0.211.qdz',
	'c5' : 'https://download.altera.com/akdlm/software/acdsinst/16.0/211/ib_installers/cyclonev-16.0.0.211.qdz',
	'm2' : 'https://download.altera.com/akdlm/software/acdsinst/16.0/211/ib_installers/max-16.0.0.211.qdz',
	'm10' : 'https://download.altera.com/akdlm/software/acdsinst/16.0/211/ib_installers/max10-16.0.0.211.qdz',
	's4' : 'https://download.altera.com/akdlm/software/acdsinst/16.0/211/ib_installers/stratixiv-16.0.0.211.qdz',
	's5' : 'https://download.altera.com/akdlm/software/acdsinst/16.0/211/ib_installers/stratixv-16.0.0.211.qdz'
}

quartus_url_151std = {
	'setup' : 'https://download.altera.com/akdlm/software/acdsinst/15.1/185/ib_installers/QuartusSetup-15.1.0.185-windows.exe',
	'modelsim' : 'https://download.altera.com/akdlm/software/acdsinst/15.1/185/ib_installers/ModelSimSetup-15.1.0.185-windows.exe',
	'a2' : 'https://download.altera.com/akdlm/software/acdsinst/15.1/185/ib_installers/arria-15.1.0.185.qdz',
	'a10_part1' : 'https://download.altera.com/akdlm/software/acdsinst/15.1/185/ib_installers/arria10_part1-15.1.0.185.qdz',
	'a10_part2' : 'https://download.altera.com/akdlm/software/acdsinst/15.1/185/ib_installers/arria10_part2-15.1.0.185.qdz',
	'a10_part3' : 'https://download.altera.com/akdlm/software/acdsinst/15.1/185/ib_installers/arria10_part3-15.1.0.185.qdz',
	'a5' : 'https://download.altera.com/akdlm/software/acdsinst/15.1/185/ib_installers/arriav-15.1.0.185.qdz',
	'a5gz' : 'https://download.altera.com/akdlm/software/acdsinst/15.1/185/ib_installers/arriavgz-15.1.0.185.qdz',
	'c4' : 'https://download.altera.com/akdlm/software/acdsinst/15.1/185/ib_installers/cyclone-15.1.0.185.qdz',
	's4' : 'https://download.altera.com/akdlm/software/acdsinst/15.1/185/ib_installers/stratixiv-15.1.0.185.qdz',
	's5' : 'https://download.altera.com/akdlm/software/acdsinst/15.1/185/ib_installers/stratixv-15.1.0.185.qdz'
}

quartus_url_150web = {
        'setup' : 'https://download.altera.com/akdlm/software/acdsinst/15.0/145/ib_installers/QuartusSetupWeb-15.0.0.145-windows.exe',
        'modelsim' : 'https://download.altera.com/akdlm/software/acdsinst/15.0/145/ib_installers/ModelSimSetup-15.0.0.145-windows.exe',
        'a2' : 'https://download.altera.com/akdlm/software/acdsinst/15.0/145/ib_installers/arria-15.0.0.145.qdz',
        'c4' : 'https://download.altera.com/akdlm/software/acdsinst/15.0/145/ib_installers/cyclone-15.0.0.145.qdz',
        'c5' : 'https://download.altera.com/akdlm/software/acdsinst/15.0/145/ib_installers/cyclonev-15.0.0.145.qdz',
        'm2' : 'https://download.altera.com/akdlm/software/acdsinst/15.0/145/ib_installers/max-15.0.0.145.qdz',
        'm10' : 'https://download.altera.com/akdlm/software/acdsinst/15.0/145/ib_installers/max10-15.0.0.145.qdz'
}

quartus_url_141web = {
        'setup' : 'https://download.altera.com/akdlm/software/acdsinst/14.1/186/ib_installers/QuartusSetupWeb-14.1.0.186-windows.exe',
        'modelsim' : 'https://download.altera.com/akdlm/software/acdsinst/14.1/186/ib_installers/ModelSimSetup-14.1.0.186-windows.exe',
        'a2' : 'https://download.altera.com/akdlm/software/acdsinst/14.1/186/ib_installers/arria-14.1.0.186.qdz',
        'c4' : 'https://download.altera.com/akdlm/software/acdsinst/14.1/186/ib_installers/cyclone-14.1.0.186.qdz',
        'c5' : 'https://download.altera.com/akdlm/software/acdsinst/14.1/186/ib_installers/cyclonev-14.1.0.186.qdz',
        'm2' : 'https://download.altera.com/akdlm/software/acdsinst/14.1/186/ib_installers/max-14.1.0.186.qdz',
        'm10' : 'https://download.altera.com/akdlm/software/acdsinst/14.1/186/ib_installers/max10-14.1.0.186.qdz'
}

quartus_url_140web = {
        'setup' : 'https://download.altera.com/akdlm/software/acdsinst/14.0/200/ib_installers/QuartusSetupWeb-14.0.0.200-windows.exe',
        'modelsim' : 'https://download.altera.com/akdlm/software/acdsinst/14.0/200/ib_installers/ModelSimSetup-14.0.0.200-windows.exe',
        'a2' : 'https://download.altera.com/akdlm/software/acdsinst/14.0/200/ib_installers/arria-14.0.0.200.qdz',
        'c4' : 'https://download.altera.com/akdlm/software/acdsinst/14.0/200/ib_installers/cyclone-14.0.0.200.qdz',
        'c5' : 'https://download.altera.com/akdlm/software/acdsinst/14.0/200/ib_installers/cyclonev-14.0.0.200.qdz',
        'm2' : 'https://download.altera.com/akdlm/software/acdsinst/14.0/200/ib_installers/max-14.0.0.200.qdz',
}

quartus_url_131web = {
        'setup' : 'https://download.altera.com/akdlm/software/acdsinst/13.1/162/ib_installers/QuartusSetupWeb-13.1.0.162.exe',
        'modelsim' : 'https://download.altera.com/akdlm/software/acdsinst/13.1/162/ib_installers/ModelSimSetup-13.1.0.162.exe',
        'a2' : 'https://download.altera.com/akdlm/software/acdsinst/13.1/162/ib_installers/arria-13.1.0.162.qdz',
        'c4' : 'https://download.altera.com/akdlm/software/acdsinst/13.1/162/ib_installers/cyclone-13.1.0.162.qdz',
        'c5' : 'https://download.altera.com/akdlm/software/acdsinst/13.1/162/ib_installers/cyclonev-13.1.0.162.qdz',
        'm2' : 'https://download.altera.com/akdlm/software/acdsinst/13.1/162/ib_installers/max-13.1.0.162.qdz',
}

quartus_url_130sp1web = {
        'setup' : 'https://download.altera.com/akdlm/software/acdsinst/13.0sp1/232/ib_installers/QuartusSetupWeb-13.0.1.232.exe',
        'modelsim' : 'https://download.altera.com/akdlm/software/acdsinst/13.0sp1/232/ib_installers/ModelSimSetup-13.0.1.232.exe',
        'a2' : 'https://download.altera.com/akdlm/software/acdsinst/13.0sp1/232/ib_installers/arria-13.0.1.232.qdz',
        'c4' : 'https://download.altera.com/akdlm/software/acdsinst/13.0sp1/232/ib_installers/cyclone-13.0.1.232.qdz',
        'c5' : 'https://download.altera.com/akdlm/software/acdsinst/13.0sp1/232/ib_installers/cyclonev-13.0.1.232.qdz',
        'm2' : 'https://download.altera.com/akdlm/software/acdsinst/13.0sp1/232/ib_installers/max-13.0.1.232.qdz',
}


quartus_versions = {
    '13.0sp1web' : quartus_url_130sp1web,
    '13.1web' : quartus_url_131web,
    '14.0web' : quartus_url_140web,
    '14.1web' : quartus_url_141web,
    '15.0web' : quartus_url_150web,
    '15.1std' : quartus_url_151std,
    '16.0std' : quartus_url_160std,
    '16.1std' : quartus_url_161std,
    '17.0pro' : quartus_url_170pro,
    '17.0std' : quartus_url_170std,
    '17.1pro' : quartus_url_171pro,
    '17.1std' : quartus_url_171std,
    '17.1lite' : quartus_url_171lite,
    '18.0pro' : quartus_url_180pro,
    '18.0std' : quartus_url_180std,
    '18.0lite' : quartus_url_180lite,
    '18.1pro' : quartus_url_181pro,
    '18.1std' : quartus_url_181std,
    '18.1lite' : quartus_url_181lite,
    '19.1std' : quartus_url_191std,
    '19.1lite' : quartus_url_191lite,	
    '19.1pro' : quartus_url_191pro,
    '19.2pro' : quartus_url_192pro,
    '19.3pro' : quartus_url_193pro,
    '19.4pro' : quartus_url_194pro,
    '20.1std' : quartus_url_201std,
    '20.1.1std' : quartus_url_2011std,
    '20.1lite' : quartus_url_201lite,
    '20.1.1lite' : quartus_url_2011lite,
    '20.1pro' : quartus_url_201pro,
    '20.2pro' : quartus_url_202pro,
    '20.3pro' : quartus_url_203pro
}


import os
import subprocess
import sys
import argparse
import tempfile
import stat

def match_wanted_parts(version, devices):
    # work out what devices we have available
    # and filter down to the list we want
    parts = list(quartus_versions[version].keys())
    parts.remove('setup')
    wanted_parts = []
    for part in parts:
        if part.split("_",1)[0] in devices:
            wanted_parts.append(part)
        if part.split("_",1)[0] == "patch":
            wanted_parts.append(part)
        if part.split("_",1)[0] == "update":
            wanted_parts.append(part)
        if part == "setup_part2":
            wanted_parts.append(part)
    return wanted_parts


def download_quartus(version, parts, args):
    # convert the pieces we need to a list of URLs
    urls = {x: quartus_versions[version][x] for x in parts}.values()
    for url in urls:
            print(url)
    return urls


def install_quartus(version, installdir):
    setup = quartus_versions[version]['setup']
    rc = run_installer(setup, installdir)
    return rc
    
def run_installer(installerfile, installdir):
    leafname = os.path.basename(installerfile)
    target = os.path.abspath(installdir)
    args = ['--mode', 'unattended', '--unattendedmodeui', 'minimal']
    numeric_version = ''.join(i for i in version if i.isdigit() or i=='.')
    if numeric_version >= '17.1':
        args = args + ['--accept_eula', '1']
    process = subprocess.Popen(['./'+leafname] + args + ['--installdir', target], bufsize=1)
    rc = process.wait()
    return rc
#            ./$QUARTUS_SCRIPT --mode unattended --unattendedmodeui minimal --installdir $QUARTUS_DIR && \
    
def install_patch(version, installdir, patchname):
    patchfile = quartus_versions[version][patchname]
    rc = run_installer(patchfile, installdir)
    return rc

def cmd_exists(cmd):
    return subprocess.call("type " + cmd, shell=True, 
        stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0



parser = argparse.ArgumentParser(description='Download and install Quartus.')
parser.add_argument('--download-only', action='store_true', help='Only download, don\'t install')
parser.add_argument('version', help='Quartus version, eg 18.0pro, 17.1lite, 16.1std')
parser.add_argument('target', help='Directory to install Quartus in')
parser.add_argument('device', nargs='+', help='Device to download/install in Quartus, eg s5 (Stratix 5), a10 (Arria 10), m2 (MAX II), c10gx (Cyclone 10GX)')
args = parser.parse_args(sys.argv[1:])

version = args.version
target = args.target
parts = []


if version not in quartus_versions.keys():
    print("Unrecognised Quartus version '%s'" % version)
    print("Supported versions are:")
    for key in quartus_versions.keys():
        print(key)
    sys.exit(1)

if not args.nosetup:
    parts = parts + ['setup']
parts = parts + match_wanted_parts(version, args.device)
if not args.install_only:
    print("Downloading Quartus %s parts %s\n" % (version, parts))
    urls = download_quartus(version, parts, args)
    for url in urls:
        leafname = url[url.rfind("/")+1:]




