#
# file: __init__.py
# content: init file for fswp2pdf package
# created: 2025 January 11 Saturday
# modified: 2025 January 16 Wednesday
# modification: clean up
# author: roch schanen
# comment: package is under heavy development, version 0.0.0

version_history = {}

""" 
    __init__.py

    designed to be used as template for new package modules

"""

###########
# version #
###########

version = "0.0.0"

version_history["0.0"] = """
version 0.0 (15 January 2025)

    add version property: version = "0.0.0"

"""
 
########
# info #
########

if __name__ == "__main__":

    ###  display version ###

    current_version = list(version_history.keys())[-1]

    print(f"__init__ current version: {current_version}")
    print(f"-------------------------")

    print()
    print(f"history")
    print(f"-------")
    for v in version_history.values():
        print(v)

    # test list
    TESTS = [
        current_version,
        # "0.0",
        # "x.x",
        ]

    #############
    # tests 0.0 #
    #############

    if current_version == "0.0":

        print(f"fswp2pdf version is {version}")

        ###########
        # IMPORTS #
        ###########

        """ 
            imports differs when running from the local folder
            or from the built library. Try one or the other and
            swap if not found.
        """

        # # from the local package
        # # ----------------------
        # try:

        #     # import from built
        #     # -----------------
        #     from fswp2pdf import sielib
        #     from fswp2pdf import splotlib
        #     from fswp2pdf import sfitlib

        # except ImportError as error:

        #     # import from .
        #     # -------------
        #     import sielib
        #     import splotlib
        #     import sfitlib

        print("done.")

    #############
    # tests x.x #
    #############

    if current_version == "x.x":
        pass
