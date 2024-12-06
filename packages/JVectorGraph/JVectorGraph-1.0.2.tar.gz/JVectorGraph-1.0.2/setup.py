from setuptools import setup, find_packages

VERSION = '1.0.2' 
DESCRIPTION = 'JVectorGraph'
LONG_DESCRIPTION = '''

JVectorGraph is a Python library designed for editing Matplotlib-generated plots, allowing users to modify chart elements interactively. Features include removing elements, repositioning components, adjusting colors, and customizing visual styles. The library supports saving the edited plots in various formats, including SVG, PNG, and JPEG, enabling seamless integration with graphic design workflows and high-quality export for publication.

'''


# Setting up
setup(
        name="JVectorGraph", 
        version=VERSION,
        author="Jakub Kubis",
        author_email="jbiosystem@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=['JVG'],
        include_package_data=True, 
        install_requires=[
                "matplotlib",
                "pyvis",
                "networkx"
            ], 
        keywords=['vector', 'graph', 'svg', 'png', 'mpl', 'jpeg'],
        license = 'MIT',
        classifiers = [
            "Development Status :: 3 - Alpha",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
            "Operating System :: POSIX :: Linux",
        ],
        python_requires='>=3.7',
)


