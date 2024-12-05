from setuptools import setup, find_packages

# Load the README file as the long description
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name= "kitikiplot",
    version= "0.1.0",
    author="Boddu Sri Pavan and Boddu Swathi Sree",
    author_email="your-email@example.com",  # Update with your email
    description="A Python library for visualizing sequential and time-series categorical Sliding Window data.",
    long_description=long_description,
    long_description_content_type= "text/markdown",
    url="https://github.com/BodduSriPavan-111/kitikiplot",
    packages= find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # License type
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Visualization",
    ],
    # python_requires=">=3.11.0",
    # install_requires=[
    #     "numpy",
    #     "pandas",
    #     "matplotlib"
    # ],
    project_urls={
        "Bug Tracker": "https://github.com/BodduSriPavan-111/kitikiplot/issues",
        "Documentation": "https://github.com/BodduSriPavan-111/kitikiplot/wiki",
        "Source Code": "https://github.com/BodduSriPavan-111/kitikiplot",
    },
    keywords=[
        "kitikiplot", 
        "sliding window", 
        "sequential",
        "time-series", 
        "categorical data",
    ],
    license="LICENSE",
)