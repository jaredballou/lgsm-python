# LGSM-Python

This is my work in progress of building the core of a new Linux Game Server Manager in Python. It is being done from scratch to try to redo some of the things I dislike about the original. Some key features I am looking to implement:

* [ ] GitHub repos to source the gamedata and modules and be updated via pull.
* [ ] Break out major functions into separate modules
* [ ] Simple installer that users can operate via menu to handle installation of the script itself and its prereqs.
* [ ] Module-based implementation of features and game support libraries. Still not sure how this should look, because I am a noob at Python.
* [ ] Gamedata structure that allows inheritance and overriding of most aspects of the program, to support as many applications as possible with minimal duplication.
* [ ] Create and manage game config files from script.
* [ ] Install mods or other "add-on" features for game servers.
* [ ] Complete command line support, including headless mode.
* [ ] Tie-in with Steam APIs to get data about games.
* [ ] Workshop support, including listing files and verifying correct installation.
* [ ] Backup and restore of all critical files for an instance, including LGSM configs, game config files, and anything else that is tagged via gamedata as important.
* [ ] Updating via the easiest method possible, either Pip, Git, or something else?
* [ ] Game server script interface, for sending commands and fetching data.
* [ ] Log cleanup and rotation.
* [ ] Prerequisites checker and installer.
