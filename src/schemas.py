from pydantic import BaseModel

class ContentFeedback(BaseModel):
    grammar_score: int
    clarity_score: int
    style_score: int
    to_do_score: str

class SEOFeedback(BaseModel):
    seo_score: int
    to_do: str
