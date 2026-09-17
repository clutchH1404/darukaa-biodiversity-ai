DARK_THEME_CSS = """
<style>
/* Global Imports & Reset */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* Header Styling */
.darukaa-header {
    background: linear-gradient(135deg, rgba(16, 185, 129, 0.12) 0%, rgba(6, 182, 212, 0.08) 100%);
    border: 1px solid rgba(16, 185, 129, 0.25);
    border-radius: 16px;
    padding: 24px 32px;
    margin-bottom: 24px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
}

.darukaa-title {
    font-size: 2.2rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    background: linear-gradient(120deg, #34D399, #38BDF8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 6px;
}

.darukaa-subtitle {
    font-size: 1.05rem;
    color: #94A3B8;
    font-weight: 400;
}

/* Scientific Badges */
.badge {
    display: inline-block;
    padding: 4px 10px;
    border-radius: 9999px;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-right: 6px;
    margin-bottom: 4px;
}
.badge-emerald {
    background-color: rgba(16, 185, 129, 0.15);
    color: #34D399;
    border: 1px solid rgba(52, 211, 153, 0.3);
}
.badge-cyan {
    background-color: rgba(6, 182, 212, 0.15);
    color: #38BDF8;
    border: 1px solid rgba(56, 189, 248, 0.3);
}
.badge-amber {
    background-color: rgba(245, 158, 11, 0.15);
    color: #FBBF24;
    border: 1px solid rgba(251, 191, 36, 0.3);
}

/* Scientific Metric Cards */
.metric-card {
    background: #111827;
    border: 1px solid #1F2937;
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 12px;
    transition: transform 0.2s ease, border-color 0.2s ease;
}
.metric-card:hover {
    border-color: #10B981;
    transform: translateY(-2px);
}

.recommendation-card {
    background: linear-gradient(180deg, #131D2D 0%, #0D1520 100%);
    border: 1px solid rgba(56, 189, 248, 0.2);
    border-left: 4px solid #10B981;
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
}

/* Citations Box */
.citation-box {
    background: #0B1120;
    border: 1px solid #1E293B;
    border-radius: 8px;
    padding: 12px;
    font-size: 0.85rem;
    color: #94A3B8;
    margin-top: 10px;
}

/* Demo Flow Steps */
.pipeline-step {
    background: rgba(30, 41, 59, 0.5);
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 8px 12px;
    font-size: 0.8rem;
    font-weight: 600;
    color: #E2E8F0;
    text-align: center;
}

pre, code {
    font-family: 'JetBrains Mono', monospace !important;
}
</style>
"""
