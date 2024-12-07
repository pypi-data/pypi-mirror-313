from setuptools import setup

setup(
    name='umkt-service-utility-v2',
    version='1.0',
    author='2ez4ad1',
    author_email='mra441@umkt.ac.id',
    description='This is description',
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