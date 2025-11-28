"""
FastAPI Application - Job Posting Analyzer API
Exposes job analysis functionality via REST endpoints
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import sys
import os

# Add parent directory to path to import project modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scraper import JobScraper
from skills_extractor_v2 import EnhancedSkillExtractor
from api.models import (
    JobAnalysisRequest,
    JobAnalysisResponse,
    ErrorResponse,
    HealthResponse,
    SkillsAnalysis,
    ExperienceInfo
)
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app):
    # --- Startup actions here ---
    print("=" * 70)
    print("🚀 Job Posting Analyzer API Starting...")
    print("=" * 70)
    print("\n📚 Loading models...")

    get_extractor()  # Preload models if desired

    print("✓ API Ready!")
    print("\n📖 Documentation: http://localhost:8000/docs")
    print("=" * 70)
    yield
    # --- Shutdown actions here ---
    print("\n" + "=" * 70)
    print("👋 Shutting down API...")
    print("=" * 70)

# Initialize FastAPI app
app = FastAPI(
    title="Job Posting Analyzer API",
    description="Extract skills and requirements from job postings using NLP",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan  
)


# Add CORS middleware (allows frontend to call API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components (lazy loading for better performance)
scraper = None
extractor = None


def get_scraper():
    """Get or initialize scraper"""
    global scraper
    if scraper is None:
        scraper = JobScraper()
    return scraper


def get_extractor():
    """Get or initialize skill extractor"""
    global extractor
    if extractor is None:
        extractor = EnhancedSkillExtractor()
    return extractor


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint - API information"""
    return {
        "name": "Job Posting Analyzer API",
        "version": "1.0.0",
        "status": "active",
        "endpoints": {
            "health": "/health",
            "analyze": "/api/analyze",
            "docs": "/docs"
        }
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        version="1.0.0"
    )


@app.post(
    "/api/analyze",
    response_model=JobAnalysisResponse,
    responses={
        200: {"description": "Successful analysis"},
        400: {"model": ErrorResponse, "description": "Invalid request"},
        500: {"model": ErrorResponse, "description": "Server error"}
    },
    tags=["Analysis"]
)
async def analyze_job(request: JobAnalysisRequest):
    """
    Analyze a job posting from URL
    
    Extracts:
    - Technical skills (programming languages, frameworks, tools)
    - Experience requirements (years and level)
    - Skill categories
    
    Returns complete analysis with categorized skills.
    """
    try:
        # Convert URL to string
        job_url = str(request.url)
        
        print(f"[API] Analyzing job from: {job_url}")
        
        # Step 1: Scrape job posting
        scraper_instance = get_scraper()
        scrape_result = scraper_instance.scrape_job(job_url)
        
        if not scrape_result:
            raise HTTPException(
                status_code=400,
                detail="Failed to scrape job posting. URL may be invalid or inaccessible."
            )
        
        print(f"[API] Scraped {len(scrape_result['text'])} characters")
        
        # Step 2: Extract skills
        extractor_instance = get_extractor()
        analysis = extractor_instance.analyze_skills(scrape_result['text'])
        
        print(f"[API] Found {analysis['total_skills']} skills")
        
        # Step 3: Format response
        response = JobAnalysisResponse(
            success=True,
            job_url=job_url,
            text_length=len(scrape_result['text']),
            word_count=len(scrape_result['text'].split()),
            skills_analysis=SkillsAnalysis(
                total_skills=analysis['total_skills'],
                all_skills=analysis['all_skills'],
                categorized=analysis['categorized'],
                experience_required=ExperienceInfo(**analysis['experience_required'])
            )
        )
        
        return response
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
        
    except Exception as e:
        print(f"[API] Error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@app.get("/api/stats", tags=["Statistics"])
async def get_stats():
    """Get API usage statistics"""
    return {
        "total_skills_database": len(get_extractor().all_skills),
        "skill_categories": len(get_extractor().skills_database),
        "skill_variations": len(get_extractor().skill_variations)
    }


# Exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            success=False,
            error=exc.detail
        ).dict()
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions"""
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            success=False,
            error="Internal server error",
            details=str(exc)
        ).dict()
    )


# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize on startup"""
    print("=" * 70)
    print("🚀 Job Posting Analyzer API Starting...")
    print("=" * 70)
    print("\n📚 Loading models...")
    
    # Preload models for faster first request
    get_extractor()
    
    print("✓ API Ready!")
    print("\n📖 Documentation: http://localhost:8000/docs")
    print("=" * 70)


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    print("\n" + "=" * 70)
    print("👋 Shutting down API...")
    print("=" * 70)
