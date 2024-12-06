#
#  MAKINAROCKS CONFIDENTIAL
#  ________________________
#
#  [2017] - [2024] MakinaRocks Co., Ltd.
#  All Rights Reserved.
#
#  NOTICE:  All information contained herein is, and remains
#  the property of MakinaRocks Co., Ltd. and its suppliers, if any.
#  The intellectual and technical concepts contained herein are
#  proprietary to MakinaRocks Co., Ltd. and its suppliers and may be
#  covered by U.S. and Foreign Patents, patents in process, and
#  are protected by trade secret or copyright law. Dissemination
#  of this information or reproduction of this material is
#  strictly forbidden unless prior written permission is obtained
#  from MakinaRocks Co., Ltd.
from runway.common.enum_ import StrEnum, auto


class DatasetFileType(StrEnum):
    """Dataset File Type."""

    # Supported by `save_dataset`
    csv = auto()
    parquet = auto()
    npy = auto()
    pickle = auto()

    # Not supported by `save_dataset`
    tsv = auto()
    excel = auto()
