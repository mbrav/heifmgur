from rest_framework.throttling import AnonRateThrottle


class ListThrottleBurst(AnonRateThrottle):
    scope = 'list.burst'


class ListThrottleSustained(AnonRateThrottle):
    scope = 'list.sustained'


class DetailThrottleBurst(AnonRateThrottle):
    scope = 'detail.burst'


class DetailThrottleSustained(AnonRateThrottle):
    scope = 'detail.sustained'


class ActionThrottleBurst(AnonRateThrottle):
    scope = 'action.burst'


class ActionThrottleSustained(AnonRateThrottle):
    scope = 'detail.sustained'
