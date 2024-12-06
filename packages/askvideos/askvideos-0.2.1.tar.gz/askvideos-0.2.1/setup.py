from setuptools import setup, find_packages

setup(
    name='askvideos',  # Replace 'your_package_name' with the name of your package
    version='0.2.1',  # Version number for your package
    author='AskVideos',  # Your name or your organization's name
    author_email='askutubeai@gmail.com',  # Your email or your organization's contact email
    description='AskVideos python library',  # A brief description of your package
    long_description=open('README.md').read(),  # A long description from your README.md
    long_description_content_type='text/markdown',  # Specifies that the long description is in Markdown
    url='https://github.com/AskYoutubeAI/askvideos-py',  # URL to your package's repository
    #packages=find_packages(exclude=('tests', 'docs')),  # Automatically find all packages in your project
    install_requires=[
        # List your project's dependencies here.
        # They will be installed by pip when your package is installed.
        # Example: 'requests>=2.19.1'
        "requests",
    ],
    python_requires='>=3.6',  # Minimum version requirement of Python
    #entry_points={
    #    'console_scripts': [
    #        # Entry points for console scripts
    #        # Example: 'your_script_name = your_package.module:function'
    #    ],
    #},
)

