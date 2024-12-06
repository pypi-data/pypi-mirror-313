from setuptools import setup, find_packages

setup(
    name="nciscraper",  # Name of your package
    version="0.3.0",  # Version number
    author="Tux MacGiver",  # Your name or the name of your organization
    author_email="tuxmacg1v991@gmail.com",  # Your email address
    description="A Python package to fetch web content using different advance methods.",
    long_description=open('README.md').read(),  # Read long description from README.md
    long_description_content_type="text/markdown",  # Use markdown for README
    url="https://github.com/Tux-MacG1v/nciscraper",  # URL of your GitHub repo
    license='MIT',  # License type
    include_package_data=True,
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # Adjust if using another license
        'Operating System :: OS Independent',
    ],
    install_requires=[
        "requests",
        "cloudscraper",
        "selenium",
        "seleniumbase",
        "playwright",
        "beautifulsoup4",
        "fake_useragent",
        "webdriver-manager",
        "bs4",
        "tenacity",
    ],
    python_requires='>=3.6',  # Minimum Python version required
)
