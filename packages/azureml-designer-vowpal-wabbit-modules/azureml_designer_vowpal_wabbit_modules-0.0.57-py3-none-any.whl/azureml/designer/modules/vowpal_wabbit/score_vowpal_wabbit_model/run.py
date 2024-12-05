from azureml.designer.modules.vowpal_wabbit.score_vowpal_wabbit_model.score_vowpal_wabbit_model import \
    ScoreVowpalWabbitModelModule
from azureml.designer.modules.vowpal_wabbit.common.entry_utils import build_cli_args
from azureml.studio.internal.error_handler import error_handler


@error_handler
def main():
    kwargs = build_cli_args(ScoreVowpalWabbitModelModule().run)
    ScoreVowpalWabbitModelModule().run(**kwargs)


if __name__ == "__main__":
    main()
