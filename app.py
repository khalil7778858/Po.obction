def ai_analyze(img, tf, key):
    client = genai.Client(api_key=key)
    prompt = (
        f"Selected timeframe in app: {tf}. "
        "Inspect the chart image and read the timeframe shown on the chart if visible (e.g. M1, M5, M15, M30, or UNKNOWN). "
        "Return JSON only with keys: "
        "detected_tf (string), ema (UP|DOWN|CHOP), candle (BULL|BEAR|WEAK), "
        "rsi (BULL|BEAR|NEUTRAL), macd (BULL|BEAR|WEAK), note (short Arabic)."
    )
    resp = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[img, prompt],
        config=types.GenerateContentConfig(response_mime_type="application/json", temperature=0.1),
    )
    txt = (resp.text or "").strip()
    m = re.search(r"\{.*\}", txt, re.DOTALL)
    return json.loads(m.group(0) if m else txt)
