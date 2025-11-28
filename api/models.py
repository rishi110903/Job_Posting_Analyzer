"""
API Data Models using Pydantic
Defines request and response structures
"""

from typing import List, Dict, Optional
from pydantic import BaseModel, HttpUrl, Field


class JobAnalysisRequest(BaseModel):
    """Request model for job analysis"""
    url: HttpUrl = Field(
        ...,
        description="URL of the job posting to analyze",
        example="https://www.python.org/jobs/6940/"
    )


class ExperienceInfo(BaseModel):
    """Experience requirements model"""
    years: Optional[str] = Field(
        None,
        description="Years of experience required (e.g., '5+', '3')"
    )
    level: Optional[str] = Field(
        None,
        description="Experience level (junior, mid-level, senior, expert)"
    )
    keywords: List[str] = Field(
        default_factory=list,
        description="Experience-related keywords found"
    )


class SkillsAnalysis(BaseModel):
    """Skills analysis results model"""
    total_skills: int = Field(
        ...,
        description="Total number of skills found"
    )
    all_skills: List[str] = Field(
        ...,
        description="List of all skills detected"
    )
    categorized: Dict[str, List[str]] = Field(
        ...,
        description="Skills grouped by category"
    )
    experience_required: ExperienceInfo = Field(
        ...,
        description="Experience requirements detected"
    )


class JobAnalysisResponse(BaseModel):
    """Response model for job analysis"""
    success: bool = Field(
        ...,
        description="Whether analysis was successful"
    )
    job_url: str = Field(
        ...,
        description="URL of analyzed job posting"
    )
    text_length: int = Field(
        ...,
        description="Length of extracted text in characters"
    )
    word_count: int = Field(
        ...,
        description="Number of words in job posting"
    )
    skills_analysis: SkillsAnalysis = Field(
        ...,
        description="Complete skills analysis results"
    )


class ErrorResponse(BaseModel):
    """Error response model"""
    success: bool = Field(
        False,
        description="Always false for errors"
    )
    error: str = Field(
        ...,
        description="Error message"
    )
    details: Optional[str] = Field(
        None,
        description="Additional error details"
    )


class HealthResponse(BaseModel):
    """Health check response"""
    status: str = Field(
        ...,
        description="API status"
    )
    version: str = Field(
        ...,
        description="API version"
    )
