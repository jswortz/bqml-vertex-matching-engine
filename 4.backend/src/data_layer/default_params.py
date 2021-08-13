import os

HP_PLACEMENT = os.environ.get(
    'HP_PLACEMENT',
    'homepage'
)  # update to recommendation placement

PARAMS = {
    "placement_name": HP_PLACEMENT,
    "params": {
        "dryRun": "false",
        "userEvent": {
            "eventType": "detail-page-view",
            "userInfo": {
                "visitorId": ""
            },
            "productEventDetail": {
                "productDetails": [
                    {
                        "id": ''
                    }
                ]
            }
        }
    }
}
