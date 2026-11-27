import json
import os
import re
import uuid
from datetime import date
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from engine import CRSAuthError, CRSError
from evolution import ConceptEvolutionEngine
from extra_data import load_extended_data
from language_adapter import LanguageAdapter
from models import ActorRole, Claim, Concept, Entity, EpistemicState, Polarity, to_dict
from reasoning import ReasoningEngine
from seed import build_demo_crs
from supervisor import CognitiveSupervisor

STATIC_DIR = Path(__file__).parent / "static"
ENV_FILE = Path(__file__).parent / ".env"
STATIC_FILES = {
    "/": ("index.html", "text/html; charset=utf-8"),
    "/static/style.css": ("style.css", "text/css; charset=utf-8"),
    "/static/app.js": ("app.js", "application/javascript; charset=utf-8"),
}


def _load_dotenv(path: Path = ENV_FILE) -> None:
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError):
        return

    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[7:].lstrip()

        key, separator, value = line.partition("=")
        key = key.strip()
        if not separator or not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", key):
            continue

        value = value.strip()
        if value[:1] in ("'", '"'):
            quote = value[0]
            closing_quote = value.find(quote, 1)
            if closing_quote >= 0:
                value = value[1:closing_quote]
        else:
            value = value.split("#", 1)[0].rstrip()
        os.environ.setdefault(key, value)


def run_server(port: int = 8080) -> None:
    _load_dotenv()
    crs = build_demo_crs(db_path="ecos_crs.db")
    load_extended_data(crs)
    reasoner = ReasoningEngine(crs)
    supervisor = CognitiveSupervisor(crs)
    evolution = ConceptEvolutionEngine(crs)
    adapter = LanguageAdapter(crs)

    class Handler(BaseHTTPRequestHandler):
        def _send_bytes(self, code: int, content_type: str, data: bytes) -> None:
            self.send_response(code)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def _json(self, code: int, payload: object) -> None:
            raw = json.dumps(to_dict(payload), ensure_ascii=False).encode("utf-8")
            self._send_bytes(code, "application/json; charset=utf-8", raw)

        def _read_body(self) -> dict:
            length = int(self.headers.get("Content-Length", "0"))
            if length == 0:
                return {}
            return json.loads(self.rfile.read(length).decode("utf-8"))

        def do_GET(self) -> None:
            parsed = urlparse(self.path)
            qs = parse_qs(parsed.query)

            if parsed.path in STATIC_FILES:
                filename, mime = STATIC_FILES[parsed.path]
                file_path = STATIC_DIR / filename
                if file_path.exists():
                    self._send_bytes(200, mime, file_path.read_bytes())
                else:
                    self._json(404, {"error": f"Missing frontend file: {filename}"})
                return

            if parsed.path == "/api/overview":
                inferred_claims = []
                for claim in crs.query_claims(epistemic_state=EpistemicState.INFERRED):
                    chain = crs.trace_provenance(claim.provenance_id or "")
                    trace = " <- ".join(f"{n.kind}({n.summary})" for n in chain) or "—"
                    inferred_claims.append({"claim": claim, "provenance_trace": trace})

                learned_claims = crs.query_claims(epistemic_state=EpistemicState.INTERPRETED)

                self._json(
                    200,
                    {
                        "stats": {
                            "concepts": len(crs.concepts),
                            "entities": len(crs.entities),
                            "events": len(crs.events),
                            "claims": len(crs.claims),
                            "inferred": len(inferred_claims),
                            "learned": len(learned_claims),
                            "contradictions": len(crs.get_contradictions()),
                            "audit_logs": len(crs.audit_log),
                        },
                        "concepts": list(crs.concepts.values()),
                        "entities": list(crs.entities.values()),
                        "inferred": inferred_claims,
                        "learned": learned_claims,
                        "contradictions": crs.get_contradictions(),
                        "unknown": crs.query_claims(epistemic_state=EpistemicState.UNKNOWN),
                        "provenance": crs.trace_provenance("inf_01"),
                        "lineage": crs.lineage,
                    },
                )
            elif parsed.path == "/api/concepts":
                self._json(200, crs.find_concepts(qs.get("q", [""])[0]))
            elif parsed.path == "/api/temporal":
                subj = qs.get("subject", ["ent_car_001"])[0]
                dt = date.fromisoformat(qs.get("date", ["2026-03-15"])[0])
                self._json(200, crs.query_claims(subject_id=subj, valid_on=dt))
            elif parsed.path == "/api/ask":
                q = qs.get("q", [""])[0]
                self._json(200, adapter.ask(q))
            else:
                self._json(404, {"error": "Not found"})

        def do_POST(self) -> None:
            try:
                data = self._read_body()
                if self.path == "/api/chat":
                    message = data.get("message", "")
                    if not isinstance(message, str):
                        raise ValueError("Message must be a string.")
                    history = data.get("history", [])
                    if not isinstance(history, list):
                        history = []
                    self._json(200, adapter.chat(message, history))
                elif self.path == "/api/ingest":
                    result = adapter.ingest_sentence(
                        sentence=data.get("sentence", ""),
                        mode=data.get("mode", "rule"),
                    )
                    self._json(201, result)
                elif self.path == "/api/reason":
                    self._json(200, reasoner.run_all())
                elif self.path == "/api/supervise":
                    self._json(200, supervisor.review())
                elif self.path == "/api/evolve":
                    self._json(200, evolution.run_evolution())
                elif self.path == "/api/concepts":
                    if not data.get("id") or not data.get("canonical"):
                        raise ValueError("Both Concept ID and Canonical name are required.")
                    labels = {}
                    for lang in ("en", "hi", "gu"):
                        items = tuple(x.strip() for x in data.get(lang, "").split(",") if x.strip())
                        if items:
                            labels[lang] = items
                    concept = Concept(id=data["id"], canonical=data["canonical"], labels=labels)
                    crs.add_concept(concept)
                    self._json(201, concept)
                elif self.path == "/api/entities":
                    if not data.get("id") or not data.get("concept_id"):
                        raise ValueError("Entity ID and Concept are required.")
                    label = data.get("label") or data["id"]
                    entity = Entity(id=data["id"], concept_id=data["concept_id"], labels=(label,))
                    crs.add_entity(entity)
                    self._json(201, entity)
                elif self.path == "/api/claims":
                    claim = Claim(
                        id=f"clm_{uuid.uuid4().hex[:6]}",
                        subject_id=data["subject_id"],
                        relation=data["relation"],
                        object_value=data["object_value"],
                        epistemic_state=EpistemicState(data["epistemic_state"]),
                        polarity=Polarity(data["polarity"]),
                    )
                    crs.add_claim(claim, actor=ActorRole(data["actor"]))
                    self._json(201, claim)
                else:
                    self._json(404, {"error": "Not found"})
            except CRSAuthError as exc:
                self._json(403, {"error": str(exc)})
            except (CRSError, ValueError, KeyError) as exc:
                self._json(400, {"error": str(exc)})
            except RuntimeError as exc:
                self._json(503, {"error": str(exc)})

    print(f"[ECOS-CRS] Web Explorer running at http://127.0.0.1:{port} (Ctrl+C to stop)")
    ThreadingHTTPServer(("127.0.0.1", port), Handler).serve_forever()


if __name__ == "__main__":
    run_server()
