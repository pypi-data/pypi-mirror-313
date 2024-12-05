from __future__ import annotations

from typing import Optional, Dict, Any


class ElnEntryPosition:
    """
    Describes the position of an entry to be added to the Experiment.
    """
    tab_id: Optional[int]
    order: Optional[int]
    column_span: Optional[int]
    column_order: Optional[int]

    def __init__(self, tab_id: Optional[int], order: Optional[int],
                 column_span: Optional[int] = None, column_order: Optional[int] = None):
        self.tab_id = tab_id
        self.order = order
        self.column_span = column_span
        self.column_order = column_order

    def to_json(self) -> Dict[str, Any]:
        return {
            'notebookExperimentTabId': self.tab_id,
            'order': self.order,
            'columnSpan': self.column_span,
            'columnOrder': self.column_order
        }

    @staticmethod
    def from_json(json_dct: Dict[str, Any]) -> ElnEntryPosition:
        tab_id: Optional[int] = json_dct.get('notebookExperimentTabId')
        order: Optional[int] = json_dct.get('order')
        column_span: Optional[int] = json_dct.get('columnSpan')
        column_order: Optional[int] = json_dct.get('columnOrder')
        return ElnEntryPosition(tab_id, order,
                                column_span=column_span, column_order=column_order)


ExperimentEntryPosition = ElnEntryPosition

