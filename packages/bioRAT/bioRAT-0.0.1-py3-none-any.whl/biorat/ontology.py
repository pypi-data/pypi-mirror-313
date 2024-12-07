import pandas as pd
from owlready2 import ThingClass, get_ontology

__author__ = "Jayaram Kancherla"
__copyright__ = "Jayaram Kancherla"
__license__ = "MIT"

# originally published to gist
# https://gist.github.com/jkanche/1f010c38a090cefd8f2f5e21c20fc1b8


def owl_to_dataframe(owl_location: str):
    """Extract nodes and their lineages from ontologies as
    :py:class:`~pandas.DataFrame`.

    Example:

        .. code-block:: python

            from biorat.ontology import (
                owl_to_dataframe,
            )

            result_df = owl_to_dataframe(
                "https://github.com/obophenotype/cell-ontology/releases/download/v2024-09-26/cl.owl"
            )
            print(result_df)

    Args:
        owl_location:
            Location or the URL of the OWL file.

            Supports any argument acceepted by
            :py:func:`~owlready.get_ontology`.

    Returns:
        A Pandas DataFrame of the nodes, their labels and lineages.
    """
    onto = get_ontology(owl_location).load()

    recs = []

    # recursively traverse the ontology
    def get_lineage(cls):
        lineage = []
        for parent in cls.is_a:
            if isinstance(parent, ThingClass):
                lineage.append((parent.label.first() or parent.name, parent.name))
                lineage.extend(get_lineage(parent))
        return lineage

    # Iterate through all classes in the ontology
    for cls in onto.classes():
        rec = {}

        rec["iri"] = cls.iri
        rec["term_id"] = cls.name

        # Get the label (use the first label if available, otherwise the class name)
        rec["label"] = cls.label.first() or cls.name

        # Get the lineage
        lineage_items = get_lineage(cls)
        rec["lineage_ids"] = " > ".join(reversed([item[0] for item in lineage_items]))
        rec["lineage_labels"] = " > ".join(reversed([item[1] for item in lineage_items]))

        recs.append(rec)

    df = pd.DataFrame(recs)

    return df
