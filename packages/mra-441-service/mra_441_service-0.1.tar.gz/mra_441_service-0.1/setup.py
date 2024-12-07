from setuptools import setup

setup(
    name='mra-441-service',
    version='0.1',
    author='adi ganteng',
    author_email='mra441@umkt.ac.id',
    description='My package description',
    long_description="""# Markdown supported!\n\n* Cheer\n* Celebrate\n""",
    long_description_content_type='text/markdown',
    url='https://git.umkt.ac.id/services/umkt-service-utility',
    packages=['umkt_service_utils'],
    install_requires=[
        'django',
        'djangorestframework',
        'requests',
        'PyJWT',
        'python-decouple',
    ],
)