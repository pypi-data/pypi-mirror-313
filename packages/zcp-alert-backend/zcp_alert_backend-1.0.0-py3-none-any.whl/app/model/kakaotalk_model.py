"""Kakao Token Model

This module contains the KakaoToken model.

Sample JSON data:
```json
{
    "access_token": "fdSRpldtdyBf51jUNFL06l4cMn6W1zZU6AAAAAQo9cuoAAAGRcq9EIG1lzvpaqIEo",
    "token_type": "bearer",
    "refresh_token": "IwJhTRaxzSDqQbUwdHw203rmfG7iIeWPTAAAAAgo9cuoAAAGRcq9EHW1lzvpaqIEo",
    "id_token": "eyJraWQiOiI5ZjI1MmRhZGQ1ZjIzM2Y5M2QtyZmE1MjhkMTJmZWEiLCJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIyNTNlNmNlNzRmNGQ4NTJiZDc2OGJmMDQ1YTExZmRhMCIsInN1YiI6IjM2NjE4MzczNDMiLCJhdXRoX3RpbWUiOjE3MjQyMDU5NzQsImlzcyI6Imh0dHBzOi8va2F1dGgua2FrYW8uY29tIiwibmlja25hbWUiOiLqsJXquLjsiJgiLCJleHAiOjE3MjQyMjc1NzQsImlhdCI6MTcyNDIwNTk3NCwicGljdHVyZSI6Imh0dHBzOi8vdDEua2FrYW9jZG4ubmV0L2FjY291bnRfaW1hZ2VzL2RlZmF1bHRfcHJvZmlsZS5qcGVnLnR3Zy50aHVtYi5SMTEweDExMCIsImVtYWlsIjoia2lsc29vNzVAZ21haWwuY29tIn0.nM6sVFH-JXLBi0pbchwLp6zEs4D5ARDS52kqnyVY5zexn39l01-MDlAZC3XFTIAcGYgjI2InP8QYboY-Fekkv0EZTqk1ZoWs7dop8YZ3qDOfISyTg402tWen0-pB1oV8PHUgQVaGz4MD1nCgV0YeF5GElkjFapw2NMP9wIN-fMyzorCd8MFExP18rmaOGiivpmywpQOGLlCx5h3ECuLtstmgAmjlU_LZ72WpFLgI61DGXRkjinBCR4nMCUnCaVC2GGI-ZmD3F8_D7bNQydBxjk1ReZ-64ztMA3mRvw-BAZ59_Hdvx3_7UgOoNMECGXH5XehU50NlrLxQd8ZPu6iL8w",
    "expires_in": 21599,
    "scope": "account_email profile_image talk_message openid profile_nickname friends",
    "refresh_token_expires_in": 5183999
}
```
"""

from datetime import datetime, timedelta
from typing import Optional

from pydantic import BaseModel, field_serializer

from app.model.alert_model import AlertBaseModel
from app.utils.time_utils import DEFAULT_TIME_ZONE


class KakaoTalkToken(AlertBaseModel):
    access_token: Optional[str]
    token_type: Optional[str]
    refresh_token: Optional[str] = None
    id_token: Optional[str] = None
    expires_in: Optional[int]
    scope: Optional[str] = None
    refresh_token_expires_in: Optional[int] = None

    channel_id: Optional[str] = None
    access_token_updated_at: Optional[datetime] = None
    refresh_token_updated_at: Optional[datetime] = None

    @field_serializer("refresh_token_updated_at", "access_token_updated_at")
    def _serialize_refresh_token_updated_at(
        self, dt: Optional[datetime]
    ) -> Optional[str]:
        return dt.isoformat(timespec="milliseconds") if dt else None

    def is_expired_access_token(self):
        current_time = datetime.now(DEFAULT_TIME_ZONE)
        expired_time = (
            self.access_token_updated_at
            if self.access_token_updated_at
            else self.created_at
        ) + timedelta(seconds=self.expires_in)

        return expired_time < current_time

    def is_expired_refresh_token(self):
        current_time = datetime.now(DEFAULT_TIME_ZONE)
        expired_time = (
            self.refresh_token_updated_at
            if self.refresh_token_updated_at
            else self.created_at
        ) + timedelta(seconds=self.refresh_token_expires_in)

        return expired_time < current_time


class KakaoTalkFriend(BaseModel):
    """Kakao friend response model for the restful api"""

    profile_nickname: str | None = None
    profile_thumbnail_image: str | None = None
    allowed_msg: bool | None = False
    id: int | None = None
    uuid: str | None = None
    favorite: bool | None = False
