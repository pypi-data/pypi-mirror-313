from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as arq:
    readme = arq.read()

setup(
    name='simplecmd_discordpy',
    version='2.0.1',
    license='MIT',
    author='Anão Lenda',
    author_email='4x0bfuscator@gmail.com',
    description='Uma biblioteca mais simples para a criação de comandos no Discord.py',
    long_description=readme,
    long_description_content_type="text/markdown",
    keywords='simplecmd discordpy comandos',
    packages=find_packages(where="."),
    install_requires=['discord'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Framework :: AsyncIO',
    ],
    python_requires='>=3.9',
)