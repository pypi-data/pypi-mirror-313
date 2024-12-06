from datetime import datetime

import media_muncher.profile as PG
from media_muncher.analysers.dash import DashAnalyser
from media_muncher.analysers.hls import HlsAnalyser
from media_muncher.exceptions import MediaHandlerError
from media_muncher.handlers import ContentHandler, DASHHandler, HLSHandler


def make_transcoding_profile(
    handler: ContentHandler, schema_version: str, name: str = ""
):
    analyser = None
    if isinstance(handler, HLSHandler):
        analyser = HlsAnalyser(handler)
    elif isinstance(handler, DASHHandler):
        analyser = DashAnalyser(handler)
    else:
        raise Exception("Unsupported handler type")

    # Check that the stream is readable first
    handler.document
    if handler.status > 299:
        raise MediaHandlerError(f"The stream is not readable: HTTP {handler.status}")
    
    renditions = analyser.extract_renditions()
    packaging = analyser.extract_packaging_info()

    generator = PG.ABRProfileGenerator(schema=schema_version)
    profile = generator.generate(renditions, packaging, name)

    # decorate the profile
    profile["_generated_from"] = handler.original_url
    profile["_generated"] = datetime.now().isoformat()

    return (profile, analyser.messages + generator.messages)
