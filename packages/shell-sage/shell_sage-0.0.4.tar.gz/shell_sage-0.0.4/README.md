# ShellSage

## Usage

### Installation

Install latest from the GitHub
[repository](https://github.com/AnswerDotAI/shell_sage):

or from [pypi](https://pypi.org/project/shell_sage/)

```sh
pip install shell_sage
```

We recommend also setting up your terminal editor of choice to keep the editor content's displayed in the terminal on exit. This allows `ShellSage` to see the files you have been working on. Here is how you can do this in vim:

```sh
echo "set t_ti= t_te=" >> ~/.vimrc
```

for `neovim` the above won't work.. but you can set it up in tmux:

```
set-option -g alternate-screen off
```

You will also need to get an Anthropic API key and set its environment variable:

```sh
export ANTHROPIC_API_KEY=sk...
```

## How to use

`ShellSage` is designed to be ran inside a tmux session since it relies on tmux for getting what has is displayed on your terminal as context. If you don't want to use tmux, you will need to use the `--NH` command, which will not include your terminal history.

```sh
ssage hi ShellSage
```

```markdown
Hello! I'm ShellSage, your command-line assistant. I can help you with:

- Bash commands and scripting
- System administration tasks
- Git operations
- File management
- Process handling
- And more!
```

You can also pipe outputs into `ShellSage`:

```sh
cat file.txt | ssage summarize this file
```

You can also select a specific pane for context to come from instead of the default current pane.

```sh
ssage --pid %3 your question
```

> Tip: To use the pane-id selection feature, it is helpful to add `set -g status-right '#{pane_id}'` to your `~/.tmux.conf` file.  Once done, you can reload your tmux config with `tmux source ~/.tmux.conf` to have the pane id displayed on the right hand side of your tmux status bar.

### Configuration

Sage uses a configuration file located at `~/.config/shell_sage/shell_sage.conf`. You can overwrite these configurations by modifying this file or by passing the ShellSage CLI tool a specific argument. By default, ShellSage will use Anthropic's Claude Sonnet 3.5 model. However, you can also use any OpenAI model as well. For example, you can modify your configuration file to be the following:

```
[DEFAULT]
model = gpt-4o-mini
provider = openai
history_lines = -1
code_theme = monokai
code_lexer = python
sassy_mode = False
```

And now when you run ShellSage, it will use GPT 4o mini rather than Cloud Sonnet 3.5. From the command line, you could also do this:

```sh
ssage hi --provider openai --model gpt-4o-mini
```

Remember, this does require you to have set up your OpenAI API key as an environment variable.