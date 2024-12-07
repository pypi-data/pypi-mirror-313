from setuptools import setup, find_packages
from setuptools.command.install import install

class PostInstallCommand(install):
    """Post-installation for copying lab manuals."""
    def run(self):
        # Run the standard installation process
        install.run(self)

        # Run the post-install script
        try:
            from compiler_lab_manual.post_install import copy_lab_manuals
            copy_lab_manuals()
        except ImportError as e:
            print(f"Error: {e}")
            print("Could not copy lab manuals.")

setup(
    name='compiler-lab-manual',
    version='1.1.1',
    author='Problem Solver',
    author_email='treecse@gmail.com',
    description='A package for Compiler Lab Manual exercises',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/trackers-new/compiler-lab-manual',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,  # Include lab manual files
    package_data={
        'compiler_lab_manual': ['lab_manuals/*'],  # Include all files in lab_manuals
    },
    cmdclass={
        'install': PostInstallCommand,  # Use custom install command
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
