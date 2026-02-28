from typing import Dict, Any, Optional, Callable, List
from dataclasses import dataclass, field
from datetime import datetime
import asyncio

@dataclass
class ApiState:
    loading: bool = False
    data: Any = None
    error: Optional[str] = None
    last_updated: Optional[datetime] = None

class StateManager:
    def __init__(self):
        self._states: Dict[str, ApiState] = {}
        self._subscribers: Dict[str, List[Callable]] = {}
    
    def get_state(self, key: str) -> ApiState:
        if key not in self._states:
            self._states[key] = ApiState()
        return self._states[key]
    
    def set_state(self, key: str, state: ApiState):
        self._states[key] = state
        self._notify(key)
    
    def subscribe(self, key: str, callback: Callable):
        if key not in self._subscribers:
            self._subscribers[key] = []
        self._subscribers[key].append(callback)
    
    def _notify(self, key: str):
        if key in self._subscribers:
            for callback in self._subscribers[key]:
                callback(self._states[key])

state_manager = StateManager()

async def fetch_with_state(client, key: str, adapter: str, endpoint: str, **kwargs):
    state_manager.set_state(key, ApiState(loading=True))
    
    try:
        response = await client.get(adapter, endpoint, **kwargs)
        state_manager.set_state(key, ApiState(
            loading=False,
            data=response.get('data'),
            last_updated=datetime.utcnow()
        ))
        return response
    except Exception as e:
        state_manager.set_state(key, ApiState(loading=False, error=str(e)))
        raise
