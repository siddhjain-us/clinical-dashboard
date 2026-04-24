"""
RandomForest + TF-IDF on clinical note text. Model file: priority_model.pkl next to this module.
Used by the orchestrator (one predict per request) and surfaced on each patient as ml_note.
"""
from __future__ import annotations

import logging
import pickle
from pathlib import Path

log = logging.getLogger(__name__)

_model: dict | None = None
_load_attempted = False

TIER_BONUS = {"HIGH": 40, "MEDIUM": 20, "LOW": 5}


def model_path() -> Path:
    return Path(__file__).resolve().parent / "priority_model.pkl"


def get_model() -> dict | None:
    global _model, _load_attempted
    if _load_attempted:
        return _model
    _load_attempted = True
    p = model_path()
    if not p.exists():
        return None
    try:
        with open(p, "rb") as f:
            _model = pickle.load(f)
    except Exception as e:  # noqa: BLE001 — surface at predict layer
        log.warning("Could not load priority model from %s: %s", p, e)
        _model = None
    return _model


def reset_model_cache() -> None:
    """Test hook to reload model from disk."""
    global _model, _load_attempted
    _model = None
    _load_attempted = False


def predict_note_tier(notes: str) -> dict:
    """
    Returns a dict safe to merge into API / pass to history + summary.
    If no model, history_ml_bonus is 0 and model_available is False.
    """
    m = get_model()
    if not m:
        return {
            "model_available": False,
            "tier": None,
            "proba": None,
            "history_ml_bonus": 0,
        }
    text = (notes or "").strip() or "no clinical note"
    try:
        vec = m["vectorizer"]
        clf = m["clf"]
        v = vec.transform([text])
        tier = str(clf.predict(v)[0])
        prob_row = clf.predict_proba(v)[0]
        classes = [str(c) for c in clf.classes_]
        proba = {classes[i]: float(prob_row[i]) for i in range(len(classes))}
    except Exception as e:  # noqa: BLE001
        log.warning("ML prediction failed: %s", e)
        return {
            "model_available": True,
            "tier": None,
            "proba": None,
            "history_ml_bonus": 0,
            "ml_error": str(e),
        }
    bonus = TIER_BONUS.get(tier, 10)
    return {
        "model_available": True,
        "tier": tier,
        "proba": proba,
        "history_ml_bonus": bonus,
    }
