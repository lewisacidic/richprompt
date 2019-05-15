from IPython.terminal.prompts import Prompts, Token
import datetime
import os


class RichPrompts(Prompts):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_path = self.curpath()

    def vi_token(self):
        if (
            getattr(self.shell.pt_app, "editing_mode", None) == "VI"
            and self.shell.prompt_includes_vi_mode
        ):

            mode = str(self.shell.pt_app.app.vi_state.input_mode)[3].upper()
            if mode == "I":
                token = Token.PromptInsertMode
            elif mode == "N":
                token = Token.PromptNormalMode
            else:
                token = Token.Prompt
            return (token, " [" + mode + "]")
        return ""

    @staticmethod
    def curpath():
        home = os.path.expanduser("~")
        curdir = os.getcwd()
        if curdir == home:
            return "~"
        elif home == os.path.commonpath([home, curdir]):
            return os.path.join("~", os.path.relpath(curdir, home))
        else:
            return curdir

    def path_tokens(self):
        curpath = self.curpath()
        if self.start_path != curpath:
            return [(Token.PromptPath, curpath)]
        else:
            return []

    @staticmethod
    def format_time(t):
        days, remainder = divmod(t, 60 * 60 * 24)
        hours, remainder = divmod(remainder, 60 * 60)
        minutes, remainder = divmod(remainder, 60)
        seconds, remainder = divmod(remainder, 1)
        ms = remainder * 1000
        ans = "{:.0f}ms".format(ms)
        if seconds:
            ans = "{:.0f}s ".format(seconds) + ans
        if minutes:
            ans = "{:.0f}m ".format(minutes) + ans
        if hours:
            ans = "{:.0f}h ".format(hours) + ans
        if days:
            ans = "{:.0f}d ".format(days) + ans
        return ans

    def execution_time_tokens(self):
        time_taken = self.shell.user_ns.get("time_taken")
        if time_taken and time_taken > self.minimum_time_delta:
            return [
                (Token.PromptNormal, "took "),
                (Token.PromptTime, self.format_time(time_taken)),
            ]
        else:
            return []

    def prompt_token(self):
        return (Token.Prompt, " >>> ")

    def first_line_tokens(self):
        tokens = [*self.path_tokens(), *self.execution_time_tokens()]
        if len(tokens):
            tokens += [(Token.Prompt, "\n")]
        return tokens

    def in_prompt_tokens(self):
        return [*self.first_line_tokens(), self.vi_token(), self.prompt_token()]
