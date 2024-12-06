from test_dev_toml.lib.main import mod_fn


# --------------------
## sample App to set up a background process to run the OnelineServer and
# to run the OnelineClient locally
class App:
    # --------------------
    ## constructor
    def __init__(self):
        pass

    # --------------------
    ## initialize
    #
    # @return None
    def init(self):
        pass

    # --------------------
    ## run the client for various scenarios
    #
    # @return None
    def run(self):
        mod_fn()
