"""
ZEKIYE JARVIS - DARWIN-ES Bridge for Telegram Bot
DARWIN Evolution Strategy motorunu Telegram botuna entegre eder.
"""

import json
import random
import time
import logging
from pathlib import Path
from typing import Dict, List, Tuple, Optional

logger = logging.getLogger("DARWIN_BRIDGE")

# Strateji tanımları
JARVIS_STRATEGIES = {
    0: "direct_command",
    1: "context_lookup",
    2: "llm_inference",
    3: "cached_response",
    4: "pattern_match",
    5: "semantic_search",
    6: "multi_step_plan",
    7: "tool_call",
    8: "clarification_request",
    9: "fallback_response",
    10: "knowledge_base_query",
    11: "system_command",
    12: "memory_retrieve",
    13: "composite_strategy",
    14: "adaptive_response",
    15: "hf_pipeline",
    16: "hf_text_generation",
    17: "hf_zero_shot",
    18: "hf_sentiment",
    19: "hf_summarize",
}

NUM_STRATEGIES = len(JARVIS_STRATEGIES)


class DarwinBridge:
    """
    Telegram bot için hafif DARWIN-ES implementasyonu.
    Strateji seçimi ve fitness takibi yapar.
    """

    MU = 5
    LAMBDA = 4

    def __init__(self, state_path: str = "data/darwin_state.json"):
        self.state_path = Path(state_path)
        self.state_path.parent.mkdir(parents=True, exist_ok=True)
        self.generation: int = 0
        self.total_evaluations: int = 0
        self.strategy_usage: Dict[int, int] = {i: 0 for i in range(NUM_STRATEGIES)}
        self.strategy_success: Dict[int, int] = {i: 0 for i in range(NUM_STRATEGIES)}
        self.parents: List[Dict] = []
        self._load_or_init()
        logger.info(f"[DARWIN] Bridge başlatıldı. Nesil: {self.generation}")

    def _load_or_init(self):
        """Durum yükle veya yeni başlat"""
        if self.state_path.exists():
            try:
                with open(self.state_path) as f:
                    state = json.load(f)
                self.generation = state.get("generation", 0)
                self.total_evaluations = state.get("total_evaluations", 0)
                self.strategy_usage = {int(k): v for k, v in state.get("strategy_usage", {}).items()}
                self.strategy_success = {int(k): v for k, v in state.get("strategy_success", {}).items()}
                self.parents = state.get("parents", [])
                return
            except Exception:
                pass
        self._init_population()

    def _init_population(self):
        """Rastgele popülasyon başlat"""
        self.parents = []
        for _ in range(self.MU):
            genes = [random.randint(0, 1) for _ in range(NUM_STRATEGIES)]
            if sum(genes) == 0:
                genes[random.randint(0, NUM_STRATEGIES - 1)] = 1
            self.parents.append({
                "genes": genes,
                "fitness": 0.5,
                "use_count": 0,
                "success_count": 0,
            })

    def select_strategy(self) -> Tuple[int, int]:
        """Strateji seç"""
        parent_idx = random.randint(0, len(self.parents) - 1)
        parent = self.parents[parent_idx]
        active = [i for i, g in enumerate(parent["genes"]) if g == 1]
        if not active:
            strategy_id = random.randint(0, NUM_STRATEGIES - 1)
        else:
            strategy_id = random.choice(active)
        self.strategy_usage[strategy_id] = self.strategy_usage.get(strategy_id, 0) + 1
        return strategy_id, parent_idx

    def report_feedback(self, parent_idx: int, strategy_id: int, success: bool, quality: float = 0.5):
        """Geri bildirim"""
        parent = self.parents[parent_idx]
        parent["use_count"] += 1
        if success:
            parent["success_count"] += 1
            self.strategy_success[strategy_id] = self.strategy_success.get(strategy_id, 0) + 1

        if parent["use_count"] > 0:
            parent["fitness"] = parent["success_count"] / parent["use_count"]

        self.total_evaluations += 1

        # Evrim adımı
        if self.total_evaluations % (self.LAMBDA * self.MU) == 0:
            self._evolution_step(parent_idx)

        # Periyodik kaydet
        if self.total_evaluations % 20 == 0:
            self.save_state()

    def _evolution_step(self, parent_idx: int):
        """Evrim adımı - bit-flip pertürbasyonu"""
        parent = self.parents[parent_idx]
        best = parent.copy()

        for _ in range(self.LAMBDA):
            child_genes = parent["genes"].copy()
            flip_idx = random.randint(0, NUM_STRATEGIES - 1)
            child_genes[flip_idx] = 1 - child_genes[flip_idx]
            if sum(child_genes) == 0:
                child_genes[random.randint(0, NUM_STRATEGIES - 1)] = 1

            child_fitness = parent["fitness"] * 0.8
            if child_fitness > best["fitness"]:
                best = {
                    "genes": child_genes,
                    "fitness": child_fitness,
                    "use_count": max(1, parent["use_count"] // 2),
                    "success_count": int(max(1, parent["use_count"] // 2) * child_fitness),
                }

        self.parents[parent_idx] = best
        self.generation += 1

    def get_stats(self) -> Dict:
        """İstatistikler"""
        total_usage = sum(self.strategy_usage.values()) or 1
        top_strategies = sorted(
            self.strategy_usage.items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]

        return {
            "generation": self.generation,
            "total_evaluations": self.total_evaluations,
            "mu": self.MU,
            "lambda": self.LAMBDA,
            "top_strategies": [
                {
                    "id": sid,
                    "name": JARVIS_STRATEGIES[sid],
                    "usage": count,
                    "usage_pct": f"{count / total_usage * 100:.1f}%",
                    "success_rate": f"{(self.strategy_success.get(sid, 0) / max(count, 1)) * 100:.1f}%",
                }
                for sid, count in top_strategies
            ],
            "parents_summary": [
                {
                    "id": i,
                    "fitness": f"{p['fitness']:.3f}",
                    "active_strategies": sum(p["genes"]),
                }
                for i, p in enumerate(self.parents)
            ],
        }

    def get_active_strategies(self) -> List[Dict]:
        """Tüm aktif stratejileri döndür"""
        all_active = set()
        for parent in self.parents:
            for i, g in enumerate(parent["genes"]):
                if g == 1:
                    all_active.add(i)

        return [
            {
                "id": sid,
                "name": JARVIS_STRATEGIES[sid],
                "usage": self.strategy_usage.get(sid, 0),
                "success": self.strategy_success.get(sid, 0),
                "success_rate": f"{(self.strategy_success.get(sid, 0) / max(self.strategy_usage.get(sid, 1), 1)) * 100:.1f}%",
            }
            for sid in sorted(all_active)
        ]

    def save_state(self):
        """Durum kaydet"""
        state = {
            "generation": self.generation,
            "total_evaluations": self.total_evaluations,
            "strategy_usage": self.strategy_usage,
            "strategy_success": self.strategy_success,
            "parents": self.parents,
            "saved_at": time.time(),
        }
        with open(self.state_path, "w") as f:
            json.dump(state, f, indent=2)

    def reset(self):
        """Sıfırla"""
        self.generation = 0
        self.total_evaluations = 0
        self.strategy_usage = {i: 0 for i in range(NUM_STRATEGIES)}
        self.strategy_success = {i: 0 for i in range(NUM_STRATEGIES)}
        self._init_population()
        self.save_state()


# Singleton instance
darwin = DarwinBridge()
