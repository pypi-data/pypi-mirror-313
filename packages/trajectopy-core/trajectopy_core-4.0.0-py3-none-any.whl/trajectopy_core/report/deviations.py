"""
Trajectopy - Trajectory Evaluation in Python

Gereon Tombrink, 2024
mail@gtombrink.de
"""

import logging
from typing import Union


from trajectopy_core.evaluation.ate_result import ATEResult
from trajectopy_core.evaluation.rpe_result import RPEResult
from trajectopy_core.report.multi import render_multi_report
from trajectopy_core.report.single import render_single_report
from trajectopy_core.settings.report import ReportSettings


logger = logging.getLogger("root")


def create_deviation_report(
    ate_result: Union[ATEResult, list[ATEResult]],
    rpe_result: Union[RPEResult, list[RPEResult], None],
    report_settings: ReportSettings = ReportSettings(),
):
    """
    Create a deviation report.

    Args:
        ate_result (Union[ATEResult, list[ATEResult]]): The absolute trajectory error results
        rpe_result (Union[RPEResult, list[RPEResult]]): The relative pose error results
        report_settings (ReportSettings): The report settings

    Returns:
        str: The deviation report
    """
    if (ate_result is not None and isinstance(ate_result, list)) or (
        rpe_result is not None and isinstance(rpe_result, list)
    ):
        return render_multi_report(ate_results=ate_result, rpe_results=rpe_result, report_settings=report_settings)

    return render_single_report(ate_result=ate_result, rpe_result=rpe_result, report_settings=report_settings)
