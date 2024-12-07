from setuptools import setup, find_packages

setup(
    name="server_report",  # The name of your package (used during installation)
    version="0.1",  # The version of your package
    packages=find_packages(where='src'),  # Look for packages inside the src folder
    package_dir={'': 'src'},  # Where to find the package (in the 'src' directory)
    install_requires=[  # Dependencies
        'psutil',
        'requests',
    ],
    include_package_data=True,  # Include non-Python files like config.yaml
    data_files=[('config', ['src/config.yaml'])],  # Optional: If you want to include a config file
    entry_points={
        'console_scripts': [
            'server_report = server_report.agent:main',  # Define the command to run your agent
        ],
    },
    description="A simple Python agent for monitoring system and server status.",
    author="Amrutha",
    author_email="demo16609@gmail.com",
    # url="https://github.com/your-repository-url",  # URL of your project
)
