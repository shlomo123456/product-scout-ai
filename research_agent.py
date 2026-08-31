
import os
from openai import OpenAI

SYSTEM_PROMPT = """
You are Product Scout AI, a product research agent for lawful, ordinary consumer and business products.

Your job is to research products and product ideas across Israel and international markets.
You must search in both Hebrew and English when useful.

Priority source types:
1. Official manufacturer websites
2. Official distributors / wholesalers
3. Large marketplaces such as Amazon, AliExpress, Alibaba, eBay, Walmart and relevant local Israeli stores
4. Other reputable retailers and industry sources

Rules:
- Never invent a price, seller, manufacturer, specification, MOQ, shipping option, or URL.
- If a price is not publicly shown, write "לא פורסם מחיר".
- Distinguish clearly between manufacturer, wholesaler, marketplace seller, distributor and retailer.
- If a marketplace listing looks like the same product sold under multiple names, flag a possible duplicate.
- Prefer direct product pages and manufacturer pages over listicles.
- For marketplace prices, note that price may change and may depend on variant, quantity, shipping, tax or location.
- When the task is commercially oriented, check whether comparable products are already sold in Israel.
- For idea discovery, do iterative research: discover relevant product-category terms, search again using those terms, then compare the strongest candidates.
- Return the final answer in Hebrew.
- Include clickable source URLs for every important product/result when available.
- Do not research restricted, illegal, dangerous, age-restricted or harmful products.
"""

def _client():
    return OpenAI(api_key=os.environ["OPENAI_API_KEY"])

def build_plan(query: str, mode: str, model: str) -> str:
    client = _client()

    mode_instructions = """
The user wants a SPECIFIC PRODUCT search.
Create a compact research plan with:
- Hebrew search terms
- English search terms
- likely synonyms / professional category names
- which source types to prioritize
- what fields should be compared
""" if mode == "מוצר ספציפי" else """
The user wants IDEA DISCOVERY.
Create a compact iterative research plan:
- infer the underlying need / customer
- generate 5-10 candidate product categories
- Hebrew and English search terminology for the strongest categories
- how to test whether each idea is already common in Israel
- what commercial signals to compare
"""

    response = client.responses.create(
        model=model,
        reasoning={"effort": "medium"},
        input=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"{mode_instructions}\n\nUser request:\n{query}"}
        ],
    )
    return response.output_text

def run_research(query: str, mode: str, model: str = None) -> dict:
    model = model or os.getenv("OPENAI_MODEL", "gpt-5.6-sol")
    plan = build_plan(query, mode, model)
    client = _client()

    if mode == "מוצר ספציפי":
        task = f"""
Research this specific product request thoroughly:
{query}

Research plan:
{plan}

Search the live web. Intentionally look for relevant results from:
- official manufacturers
- official distributors / wholesalers
- Amazon
- AliExpress
- Alibaba
- eBay and Walmart when relevant
- Israeli ecommerce / distributors / retailers
- other major relevant marketplaces or specialist sites you discover

Do multiple searches where needed, in Hebrew and English.

Final answer structure:
## מסקנה קצרה
3-7 bullets with the most useful findings.

## תוצאות מובילות
A markdown table with:
Product | Company/Seller | Source type | Country/market | Published price | MOQ if shown | Israel availability | Why relevant | URL

Aim for 8-15 strong, non-duplicate results when the web provides enough evidence.

## השוואת מחירים
Explain the observed range and distinguish retail from wholesale.

## יצרנים / ספקים מעניינים
Call out likely manufacturers or wholesalers separately.

## מה מצאתי בישראל
Explain local competition / comparable products.

## הערות ואזהרות
State uncertainties, dynamic marketplace pricing, shipping/tax caveats, and anything not verified.
"""
    else:
        task = f"""
Perform product IDEA DISCOVERY for:
{query}

Research plan:
{plan}

Search the live web iteratively. First discover relevant product categories and terminology.
Then search the strongest categories across:
- official manufacturers
- wholesalers
- Amazon
- AliExpress
- Alibaba
- eBay and Walmart when relevant
- Israeli ecommerce / distributors / retailers
- other major relevant marketplaces or specialist sites you discover

Do searches in Hebrew and English and explicitly test whether similar products are already common in Israel.

Final answer structure:
## המסקנה
Explain the 2-4 most promising directions.

## דירוג הזדמנויות
A markdown table with:
Rank | Product idea | Problem solved | Example sources | Published price range | Israel competition | Supplier/manufacturer signal | Opportunity score (1-10) | Why

## בדיקה מעמיקה של כל רעיון מוביל
For each strong idea:
- what the product is
- examples found
- retail price signals
- wholesale/manufacturer signals
- presence in Israel
- risks / weaknesses
- source URLs

## רעיונות שנפסלו
Briefly state ideas that looked weak and why.

## הצעד הבא
Suggest the most useful deeper research query, but do not perform purchases or contact sellers.
"""

    response = client.responses.create(
        model=model,
        reasoning={"effort": "high"},
        tools=[{"type": "web_search"}],
        input=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": task}
        ],
    )
    return {"plan": plan, "report": response.output_text, "model": model}
