from setuptools import setup, find_packages
import TotpApp as package

setup(
    name='TotpApp',
    version=package.__version__,
    py_modules=['TotpApp'],
    packages=find_packages(include=[]),
    install_requires=[],
    scripts=[],
    author="Maurice Lambert",
    author_email="mauricelambert434@gmail.com",
    maintainer="Maurice Lambert",
    maintainer_email="mauricelambert434@gmail.com",
    description="This little app generates your TOTP from your secret (you can use secret as password in a password manager), you don't need any phone or other device",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/mauricelambert/TotpApp",
    project_urls={
        "Github": "https://github.com/mauricelambert/TotpApp",
        "Documentation": "https://mauricelambert.github.io/info/python/security/TotpApp.html",
        "Python Executable": "https://mauricelambert.github.io/info/python/security/TotpApp.pyz",
        "Windows Executable": "https://mauricelambert.github.io/info/python/security/TotpApp.exe",
    },
    download_url="https://mauricelambert.github.io/info/python/security/TotpApp.pyz",
    include_package_data=True,
    classifiers=[
        "Topic :: Security",
        'Operating System :: POSIX',
        "Natural Language :: English",
        "Programming Language :: Python",
        "Intended Audience :: Developers",
        'Operating System :: MacOS :: MacOS X',
        "Programming Language :: Python :: 3.8",
        'Operating System :: Microsoft :: Windows',
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
    ],
    keywords=['TOTP', 'application', 'password', 'authentication', '2FA', 'MFA', 'tkinter'],
    platforms=['Windows', 'Linux', "MacOS"],
    license="GPL-3.0 License",
    entry_points = {
        'gui_scripts': [
            'TotpApp = TotpApp:main'
        ],
    },
    python_requires='>=3.8',
)