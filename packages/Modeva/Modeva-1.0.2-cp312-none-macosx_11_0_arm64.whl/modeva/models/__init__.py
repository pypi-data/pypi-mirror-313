# used to solve the failure of mac M1 gpu
import os
os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = str(1)

from .wrappers.builtin.linear_model import MoElasticNet, MoLogisticRegression
from .wrappers.builtin.decision_tree import MoDecisionTreeRegressor, MoDecisionTreeClassifier
from .wrappers.builtin.gradientboosting import MoGradientBoostingRegressor, MoGradientBoostingClassifier
from .wrappers.builtin.randomforest import MoRandomForestRegressor, MoRandomForestClassifier
from .wrappers.builtin.lightgbm import MoLGBMClassifier, MoLGBMRegressor
from .wrappers.builtin.catboost import MoCatBoostRegressor, MoCatBoostClassifier
from .wrappers.builtin.xgboost import MoXGBRegressor, MoXGBClassifier

from .reludnn.api import MoReLUDNNRegressor, MoReLUDNNClassifier
from .gaminet.api import MoGAMINetRegressor, MoGAMINetClassifier
from .glmtree.glmtree import MoGLMTreeRegressor, MoGLMTreeClassifier
from .glmtree.glmtreeboost import MoGLMTreeBoostRegressor, MoGLMTreeBoostClassifier
from .glmtree.neural_tree import MoNeuralTreeRegressor, MoNeuralTreeClassifier
from .moe.api import MoMoERegressor, MoMoEClassifier

from .wrappers.arbitrary import MoRegressor, MoClassifier
from .wrappers.sklearn import MoSKLearnRegressor, MoSKLearnClassifier
from .wrappers.scored import MoScoredRegressor, MoScoredClassifier

from .tune import ModelTunePSO, ModelTuneOptuna, ModelTuneGridSearch, ModelTuneRandomSearch


__all__ = ["MoElasticNet", "MoLogisticRegression",
           "MoDecisionTreeRegressor", "MoDecisionTreeClassifier",
           "MoGradientBoostingRegressor", "MoGradientBoostingClassifier",
           "MoRandomForestRegressor", "MoRandomForestClassifier",
           "MoXGBRegressor", "MoXGBClassifier",
           "MoLGBMRegressor", "MoLGBMClassifier",
           "MoCatBoostRegressor", "MoCatBoostClassifier",
           "MoGAMINetRegressor", "MoGAMINetClassifier",
           "MoReLUDNNRegressor", "MoReLUDNNClassifier",
           "MoGLMTreeRegressor", "MoGLMTreeClassifier",
           "MoGLMTreeBoostRegressor", "MoGLMTreeBoostClassifier",
           "MoNeuralTreeRegressor", "MoNeuralTreeClassifier",
           "MoMoERegressor", "MoMoEClassifier",
           "MoRegressor", "MoClassifier",
           "MoSKLearnRegressor", "MoSKLearnClassifier",
           "MoScoredRegressor", "MoScoredClassifier",
           "ModelTunePSO", "ModelTuneOptuna", "ModelTuneGridSearch", "ModelTuneRandomSearch"]
