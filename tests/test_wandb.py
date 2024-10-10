import wandb


def init_run():
    wandb.init(id="my_id3", config={"key1": "value1"})
    wandb.log({"loss": 1})
    print(wandb.config)
    wandb.finish()


def resume_run():
    wandb.init(id="my_id3", resume=True, config={"key2": "value2"})
    wandb.log({"loss": 2})
    print(wandb.config)
    wandb.finish()


if __name__ == "__main__":
    # init_run()
    # resume_run()
    run = wandb.Api().run("expy-tests/my_id3")
    config = run.config
    print(config)
