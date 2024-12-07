from setuptools import setup, find_packages

setup(
    name="indian_pincode_finder",  # Replace with your module's name
    version="0.1.1",  # Your module's version
    author="Honey Kumar",
    author_email="sdithoney@gmail.com",
    description="Finds state, city , district and pincode of India",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),  # Automatically finds all sub-packages
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",  # Specify the Python version compatibility
    install_requires=[
            "numpy>=2.0.2",      # Example: Numerical computing
            "pandas>=2.2.3",      # Example: Data analysis
        ],
    package_data={
        "indian_pincode_finder": ["data/india_pincode_final.csv"],  # Include all CSV files in the `data/` directory
    },
    include_package_data=True,
)