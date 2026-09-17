"""
Reorders and numbers README.md sections according to the exact 25-phase hackathon structure.
"""
import re

def update_readme():
    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()

    # Define the replacements for the headings
    replacements = [
        (r"## 4\. System Architecture", "## 5. System Architecture"),
        (r"## 5\. AI Pipeline", "## 6. AI Pipeline"),
        (r"## 6\. Knowledge & RAG System", "## 7. Knowledge Base & RAG"),
        (r"## 7\. Multi-Metric Reasoning", "## 8. Multi-Metric Reasoning"),
        (r"## 8\. Conversational Intelligence", "## 9. Conversational Intelligence"),
        (r"## 9\. Recommendation Output", "## 10. Recommendation Output"),
        (r"## 10\. Technology Stack", "## 11. Technology Stack"),
        (r"## 11\. Project Structure", "## 12. Project Structure"),
        (r"## 12\. Database / Schema", "## 13. Database / Schema"),
    ]

    for pat, rep in replacements:
        content = re.sub(pat, rep, content)

    # Now let's extract sections 13 to 24 and place them in exact Phase 9 order:
    # 13: Database / Schema (already in place)
    # 14: API Documentation
    # 15: Local Installation
    # 16: Environment Variables
    # 17: Docker Setup
    # 18: Deployment
    # 19: Demo Scenarios
    # 20: Hackathon Evaluation Alignment
    # 21: Testing
    # 22: Security
    # 23: Limitations
    # 24: Future Scope
    # 25: Project Links

    # Split by section boundaries
    sec_map = {}
    parts = re.split(r'\n(?=## \d+\. )', content)
    header_part = parts[0]
    
    for p in parts[1:]:
        m = re.match(r'## \d+\. ([^\n]+)', p)
        if m:
            title = m.group(1).strip()
            sec_map[title] = p

    # Desired 25 sections in order
    ordered_titles = [
        ("1. Project Overview", ["Project Overview"]),
        ("2. Problem Statement", ["Problem Statement"]),
        ("3. Solution", ["Solution"]),
        ("4. Key Features", ["Key Features"]),
        ("5. System Architecture", ["System Architecture"]),
        ("6. AI Pipeline", ["AI Pipeline"]),
        ("7. Knowledge Base & RAG", ["Knowledge Base & RAG", "Knowledge & RAG System"]),
        ("8. Multi-Metric Reasoning", ["Multi-Metric Reasoning"]),
        ("9. Conversational Intelligence", ["Conversational Intelligence"]),
        ("10. Recommendation Output", ["Recommendation Output"]),
        ("11. Technology Stack", ["Technology Stack"]),
        ("12. Project Structure", ["Project Structure"]),
        ("13. Database / Schema", ["Database / Schema"]),
        ("14. API Documentation", ["API Documentation"]),
        ("15. Local Installation", ["Local Installation"]),
        ("16. Environment Variables", ["Environment Variables"]),
        ("17. Docker Setup", ["Running with Docker", "Docker Setup"]),
        ("18. Deployment", ["Deployment Architecture", "Deployment"]),
        ("19. Demo Scenarios", ["Demo Scenarios"]),
        ("20. Hackathon Evaluation Alignment", ["Hackathon Evaluation Alignment"]),
        ("21. Testing", ["Testing"]),
        ("22. Security", ["Security"]),
        ("23. Limitations", ["Limitations"]),
        ("24. Future Scope", ["Future Scope"]),
        ("25. Project Links", ["Hackathon Submission Links", "Project Links"])
    ]

    new_sections = [header_part]
    for num_title, keys in ordered_titles:
        found = False
        for k in keys:
            if k in sec_map:
                sec_text = sec_map[k]
                # Rewrite the heading line to match num_title
                sec_text = re.sub(r'## \d+\. [^\n]+', f'## {num_title}', sec_text, count=1)
                new_sections.append(sec_text)
                found = True
                break
        if not found:
            print(f"Warning: Section '{num_title}' not found in existing document!")

    final_content = "\n".join(new_sections)

    # Ensure verified URLs in section 25
    final_content = final_content.replace("http://localhost:8000/docs", "https://darukaa-biodiversity-backend.onrender.com/docs")
    if "https://darukaa-biodiversity-backend.onrender.com" not in final_content:
        final_content = final_content.replace(
            "## 25. Project Links",
            "## 25. Project Links\n\n"
            "- **GitHub Repository**: [https://github.com/clutchH1404/darukaa-biodiversity-ai](https://github.com/clutchH1404/darukaa-biodiversity-ai)\n"
            "- **Production Live Demo**: [https://darukaa-biodiversity-ai.vercel.app](https://darukaa-biodiversity-ai.vercel.app)\n"
            "- **Production Backend API**: [https://darukaa-biodiversity-backend.onrender.com](https://darukaa-biodiversity-backend.onrender.com)\n"
            "- **Interactive Swagger Docs**: [https://darukaa-biodiversity-backend.onrender.com/docs](https://darukaa-biodiversity-backend.onrender.com/docs)\n"
            "- **API Health Verification**: [https://darukaa-biodiversity-backend.onrender.com/health](https://darukaa-biodiversity-backend.onrender.com/health)"
        )

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(final_content)

    print("README.md successfully restructured to exact 25-section format!")

if __name__ == "__main__":
    update_readme()
