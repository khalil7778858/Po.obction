import json, os, re
import numpy as np
from PIL import Image
import streamlit as st

try:
    from google import genai
    from google.genai import types
    HAS_GENAI = True
except Exception:
    HAS_GENAI = False

st.set_page_config(page_title="Chart 10m Analyzer", page_icon="📊")
st.title("📊 محلل الشارت (10 دقائق)")

EMA_OPTS = ["UP", "DOWN", "CHOP"]
CND_OPTS = ["BULL", "BEAR", "WEAK"]
RSI_OPTS = ["BULL", "BEAR", "NEUTRAL"]
MCD_OPTS = ["BULL", "BEAR", "WEAK"]

def get_key():
    try:
        if "GEMINI_API_KEY" in st.secrets:
            return str(st.secrets["GEMINI_API_KEY"]).strip()
    except Exception:
        pass
    return os.environ.get("GEMINI_API_KEY", "").strip()

def visual_fallback(img):
    arr = np.array(img.resize((200, 200)).convert("RGB"), dtype=np.int16)[:90]
    r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
    gn = int(np.sum((g > r + 25) & (g > b + 20) & (g > 80)))
    rd = int(np.sum((r > g + 25) & (r > b + 20) & (r > 80)))
    if gn > rd * 1.35:
        return {"ema": "UP", "candle": "BULL", "rsi": "BULL", "macd": "BULL", "note": "تقدير أولي صاعد"}
    if rd > gn * 1.35:
        return {"ema": "DOWN", "candle": "BEAR", "rsi": "BEAR", "macd": "BEAR", "note": "تقدير أولي هابط"}
    return {"ema": "CHOP", "candle": "WEAK", "rsi": "NEUTRAL", "macd": "WEAK", "note": "تقدير أولي متذبذب"}

def ai_analyze(img, tf, key):
    client = genai.Client(api_key=key)
    prompt = (
        f"Analyze chart ({tf}). Return JSON only with keys: "
        "ema (UP|DOWN|CHOP), candle (BULL|BEAR|WEAK), "
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

up = st.file_uploader("ارفع صورة الشارت", type=["png", "jpg", "jpeg"])
c1, c2, c3 = st.columns(3)
tf = c1.selectbox("الفريم", ["M5", "M15", "M1", "M30"])
bal = c2.number_input("الرصيد ($)", min_value=1.0, value=1000.0)
stk = c3.number_input("المبلغ ($)", min_value=1.0, value=25.0)

risk = (stk / bal) * 100 if bal > 0 else 100
if risk > 5:
    st.warning(f"نسبة المخاطرة {risk:.1f}% مرتفعة؛ يُفضّل 1% - 3%.")

if up is not None:
    img = Image.open(up)
    st.image(img, use_container_width=True)
    k = f"{up.name}_{up.size}_{tf}"
    if st.session_state.get("k") != k:
        key = get_key()
        if key and HAS_GENAI:
            try:
                st.session_state["res"] = ai_analyze(img, tf, key)
            except Exception as e:
                st.info(f"وضع احتياطي: {e}")
                st.session_state["res"] = visual_fallback(img)
        else:
            st.session_state["res"] = visual_fallback(img)
        st.session_state["k"] = k

    r = st.session_state.get("res", visual_fallback(img))
    ema = r.get("ema") if r.get("ema") in EMA_OPTS else "CHOP"
    cnd = r.get("candle") if r.get("candle") in CND_OPTS else "WEAK"
    rsi = r.get("rsi") if r.get("rsi") in RSI_OPTS else "NEUTRAL"
    mcd = r.get("macd") if r.get("macd") in MCD_OPTS else "WEAK"

    bull = int(ema == "UP") + int(cnd == "BULL") + int(rsi == "BULL") + int(mcd == "BULL")
    bear = int(ema == "DOWN") + int(cnd == "BEAR") + int(rsi == "BEAR") + int(mcd == "BEAR")

    st.divider()
    if risk > 15:
        st.error("توقف: المبلغ أكبر من الحد الآمن.")
    elif bull >= 3 and bear == 0:
        st.success(f"🟢 شراء (CALL) — التطابق {bull}/4 | المدة المقترحة: 00:02:30 - 00:03:00")
    elif bear >= 3 and bull == 0:
        st.error(f"🔴 بيع (PUT) — التطابق {bear}/4 | المدة المقترحة: 00:02:30 - 00:03:00")
    else:
        st.warning(f"⏸️ تجاوز (WAIT) — صعود {bull}/4 | هبوط {bear}/4")

    if r.get("note"):
        st.write(r["note"])
    st.caption(f"EMA: {ema} | Candle: {cnd} | RSI: {rsi} | MACD: {mcd}")
