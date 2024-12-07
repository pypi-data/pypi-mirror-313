from yaspin import yaspin
from yaspin.spinners import Spinners


class Spinner:
    def __init__(
        self, start_text="", success_text=None, fail_text=None, disappearing=False
    ):
        self.success_text = success_text or start_text
        self.fail_text = fail_text or start_text
        self.disappearing = disappearing
        self.spinner = yaspin(
            Spinners.binary,
            text=start_text,
            color="green",
        )

    def __enter__(self):
        self.spinner.start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.spinner.text = self.fail_text
            self.spinner.fail("❌")
        elif self.disappearing:
            self.spinner.text = ""
            self.spinner.stop()
        else:
            self.spinner.text = self.success_text
            self.spinner.ok("✅")

        self.spinner.stop()


class DisappearingSpinner(Spinner):
    def __init__(self, start_text="", success_text=None, fail_text=None):
        super().__init__(start_text, success_text, fail_text, disappearing=True)


class ComputingSpinner(DisappearingSpinner):
    def __init__(self):
        super().__init__("Gibson is computing...")
