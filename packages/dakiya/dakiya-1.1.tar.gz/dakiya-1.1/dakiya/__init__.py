import base64
import json
import os
from datetime import datetime
import requests

AUTH = os.getenv("DAKIYA_AUTH", "local_dev_key")
APP_NAME = os.getenv("DAKIYA_APPNAME", "GLOBAL")

HOST = "https://dakiya.nitrocommerce.ai"
if os.getenv("MODE", "") == "DEVELOPMENT":
    HOST = os.getenv("DAKIYA_HOST", "http://localhost:10400")


def serialize(obj):
    # If it's a datetime, return its ISO format string
    if isinstance(obj, datetime):
        return obj.isoformat()

    # If it's a dict, recursively serialize all values
    if isinstance(obj, dict):
        return {key: serialize(value) for key, value in obj.items()}

    # If it's a list, recursively serialize all items
    if isinstance(obj, list):
        return [serialize(element) for element in obj]

    # If the object has a __dict__, serialize it to its dictionary representation
    if hasattr(obj, "__dict__"):
        return obj.__dict__

    # Fallback to converting the object to a string
    return str(obj)


class TransmitterException(Exception):
    pass


class Transmitter:

    def send_x(self, what, template, *k, **kw):
        assert what in ["email", "sms", "whatsapp", "telegram"]
        assert template.endswith(".html")

        # Ensure the serialization of the kw arguments to handle datetime
        # serialized_kw = {key: serialize(value) for key, value in kw.items()}

        encoded_attachements = []
        if "attachments" in kw:
            all_attachments = kw["attachments"]
            if not isinstance(all_attachments, list):
                all_attachments = [all_attachments]

            for attachment in all_attachments:
                size = os.fstat(attachment.fileno()).st_size
                name = os.path.basename(attachment.name)

                if size > 25 * 1024 * 1024:
                    raise TransmitterException(
                        2, "Cannot size file of size more than 25MB"
                    )

                fcontents = None
                try:
                    fcontents = attachment.read()
                except:
                    pass
                if not fcontents:
                    raise TransmitterException(
                        3,
                        "Cannot read attachment, make sure you open file in rb+ mode.",
                    )

                encoded = base64.encodebytes(fcontents)
                encoded_attachements.append(
                    {
                        "filename": name,
                        "size": size,
                        "base64_encoded_data": encoded.decode(),
                    }
                )

            kw["attachments"] = encoded_attachements

        res = None

        # Now, serialize kw before sending
        payload = json.dumps(kw, default=serialize)
        if os.getenv("MODE", "") == "DEVELOPMENT":
            print("Payload", payload)

        try:
            res = requests.post(
                f"{HOST}/relay/{what}/{template}",
                data=payload,
                headers={
                    "Authorization": f"S2S {AUTH}",
                    "X-App": APP_NAME,
                    "Content-Type": "application/json",
                },
            )
        except requests.exceptions.ConnectionError:
            import traceback

            traceback.print_exc()

        if res is None:
            raise TransmitterException(0, "Connection Error")

        if res.ok:
            res = res.json()
            return res

        try:
            res = res.json()
        except Exception as e:
            print("Exception in JSON.load", e)
            pass

        if res is not None:
            raise TransmitterException(res["code"], res["message"])

        raise TransmitterException(0, "JSON Decode Error from Downstream")

    def __getattr__(self, name):
        name = name.split("_")[1]

        def fn(template, *k, **kw):
            return self.send_x(name, template, *k, **kw)

        return fn


transmitter = Transmitter()


if __name__ == "__main__":
    var = {
        "who": "Shamail",
        "time": "1:10",
        "name": "Sample",
        "timestamp": datetime.now(),
        "nested": {"value": 42, "date": datetime(2024, 12, 4, 15, 0)},
    }
    result = transmitter.send_email(
        "nitrox/welcome.html",
        to="pleomax00@gmail.com",
        subject="Hello World!",
        attachments=[open("/tmp/a.png", "rb+")],
        vars=var,
    )
    print(result)
