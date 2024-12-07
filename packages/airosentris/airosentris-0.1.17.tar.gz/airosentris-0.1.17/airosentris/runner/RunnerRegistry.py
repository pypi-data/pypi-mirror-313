class RunnerRegistry:
    _runners = {}

    @classmethod
    def register_runner(cls, key, runner_class):
        """Register a runner with a specific key."""
        normalized_key = key.lower()
        cls._runners[normalized_key] = runner_class

    @classmethod
    def get_runner(cls, key):
        """Retrieve a runner by its key."""
        normalized_key = key.lower()
        runner_class = cls._runners.get(normalized_key)
        if not runner_class:
            print(f"Available runners: {cls._runners.keys()}")
            raise ValueError(f"No runner registered with key: {key}")
        print(f"Runner retrieved with key: {normalized_key}")
        return runner_class

    @classmethod
    def get_all_runners(cls):
        """Return a list of all registered runners."""
        return list(cls._runners.keys())
