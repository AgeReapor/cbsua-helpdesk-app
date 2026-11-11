from setuptools import find_packages, setup

from cbsua_helpdesk import __version__


setup(
    name="cbsua_helpdesk",
    version=__version__,
    description="CBSUA-specific extensions for Frappe Helpdesk",
    author="CBSUA",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)
