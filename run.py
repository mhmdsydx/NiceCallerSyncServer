from core.sync_engine import SyncEngine

engine = SyncEngine()
engine.sync()

print(engine.stats)
