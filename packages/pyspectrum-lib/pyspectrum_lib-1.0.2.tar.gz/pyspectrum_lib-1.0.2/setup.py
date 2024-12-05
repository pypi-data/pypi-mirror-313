from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='pyspectrum_lib',
    version='1.0.2',
    py_modules=['spectrum_lib.spectrum_lib'],
    packages=['spectrum_lib'],
    url='https://sdk.brainbit.com/lib-spectrum/',
    license='MIT',
    author='Brainbit Inc.',
    author_email='support@brainbit.com',
    description='Python wrapper for Spectrum math library',
    long_description=long_description,
    long_description_content_type='text/markdown',
    include_package_data=True,
    package_data={"spectrum_lib": ['libs\\win\\spectrumlib-x64.dll',
                                   'libs\\win\\spectrumlib-x86.dll',
                                   'libs\\macos\\libspectrumlib.dylib']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
        "Intended Audience :: Developers",
    ],
    python_requires='>=3.7',
)