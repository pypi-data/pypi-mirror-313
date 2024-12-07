## pyqqq-cli

### Installation

You can install `pyqqq-cli` via pip:

```bash
pip install pyqqq-cli
```

### Usage

After installation, the `qqq` command will be available. You can execute it with various subcommands:

```bash
qqq [OPTIONS] COMMAND [ARGS]...
```

#### Options

- `--help`: Show the help message and exit.

#### Commands

- `backtest`: Deploy a backtest
- `delete`: Delete a deployed strategy
- `deploy`: Deploy a strategy
- `lint`: Ensure that pylint is installed in the current python...
- `list`: List deployed strategies
- `logs`: Show logs of a deployed strategy
- `pause`: Pause a deployed strategy
- `pull`: Download an strategy from the registry
- `resume`: Resume a paused strategy
- `run`: Run a strategy
- `search`: Search for stock investment strategies
- `update`: Update the environment of the deployed strategy
- `version`: Show version number and quit

### Example

```bash
qqq deploy my_strategy_name
```

This command deploys a strategy named `my_strategy_name`.

```bash
qqq list
```

This command lists all deployed strategies.

```bash
qqq logs my_strategy_name
```

This command shows logs of the deployed strategy named `my_strategy_name`.

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


