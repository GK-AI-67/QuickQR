# Lost & Found QR Feature

This module provides Lost & Found QR functionality for the QuickQR app.

## Features
- Generate a QR code by providing a name.
- Each QR code links to an API endpoint for updating or viewing details.
- If the QR is mapped to a user (in `user_qr_mpg`), it shows the mapped info.
- If not mapped, the first scan prompts for details update (in `lost_and_found_qr`).
- On login, the user's Gmail, first name, and last name are stored in `user_dtls`.

## API Endpoints
- `POST /api/lost-and-found/generate` — Generate a new QR code by name.
- `POST /api/lost-and-found/update` — Update QR details (first scan or edit).
- `GET /api/lost-and-found/{qr_id}` — Retrieve QR info or prompt for update.

## Frontend Flow
1. User enters a name and generates a QR code.
2. After generation, user can edit details (first/last name, address, location).
3. The QR code links to the backend API for further actions.

## Backend Flow
- Models are defined in `backend/app/lost_and_found_qr/models/` using Pydantic.
- API logic is in `backend/app/api/lost_and_found.py`.
- Exception and error handling is implemented for all endpoints.

## Error Handling
- All endpoints return clear error messages on failure.
- 404 for not found, 500 for server errors, and validation errors as needed.

## Setup
- Ensure all dependencies are installed (see `requirements.txt`).
- Include the router in your FastAPI app:

```python
from app.api.lost_and_found import router as lost_and_found_router
app.include_router(lost_and_found_router)
```

---
For more details, see the code and comments in each file.
