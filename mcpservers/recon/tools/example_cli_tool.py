"""
Example Command-Line Tool Plugin

This is an example plugin that demonstrates how to create a tool that wraps
a command-line application. The tool uses subprocess to execute CLI commands.
"""

import subprocess
import json
from typing import Dict, Any, Optional
from hd_logging import setup_logger

logger = setup_logger(__name__, log_file_path="logs/recon_tools.log")


def ping_host(host: str, count: int = 4, timeout: int = 5) -> Dict[str, Any]:
    """
    Ping a host using the system ping command.
    
    This tool demonstrates how to wrap a command-line application.
    
    Args:
        host: Hostname or IP address to ping
        count: Number of ping packets to send (default: 4)
        timeout: Timeout in seconds (default: 5)
        
    Returns:
        Dictionary with ping results
    """
    logger.info(f"[ping_host] Pinging {host} with count={count}, timeout={timeout}")
    
    try:
        # Determine ping command based on OS
        import platform
        system = platform.system().lower()
        
        if system == "windows":
            cmd = ["ping", "-n", str(count), "-w", str(timeout * 1000), host]
        else:
            cmd = ["ping", "-c", str(count), "-W", str(timeout), host]
        
        logger.debug(f"[ping_host] Executing command: {' '.join(cmd)}")
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout + 5  # Add buffer to timeout
        )
        
        return {
            "status": "success" if result.returncode == 0 else "error",
            "host": host,
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "command": " ".join(cmd)
        }
        
    except subprocess.TimeoutExpired:
        logger.error(f"[ping_host] Ping timed out for {host}")
        return {
            "status": "error",
            "host": host,
            "message": "Ping command timed out"
        }
    except FileNotFoundError:
        logger.error("[ping_host] ping command not found")
        return {
            "status": "error",
            "host": host,
            "message": "ping command not available on this system"
        }
    except Exception as e:
        logger.error(f"[ping_host] Error: {e}", exc_info=True)
        return {
            "status": "error",
            "host": host,
            "message": str(e)
        }


def nslookup(domain: str, record_type: str = "A") -> Dict[str, Any]:
    """
    Perform DNS lookup using nslookup command.
    
    Args:
        domain: Domain name to lookup
        record_type: DNS record type (A, AAAA, MX, TXT, etc.)
        
    Returns:
        Dictionary with DNS lookup results
    """
    logger.info(f"[nslookup] Looking up {domain} (type: {record_type})")
    
    try:
        import platform
        system = platform.system().lower()
        
        if system == "windows":
            cmd = ["nslookup", "-type=" + record_type, domain]
        else:
            cmd = ["nslookup", "-type=" + record_type, domain]
        
        logger.debug(f"[nslookup] Executing command: {' '.join(cmd)}")
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=10
        )
        
        return {
            "status": "success" if result.returncode == 0 else "error",
            "domain": domain,
            "record_type": record_type,
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "command": " ".join(cmd)
        }
        
    except FileNotFoundError:
        logger.error("[nslookup] nslookup command not found")
        return {
            "status": "error",
            "domain": domain,
            "message": "nslookup command not available on this system"
        }
    except Exception as e:
        logger.error(f"[nslookup] Error: {e}", exc_info=True)
        return {
            "status": "error",
            "domain": domain,
            "message": str(e)
        }

