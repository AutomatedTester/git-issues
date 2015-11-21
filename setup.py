from setuptools import setup, find_packages

setup(name='git-issues',
      version='0.1.0',
      description='A binary for taking issues offline with you',
      author='David Burns',
      author_email='david.burns at theautomatedtester dot co dot uk',
      url='https://github.com/AutomatedTester/git-issues',
      classifiers=['Development Status :: 3 - Alpha',
                  'Intended Audience :: Developers',
                  'License :: OSI Approved :: Apache Software License',
                  'Operating System :: POSIX',
                  'Operating System :: Microsoft :: Windows',
                  'Operating System :: MacOS :: MacOS X',
                  'Topic :: Software Development :: Libraries',
                  'Programming Language :: Python'],
        packages = find_packages(),
        install_requires=['requests>=2.8.1'],
        )
