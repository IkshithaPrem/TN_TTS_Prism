from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, List
import uvicorn

from normalization.pipeline import NormalizationPipeline
from normalization.ssml_generator import SSMLGenerator

app = FastAPI(
    title="Indian Language Text Normalization API",
    description="Text Normalization + SSML Rule Generator for TTS",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize pipeline
pipeline = NormalizationPipeline()
ssml_generator = SSMLGenerator()


class NormalizeRequest(BaseModel):
    locale: str
    text: str


class SSMLRequest(BaseModel):
    locale: str
    text: str
    use_ssml: bool = True


class NormalizeResponse(BaseModel):
    original_text: str
    normalized_text: str
    locale: str
    tokens: List[Dict]


class SSMLResponse(BaseModel):
    original_text: str
    normalized_text: str
    ssml: str
    locale: str


@app.get("/")
async def root():
    return {
        "message": "Indian Language Text Normalization API",
        "version": "1.0.0",
        "supported_locales": pipeline.get_supported_locales()
    }


@app.get("/locales")
async def get_locales():
    """Get all supported locales"""
    return {
        "locales": pipeline.get_supported_locales(),
        "count": len(pipeline.get_supported_locales())
    }


@app.post("/normalize", response_model=NormalizeResponse)
async def normalize_text(request: NormalizeRequest):
    """Normalize text for a given locale"""
    if request.locale not in pipeline.get_supported_locales():
        raise HTTPException(
            status_code=400,
            detail=f"Locale '{request.locale}' not supported. Supported locales: {pipeline.get_supported_locales()}"
        )
    
    try:
        result = pipeline.normalize(request.text, request.locale)
        return NormalizeResponse(
            original_text=request.text,
            normalized_text=result["normalized_text"],
            locale=request.locale,
            tokens=result.get("tokens", [])
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/generate_ssml", response_model=SSMLResponse)
async def generate_ssml(request: SSMLRequest):
    """Generate SSML output for normalized text"""
    if request.locale not in pipeline.get_supported_locales():
        raise HTTPException(
            status_code=400,
            detail=f"Locale '{request.locale}' not supported"
        )
    
    try:
        result = pipeline.normalize(request.text, request.locale)
        normalized_text = result["normalized_text"]
        tokens = result.get("tokens", [])
        
        ssml = ssml_generator.generate(normalized_text, tokens, request.locale)
        
        return SSMLResponse(
            original_text=request.text,
            normalized_text=normalized_text,
            ssml=ssml,
            locale=request.locale
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/export_rules/{locale}")
async def export_rules(locale: str):
    """Export normalization rules for a locale"""
    if locale not in pipeline.get_supported_locales():
        raise HTTPException(
            status_code=404,
            detail=f"Locale '{locale}' not found"
        )
    
    try:
        rules = pipeline.get_rules(locale)
        return {
            "locale": locale,
            "rules": rules
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
