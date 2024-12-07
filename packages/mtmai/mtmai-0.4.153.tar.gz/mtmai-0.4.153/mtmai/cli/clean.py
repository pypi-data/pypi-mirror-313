def register_clean_commands(cli):
    @cli.command()
    def clean():
        """Run clean-up"""
        from mtmai.mtlibs import dev_helper

        dev_helper.run_clean()
