    def {name}(self, command : Commands.{upperName}Command):
        self.log.info("Executing command %s." % command.name)
        self.processStateCommandResult(self.state.{name}(command, self.model))
