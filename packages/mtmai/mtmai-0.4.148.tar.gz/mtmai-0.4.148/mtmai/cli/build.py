def register_build_commands(cli):
    @cli.group()
    def build():
        """Build related commands"""
        pass

    @build.command()
    def docker_base():
        """Build Docker base image"""
        # CliBuild().run("docker_base")
        print("build docker_base")

    @build.command()
    def frontend():
        """Build frontend assets"""
        print("build frontend")
