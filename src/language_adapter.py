import json
import os
import re
import urllib.error
import urllib.request
import uuid
from typing import Any, Dict, List, Optional, Tuple

from engine import CRSEngine
from models import (
    ActorRole,
    Claim,
    Concept,
    Entity,
    EpistemicState,
    Polarity,
    ProvenanceNode,
)


class LanguageAdapter:
    """
    Language Adapter boundary (Sections 48, 74, 97).
    Translates between natural language (EN / HI / GU) and structured CRS claims/queries
    without storing raw prose as ground truth or bypassing CRS validation.
    """

    def __init__(self, crs: CRSEngine) -> None:
        self.crs = crs

    def _match_entity(self, text: str) -> Optional[Entity]:
        lower = text.lower()
        for ent in self.crs.entities.values():
            candidates = [ent.id.lower(), *(lbl.lower() for lbl in ent.labels)]
            if any(re.search(rf"(?<!\w){re.escape(tok)}(?!\w)", lower) for tok in candidates if tok):
                return ent
        return None

    def _match_concept(self, text: str) -> Optional[str]:
        hits = self.crs.find_concepts(text)
        return hits[0].id if hits else None

    def _detect_epistemic_state(self, sentence: str) -> Tuple[EpistemicState, Dict[str, Any]]:
        s = sentence.lower()
        if any(k in s for k in ("maybe", "might", "possibly", "hypothesis", "suspect")):
            return EpistemicState.HYPOTHESIZED, {"parser": "modal_uncertainty"}
        if any(k in s for k in ("witness", "reported", "says", "said", "claimed", "rumor")):
            return EpistemicState.REPORTED, {"parser": "reported_speech"}
        if any(k in s for k in ("observed", "measured", "sensor", "saw", "seen")):
            return EpistemicState.OBSERVED, {"parser": "direct_observation"}
        return EpistemicState.REPORTED, {"parser": "default_assertion"}

    def _rule_parse(self, sentence: str) -> Dict[str, Any]:
        clean = sentence.strip()
        state, uncertainty = self._detect_epistemic_state(clean)
        polarity = Polarity.NEGATIVE if re.search(r"\b(not|no|never|isn't|aren't|doesn't)\b", clean.lower()) else Polarity.POSITIVE

        entity = self._match_entity(clean)
        subject_id = entity.id if entity else None

        # Pattern 1: "<Subject> owns/has a/an <Concept/Value>"
        m_owns = re.search(r"\b(owns?|has)\s+(?:a|an|the)?\s*([a-zA-Z0-9_\-\u0900-\u097F\u0A80-\u0AFF]+)", clean, re.IGNORECASE)
        if m_owns:
            raw_obj = m_owns.group(2).strip()
            matched_concept = self._match_concept(raw_obj)
            # If a known concept is mentioned (e.g. car, કાર, smartphone), create a typed entity instance
            obj_val = raw_obj
            created_entity_id = None
            if matched_concept:
                created_entity_id = f"ent_{raw_obj.lower()}_{uuid.uuid4().hex[:4]}"
                self.crs.add_entity(
                    Entity(id=created_entity_id, concept_id=matched_concept, labels=(raw_obj,)),
                    actor=ActorRole.LANGUAGE_ADAPTER,
                )
                obj_val = created_entity_id
            return {
                "subject_id": subject_id,
                "relation": "owns",
                "object_value": obj_val,
                "epistemic_state": state.value,
                "polarity": polarity.value,
                "uncertainty": uncertainty,
                "created_entity": created_entity_id,
            }

        # Pattern 2: "<Subject> is/was [in/at] <Value>"
        m_is = re.search(r"\b(?:is|was|are|were)\s+(?:in|at)?\s*([a-zA-Z0-9_\-\u0900-\u097F\u0AFF ]+?)(?:[.!?]|$)", clean, re.IGNORECASE)
        if m_is:
            val = m_is.group(1).strip()
            rel = "location" if re.search(r"\b(?:in|at)\s+" + re.escape(val), clean, re.IGNORECASE) else "attribute"
            matched_ent = self._match_entity(val)
            if matched_ent:
                val = matched_ent.id
            return {
                "subject_id": subject_id,
                "relation": rel,
                "object_value": val,
                "epistemic_state": state.value,
                "polarity": polarity.value,
                "uncertainty": uncertainty,
            }

        # Fallback relation
        return {
            "subject_id": subject_id,
            "relation": "stated_assertion",
            "object_value": clean,
            "epistemic_state": state.value,
            "polarity": polarity.value,
            "uncertainty": uncertainty,
        }

    def _llm_parse(self, sentence: str, mode: str) -> Optional[Dict[str, Any]]:
        """
        Optional LLM parser supporting 'ollama' (local Fedora service) or 'gemini' (GEMINI_API_KEY).
        Returns None if LLM call isn't configured or fails so callers can fall back cleanly.
        """
        prompt = (
            "Extract ONE structured claim JSON from this sentence for a symbolic knowledge graph.\n"
            "Known entity IDs: " + ", ".join(self.crs.entities.keys()) + "\n"
            "Epistemic states: OBSERVED, REPORTED, HYPOTHESIZED, SUPPORTED, CONTESTED, UNKNOWN\n"
            "Polarities: POSITIVE, NEGATIVE, UNKNOWN\n"
            'Return ONLY JSON with keys: {"subject_id": str, "relation": str, "object_value": str, '
            '"epistemic_state": str, "polarity": str}\n'
            f"Sentence: {sentence}"
        )

        try:
            if mode == "ollama":
                base_url = os.environ.get("OLLAMA_URL", "http://127.0.0.1:11434").rstrip("/")
                model = os.environ.get("OLLAMA_MODEL", "llama3.2")
                payload = json.dumps({"model": model, "prompt": prompt, "stream": False, "format": "json"}).encode("utf-8")
                req = urllib.request.Request(
                    f"{base_url}/api/generate",
                    data=payload,
                    headers={"Content-Type": "application/json"},
                    method="POST",
                )
                with urllib.request.urlopen(req, timeout=15) as resp:
                    outer = json.loads(resp.read().decode("utf-8"))
                    return json.loads(outer.get("response", "{}"))

            if mode == "gemini":
                api_key = os.environ.get("GEMINI_API_KEY", "").strip()
                if not api_key:
                    return None
                model = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
                body = {
                    "contents": [{"parts": [{"text": prompt}]}],
                    "generationConfig": {"responseMimeType": "application/json"},
                }
                req = urllib.request.Request(
                    url,
                    data=json.dumps(body).encode("utf-8"),
                    headers={"Content-Type": "application/json"},
                    method="POST",
                )
                with urllib.request.urlopen(req, timeout=15) as resp:
                    outer = json.loads(resp.read().decode("utf-8"))
                    txt = outer["candidates"][0]["content"]["parts"][0]["text"]
                    return json.loads(txt)
        except (urllib.error.URLError, TimeoutError, KeyError, json.JSONDecodeError, ValueError):
            return None

        return None

    def ingest_sentence(self, sentence: str, mode: str = "rule") -> Dict[str, Any]:
        """Parses a natural-language sentence and submits a Claim via ActorRole.LANGUAGE_ADAPTER."""
        if not sentence or not sentence.strip():
            raise ValueError("Sentence cannot be empty.")

        parsed = self._llm_parse(sentence, mode) if mode in ("ollama", "gemini") else None
        used_mode = mode if parsed else "rule"
        if not parsed:
            parsed = self._rule_parse(sentence)

        subject_id = parsed.get("subject_id")
        if not subject_id or subject_id not in self.crs.entities:
            # Default to first available entity or raise clear guidance
            fallback_ent = self._match_entity(sentence)
            if fallback_ent:
                subject_id = fallback_ent.id
            else:
                raise ValueError(
                    f"Could not resolve a known entity in '{sentence}'. "
                    f"Known entities: {', '.join(self.crs.entities.keys())}"
                )

        state = EpistemicState(parsed.get("epistemic_state", "REPORTED"))
        polarity = Polarity(parsed.get("polarity", "POSITIVE"))
        if state == EpistemicState.UNKNOWN:
            polarity = Polarity.UNKNOWN

        prov_id = f"prov_nlp_{uuid.uuid4().hex[:6]}"
        self.crs.add_provenance(
            ProvenanceNode(
                id=prov_id,
                kind="interpretation",
                summary=f"[{used_mode}] Parsed from text: '{sentence.strip()}'",
                derived_from=(),
            ),
            actor=ActorRole.LANGUAGE_ADAPTER,
        )

        claim = Claim(
            id=f"clm_nlp_{uuid.uuid4().hex[:6]}",
            subject_id=subject_id,
            relation=str(parsed.get("relation", "stated_assertion")).strip().replace(" ", "_").lower(),
            object_value=parsed.get("object_value", sentence.strip()),
            epistemic_state=state,
            polarity=polarity,
            provenance_id=prov_id,
            uncertainty={**(parsed.get("uncertainty") or {}), "adapter_mode": used_mode},
        )
        self.crs.add_claim(claim, actor=ActorRole.LANGUAGE_ADAPTER)

        return {
            "parser_used": used_mode,
            "input_sentence": sentence.strip(),
            "created_entity": parsed.get("created_entity"),
            "claim": claim,
        }

    def ask(self, question: str) -> Dict[str, Any]:
        """Answers a natural-language question using multilingual concept lookup and CRS claims."""
        q = question.strip()
        if not q:
            raise ValueError("Question cannot be empty.")

        matched_concepts = self.crs.find_concepts(q)
        matched_entity = self._match_entity(q)

        claims_for_entity = (
            [c for c in self.crs.claims.values() if c.subject_id == matched_entity.id]
            if matched_entity
            else []
        )

        # Also check concept-linked entities if no direct entity matched
        if not claims_for_entity and matched_concepts:
            c_ids = {c.id for c in matched_concepts}
            ent_ids = {e.id for e in self.crs.entities.values() if e.concept_id in c_ids}
            claims_for_entity = [c for c in self.crs.claims.values() if c.subject_id in ent_ids]

        if claims_for_entity:
            parts = [
                f"{c.subject_id}.{c.relation} = {c.object_value} [{c.epistemic_state.value}]"
                for c in claims_for_entity[:6]
            ]
            answer = " | ".join(parts)
        elif matched_concepts:
            names = ", ".join(f"{c.canonical} ({c.id})" for c in matched_concepts)
            answer = f"Matched concept(s): {names}, but no entity claims found yet."
        else:
            answer = "No matching concept or entity claims found in CRS."

        return {
            "question": q,
            "matched_concepts": [c.id for c in matched_concepts],
            "matched_entity": matched_entity.id if matched_entity else None,
            "claims_found": len(claims_for_entity),
            "answer": answer,
        }

    def _find_chat_concept(self, name: str) -> Optional[Concept]:
        normalized = name.strip().casefold()
        for concept in self.crs.concepts.values():
            labels = (label for values in concept.labels.values() for label in values)
            if concept.canonical.casefold() == normalized or any(
                label.casefold() == normalized for label in labels
            ):
                return concept
        return None

    def _get_or_create_chat_concept(
        self, canonical: str, raw_labels: Any = None
    ) -> Tuple[Concept, bool]:
        existing = self._find_chat_concept(canonical)
        if existing:
            return existing, False

        if isinstance(raw_labels, str):
            raw_labels = [raw_labels]
        elif not isinstance(raw_labels, (list, tuple)):
            raw_labels = []
        labels = tuple(
            dict.fromkeys(
                [canonical]
                + [
                    label.strip()
                    for label in raw_labels or []
                    if isinstance(label, str) and label.strip()
                ]
            )
        )
        slug = re.sub(r"[^a-z0-9]+", "_", canonical.casefold()).strip("_")[:48]
        concept = Concept(
            id=f"concept_chat_{slug or 'new'}_{uuid.uuid4().hex[:6]}",
            canonical=canonical,
            labels={"en": labels},
        )
        self.crs.add_concept(concept, actor=ActorRole.LANGUAGE_ADAPTER)
        return concept, True

    def chat(
        self,
        message: str,
        history: Optional[List[Dict[str, str]]] = None,
    ) -> Dict[str, Any]:
        """Chat with Qwen and add explicitly mentioned concepts and entities to the CRS."""
        message = message.strip()
        if not message:
            raise ValueError("Message cannot be empty.")
        if len(message) > 4000:
            raise ValueError("Message is too long (maximum 4000 characters).")

        api_key = os.environ.get("GROQ_API_KEY", "").strip()
        if not api_key:
            raise RuntimeError(
                "Groq is not configured. Set GROQ_API_KEY before starting the server."
            )

        known_concepts = ", ".join(
            concept.canonical for concept in list(self.crs.concepts.values())[:100]
        )
        system_prompt = (
            "You are a conversational assistant connected to a symbolic knowledge graph. "
            "Answer the user's latest message naturally. Extract only concepts and named "
            "entities explicitly stated in that latest user message; use prior turns only "
            "to resolve references, and never invent facts. A concept is a reusable type "
            "or category. Each entity must name its concept, and concepts should be "
            "included when they are not already known. Existing concepts: "
            f"{known_concepts}. Return only a JSON object with this shape: "
            '{"reply":"...","concepts":[{"canonical":"...","labels":["..."]}],'
            '"entities":[{"name":"...","concept":"..."}]}. Use empty arrays '
            "when nothing new is explicit."
        )
        messages: List[Dict[str, str]] = [
            {"role": "system", "content": system_prompt}
        ]
        for item in (history or [])[-12:]:
            if not isinstance(item, dict):
                continue
            role = item.get("role")
            content = item.get("content")
            if role in ("user", "assistant") and isinstance(content, str):
                messages.append({"role": role, "content": content[:2000]})
        messages.append({"role": "user", "content": message})

        request_body = {
            "model": os.environ.get("GROQ_MODEL", "qwen/qwen3.8-27b"),
            "messages": messages,
            "temperature": 0.2,
            "response_format": {"type": "json_object"},
        }
        request = urllib.request.Request(
            "https://api.groq.com/openai/v1/chat/completions",
            data=json.dumps(request_body).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )

        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                api_response = json.loads(response.read().decode("utf-8"))
            content = api_response["choices"][0]["message"]["content"]
            extracted = json.loads(content)
        except urllib.error.HTTPError as exc:
            try:
                error_payload = json.loads(exc.read().decode("utf-8", "replace"))
                error_detail = error_payload.get("error", error_payload)
                if isinstance(error_detail, dict):
                    error_detail = error_detail.get("message", "")
                if not isinstance(error_detail, str):
                    error_detail = ""
            except (json.JSONDecodeError, AttributeError, OSError):
                error_detail = ""
            error_detail = error_detail.replace(api_key, "[redacted]").strip()[:500]
            if exc.code == 401:
                message = "Groq authentication failed"
            else:
                message = f"Groq API returned HTTP {exc.code}"
            if error_detail:
                message = f"{message}: {error_detail}"
            elif exc.code == 401:
                message = f"{message}. Check GROQ_API_KEY."
            raise RuntimeError(message) from exc
        except (urllib.error.URLError, TimeoutError) as exc:
            raise RuntimeError("Could not reach the Grok API.") from exc
        except (KeyError, IndexError, TypeError, json.JSONDecodeError) as exc:
            raise RuntimeError("Grok returned an invalid structured response.") from exc

        if not isinstance(extracted, dict):
            raise RuntimeError("Grok returned an invalid structured response.")
        reply = extracted.get("reply")
        if not isinstance(reply, str) or not reply.strip():
            raise RuntimeError("Grok did not return a chat reply.")

        added_concepts: List[Dict[str, str]] = []
        concept_records = extracted.get("concepts", [])
        if isinstance(concept_records, list):
            for record in concept_records[:20]:
                if not isinstance(record, dict):
                    continue
                canonical = record.get("canonical")
                if not isinstance(canonical, str) or not canonical.strip():
                    continue
                canonical = canonical.strip()[:120]
                concept, created = self._get_or_create_chat_concept(
                    canonical, record.get("labels")
                )
                if created:
                    added_concepts.append(
                        {"id": concept.id, "canonical": concept.canonical}
                    )

        added_entities: List[Dict[str, str]] = []
        entity_records = extracted.get("entities", [])
        if isinstance(entity_records, list):
            for record in entity_records[:30]:
                if not isinstance(record, dict):
                    continue
                name = record.get("name")
                concept_name = record.get("concept")
                if not isinstance(name, str) or not isinstance(concept_name, str):
                    continue
                name = name.strip()[:120]
                concept_name = concept_name.strip()[:120]
                if not name or not concept_name:
                    continue

                concept, created = self._get_or_create_chat_concept(concept_name)
                if created:
                    added_concepts.append(
                        {"id": concept.id, "canonical": concept.canonical}
                    )
                normalized_name = name.casefold()
                existing_entity = next(
                    (
                        entity
                        for entity in self.crs.entities.values()
                        if entity.id.casefold() == normalized_name
                        or any(label.casefold() == normalized_name for label in entity.labels)
                    ),
                    None,
                )
                if existing_entity:
                    continue

                slug = re.sub(r"[^a-z0-9]+", "_", name.casefold()).strip("_")[:48]
                entity = Entity(
                    id=f"ent_chat_{slug or 'new'}_{uuid.uuid4().hex[:6]}",
                    concept_id=concept.id,
                    labels=(name,),
                )
                self.crs.add_entity(entity, actor=ActorRole.LANGUAGE_ADAPTER)
                added_entities.append(
                    {
                        "id": entity.id,
                        "name": name,
                        "concept_id": concept.id,
                    }
                )

        return {
            "reply": reply.strip(),
            "added": {"concepts": added_concepts, "entities": added_entities},
            "model": request_body["model"],
        }
