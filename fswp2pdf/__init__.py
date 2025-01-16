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

    #############
    # tests 0.0 #
    #############

    if current_version == "0.0":

        print(f"fswp2pdf version is {version}")
        print("done.")

    #############
    # tests x.x #
    #############

    if current_version == "x.x":
        pass
