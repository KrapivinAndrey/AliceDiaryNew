def handler(event, context=None):

    try:
        marusia_request = RequestModel.parse_raw(request.body)
    except ValidationError as e:
        print(e.json())
        return e.json(), 400

    adapter = MarusiaAdapter()

    event = adapter.event(marusia_request)
    event_result = handler(event)

    marusia_response = adapter.response(event_result)
    return marusia_response.json(exclude_none=True), 200
