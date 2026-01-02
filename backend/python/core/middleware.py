from fastapi import Request, HTTPException
from core.logger import Logger
from core.bootstrap import get_session_store
from utils import session_utils

logger = Logger.get_logger(__name__)

async def validate_session_id_in_request(request: Request):
    session_id = request.cookies.get("session_id")
    if not session_id:
        logger.warning("No session_id found in cookies.")
        raise HTTPException(status_code=403, detail="No session_id found in cookies.")
    else:
        logger.info(f"Checking existing session_id in cookies: {session_id}")
        session_store = get_session_store()
        existing_session = await session_store.get_session(session_id)
        if not existing_session:
            logger.warning(f"No active session found for session_id: {session_id}")
            raise HTTPException(status_code=403, detail=f"No active session found for session_id: {session_id}")
        else:
            logger.info(f"Session found for session_id: {session_id}, validating expiry.")
            session_expires_at = existing_session.get('expires_at')
            if not session_expires_at:
                logger.warning(f"Session data malformed for session_id: {session_id}, deleting session.")
                await session_store.delete_session(session_id)
                raise HTTPException(status_code=403, details=f"Session data malformed for session_id: {session_id}")
            elif session_utils.is_session_valid(session_expires_at):
                logger.info(f"Existing session is valid for session_id: {session_id}.")
                return
            else:
                logger.info(f"Existing session has expired for session_id: {session_id}, deleting session.")
                await session_store.delete_session(session_id)    
                raise HTTPException(status_code=403, details=f"Existing session has expired for session_id: {session_id}")