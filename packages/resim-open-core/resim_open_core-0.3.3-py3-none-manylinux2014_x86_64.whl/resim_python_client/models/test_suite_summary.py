from typing import Any, Dict, Type, TypeVar, Tuple, Optional, BinaryIO, TextIO, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Dict
from typing import cast, List
from typing import cast

if TYPE_CHECKING:
  from ..models.test_suite_batch_summary_job_results import TestSuiteBatchSummaryJobResults
  from ..models.test_suite_summary_summary import TestSuiteSummarySummary





T = TypeVar("T", bound="TestSuiteSummary")


@_attrs_define
class TestSuiteSummary:
    """ 
        Attributes:
            batches (List['TestSuiteBatchSummaryJobResults']):
            branch_id (str):
            name (str):
            project_id (str):
            report_id (str):
            summary (TestSuiteSummarySummary):
            system_id (str):
            test_suite_id (str):
            test_suite_revision (int):
     """

    batches: List['TestSuiteBatchSummaryJobResults']
    branch_id: str
    name: str
    project_id: str
    report_id: str
    summary: 'TestSuiteSummarySummary'
    system_id: str
    test_suite_id: str
    test_suite_revision: int
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        from ..models.test_suite_batch_summary_job_results import TestSuiteBatchSummaryJobResults
        from ..models.test_suite_summary_summary import TestSuiteSummarySummary
        batches = []
        for batches_item_data in self.batches:
            batches_item = batches_item_data.to_dict()
            batches.append(batches_item)



        branch_id = self.branch_id

        name = self.name

        project_id = self.project_id

        report_id = self.report_id

        summary = self.summary.to_dict()

        system_id = self.system_id

        test_suite_id = self.test_suite_id

        test_suite_revision = self.test_suite_revision


        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "batches": batches,
            "branchID": branch_id,
            "name": name,
            "projectID": project_id,
            "reportID": report_id,
            "summary": summary,
            "systemID": system_id,
            "testSuiteID": test_suite_id,
            "testSuiteRevision": test_suite_revision,
        })

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.test_suite_batch_summary_job_results import TestSuiteBatchSummaryJobResults
        from ..models.test_suite_summary_summary import TestSuiteSummarySummary
        d = src_dict.copy()
        batches = []
        _batches = d.pop("batches")
        for batches_item_data in (_batches):
            batches_item = TestSuiteBatchSummaryJobResults.from_dict(batches_item_data)



            batches.append(batches_item)


        branch_id = d.pop("branchID")

        name = d.pop("name")

        project_id = d.pop("projectID")

        report_id = d.pop("reportID")

        summary = TestSuiteSummarySummary.from_dict(d.pop("summary"))




        system_id = d.pop("systemID")

        test_suite_id = d.pop("testSuiteID")

        test_suite_revision = d.pop("testSuiteRevision")

        test_suite_summary = cls(
            batches=batches,
            branch_id=branch_id,
            name=name,
            project_id=project_id,
            report_id=report_id,
            summary=summary,
            system_id=system_id,
            test_suite_id=test_suite_id,
            test_suite_revision=test_suite_revision,
        )


        test_suite_summary.additional_properties = d
        return test_suite_summary

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
