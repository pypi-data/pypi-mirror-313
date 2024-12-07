import xm_slurm


def main():
    if wu := xm_slurm.get_current_work_unit():
        wu.context.artifacts.add(xm_slurm.Artifact(name="wandb", uri="//wandb.ai"))


if __name__ == "__main__":
    main()
