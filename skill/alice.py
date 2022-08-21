class Request:
    def __init__(self, request_body):
        self.request_body = request_body

    def __getitem__(self, key):
        return self.request_body[key]

    @property
    def command(self):
        return self.request_body.get("request", {}).get("original_utterance", "")

    @property
    def tokens(self):
        return self.request_body.get("request", {}).get("nlu", {}).get("tokens", [])

    @property
    def intents(self):
        return self.request_body.get("request", {}).get("nlu", {}).get("intents", {})

    @property
    def entities(self):
        return self.request_body.get("request", {}).get("nlu", {}).get("entities", {})

    def restore_entities(self, saved: dict):
        if self.request_body.get("request") is None:
            self.request_body["request"] = {}
        if self.request_body.get("request").get("nlu") is None:
            self.request_body["request"]["nlu"] = {}
        if self.request_body.get("request").get("nlu").get("entities") is None:
            self.request_body["request"]["nlu"]["entities"] = []
        self.request_body["request"]["nlu"]["entities"] += saved

    def restore_intents(self, saved: dict):
        if self.request_body.get("request") is None:
            self.request_body["request"] = {}
        if self.request_body.get("request").get("nlu") is None:
            self.request_body["request"]["nlu"] = {}
        if self.request_body.get("request").get("nlu").get("intents") is None:
            self.request_body["request"]["nlu"]["intents"] = {}
        self.request_body["request"]["nlu"]["intents"].update(saved)

    @property
    def entities_list(self):
        return [entity["type"] for entity in self.entities]

    @property
    def type(self):
        return self.request_body.get("request", {}).get("type")

    @property
    def session(self) -> dict:
        return self.request_body.get("state", {}).get("session", {})

    @property
    def user(self):
        return self.request_body.get("state", {}).get("user", {})

    @property
    def application(self):
        return self.request_body.get("state", {}).get("application", {})

    @property
    def access_token(self):
        return (
            self.request_body.get("session", {})
            .get("user", {})
            .get("access_token", None)
        )

    @property
    def authorization_complete(self):
        return self.request_body.get("account_linking_complete_event") is not None

    def slots(self, intent: str):
        return (
            self.request_body.get("request", {})
            .get("nlu", {})
            .get("intents", {})
            .get(intent, {})
            .get("slots", {})
            .keys()
        )

    def slot(self, intent: str, slot: str):
        return (
            self.request_body.get("request", {})
            .get("nlu", {})
            .get("intents", {})[intent]
            .get("slots", {})
            .get(slot, {})
            .get("value", None)
        )

    def entity(self, entity_type: str):
        return [
            RequestEntity(entity)
            for entity in self.entities
            if entity["type"] == entity_type
        ]

    def is_intent(self, intent: str):
        return intent in self.intents


class RequestEntity:
    def __init__(self, entity):
        self.value = entity["value"]
        self.start = entity["tokens"]["start"]
        self.end = entity["tokens"]["end"]

    def __eq__(self, other):
        if isinstance(other, str):
            return self.value == other
        else:
            raise Exception("Можно сравнивать только со строкой")

    def __str__(self):
        return self.value

    def __repr__(self):
        return str(self)


def big_image(image_id: list, title=None, description=None):
    my_image = {"type": "BigImage", "image_id": image_id}
    if title:
        my_image["title"] = title
    if description:
        my_image["description"] = description

    return my_image


def image_list(
    image_ids: list,
    header="",
    footer="",
    button_text="",
    button_url="",
    button_payload="",
):
    card: dict = {
        "type": "ItemsList",
        "items": image_ids,
    }
    if header:
        card["header"] = {"text": header}  # type: ignore[assignment]
    if footer or button_text or button_url or button_payload:
        card["footer"] = dict()
        if footer:
            card["footer"]["text"] = footer  # type: ignore[assignment]
        if button_text or button_url or button_payload:
            card["footer"]["button"] = dict()
            if button_text:
                card["footer"]["button"]["text"] = button_text  # type: ignore[assignment]
            if button_url:
                card["footer"]["button"]["url"] = button_url  # type: ignore[assignment]
            if button_payload:
                card["footer"]["button"]["payload"] = button_payload  # type: ignore[assignment]

    return card


def image_gallery(image_ids: list):
    if image_ids and image_ids[0] != "":

        items = [{"image_id": image_id} for image_id in image_ids]
        return {
            "type": "ImageGallery",
            "items": items,
        }
    else:
        return {}


def image_button(
    image_id="",
    title="",
    description="",
    button_text="",
    button_url="",
    button_payload="",
):
    image = {}
    if image_id:
        image["image_id"] = image_id
    if title:
        image["title"] = title
    if description:
        image["description"] = description
    if button_text or button_url or button_payload:
        my_button = {}
        if button_text:
            my_button["text"] = button_text
        if button_url:
            my_button["url"] = button_url
        if button_payload:
            my_button["payload"] = button_payload
        image["button"] = my_button

    return image


def button(title, payload=None, url=None, hide=False):
    my_button = {
        "title": title,
        "hide": hide,
    }
    if payload is not None:
        my_button["payload"] = payload
    if url is not None:
        my_button["url"] = url
    return my_button
