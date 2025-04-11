"""
RCON connection handler for Minecraft server commands.
"""
import os
import logging
from typing import Optional
import mcrcon
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RconHandler:
    """Handles RCON connections and commands for the Minecraft server."""
    
    def __init__(self) -> None:
        """Initialize RCON connection parameters."""
        self.host = os.getenv("RCON_HOST")
        self.port = int(os.getenv("RCON_PORT", "25575"))
        self.password = os.getenv("RCON_PASSWORD")
        self.rcon = mcrcon.MCRcon(self.host, self.password, self.port)
        logger.info(f"Initialized RCON handler for {self.host}:{self.port}")
    
    async def whitelist_add(self, username: str) -> bool:
        """Add a player to the server whitelist."""
        try:
            logger.info(f"Attempting to add {username} to whitelist")
            self.rcon.connect()
            response = self.rcon.command(f"glist-send lobby:vpw add {username}")
            logger.info(f"RCON response: {response}")
            return "added" in response.lower()
        except ConnectionRefusedError:
            logger.error("RCON connection refused. Is the Minecraft server running?")
            return False
        except TimeoutError:
            logger.error("RCON connection timed out. Is the server reachable?")
            return False
        except Exception as e:
            logger.error(f"RCON error: {str(e)}")
            return False
        finally:
            try:
                self.rcon.disconnect()
            except:
                pass
    
    async def whitelist_remove(self, username: str) -> bool:
        """Remove a player from the server whitelist."""
        try:
            logger.info(f"Attempting to remove {username} from whitelist")
            self.rcon.connect()
            response = self.rcon.command(f"glist-send lobby:vpw remove {username}")
            logger.info(f"RCON response: {response}")
            return "removed" in response.lower()
        except ConnectionRefusedError:
            logger.error("RCON connection refused. Is the Minecraft server running?")
            return False
        except TimeoutError:
            logger.error("RCON connection timed out. Is the server reachable?")
            return False
        except Exception as e:
            logger.error(f"RCON error: {str(e)}")
            return False
        finally:
            try:
                self.rcon.disconnect()
            except:
                pass

    async def execute_command(self, command: str) -> str:
        """Execute a custom RCON command."""
        try:
            logger.info(f"Executing command: {command}")
            self.rcon.connect()
            # Füge 'glist-send lobby:' vor dem Befehl hinzu, wenn es nicht bereits vorhanden ist
            if not command.startswith("glist-send lobby:"):
                command = f"glist-send lobby:{command}"
            response = self.rcon.command(command)
            logger.info(f"RCON response: {response}")
            return response
        except ConnectionRefusedError:
            logger.error("RCON connection refused. Is the Minecraft server running?")
            return "Error: Connection refused"
        except TimeoutError:
            logger.error("RCON connection timed out. Is the server reachable?")
            return "Error: Connection timeout"
        except Exception as e:
            logger.error(f"RCON error: {str(e)}")
            return f"Error: {str(e)}"
        finally:
            try:
                self.rcon.disconnect()
            except:
                pass 