from setuptools import setup, find_packages

setup(
    name='neurostats_API',
    version='0.0.12',
    long_description=open('README.md', 'r', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    install_requires=[
    ],
    author='JasonWang@Neurowatt',
    packages=find_packages(exclude=['.venv', 'test*', 'data_in_db', '.pytest_cache']),
    include_package_data=True,
    # package_dir={'neurostats_service': 'src'},
    package_data={'neurostats_API': ['tools/*.yaml', 'tools/*.txt']},
    author_email='jason@neurowatt.ai',
    description='The service of NeuroStats website',
    url='https://github.com/NeurowattStats/NeuroStats_API.git',
    python_requires='>=3.6'
)
