import json
import falcon


class JSONMiddleware:
    def process_response(self, req, resp, resource, req_succeeded):
        if req_succeeded:
            response = {
                "status": resp.status,
                "data": resp.body
            }
        else:
            response = {
                "status": falcon.HTTP_500,
                "message": "error"
            }

        resp.text = json.dumps(response)
