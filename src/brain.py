"""
UniversalBrain V2
-----------------
Upgrades:
1. Transparency: Tracks WHICH plugin fired and WHY.
2. Debugging: Returns a 'reason' log for the UI.
"""

import os
import importlib.util

class UniversalBrain:
    def __init__(self):
        self.plugins = []
        self._load_plugins()

    def _load_plugins(self):
        base_dir = os.path.dirname(__file__)
        plugin_dir = os.path.join(base_dir, "plugins")
        os.makedirs(plugin_dir, exist_ok=True)

        for fname in os.listdir(plugin_dir):
            if fname.endswith(".py") and fname != "__init__.py":
                path = os.path.join(plugin_dir, fname)
                spec = importlib.util.spec_from_file_location(fname[:-3], path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                if hasattr(module, "TRIGGERS") and hasattr(module, "run"):
                    self.plugins.append(module)

    def process_query(self, query, results):
        query_l = query.lower()
        
        # 1. Identify Interested Plugins
        active_plugins = [
            p for p in self.plugins
            if any(t in query_l for t in p.TRIGGERS)
        ]

        if not active_plugins:
            return results

        enhanced = []

        for hit in results:
            score = hit["score"]
            text = hit["payload"]["text"]

            # Trackers for UI
            active_badges = []  # ["Admin", "FengShui"]
            reasons = []        # ["Found date", "Mentioned 'placement'"]
            extracted_answer = None

            for plugin in active_plugins:
                # Plugins now return 3 things: boost, extracted_info, reason
                # We handle old plugins gracefully with try/except
                try:
                    boost, extracted, reason = plugin.run(text, query_l)
                except ValueError:
                    # Fallback for old plugins that only return 2 values
                    boost, extracted = plugin.run(text, query_l)
                    reason = "Matched Keywords"

                if boost > 0:
                    score += boost
                    active_badges.append(plugin.__name__.split('.')[-1]) # clean name
                    if reason:
                        reasons.append(reason)
                
                if extracted and not extracted_answer:
                    extracted_answer = extracted

            # Attach metadata to the result for the UI
            hit["score"] = score
            hit["badges"] = list(set(active_badges)) # Remove duplicates
            hit["reasons"] = reasons
            
            if extracted_answer:
                hit["direct_answer"] = extracted_answer

            enhanced.append(hit)

        enhanced.sort(key=lambda x: x["score"], reverse=True)
        return enhanced