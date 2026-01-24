# Application Security DAST MCP Server

MCP server providing Dynamic Application Security Testing (DAST) tools:
- **ZAP**: OWASP ZAP - Web app DAST (baseline, full, API scans)
- **Nikto**: Web server scanner
- **SQLMap**: SQL injection testing tool
- **Wapiti**: Web application vulnerability scanner
- **Metasploit**: Penetration testing framework (SAFE MODE ONLY)
- **W3AF**: Web app attack and audit framework

## Deployment

### Docker
```bash
docker build -f appsec_dast/Dockerfile -t appsec-dast-mcp:latest .
docker run -it --rm \
  -v /path/to/tools:/app/application_security_tools:ro \
  appsec-dast-mcp:latest
```

### uvx
```bash
uvx appsec-dast-mcp
```

## Tools

- `zap_baseline_scan(target_url, ...)`
- `zap_full_scan(target_url, ...)`
- `zap_api_scan(target_url, ...)`
- `nikto_scan_website(target_url, ...)`
- `sqlmap_scan_url(target_url, ...)`
- `wapiti_scan_url(target_url, ...)`
- `metasploit_scan_web_target(target_url, ...)`
- `w3af_scan_url(target_url, ...)`

