import os
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from ..services.processor import EmailProcessor

base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
template_path = os.path.join(base_dir, "templates")

templates = Jinja2Templates(directory=template_path)
router = APIRouter()
processor = EmailProcessor()


@router.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={})


@router.post("/analyze-only")
async def analyze_only(payload: dict):
    email_text = payload.get("content")
    if not email_text:
        raise HTTPException(status_code=400, detail="No content provided")

    result = processor.process_email(email_text)
    data = result.data

    if getattr(data, "type", None) == "flagged":
        return {
            "status": result.status.value,
            "type": "flagged",
            "reason": data.reason,
        }

    return {
        "status": result.status.value,
        "type": "ticket",
        "category": data.category.value,
        "urgency": data.urgency.value,
        "summary": data.summary,
        "action_items": ", ".join(data.items_to_action),
    }