from setuptools import setup, find_packages
setup(
    name='KS_Constants',
    version="1.2.69",  # Make sure there are no spaces around =
    license='MIT',
    author="Steven Su",
    author_email='ks2devteam@gmail.com',
    packages=find_packages(),
    url='https://github.com/kerrigan-survival-team/ks_constants_py',
    description='Contains constants defined for Kerrigan Survival 2',  # Add a short description
    long_description="Contains constants defined for Kerrigan Survival 2",
    long_description_content_type='text/markdown'  # Specify content type
)