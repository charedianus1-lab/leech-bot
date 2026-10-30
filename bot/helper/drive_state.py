#!/usr/bin/env python3
# Drive-backed JSON state for the owner's personal features
# (reminders, tasks, notes, RSS, saved city). Reuses the bot's existing
# Drive credentials (token.pickle or service accounts) - no new env vars.
# The state file lives in the bot's own configured Drive upload folder,
# the same place the owner's leeched files already go.
# If Drive is unavailable the module degrades to memory-only state and
# reports available=False, so features still work until the next restart.
import asyncio
from json import dumps, loads
from os import path as ospath

from bot import config_dict, LOGGER

_FILE_NAME = "linked123_state.json"
_lock = asyncio.Lock()
_state = None
_drive = None
_account = None
_checked = False
_available = False


def _build_drive():
    try:
        from googleapiclient.discovery import build
        scopes = ["https://www.googleapis.com/auth/drive"]
        creds = None
        if config_dict.get("USE_SERVICE_ACCOUNTS") and ospath.exists("accounts"):
            from os import listdir
            from random import randrange
            from google.oauth2 import service_account
            files = listdir("accounts")
            creds = service_account.Credentials.from_service_account_file(
                f"accounts/{files[randrange(len(files))]}", scopes=scopes
            )
        elif ospath.exists("token.pickle"):
            from pickle import load as pload
            with open("token.pickle", "rb") as f:
                creds = pload(f)
        if creds is None:
            return None
        return build("drive", "v3", credentials=creds, cache_discovery=False)
    except Exception as e:
        LOGGER.error(f"drive_state: Drive auth failed: {e}")
        return None


def _find_or_create(drive):
    from io import BytesIO
    from googleapiclient.http import MediaIoBaseUpload
    folder = (config_dict.get("GDRIVE_ID") or "").strip()
    q = f"name='{_FILE_NAME}' and trashed=false"
    if folder:
        q += f" and '{folder}' in parents"
    res = drive.files().list(
        q=q, fields="files(id)", spaces="drive",
        supportsAllDrives=True, includeItemsFromAllDrives=True,
    ).execute()
    if res.get("files"):
        return res["files"][0]["id"]
    body = {"name": _FILE_NAME}
    if folder:
        body["parents"] = [folder]
    media = MediaIoBaseUpload(BytesIO(b"{}"), mimetype="application/json")
    created = drive.files().create(
        body=body, media_body=media, fields="id", supportsAllDrives=True
    ).execute()
    return created["id"]


def _read_file(drive, fid):
    data = drive.files().get_media(fileId=fid, supportsAllDrives=True).execute()
    try:
        parsed = loads(data.decode("utf-8"))
        return parsed if isinstance(parsed, dict) else {}
    except Exception:
        return {}


def _write_file(drive, fid, state):
    from io import BytesIO
    from googleapiclient.http import MediaIoBaseUpload
    raw = dumps(state, ensure_ascii=False).encode("utf-8")
    media = MediaIoBaseUpload(BytesIO(raw), mimetype="application/json")
    drive.files().update(fileId=fid, media_body=media, supportsAllDrives=True).execute()


async def _ensure():
    global _drive, _account, _checked, _available
    if _checked:
        return _available
    _checked = True
    drive = await asyncio.to_thread(_build_drive)
    if drive is None:
        LOGGER.warning("drive_state: no Drive credentials - memory-only state")
        return False
    try:
        about = await asyncio.to_thread(
            lambda: drive.about().get(fields="user").execute()
        )
        _account = (about.get("user") or {}).get("emailAddress")
        LOGGER.info(f"drive_state: Drive account is {_account}")
        _drive = drive
        _available = True
    except Exception as e:
        LOGGER.error(f"drive_state: Drive check failed: {e}")
    return _available


async def load():
    global _state
    async with _lock:
        if _state is not None:
            return _state
        if await _ensure():
            try:
                fid = await asyncio.to_thread(_find_or_create, _drive)
                _state = await asyncio.to_thread(_read_file, _drive, fid)
            except Exception as e:
                LOGGER.error(f"drive_state: load failed: {e}")
                _state = {}
        else:
            _state = {}
        return _state


async def save():
    async with _lock:
        if _state is None:
            return False
        if not await _ensure():
            return False
        try:
            fid = await asyncio.to_thread(_find_or_create, _drive)
            await asyncio.to_thread(_write_file, _drive, fid, _state)
            return True
        except Exception as e:
            LOGGER.error(f"drive_state: save failed: {e}")
            return False


async def get(key, default):
    state = await load()
    return state.get(key, default)


async def put(key, value):
    await load()
    _state[key] = value
    return await save()


async def status():
    await load()
    return {
        "available": _available,
        "account": _account,
    }
