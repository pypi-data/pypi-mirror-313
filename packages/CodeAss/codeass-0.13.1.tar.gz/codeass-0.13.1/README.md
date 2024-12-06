# Code Assistant [CodeAss]

An assistant I want to use when coding. With help of ChatGPT or not.

[PyPi](https://pypi.org/project/CodeAss/)

## 🚀 Features

### 💻 Commit messages

- AI based commit messages based on semantic version and context in what changed.
- Commit directly with AI based commit messages

## 🔮 Future Features

### Git
- Rewrite all local commits to one big one not yet on origin to one commit. and get a nice commit msg for that one
  e.g. git reset --soft (until what commit is on origin on this branch) and then git add . git commit etc.

### AI
- Output of prompts
- Give context to assistant to help the assistant to help coding
  - Content of code files and 
  - Comments in top of each file with the path of the file
  - Lint messages
  - Error messages
  - add this command:  tree --gitignore -pugf to give tree with permissions and user, group
  - bash / zsh history last hour?
  - environment variables (can be risky!)
  - Give other context
  - glab ci trace

### Glab
- open view latest pipeline automatically
- check on latest pipeline from this commit and constantly check job status, if fail then print trace something
- check ci lint (glab ci lint) if .gitlab-ci.yml exists

### Combined

#### lint
run all lint for all that exist. 
  - If javascript project run npx lint / bun lint
  - if python run flake or similar.
  - if .gitlab-ci.yml run glab lint



## ⚡ Installation

**1.** Install [Python](https://www.python.org/downloads/) 🐍

**2.** 💻 Open a terminal and run

```bash
pip install --upgrade codeass
```

**3.** Done 🎉

## 🎈 How to use

Then run ```ca``` in a 💻 terminal to use the app.


## 💩 Development

Create virtual environment with `venv` & activate


`pip install -e .`