# Website Crawler & Competitive Analysis

A Python-based web crawler for extracting content from websites with strategic competitive analysis tools.

## How to Run

To run the `main.py` script, execute the following command in your terminal:

```bash
python main.py
```

## How to Test

To run the tests for this project, execute the following command in your terminal:

```bash
pytest test_main.py
```

---

## Competitive Analysis Matrix

Interactive visualization combining competitor intelligence with strategic positioning insights.

### What It Does

The Competitive Analysis Matrix provides a comprehensive view of your competitive landscape by:
- Analyzing scraped website data from Sierra.ai, Fin.ai, and Databricks
- Integrating strategic insights from team transcripts and market research
- Highlighting strengths, weaknesses, and opportunities across 4 key dimensions
- Identifying gaps requiring team input with clear action items

### Quick Start

1. **Open the matrix:**
   ```bash
   open competitive_analysis_matrix.html
   ```
   (Or simply double-click the file in Finder)

2. **Review the analysis:**
   - Green cells = Your competitive strengths
   - Yellow cells = Parity or unclear positioning
   - Red cells = Competitor advantages to address
   - Gray cells = [BLANK] items requiring team input

3. **Filter by section:**
   - Strategic Positioning
   - Technical Differentiation
   - Go-to-Market Insights
   - Investor Narrative

4. **Export your work:**
   - Click "Export to PDF" for stakeholder reviews
   - Click "Export to CSV" for further analysis

### Data Sources

- **Competitor Data:** `raw_website_content.txt` (2,878 lines scraped 10/7/2025)
  - Sierra.ai: Homepage, product pages, blog posts, customer stories
  - Fin.ai: Capabilities, research papers, pricing, testimonials
  - Databricks: Technical docs, security features, MLflow, enterprise capabilities

- **Strategic Insights:** Meeting transcript (10/7/2025)
  - Market trends: AI funding dominance, SF valuations 2x higher
  - Competitive positioning: Sierra/Fin vs. Databricks strategy
  - Key differentiators: Eval/lineage + memory/privacy + sovereign security
  - Investor context: Series A expectations, team sizing, growth curves

- **Market Data:** [BLANK - Add additional sources as available]

### Files in This Project

```
/Users/martijnblue/Website craweler/
├── competitive_analysis_matrix.html  # Interactive visualization (main deliverable)
├── matrix_data.json                  # Structured competitor intelligence
├── raw_website_content.txt           # Scraped website content (2,878 lines)
├── complete_website_content.md       # Organized scraped content
├── scraped_content.md                # Additional scraped data
└── README.md                         # This file
```

### Action Items

The matrix identifies several [BLANK] areas requiring team input:

**Strategic:**
- Define primary target market (Enterprise? Mid-market? Vertical?)
- Finalize pricing model (SaaS? Consumption-based? Hybrid?)
- Recruit 2-3 design partners for validation

**Technical:**
- Detail security architecture and compliance roadmap
- Define customization model (who is the user?)
- Document semantic understanding differentiators

**Go-to-Market:**
- Specify use cases beyond customer service
- Plan AWS partnership strategy
- Create customer success metrics framework

**Investor:**
- Build hiring plan to Series A
- Model M&A scenarios and potential acquirers
- Define valuation comparables and multiples

### Usage Tips

1. **For Team Alignment:** Use filter buttons to focus discussions on specific areas
2. **For Investor Decks:** Export sections relevant to pitch narrative
3. **For Sales Enablement:** Reference competitor positioning in customer conversations
4. **For Product Planning:** Prioritize features based on competitive gaps

### Updating the Matrix

To update competitor data:
1. Edit `matrix_data.json` with new information
2. Refresh `competitive_analysis_matrix.html` in your browser
3. Update the "lastUpdated" field in metadata

### Next Steps

1. **Team Review Session:** Schedule meeting to fill [BLANK] cells collaboratively
2. **Validate Claims:** Cross-check competitor data against latest website updates
3. **Integrate to Deck:** Pull relevant sections into investor presentation
4. **Share with Partners:** Use matrix in design partner conversations

---

## Project Metadata

- **Created:** October 7, 2025
- **Last Updated:** October 7, 2025
- **Version:** 1.0
- **Maintained by:** Strategy Team
