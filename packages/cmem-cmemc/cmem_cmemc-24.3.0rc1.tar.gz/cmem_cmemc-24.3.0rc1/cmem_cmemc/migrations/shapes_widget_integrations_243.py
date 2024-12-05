"""Migration: Chart and Workflow Property Shapes to Widget Integration"""

from typing import ClassVar

from cmem_cmemc.migrations.abc import MigrationRecipe, components


class ChartsOnNodeShapesToToWidgetIntegrations(MigrationRecipe):
    """24.3 Migrate Chart on NodeShapes to Widget Integrations"""

    id = "charts-on-nshapes-24.3"
    description = "Migrate Charts on Node Shapes to Widget Integrations"
    component: components = "explore"
    first_version = "24.3"
    tags: ClassVar[list[str]] = ["shapes", "user"]
    check_query = """{{DEFAULT_PREFIXES}}
SELECT *
WHERE {
  GRAPH ?maybeOtherGraph {
    ?maybeOtherGraph a shui:ShapeCatalog .
    ?nodeShape a sh:NodeShape .
  }
  GRAPH ?shapeCatalog {
    ?shapeCatalog a shui:ShapeCatalog .
    ?nodeShape shui:provideChartVisualization ?shuiChart .
  }
}
    """
    move_query = """{{DEFAULT_PREFIXES}}
PREFIX  rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX  rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX shui: <https://vocab.eccenca.com/shui/>
PREFIX sh: <http://www.w3.org/ns/shacl#>

DELETE {
  GRAPH ?shapeCatalog {
    ?nodeShape shui:provideChartVisualization ?shuiChart .
  }
}
INSERT {
  GRAPH ?shapeCatalog {
    ?newWidgetIntegration a shui:WidgetIntegration ;
      shui:WidgetIntegration_widget ?shuiChart ;
      rdfs:label ?name ;
      rdfs:comment ?description ;
      sh:order -1000 .
    ?nodeShape shui:WidgetIntegration_integrate ?newWidgetIntegration .
  }
}
WHERE {
  GRAPH ?maybeOtherGraph {
    ?maybeOtherGraph a shui:ShapeCatalog .
    ?nodeShape a sh:NodeShape .
  }
  GRAPH ?shapeCatalog {
    ?shapeCatalog a shui:ShapeCatalog .
    ?nodeShape shui:provideChartVisualization ?shuiChart .
  }
  OPTIONAL { ?shuiChart rdfs:label ?name }
  OPTIONAL { ?shuiChart rdfs:comment ?description }
  BIND (IRI(CONCAT(STR(?shuiChart), "_WidgetIntegration")) as ?newWidgetIntegration)
}
    """

    def is_applicable(self) -> bool:
        """Test if the recipe can be applied."""
        node_shapes_with_charts = self._select(self.check_query)
        return len(node_shapes_with_charts) > 0

    def apply(self) -> None:
        """Apply the recipe to the current version."""
        self._update(self.move_query)


class ChartsOnPropertyShapesToWidgetIntegrations(MigrationRecipe):
    """24.3 Migrate Chart Property Shapes to Widget Integrations"""

    id = "charts-on-pshapes-24.3"
    description = "Migrate Charts on Property Shapes to Widget Integrations"
    component: components = "explore"
    first_version = "24.3"
    tags: ClassVar[list[str]] = ["shapes", "user"]
    check_query = """{{DEFAULT_PREFIXES}}
SELECT *
WHERE {
  GRAPH ?shapeCatalog {
    ?shapeCatalog a shui:ShapeCatalog .
    ?propertyShape a sh:PropertyShape ;
      shui:provideChartVisualization ?shuiChart .
  }
}
    """
    move_query = """{{DEFAULT_PREFIXES}}
DELETE {
  GRAPH ?shapeCatalog {
    ?propertyShape ?p ?o .
    ?nodeShape sh:property ?propertyShape .
  }
}
INSERT {
  GRAPH ?shapeCatalog {
    ?propertyShape a shui:WidgetIntegration ;
      shui:WidgetIntegration_widget ?shuiChart ;
      rdfs:label ?name ;
      rdfs:comment ?description ;
      sh:order ?order ;
      shui:WidgetIntegration_group ?group .
    ?nodeShape shui:WidgetIntegration_integrate ?propertyShape .
  }
}
WHERE {
  GRAPH ?shapeCatalog {
    ?shapeCatalog a shui:ShapeCatalog .
    ?propertyShape a sh:PropertyShape ;
      shui:provideChartVisualization ?shuiChart .
    ?propertyShape ?p ?o .
    OPTIONAL {?propertyShape sh:name ?name }
    OPTIONAL {?propertyShape sh:description ?description }
    OPTIONAL {?propertyShape sh:order ?order }
    OPTIONAL {?propertyShape sh:group ?group }
    OPTIONAL {?nodeShape sh:property ?propertyShape }
  }
}
    """

    def is_applicable(self) -> bool:
        """Test if the recipe can be applied."""
        chart_property_shapes = self._select(self.check_query)
        return len(chart_property_shapes) > 0

    def apply(self) -> None:
        """Apply the recipe to the current version."""
        self._update(self.move_query)


class WorkflowTriggerPropertyShapesToWidgetIntegrations(MigrationRecipe):
    """24.3 Migrate Workflow Trigger Property Shapes to Widget Integrations"""

    id = "trigger-on-pshapes-24.3"
    description = "Migrate Workflow Trigger on Property Shapes to Widget Integrations"
    component: components = "explore"
    first_version = "24.3"
    tags: ClassVar[list[str]] = ["shapes", "user"]
    check_query = """{{DEFAULT_PREFIXES}}
SELECT *
WHERE {
  GRAPH ?shapeCatalog {
    ?shapeCatalog a shui:ShapeCatalog .
    ?propertyShape a sh:PropertyShape ;
      shui:provideWorkflowTrigger ?shuiChart .
  }
}
    """
    move_query = """{{DEFAULT_PREFIXES}}
DELETE {
  GRAPH ?shapeCatalog {
    ?propertyShape ?p ?o .
    ?nodeShape sh:property ?propertyShape .
  }
}
INSERT {
  GRAPH ?shapeCatalog {
    ?propertyShape a shui:WidgetIntegration ;
      shui:WidgetIntegration_widget ?workflowTrigger ;
      rdfs:label ?name ;
      rdfs:comment ?description ;
      sh:order ?order ;
      shui:WidgetIntegration_group ?group .
    ?nodeShape shui:WidgetIntegration_integrate ?propertyShape .
  }
}
WHERE {
  GRAPH ?shapeCatalog {
    ?shapeCatalog a shui:ShapeCatalog .
    ?propertyShape a sh:PropertyShape ;
      shui:provideWorkflowTrigger ?workflowTrigger .
    ?propertyShape ?p ?o .
    OPTIONAL {?propertyShape sh:name ?name }
    OPTIONAL {?propertyShape sh:description ?description }
    OPTIONAL {?propertyShape sh:order ?order }
    OPTIONAL {?propertyShape sh:group ?group }
    OPTIONAL {?nodeShape sh:property ?propertyShape }
  }
}
    """

    def is_applicable(self) -> bool:
        """Test if the recipe can be applied."""
        chart_property_shapes = self._select(self.check_query)
        return len(chart_property_shapes) > 0

    def apply(self) -> None:
        """Apply the recipe to the current version."""
        self._update(self.move_query)
