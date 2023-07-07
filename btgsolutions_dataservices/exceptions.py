class WSTypeError(Exception):
    """
    Must provide a valid 'ws_type' parameter.
    """
    pass

class DelayedError(Exception):
    """
    Must provide a valid 'target' parameter.
    """
    pass

class BadResponse(Exception):
    """
    Api did not return status 200.
    """
    pass

class FeedError(Exception):
    """
    Must provide a valid 'feed' parameter.
    """
    pass

class MarketTypeError(Exception):
    """
    Must provide a valid 'market_type' parameter.
    """
    pass

class DelayError(Exception):
    """
    Must provide a valid 'delay' parameter.
    """
    pass