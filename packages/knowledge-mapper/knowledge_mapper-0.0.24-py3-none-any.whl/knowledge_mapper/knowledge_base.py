from __future__ import annotations
from dataclasses import dataclass
import logging as log
import requests

import knowledge_mapper.knowledge_interaction as knowledge_interaction

from knowledge_mapper.tke_exceptions import UnexpectedHttpResponseError


class KnowledgeBaseUnregistered(Exception):
    pass


class KnowledgeEngineTerminated(Exception):
    pass


@dataclass(kw_only=True)
class KnowledgeBaseRegistrationRequest:
    """Class with necessary data itemsfor registering a new knowledge base."""

    id: str
    name: str
    description: str


class KnowledgeBase:
    def __init__(self, req: KnowledgeBaseRegistrationRequest, ke_url: str):
        self.ke_url = ke_url
        self.id = req.id
        self.name = req.name
        self.description = req.description
        self.kis = dict()
        self.kis_by_name = dict()

    def from_json(kb_json: dict, ke_url: str) -> KnowledgeBase:
        kb = KnowledgeBase(
            KnowledgeBaseRegistrationRequest(
                id=kb_json["knowledgeBaseId"],
                name=kb_json["knowledgeBaseName"],
                description=kb_json["knowledgeBaseDescription"],
            ),
            ke_url=ke_url,
        )

        kb.sync_knowledge_interactions()

        return kb

    def unregister(self):
        if self.ke_url is None:
            raise Exception(
                "Cannot unregister this KB because no knowledge engine URL is known for this object."
            )

        response = requests.delete(
            f"{self.ke_url}/sc", headers={"Knowledge-Base-Id": self.id}
        )

        if not response.ok:
            raise UnexpectedHttpResponseError(response)

    def register_knowledge_interaction(
        self,
        ki: knowledge_interaction.KnowledgeInteractionRegistrationRequest,
        name=None,
    ) -> knowledge_interaction.KnowledgeInteraction:
        body = {"knowledgeInteractionType": ki.type, "prefixes": ki.prefixes}

        if name is not None:
            body["knowledgeInteractionName"] = name

        if isinstance(
            ki,
            knowledge_interaction.AskKnowledgeInteractionRegistrationRequest
            | knowledge_interaction.AnswerKnowledgeInteractionRegistrationRequest,
        ):
            body["graphPattern"] = ki.pattern
            body["knowledgeGapsEnabled"] = ki.knowledge_gaps_enabled
        elif isinstance(
            ki,
            knowledge_interaction.PostKnowledgeInteractionRegistrationRequest
            | knowledge_interaction.ReactKnowledgeInteractionRegistrationRequest,
        ):
            body["argumentGraphPattern"] = ki.argument_pattern
            body["resultGraphPattern"] = ki.result_pattern
        else:
            raise Exception("`ki` must be a concrete knowledge interaction object")

        response = requests.post(
            f"{self.ke_url}/sc/ki", headers={"Knowledge-Base-Id": self.id}, json=body
        )

        if not response.ok:
            raise UnexpectedHttpResponseError(response)

        ki_id = response.json()["knowledgeInteractionId"]

        log.info(f"Successfully registered knowledge interaction {ki_id}.")

        registered_ki = knowledge_interaction.KnowledgeInteraction.from_req(
            ki, ki_id, self
        )
        self.kis[ki_id] = registered_ki

        if name is not None:
            self.kis_by_name[name] = registered_ki

        return registered_ki

    def sync_knowledge_interactions(self):
        response = requests.get(
            f"{self.ke_url}/sc/ki", headers={"Knowledge-Base-Id": self.id}
        )

        if not response.ok:
            raise UnexpectedHttpResponseError(response)

        raw_kis = response.json()
        kis_not_seen_yet = self.kis.copy()
        kis_by_name_not_seen_yet = self.kis_by_name.copy()
        for raw_ki in raw_kis:
            if raw_ki["knowledgeInteractionType"] == "AskKnowledgeInteraction":
                req = knowledge_interaction.AskKnowledgeInteractionRegistrationRequest(
                    pattern=raw_ki["graphPattern"]
                )
            elif raw_ki["knowledgeInteractionType"] == "AnswerKnowledgeInteraction":
                req = (
                    knowledge_interaction.AnswerKnowledgeInteractionRegistrationRequest(
                        pattern=raw_ki["graphPattern"], handler=None
                    )
                )
            elif raw_ki["knowledgeInteractionType"] == "PostKnowledgeInteraction":
                req = knowledge_interaction.PostKnowledgeInteractionRegistrationRequest(
                    argument_pattern=raw_ki["argumentGraphPattern"],
                    result_pattern=raw_ki["resultGraphPattern"]
                    if "resultGraphPattern" in raw_ki
                    else None,
                )
            elif raw_ki["knowledgeInteractionType"] == "ReactKnowledgeInteraction":
                req = (
                    knowledge_interaction.ReactKnowledgeInteractionRegistrationRequest(
                        argument_pattern=raw_ki["argumentGraphPattern"],
                        result_pattern=raw_ki["resultGraphPattern"]
                        if "resultGraphPattern" in raw_ki
                        else None,
                        handler=None,
                    )
                )
            else:
                raise Exception(
                    f"Invalid KI type: {raw_ki['knowledgeInteractionType']}"
                )

            if "knowledgeInteractionName" in raw_ki:
                name = raw_ki["knowledgeInteractionName"]
            else:
                name = None

            ki_id = raw_ki["knowledgeInteractionId"]

            ki = knowledge_interaction.KnowledgeInteraction.from_req(
                req, ki_id, self, name
            )

            self.kis[ki_id] = ki
            if ki_id in kis_not_seen_yet:
                del kis_not_seen_yet[ki_id]
            if name is not None:
                self.kis_by_name[name] = ki
                if name in kis_by_name_not_seen_yet:
                    del kis_by_name_not_seen_yet[name]

        for no_longer_existing_ki_id in kis_not_seen_yet.keys():
            del self.kis[no_longer_existing_ki_id]

        for no_longer_existing_ki_name in kis_by_name_not_seen_yet.keys():
            del self.kis_by_name[no_longer_existing_ki_name]

    def get_ki(self, name=None, id=None) -> knowledge_interaction.KnowledgeInteraction:
        if name is not None and id is None:
            if name in self.kis_by_name:
                return self.kis_by_name[name]
        if id is not None and name is None:
            if id in self.kis:
                return self.kis[id]
        return None

    def start_handle_loop(self, loops=None):
        did_loops = 0
        while loops is not None and did_loops < loops or loops is None:
            status, maybe_ke_request = self.long_poll()
            did_loops += 1
            if status == "repoll":
                continue
            elif status == "reregister":
                self.reregister()
            elif status == "exit":
                log.warn("KE returned status code 410, meaning I have to exit")
                break
            elif status == "handle":
                ke_request = maybe_ke_request

                # Extract relevant data items from the KE request
                ki_id = ke_request["knowledgeInteractionId"]
                handle_request_id = ke_request["handleRequestId"]
                bindings = ke_request["bindingSet"]
                requesting_kb_id = ke_request["requestingKnowledgeBaseId"]

                ki = self.kis[ki_id]
                if isinstance(ki, knowledge_interaction.AnswerKnowledgeInteraction):
                    result_bindings = ki.answer(bindings, requesting_kb_id)
                elif isinstance(ki, knowledge_interaction.ReactKnowledgeInteraction):
                    result_bindings = ki.react(bindings, requesting_kb_id)

                self.post_handle_response(ki, handle_request_id, result_bindings)

    def long_poll(self):
        log.info("Waiting for response to long poll...")
        response = requests.get(
            f"{self.ke_url}/sc/handle", headers={"Knowledge-Base-Id": self.id}
        )
        if response.status_code == 202:
            log.info("Received 202.")
            return "repoll", None
        elif response.status_code == 500:
            log.error(response.text)
            log.error("TKE had an internal server error. Reinitiating long poll.")
            return "repoll", None
        elif response.status_code == 410:
            return "exit", None
        elif response.status_code == 200:
            return "handle", response.json()
        elif response.status_code == 404:
            log.warn("Our Knowledge Base has been unregistered!")
            raise KnowledgeBaseUnregistered()
        else:
            log.warn(f"long_poll received unexpected status {response.status_code}")
            log.warn(response.text)
            log.warn("repolling anyway..")
            return "repoll", None

    def post_handle_response(self, ki, handle_id, bindings):
        response = requests.post(
            f"{self.ke_url}/sc/handle",
            json={
                "handleRequestId": handle_id,
                "bindingSet": bindings,
            },
            headers={
                "Knowledge-Base-Id": self.id,
                "Knowledge-Interaction-Id": ki.id,
            },
        )

        if not response.ok:
            raise UnexpectedHttpResponseError(response)
