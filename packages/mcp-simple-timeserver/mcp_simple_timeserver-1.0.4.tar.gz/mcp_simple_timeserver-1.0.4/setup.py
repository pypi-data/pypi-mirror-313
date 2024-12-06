from setuptools import setup, find_packages

setup(
    name="mcp-simple-timeserver",
    version="1.0.4",
    description="A simple MCP server that returns the local time and timezone. Alternatively the server can provide current UTC time from an NTP server.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",  
    author="Andy Brandt",
    author_email="andy@codesprinters.com",
    url="https://github.com/andybrandt/mcp-simple-timeserver",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=["mcp", "ntplib"],
    entry_points={
        "console_scripts": [
            "mcp-simple-timeserver=mcp_simple_timeserver.server:main",
        ]
    },
)