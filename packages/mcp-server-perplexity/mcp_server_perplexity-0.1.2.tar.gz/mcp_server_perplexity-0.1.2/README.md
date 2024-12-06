# Perplexity MCP Server

MCP Server for the Perplexity API.

> :warning: **Limitations:**
> - The Claude Desktop client may timeout if Perplexity processing takes too long
> - This issue might be resolved if Claude Desktop implements support for long running operations and progress reporting in the future
> - Implementation updates to handle these features will be made if they become available

## Components

### Tools

- **ask_perplexity**: Request chat completion with citations from Perplexity  

## Quickstart

### Install

#### Claude Desktop

- On macOS: `~/Library/Application\ Support/Claude/claude_desktop_config.json`  
- On Windows: `%APPDATA%/Claude/claude_desktop_config.json`

```
"mcpServers": {
  "Perplexity": {
    "command": "uvx",
    "args": [
      "mcp-server-perplexity"
    ],
    "env": {
      "PERPLEXITY_API_KEY": "your-perplexity-api-key"
    }
  }
}
```
