from setuptools import setup, find_packages

setup(
    name="keta-python-sdk",
    version="2.0.3",
    keywords=["xishu", "ketaops", "sdk"],
    description="keta python sdk, simple to integrate with ketaops",
    license="Apache-2.0",
    url="https://gitee.com/xishuhq/keta-python-sdk",
    project_urls={
        "Documentation": "https://xishuhq.com",
        "Source": "https://gitee.com/xishuhq/keta-python-sdk",
        "Tracker": "https://gitee.com/xishuhq/keta-python-sdk/issues",
    },
    entry_points={},

    author="keta",
    author_email="ketaops@xishuhq.com",

    packages=find_packages(include=('keta_python_sdk', 'keta_python_sdk.*')),
    include_package_data=True,
    platforms="any",
    install_requires=[]
)
