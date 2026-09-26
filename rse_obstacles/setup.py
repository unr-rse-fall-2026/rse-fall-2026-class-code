from setuptools import find_packages, setup

package_name = 'rse_obstacles'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools', 'numpy'],
    zip_safe=True,
    maintainer='dfseifer',
    maintainer_email='dfseifer@unr.edu',
    description='TODO: Package description',
    license='BSD-3-Clause',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
                'scan_parser = rse_obstacles.scan_parser:main',
                'extra_code = rse_obstacles.extra_code:main',
        ],
    },
)
