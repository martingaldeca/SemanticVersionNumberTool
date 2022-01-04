import os

from IPython.terminal.prompts import Prompts, Token

env = os.environ


class BackendPrompt(Prompts):
    Token.Env = Token.Generic

    def in_prompt_tokens(self, cli=None):
        return [
            (Token.Env, f'{env.get("PROJECT_NAME", "NONE")}_backend_{env.get("ENVIRONMENT", "UNKNOWN")} ')
        ] + super().in_prompt_tokens()

    @staticmethod
    def get_style():
        environment_name = env.get('ENVIRONMENT', 'UNKNOWN')
        if environment_name == 'local':
            color = 'ansibrightgreen'
        elif environment_name == 'dev':
            color = 'ansibrightyellow'
        elif environment_name == 'pro':
            color = 'ansibrightred'
        else:
            color = 'ansibrightblue'

        return {Token.Env: f'bold {color}'}
