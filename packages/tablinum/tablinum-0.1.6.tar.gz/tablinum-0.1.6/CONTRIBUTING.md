The basic process with hatch

First check everything works with 

    hatch run test-cov --doctest-modules

Check current version level with

    hatch version 

and decide on new version number, and set it with

    hatch version "0.1.whatever"

write a new test for the new function, and make sure it fails.
(Perhaps using self.maxDiff=2000 for big tables..)

    hatch run test "tests/test_tab_new_or_updated_test.py"

now write the function, being aware that your function has to cope 
with Decimal numbers (or cast them to int... etc)

You will need to update the `Panther` cat of functions in tablinum.py

Re-run tests until it works ok

This will probably include updating `tests/test_tab_help.py`

Update the README.md as appropriate

    git status
    git add <all changes>
    git commit -m "Version and message"
    git push

Then do 

    hatch build
    hatch publish

And finally you can install the updated module locally with 

    pipx upgrade tablinum

