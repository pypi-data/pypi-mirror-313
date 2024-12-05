from pathlib import Path
import logging

from shiny import App, ui, reactive, Inputs, Outputs, Session

from dp_wizard.utils.argparse_helpers import get_cli_info, CLIInfo
from dp_wizard.app import analysis_panel, dataset_panel, results_panel, feedback_panel


logging.basicConfig(level=logging.INFO)

app_ui = ui.page_bootstrap(
    ui.head_content(ui.include_css(Path(__file__).parent / "css" / "styles.css")),
    ui.navset_tab(
        dataset_panel.dataset_ui(),
        analysis_panel.analysis_ui(),
        results_panel.results_ui(),
        feedback_panel.feedback_ui(),
        id="top_level_nav",
    ),
    title="DP Wizard",
)


def ctrl_c_reminder():  # pragma: no cover
    print("Session ended (Press CTRL+C to quit)")


def make_server_from_cli_info(cli_info: CLIInfo):
    def server(input: Inputs, output: Outputs, session: Session):  # pragma: no cover
        cli_csv_path = cli_info.csv_path
        csv_path = reactive.value("" if cli_csv_path is None else cli_csv_path)
        contributions = reactive.value(cli_info.contributions)

        lower_bounds = reactive.value({})
        upper_bounds = reactive.value({})
        bin_counts = reactive.value({})
        weights = reactive.value({})
        epsilon = reactive.value(1.0)

        dataset_panel.dataset_server(
            input,
            output,
            session,
            is_demo=cli_info.is_demo,
            csv_path=csv_path,
            contributions=contributions,
        )
        analysis_panel.analysis_server(
            input,
            output,
            session,
            is_demo=cli_info.is_demo,
            csv_path=csv_path,
            contributions=contributions,
            lower_bounds=lower_bounds,
            upper_bounds=upper_bounds,
            bin_counts=bin_counts,
            weights=weights,
            epsilon=epsilon,
        )
        results_panel.results_server(
            input,
            output,
            session,
            csv_path=csv_path,
            contributions=contributions,
            lower_bounds=lower_bounds,
            upper_bounds=upper_bounds,
            bin_counts=bin_counts,
            weights=weights,
            epsilon=epsilon,
        )
        feedback_panel.feedback_server(
            input,
            output,
            session,
        )
        session.on_ended(ctrl_c_reminder)

    return server


app = App(app_ui, make_server_from_cli_info(get_cli_info()))
