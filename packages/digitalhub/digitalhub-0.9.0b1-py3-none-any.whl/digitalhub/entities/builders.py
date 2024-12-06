from __future__ import annotations

from digitalhub.entities.artifact.artifact.builder import ArtifactArtifactBuilder
from digitalhub.entities.dataitem.dataitem.builder import DataitemDataitemBuilder
from digitalhub.entities.dataitem.table.builder import DataitemTableBuilder
from digitalhub.entities.model.mlflow.builder import ModelModelBuilder
from digitalhub.entities.project._base.builder import ProjectProjectBuilder
from digitalhub.entities.secret._base.builder import SecretSecretBuilder

entity_builders = (
    (ProjectProjectBuilder.ENTITY_KIND, ProjectProjectBuilder),
    (SecretSecretBuilder.ENTITY_KIND, SecretSecretBuilder),
    (ArtifactArtifactBuilder.ENTITY_KIND, ArtifactArtifactBuilder),
    (DataitemDataitemBuilder.ENTITY_KIND, DataitemDataitemBuilder),
    (DataitemTableBuilder.ENTITY_KIND, DataitemTableBuilder),
    (ModelModelBuilder.ENTITY_KIND, ModelModelBuilder),
)

##############################
#  Potential uninstalled entities
##############################


try:
    from digitalhub.entities.dataitem.iceberg.builder import DataitemIcebergBuilder

    entity_builders = (
        *entity_builders,
        (DataitemIcebergBuilder.ENTITY_KIND, DataitemIcebergBuilder),
    )
except ImportError:
    ...


try:
    from digitalhub.entities.model.model.builder import ModelMlflowBuilder

    entity_builders = (
        *entity_builders,
        (ModelMlflowBuilder.ENTITY_KIND, ModelMlflowBuilder),
    )
except ImportError:
    ...

try:
    from digitalhub.entities.model.sklearn.builder import ModelSklearnBuilder

    entity_builders = (
        *entity_builders,
        (ModelSklearnBuilder.ENTITY_KIND, ModelSklearnBuilder),
    )
except ImportError:
    ...

try:
    from digitalhub.entities.model.huggingface.builder import ModelHuggingfaceBuilder

    entity_builders = (
        *entity_builders,
        (ModelHuggingfaceBuilder.ENTITY_KIND, ModelHuggingfaceBuilder),
    )
except ImportError:
    ...
