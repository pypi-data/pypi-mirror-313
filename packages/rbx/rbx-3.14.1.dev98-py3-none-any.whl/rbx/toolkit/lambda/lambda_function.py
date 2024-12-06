from src import Options, run


def handler(event, context):
    payload = event["payload"]

    run(
        options=Options(
            url=payload["url"],
            width=payload["width"],
            height=payload["height"],
            format=payload["format"],
            output=payload.get(
                "output", "s3://474071279654-eu-west-1-dev/creatives/exports/"
            ),
            filename=payload.get("filename"),
        )
    )

    return "OK"
