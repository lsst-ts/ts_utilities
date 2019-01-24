    def >NAME<(self, command: commands.>UPPER_NAME<Command):
        self.log.info(f"Executing command {command.name}.")
        self.processStateCommandResult(self.state.>NAME<(command, self.model))
