class WandbDummyRun:
    def __getattr__(self, _):
        return self

    def __call__(self, *args, **kwargs):
        return self

    def __getitem__(self, _):
        return self

    def __setitem__(self, _, __):
        pass
