class Web3InstanceRequired(Exception):
    """ Raised when user doesn't pass web3 instance in constructor"""
    def __str__(self):
        return f'Web3 instance is required'