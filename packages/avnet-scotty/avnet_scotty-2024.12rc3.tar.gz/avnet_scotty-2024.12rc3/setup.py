# SPDX-FileCopyrightText: (C) 2022 Avnet Embedded GmbH
# SPDX-License-Identifier: GPL-3.0-only
# noqa: D100

import setuptools
import os

_version = os.environ.get('SCOTTY_VERSION', '0.0.1')

requirements = []
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

long_description = '''
Scotty is a tool to make the process of building the SimpleCore™ Distro distribution
reproducible on any Linux and Windows computer (compatible with WSL2). It uses a
container to setup the same environment used by our continuous integration
process to ensure that the build on your machine will always be successful for
any of our standard images. Scotty is based on standard open-source tools such as
Docker, repo, ... and mimics the standard bitbake command set (standard tool for
Yocto builds). If you are not familiar with building Yocto BSPs, we strongly
recommend that you use Scotty to start with.

For more details please visit our [Documentation](https://simple.embedded.avnet.com/index.hmtl?link=tools/scotty/README.html).
'''

setuptools.setup(
    author='Avnet Embedded GmbH',
    description='scotty: S(imple)C(ore) O(pen) T(echnology) T(ool for) Y(ou)',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='GPL-3.0-only',
    license_files=('LICENSE',),
    entry_points={
        'console_scripts': [
            'bumper = bumper.__main__:main',
        ],
    },
    project_urls={
        'Documentation': 'https://simple.embedded.avnet.com/?link=tools/scotty/README.html',
        'SimpleCore Documentation': 'https://simple.embedded.avnet.com/',
        'Source Code': 'https://github.com/avnet-embedded/simplecore-tools/tree/kirkstone/scotty'
    },
    packages=[
        'bumper',
    ],
    install_requires=requirements,
    include_package_data=True,
    # As scotty is already in use on PyPi our package is called
    # avnet-scotty
    name='avnet-scotty',
    scripts=[
        'scotty-doc-link-checker',
        'scotty-docker',
        'scotty-oeqa-report-enhancer',
        'scotty-runqemu',
        'scotty-test',
        'scotty',
        'scripts/scotty_vm_bundle.sh',
        'scripts/scotty_vm_create.sh.template',
        'scripts/scotty-data-gen',
        'scripts/scotty-dynamic-matrix',
        'scripts/scotty-layer-coverage',
        'scripts/scotty-qa-log-filter',
        'scripts/scotty-shutdown-check',
        'scripts/scotty-start-vm',
        'scripts/scotty-stop-vm',
        'scripts/scotty-testreport',
        'scripts/scotty-update-recipes-notification',
    ],
    # once upgraded readd 'scripts/scotty-check-layer-test',
    version=_version,
)
