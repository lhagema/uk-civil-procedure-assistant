from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import json
import os
import re

app = FastAPI(title="Legal AI Assistant", version="1.0.0")

# Create templates directory and mount static files
os.makedirs("templates", exist_ok=True)
os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Sample legal knowledge base (in a real app, this would come from GCP Vertex AI)
LEGAL_KNOWLEDGE = {
    "witness statements": {
        "answer": "There is no standard time limit in the CPR for witness statement exchange - the timing is set by specific court directions, usually made at the Case Management Conference. Under CPR 32.4(1), witness statements must be served within the time specified by the court, and CPR 32.4(2) allows the court to determine whether exchange should be simultaneous or sequential. All witness statements must be served on all parties (CPR 32.10), and crucially, if you fail to serve a witness statement within the court's deadline, that witness cannot give oral evidence unless the court gives permission (CPR 32.10(2)). Always seek specific directions from the court rather than assuming any default position, as timing varies case by case.",
        "citations": ["CPR 32.4(1)", "CPR 32.4(2)", "CPR 32.10", "CPR 32.10(2)"],
        "keywords": ["witness statement", "witness statements", "exchange", "served", "deadline", "cpr 32"]
    },
    "track allocation": {
        "answer": "The court allocates cases to one of four tracks under CPR 26.1(2): small claims (up to £10,000, or £5,000/£1,500 for personal injury), fast track (up to £25,000 with one-day trials), intermediate track (up to £100,000 with three-day trials), or multi-track (higher value or complex cases). The court considers multiple factors under CPR 26.13(1) including financial value, complexity, number of parties, and amount of evidence required. Certain cases like mesothelioma and clinical negligence claims must go to multi-track regardless of value (CPR 26.9(10)). When assessing value, the court disregards disputed amounts, interest, and costs (CPR 26.13(2)). The allocation process starts when the defendant files their defence, which triggers the directions questionnaire under CPR 26.4.",
        "citations": ["CPR 26.1(2)", "CPR 26.13(1)", "CPR 26.9(10)", "CPR 26.13(2)", "CPR 26.4"],
        "keywords": ["track", "allocation", "small claims", "fast track", "multi-track", "intermediate", "cpr 26"]
    },
    "particulars of claim": {
        "answer": "Under CPR 7.5(1), you must serve particulars of claim within **four months** of issuing the claim form if serving within the UK, or **six months** if serving outside the jurisdiction (CPR 7.5(2)). You can apply for an extension under CPR 7.6 by making a formal application under CPR 23, which must state your proposed service date and be supported by evidence. If you apply before the deadline expires, the court can use its general case management powers (CPR 3.1(2)(a)), but if you apply after the deadline has passed, the stricter 'relief from sanctions' test under CPR 3.9 applies. The court will consider factors like efficiency, proportionate cost, and the importance of enforcing compliance when deciding whether to grant relief. Extensions are possible but require proper justification and formal application procedures.",
        "citations": ["CPR 7.5(1)", "CPR 7.5(2)", "CPR 7.6", "CPR 23", "CPR 3.1(2)(a)", "CPR 3.9"],
        "keywords": ["particulars of claim", "serve", "deadline", "extension", "time limit", "cpr 7.5"]
    },
    "strike out": {
        "answer": "To strike out a statement of case, you must apply under CPR 3.4(2) using Form N244 as required by CPR 23.3, stating what order you seek and why. The main grounds for strike out include: no reasonable grounds for the claim/defence, abuse of process, or failure to comply with rules or court orders (CPR 3.4(2)). Your application must be supported by evidence explaining which parts of the statement of case you object to and why they meet the strike out criteria, as outlined in Practice Direction 3A. You must serve the application at least 3 clear days before the hearing (CPR 23.7). In the Commercial Court, stricter timetables apply under PD58 s13.1, requiring evidence in support with the application, evidence in answer within 14 days, and evidence in reply within 7 days.",
        "citations": ["CPR 3.4(2)", "CPR 23.3", "CPR 23.7", "Practice Direction 3A", "PD58 s13.1"],
        "keywords": ["strike out", "striking out", "statement of case", "application", "grounds", "n244", "cpr 3.4"]
    }
}

def search_legal_knowledge(query):
    """Smarter keyword-based search for legal information"""
    query_lower = query.lower()
    query_words = set(re.findall(r'\b\w+\b', query_lower))

    scores = {}
    for key, info in LEGAL_KNOWLEDGE.items():
        score = 0
        
        # 1. Exact phrase match on the key (high score)
        if key.lower() in query_lower:
            score += 20

        # 2. Check for matches against keywords (high score for full phrase)
        keywords = info.get("keywords", [])
        for keyword in keywords:
            if keyword.lower() in query_lower:
                # Higher score for multi-word keywords
                score += 5 * len(keyword.split())
        
        # 3. Check for individual word matches from keywords in query
        topic_words = set()
        for k in keywords:
            topic_words.update(k.lower().split())
        
        matched_words = query_words.intersection(topic_words)
        if matched_words:
            # Penalize common words slightly
            common_words = {"a", "an", "the", "is", "in", "of", "for", "to"}
            meaningful_words = [w for w in matched_words if w not in common_words]
            score += len(meaningful_words)

        if score > 0:
            scores[key] = score
    
    if scores:
        best_match = max(scores, key=scores.get)
        return LEGAL_KNOWLEDGE[best_match]
        
    return None

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/query")
async def query_legal_assistant(query: str = Form(...)):
    """API endpoint for legal queries"""
    result = search_legal_knowledge(query)
    
    if result:
        return {
            "success": True,
            "answer": result["answer"],
            "citations": result["citations"],
            "query": query
        }
    else:
        return {
            "success": False,
            "answer": "I'm sorry, I don't have specific information about that procedural question yet. This is a prototype - in the full version, I would search through the complete Civil Procedure Rules and Practice Directions to find the relevant information for you.",
            "citations": [],
            "query": query
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 