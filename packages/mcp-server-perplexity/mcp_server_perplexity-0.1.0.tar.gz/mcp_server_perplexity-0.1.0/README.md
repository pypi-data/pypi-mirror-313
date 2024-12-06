# Perplexity MCP Server

MCP Server for the Perplexity API.

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
    ]
  }
}
```
