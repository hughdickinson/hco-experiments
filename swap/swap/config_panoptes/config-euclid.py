
# Copy the contents of this file to config.py to override config
# options


def override(config):

    # Configuration for Online Swap
    config.database.name = 'swapDB_euclidTest'
    # config.parser.annotation.task = 'T0'
    # config.parser.annotation.true = ['Yes', 1]
    # config.parser.annotation.false = ['No', 0]
    #
    config.online_swap.host = 'northdown.spa.umn.edu/euclid'
    # config.online_swap.ext_port = '443'
    # config.online_swap.caesar.host = 'caesar-staging.zooniverse.org'
    # config.online_swap.caesar.port = '443'
    #
    config.online_swap.workflow = 3009
    #
    # config.logging.files.version = 'static'

    # True: static swap, False: dynamic swap
    config.back_update = False

    # Prior probability
    # config.p0 = 0.12

    # config.mdr = 0.1

    # Parse data types in csv dump
    config.database.builder.types = {}

    # Metadata in csv dump
    # config.database.builder.metadata = [
    #     'mag',
    #     'mag_err',
    #     'machine_score',
    #     'diff',
    #     'object_id'] + [
    #     'random%d' % (i + 1) for i in range(15)]
    config.database.builder.metadata = []

    # Database configuration
    config.database.name = 'swapDB_euclidTest'
    # config.database.host = 'localhost'
    # config.database.port = 27017

    ##################################################
    # Online SWAP configuration

    # Interface and port for SWAP to listen on
    config.online_swap.port = 5001
    # config.online_swap.bind = '0.0.0.0'

    # Workflow ID for incoming classifications
    config.online_swap.workflow = 3009

    # Address to send response to
    # config.online_swap.response.host = '10.10.10.10'
    # config.online_swap.response.port = 3000

    # Response AUTH token
    # config.online_swap.response.token = ''

    # Name of reducer registered in Caesar
    config.online_swap.response.reducer = 'swap_euclid'
    # Name of variable in Caesar
    config.online_swap.response.field = 'swap_score'

    return None
