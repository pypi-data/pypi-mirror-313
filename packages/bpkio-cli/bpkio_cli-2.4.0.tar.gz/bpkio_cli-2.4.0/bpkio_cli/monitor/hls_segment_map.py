from bpkio_cli.monitor.store import SignalEventType, SignalType

SYMBOLS = dict()
SYMBOLS[SignalEventType.AD] = dict(symbol="⏺", letter="A", color="green")
SYMBOLS[SignalEventType.SLATE] = dict(symbol="○", letter="S", color="blue")
SYMBOLS[SignalEventType.CONTENT] = dict(symbol="■", letter="C", color="white")
SYMBOLS[SignalType.HLS_MARKER] = dict(symbol="*", color="yellow")
SYMBOLS[SignalType.DISCONTINUITY] = dict(symbol="/", color="white")
SYMBOLS[SignalEventType.CUE_OUT] = dict(symbol="▶", color="magenta")
SYMBOLS[SignalEventType.CUE_IN] = dict(symbol="◀", color="magenta")
