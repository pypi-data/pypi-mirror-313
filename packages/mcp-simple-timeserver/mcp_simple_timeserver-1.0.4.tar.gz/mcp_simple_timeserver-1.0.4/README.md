# MCP Simple Timeserver

One of the strange design decisions Anthropic made was depriving Claude of timestamps for messages sent by the user or current time in general. Poor Claude can't tell what time it is! `mcp-simple-timeserver` is a simple MCP server that fixes that.  

It provides the current local time and timezone information from the user's machine. This way Claude can know what time it is at the user's location. He can also calculate how much time passed since his last interaction with the user should he want to do so. 

## Installation

First install the module using:

```bash
pip install mcp-simple-timeserver

```

Then configure in MCP client - the [Claude desktop app](https://claude.ai/download).

Under Mac OS this will look like this:

```json
"mcpServers": {
  "fetch": {
    "command": "python",
    "args": ["-m", "mcp_simple_timeserver"]
  }
}
```

Under Windows you have to check the path to your Python executable using `where python` in the `cmd` (Windows command line). 

Typical configuration would look like this:

```json
"mcpServers": {
  "fetch": {
    "command": "C:\\Users\\YOUR_USERNAME\\AppData\\Local\\Programs\\Python\\Python311\\python.exe",
    "args": ["-m", "mcp_simple_timeserver"]
  }
}
```

