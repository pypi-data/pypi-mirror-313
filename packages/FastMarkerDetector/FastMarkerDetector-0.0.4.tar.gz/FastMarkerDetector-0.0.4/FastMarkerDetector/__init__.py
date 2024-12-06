# 从 FastMarkerDetector 模块中导入所需函数
from .FastMarkerDetector import (
    Compare_A_B_variables_of_each_gene_in_each_cluster_v3,
    avg_jcd_score,
    dotplot,
    finder_marker
)
# 定义 __all__ 来控制导出的 API
__all__ = [
    Compare_A_B_variables_of_each_gene_in_each_cluster_v3,
    avg_jcd_score,
    dotplot,
    finder_marker
]