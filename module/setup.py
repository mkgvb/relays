from setuptools import setup
# print(str(os.getcwd)) print(os.listdir(path='.'))

setup(
    name="relays",
    packages=["relays"],
    version="DEVELOPMENT",
    description="scripts",
    author="Mike Gracia",
    include_package_data=True,
    zip_safe=False,
    entry_points={
        "console_scripts": [
            "startrelays=relays.relays:main"
        ]
    },
)
