from setuptools import setup, find_packages

# setup(
#     name='pymathis',
#     version='0.1.0',
#     description='A library of interacting function to enable exchanges between MATHIS and python at each time steps',
#     url='https://scm.cstb.fr/cape/mathis/smartmathis',
#     author='Francois DEMOUGE & Xavier FAURE',
#     author_email='francois.demouge@cstb.fr & xavier.faure@cstb.fr',
#     license='GNU Lesser General Public License',
#     packages=['pymathis'],
#     install_requires=['matplotlib'],
#     packages=find_packages,
#     include_package_data=True,
#     classifiers=[
#         'Development Status :: 1 - Planning',
#         'Intended Audience :: Science/Research',
#         'License :: GNU Lesser General Public License ',
#         'Operating System :: OS Independent',
#         'Programming Language :: Python :: 3',
#     ],
#     python_requires=">=3.1"
# )

setup(
    name='pymathis',
    version='0.2.0',
    description='A library of interacting function to enable exchanges between MATHIS and python at each time steps',
    long_description='A library of interacting function to enable exchanges between MATHIS and python at each time steps',
    long_description_content_type='text/markdown',
    url='https://gitlab.com/CSTB/pymathis',
    author='Xavier FAURE, Francois DEMOUGE',
    author_email='xavier.faure@cstb.fr, francois.demouge@cstb.fr',
    license='GNU Lesser General Public License',
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Programming Language :: Python :: 3",
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=['psutil','matplotlib'],
)
