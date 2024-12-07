from distutils.core import setup
setup(
  name = 'cpemailautomationai',         # How you named your package folder (MyLib)
  packages = [''],   # Chose the same as "name"
  version = '1.0.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'My private package from private github repo',   # Give a short description about your library
  author = 'Anand',                   # Type in your name
  author_email = 'anandraman249@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/AnandMurugan5/emailclassification',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/AnandMurugan5/emailclassification.git',    # I explain this later on
  keywords = ['EMAILCLASSIFICATION', 'WEBAUTOMATION'],   # Keywords that define your package best
  install_requires=[
    "attrs==24.2.0",
    "certifi==2024.8.30",
    "cffi==1.17.1",
    "charset-normalizer==3.4.0",
    "h11==0.14.0",
    "idna==3.10",
    "IMAPClient==3.0.1",
    "numpy==2.1.3",
    "outcome==1.3.0.post0",
    "pandas",
    "pycparser==2.22",
    "PySocks==1.7.1",
    "pyzmail36==1.0.5",
    "requests==2.32.3",
    "selenium==4.27.1",
    "sniffio==1.3.1",
    "sortedcontainers==2.4.0",
    "trio==0.27.0",
    "trio-websocket==0.11.1",
    "typing_extensions==4.12.2",
    "urllib3==2.2.3",
    "websocket-client==1.8.0",
    "wsproto==1.2.0",
],

  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11',
  ],
)