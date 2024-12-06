import os
import platform
from setuptools import setup, find_packages
from setuptools.command.install import install
import subprocess

class CustomInstallCommand(install):
    """Customized setuptools install command to convert README to man page and install it."""
    def run(self):
        if platform.system() != 'Windows':
            # Check if pandoc is available
            try:
                subprocess.run(['pandoc', '--version'], check=True)
            except subprocess.CalledProcessError:
                print("Pandoc is not available. Skipping man page generation.")
                install.run(self)
                return

            # Convert README.md to man page using pandoc
            subprocess.run(['pandoc', 'README.md', '-s', '-t', 'man', '-o', 'nomad-media-cli.1'])
            
            # Install the man page
            man_dir = '/usr/share/man/man1'
            if not os.path.exists(man_dir):
                os.makedirs(man_dir)
            subprocess.run(['sudo', 'cp', 'nomad-media-cli.1', man_dir])
            subprocess.run(['sudo', 'mandb'])
        else:
            print("Skipping man page generation on Windows.")

        # Run the standard install process
        install.run(self)

setup(
    name='nomad_media_cli',
    version='0.0.1a14',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click',
        'platformdirs',
        'nomad-media-pip==0.1.2a8',
    ],
    entry_points={
        'console_scripts': [
            'nomad-media-cli=nomad_media_cli.cli:cli',
        ],
    },
    cmdclass={
        'install': CustomInstallCommand,
    },
    author='Nomad Media',
    description='Nomad Media CLI',
    classifiers=[
        'Programming Language :: Python :: 3.12',
    ],
    python_requires='>=3.12',
)