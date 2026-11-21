import json
import math
import sqlite3
from datetime import date, datetime, timezone
from typing import Dict, List, Optional, Tuple

from models import (
    ActorRole,
    Claim,
    Concept,
    Entity,
    EpistemicLink,
    EpistemicState,
    Event,
    LineageEdge,
    Polarity,
    ProvenanceNode,
    Source,
    VectorAttachment,
    to_dict,
)


class CRSError(Exception):
    pass


class CRSAuthError(CRSError):
    pass


class CRSInvariantError(CRSError):
    pass


class CRSEngine:
    """Core CRS engine: write auth, validation, SQLite storage, and queries."""

    def __init__(self, db_path: Optional[str] = "ecos_crs.db") -> None:
        self.db_path = db_path
        self.concepts: Dict[str, Concept] = {}
        self.entities: Dict[str, Entity] = {}
        self.events: Dict[str, Event] = {}
        self.sources: Dict[str, Source] = {}
        self.claims: Dict[str, Claim] = {}
        self.provenance: Dict[str, ProvenanceNode] = {}
        self.epistemic_links: List[EpistemicLink] = []
        self.lineage: List[LineageEdge] = []
        self.vectors: Dict[str, List[VectorAttachment]] = {}
        self.audit_log: List[Dict[str, str]] = []

        if self.db_path:
            self._init_db()

    def _init_db(self) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS crs_objects (
                    kind TEXT NOT NULL,
                    obj_id TEXT NOT NULL,
                    payload TEXT NOT NULL,
                    PRIMARY KEY (kind, obj_id)
                );
                CREATE TABLE IF NOT EXISTS audit_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ts TEXT NOT NULL,
                    actor TEXT NOT NULL,
                    action TEXT NOT NULL,
                    target TEXT NOT NULL,
                    status TEXT NOT NULL,
                    detail TEXT NOT NULL
                );
                """
            )

    def _persist(self, kind: str, obj_id: str, obj: object) -> None:
        if not self.db_path:
            return
        payload = json.dumps(to_dict(obj), ensure_ascii=False)
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT OR REPLACE INTO crs_objects VALUES (?, ?, ?)",
                (kind, obj_id, payload),
            )

    def _audit(
        self, actor: ActorRole, action: str, target: str, status: str, detail: str
    ) -> None:
        entry = {
            "ts": datetime.now(timezone.utc).strftime("%H:%M:%S UTC"),
            "actor": actor.value,
            "action": action,
            "target": target,
            "status": status,
            "detail": detail,
        }
        self.audit_log.append(entry)
        if self.db_path:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(
                    "INSERT INTO audit_log (ts, actor, action, target, status, detail) "
                    "VALUES (?, ?, ?, ?, ?, ?)",
                    (
                        entry["ts"],
                        entry["actor"],
                        entry["action"],
                        entry["target"],
                        entry["status"],
                        entry["detail"],
                    ),
                )

    def _check_auth(self, actor: ActorRole, action: str, target: str) -> None:
        if actor == ActorRole.AEE:
            msg = "AEE cannot directly modify operational CRS state (Sec 60 / Inv 13)."
            self._audit(actor, action, target, "DENIED", msg)
            raise CRSAuthError(msg)

    # --- Write Operations ---
    def add_source(
        self, source: Source, actor: ActorRole = ActorRole.BOOTSTRAP
    ) -> None:
        self._check_auth(actor, "ADD_SOURCE", source.id)
        self.sources[source.id] = source
        self.provenance[source.id] = ProvenanceNode(
            source.id, "source", f"{source.source_type}: {source.name}"
        )
        self._persist("source", source.id, source)
        self._audit(actor, "ADD_SOURCE", source.id, "OK", source.name)

    def add_concept(
        self, concept: Concept, actor: ActorRole = ActorRole.BOOTSTRAP
    ) -> None:
        self._check_auth(actor, "CREATE_CONCEPT", concept.id)
        if concept.id in self.concepts:
            raise CRSInvariantError(
                f"Invariant 9: Concept '{concept.id}' already exists."
            )
        self.concepts[concept.id] = concept
        self._persist("concept", concept.id, concept)
        self._audit(
            actor,
            "CREATE_CONCEPT",
            concept.id,
            "OK",
            f"{concept.canonical} v{concept.version}",
        )

    def add_entity(
        self, entity: Entity, actor: ActorRole = ActorRole.BOOTSTRAP
    ) -> None:
        self._check_auth(actor, "CREATE_ENTITY", entity.id)
        if entity.concept_id not in self.concepts:
            raise CRSError(f"Referential error: Unknown concept '{entity.concept_id}'.")
        self.entities[entity.id] = entity
        self._persist("entity", entity.id, entity)
        self._audit(actor, "CREATE_ENTITY", entity.id, "OK", entity.concept_id)

    def add_event(
        self, event: Event, actor: ActorRole = ActorRole.BOOTSTRAP
    ) -> None:
        self._check_auth(actor, "ADD_EVENT", event.id)
        self.events[event.id] = event
        self._persist("event", event.id, event)
        self._audit(actor, "ADD_EVENT", event.id, "OK", event.event_type)

    def add_provenance(
        self, node: ProvenanceNode, actor: ActorRole = ActorRole.BOOTSTRAP
    ) -> None:
        self._check_auth(actor, "ADD_PROVENANCE", node.id)
        self.provenance[node.id] = node
        self._persist("provenance", node.id, node)
        self._audit(actor, "ADD_PROVENANCE", node.id, "OK", node.kind)

    def add_claim(
        self, claim: Claim, actor: ActorRole = ActorRole.LANGUAGE_ADAPTER
    ) -> None:
        self._check_auth(actor, "ADD_CLAIM", claim.id)

        if claim.id in self.claims:
            msg = f"Invariant 5: Claim '{claim.id}' cannot be overwritten."
            self._audit(actor, "ADD_CLAIM", claim.id, "REJECTED", msg)
            raise CRSInvariantError(msg)

        if claim.subject_id not in self.entities and claim.subject_id not in self.concepts:
            msg = f"Referential error: Subject '{claim.subject_id}' does not exist."
            self._audit(actor, "ADD_CLAIM", claim.id, "REJECTED", msg)
            raise CRSError(msg)

        if (
            claim.epistemic_state == EpistemicState.UNKNOWN
            and claim.polarity == Polarity.NEGATIVE
        ):
            msg = "Invariant 2: UNKNOWN state cannot use NEGATIVE polarity (Unknown != False)."
            self._audit(actor, "ADD_CLAIM", claim.id, "REJECTED", msg)
            raise CRSInvariantError(msg)

        if (
            claim.temporal.valid_from
            and claim.temporal.valid_to
            and claim.temporal.valid_to < claim.temporal.valid_from
        ):
            msg = "Temporal error: valid_to precedes valid_from."
            self._audit(actor, "ADD_CLAIM", claim.id, "REJECTED", msg)
            raise CRSError(msg)

        self.claims[claim.id] = claim
        self._persist("claim", claim.id, claim)
        summary = f"{claim.subject_id}.{claim.relation}={claim.object_value}"
        self._audit(actor, "ADD_CLAIM", claim.id, "OK", summary)

    def link_claims(
        self, link: EpistemicLink, actor: ActorRole = ActorRole.COGNITIVE_SUPERVISOR
    ) -> None:
        self._check_auth(actor, "LINK_CLAIMS", link.id)
        self.epistemic_links.append(link)
        self._persist("epistemic_link", link.id, link)
        self._audit(actor, "LINK_CLAIMS", link.id, "OK", f"{link.from_id}->{link.to_id}")

    def refine_concept(
        self,
        old_id: str,
        new_id: str,
        defaults: Tuple[str, ...],
        exceptions: Tuple[str, ...],
        reason: str,
        actor: ActorRole = ActorRole.CONCEPT_EVOLUTION,
    ) -> Concept:
        self._check_auth(actor, "REFINE_CONCEPT", new_id)
        old = self.concepts[old_id]
        updated = Concept(
            id=new_id,
            canonical=old.canonical,
            version=old.version + 1,
            labels=old.labels,
            defaults=defaults,
            exceptions=exceptions,
        )
        self.add_concept(updated, actor=actor)
        edge = LineageEdge(old_id, new_id, "REFINE", reason)
        self.lineage.append(edge)
        self._persist("lineage", f"{old_id}->{new_id}", edge)
        return updated

    def attach_vector(
        self, vec: VectorAttachment, actor: ActorRole = ActorRole.BOOTSTRAP
    ) -> None:
        self._check_auth(actor, "ATTACH_VECTOR", vec.object_id)
        self.vectors.setdefault(vec.object_id, []).append(vec)
        self._persist("vector", vec.vector_id, vec)

    # --- Query Operations (Section 57-58) ---
    def find_concepts(self, text: str = "") -> List[Concept]:
        q = text.strip().lower()
        if not q:
            return list(self.concepts.values())
        hits = []
        for c in self.concepts.values():
            terms = [c.id.lower(), c.canonical.lower()]
            for group in c.labels.values():
                terms.extend(lbl.lower() for lbl in group)
            if any(q in t for t in terms):
                hits.append(c)
        return hits

    def query_claims(
        self,
        subject_id: Optional[str] = None,
        relation: Optional[str] = None,
        valid_on: Optional[date] = None,
        epistemic_state: Optional[EpistemicState] = None,
    ) -> List[Claim]:
        out = []
        for c in self.claims.values():
            if subject_id and c.subject_id != subject_id:
                continue
            if relation and c.relation != relation:
                continue
            if valid_on and not c.temporal.is_valid_on(valid_on):
                continue
            if epistemic_state and c.epistemic_state != epistemic_state:
                continue
            out.append(c)
        return out

    def get_contradictions(self) -> List[Dict[str, object]]:
        pairs = []
        for link in self.epistemic_links:
            if (
                link.relation == "contradicts"
                and link.from_id in self.claims
                and link.to_id in self.claims
            ):
                pairs.append(
                    {
                        "link": link,
                        "claim_a": self.claims[link.from_id],
                        "claim_b": self.claims[link.to_id],
                    }
                )
        return pairs

    def trace_provenance(self, prov_id: str) -> List[ProvenanceNode]:
        chain, seen = [], set()

        def walk(nid: str) -> None:
            if nid in seen or nid not in self.provenance:
                return
            seen.add(nid)
            node = self.provenance[nid]
            chain.append(node)
            for parent in node.derived_from:
                walk(parent)

        walk(prov_id)
        return chain

    def vector_search(
        self, query_vec: Tuple[float, ...], model: str, top_k: int = 3
    ) -> List[Dict[str, object]]:
        def cosine(a: Tuple[float, ...], b: Tuple[float, ...]) -> float:
            dot = sum(x * y for x, y in zip(a, b))
            na = math.sqrt(sum(x * x for x in a))
            nb = math.sqrt(sum(y * y for y in b))
            return dot / (na * nb) if na and nb else 0.0

        hits = []
        for obj_id, items in self.vectors.items():
            for v in items:
                if v.model == model:
                    hits.append(
                        {
                            "object_id": obj_id,
                            "model": v.model,
                            "similarity": round(cosine(query_vec, v.values), 4),
                        }
                    )
        return sorted(hits, key=lambda item: item["similarity"], reverse=True)[:top_k]
