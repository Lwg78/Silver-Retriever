import streamlit as st
import os
from src.engine import RobustEngine
from src.brain import UniversalBrain

st.set_page_config(page_title="Silver Retriever V2", page_icon="🥈", layout="wide")

RAW_DIR = "data/raw"
os.makedirs(RAW_DIR, exist_ok=True)

@st.cache_resource
def load_system():
    return RobustEngine(), UniversalBrain()

engine, brain = load_system()

# --- SIDEBAR ---
with st.sidebar:
    st.header("📚 System Status")
    loaded = engine.get_loaded_files()
    st.success(f"Files Loaded: {len(loaded)}")
    with st.expander("Show Files"):
        for f in loaded: st.caption(f"• {f}")
    
    st.divider()
    if st.button("☢️ Nuke & Reset"):
        engine.nuke_library()
        st.cache_resource.clear()
        st.rerun()

# --- MAIN UI ---
st.title("🥈 Silver Retriever V2")

tab_upload, tab_search = st.tabs(["📤 Upload", "🔍 Search"])

with tab_upload:
    files = st.file_uploader("Upload Docs", accept_multiple_files=True)
    if files and st.button("Index Files"):
        bar = st.progress(0)
        for i, f in enumerate(files):
            path = os.path.join(RAW_DIR, f.name)
            with open(path, "wb") as w: w.write(f.getbuffer())
            engine.ingest_file(path)
            bar.progress((i+1)/len(files))
        st.success("Indexing Complete!")
        st.rerun()

with tab_search:
    query = st.text_input("Ask a question:")
    
    if query:
        raw = engine.search(query)
        results = brain.process_query(query, raw)
        
        if not results:
            st.warning("No results found.")
        else:
            # 1. Direct Answer Box
            if "direct_answer" in results[0]:
                st.success(f"**💡 Smart Answer:** {results[0]['direct_answer']}")
            
            st.markdown("### 🔍 Search Results")
            
            # 2. Detailed Results with Badges
            for hit in results[:5]:
                # Dynamic Badges
                badges = ""
                if "badges" in hit and hit["badges"]:
                    for b in hit["badges"]:
                        # Color coding based on plugin name
                        color = "red" if "admin" in b else "green" if "feng" in b else "blue"
                        badges += f":{color}[**[{b}]**] "
                
                # Reason Tooltip
                reason_text = ""
                if "reasons" in hit and hit["reasons"]:
                    reason_text = f"  \n*Why? {', '.join(hit['reasons'])}*"

                with st.expander(f"{badges} {hit['payload']['source']} (Score: {hit['score']:.2f})"):
                    st.markdown(hit['payload']['text'])
                    if reason_text:
                        st.caption(reason_text)