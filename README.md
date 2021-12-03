# :black_circle: :white_circle: pyreversi :black_circle: :white_circle: 

pyreversi is a reversi game in your terminal with IA available.

# Démo

![image](./demo_01.png)


# 🚀 How to use **pyreversi**

``pyreversi``

## IA options

- ``-b --blackbot [int]`` : black player is a bot, with level [int]
- ``-w --whitebot [int]`` : white player is a bot, with level [int]
- ``-f/--fix`` : disable random choice in the set of best choices for IA

- level 0 : one in available choices
- level 1 : max increase score
- level 2 : max increase score + target corner + not offer corner
- level 3 : max increase score + target corner + not offer corner considering next turn
- level 4 : max increase score + target corner + not offer corner considering next turn + considering safe place
## Other options

- ``-u/--update`` update the package
- ``-v/--verbose`` verbose mode
- ``-a/--auto`` auto mode (disable "press any key")
- ``-r/--rules`` display rules
# ⚙️ Install

See [this page](INSTALL.md)

# :construction_worker: Contribution

See [this page](CONTRIBUTING.md)

# :package: Changelog

See [this page](CHANGELOG.md)


# License

MIT License

Copyright (c) 2021 [thib1984](https://github.com/thib1984)

See [this page](LICENSE.txt) for details
