from setuptools import find_packages, setup

setup(
    name='netbox_cesnet_services_plugin',
    version='1.1.3',
    description='NetBox plugin for cesnet_services.',
    author='Jan Krupa',
    license='MIT',
    install_requires=[],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)
