from setuptools import setup, find_packages


setup(
    name="sop-migration",
    version="0.0.6",
    packages=find_packages(),
    include_package_data=True,
    description="Pin your migrations to any NetBox model instance",
    author="Leorevoir",
    author_email="leo.quinzler@epitech.eu",
    classifiers=[
        "Framework :: Django",
        "Programming Language :: Python :: 3",
    ],
    zip_safe=False,
)
