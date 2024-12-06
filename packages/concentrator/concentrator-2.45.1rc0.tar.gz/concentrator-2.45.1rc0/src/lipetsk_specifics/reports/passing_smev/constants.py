# coding: utf-8

from lipetsk_specifics.models import ReportType

from . import report


builder_report_types = {
    ReportType.FIRST: report.FirstTypePassingSmevReporter,
    ReportType.SECOND: report.SecondTypePassingSmevReporter,
    ReportType.THIRD: report.ThirdTypePassingSmevReporter,
    ReportType.FOURTH: report.FourthTypePassingSmevReporter
}
