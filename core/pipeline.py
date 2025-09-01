# core/pipeline.py
"""
Pipeline Module

Provides a robust pipeline engine to record, replay, and manage data transformation steps:
- Step model with operation name, parameters, timestamp, and label.
- Pipeline with add_step, undo/redo, apply, clear.
- JSON (de)serialization for save/load, with an external operation registry.

Author: Data Cleaning Tool Team
Version: 2.5.2
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional

import pandas as pd


@dataclass
class Step:
    op: str
    params: Dict[str, Any]
    ts: str
    label: Optional[str] = None


class Pipeline:
    def __init__(self, registry: Optional[Dict[str, Callable]] = None, version: str = "1.0") -> None:
        self.steps: List[Step] = []
        self._undone: List[Step] = []
        self.registry: Dict[str, Callable] = registry or {}
        self.version: str = version

    @property
    def has_steps(self) -> bool:
        return len(self.steps) > 0

    def add_step(self, op: str, params: Dict[str, Any], label: Optional[str] = None) -> None:
        step = Step(op=op, params=params, ts=datetime.utcnow().isoformat(), label=label)
        self.steps.append(step)
        self._undone.clear()

    def undo(self) -> bool:
        if not self.steps:
            return False
        self._undone.append(self.steps.pop())
        return True

    def redo(self) -> bool:
        if not self._undone:
            return False
        self.steps.append(self._undone.pop())
        return True

    def clear(self) -> None:
        self.steps.clear()
        self._undone.clear()

    def apply(self, df: pd.DataFrame, on_error: str = "skip") -> pd.DataFrame:
        result = df.copy()
        for step in self.steps:
            func = self.registry.get(step.op)
            if func is None:
                if on_error == "raise":
                    raise ValueError(f"Unknown pipeline operation: {step.op}")
                else:
                    continue
            try:
                result = func(result, **(step.params or {}))
            except Exception:
                if on_error == "raise":
                    raise
                continue
        return result

    def to_dict(self) -> Dict[str, Any]:
        return {"version": self.version, "steps": [asdict(s) for s in self.steps], "meta": {"exported_at": datetime.utcnow().isoformat()}}

    @classmethod
    def from_dict(cls, data: Dict[str, Any], registry: Optional[Dict[str, Callable]] = None) -> "Pipeline":
        version = str(data.get("version", "1.0"))
        steps_data = data.get("steps", [])
        pl = cls(registry=registry, version=version)
        for sd in steps_data:
            pl.steps.append(Step(op=sd.get("op"), params=sd.get("params", {}), ts=sd.get("ts", datetime.utcnow().isoformat()), label=sd.get("label")))
        pl._undone.clear()
        return pl