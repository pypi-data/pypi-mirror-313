from setuptools import setup, find_packages

setup(
    name='package_server_report_website_side',  # Name of your package
    version='0.1.0',  # Version of your package
    description='A tool to monitor website performance, SEO, UI, and security, and generate reports.',
    long_description=open('README.md').read(),  # Read long description from README.md
    long_description_content_type='text/markdown',
    author='Your Name',  # Your name here
    author_email='your-email@example.com',  # Your email here
    url='https://github.com/yourusername/package_server_report_website_side',  # GitHub URL or your project URL
    license='MIT',  # License type (e.g., MIT License)
    packages=find_packages(),  # Automatically finds all Python packages
    include_package_data=True,  # Ensures non-Python files are included
    install_requires=[  # List of dependencies
        'flask',
        'requests',
        'beautifulsoup4',
        'pandas',
        'openpyxl',
        'reportlab',
        'lxml',
    ],
    entry_points={  # Entry point for console scripts
        'console_scripts': [
            'website-monitor = package_server_report_website_side.app:main',  # Point to app.py
        ],
    },
    classifiers=[  # Classifiers help others find your package
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Minimum Python version required
)
