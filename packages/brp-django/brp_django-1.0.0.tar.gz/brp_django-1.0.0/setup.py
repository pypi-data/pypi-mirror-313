from setuptools import setup, find_packages

with open("README.md", "r") as f:
    description = f.read()
    
setup(
    name="brp_django",
    version="1.0.0",
    author="Binay Raj Parajuli",
    author_email="binayaparajuli17@gmail.com",
    packages=find_packages(),
    install_requires=[
        "Django>=4.0",
        "djangorestframework>=3.14",
    ],
    entry_points={
        # "console_scripts":[
        #     "brp_django = brp_django:my_name",
        # ],
    },
    long_description=description,
    long_description_content_type="text/markdown"
)