from src.engine import RobustEngine

print("1. Loading Engine class...")
try:
    engine = RobustEngine()
    print("   ✅ Engine Initialized.")
except Exception as e:
    print(f"   ❌ Engine Failed Init: {e}")

print("2. Checking for 'search' method...")
if hasattr(engine, 'search'):
    print("   ✅ 'search' method FOUND.")
else:
    print("   ❌ 'search' method MISSING. Check indentation in engine.py!")

print("3. Checking for 'nuke_library' method...")
if hasattr(engine, 'nuke_library'):
    print("   ✅ 'nuke' method FOUND.")
else:
    print("   ❌ 'nuke' method MISSING.")