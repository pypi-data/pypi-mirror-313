from pathlib import Path
import logging

import fabric
import fabric.transfer

logger = logging.getLogger(__name__)


class RemoteHost:
    """
    Class representing some network location - can
    be used to put or get files to or from that location
    """

    def __init__(self, name) -> None:
        self.name = name
        self.cxn: None | fabric.Connection = None

    def upload(self, source: Path, target: Path):
        self._init_connect()

        assert self.cxn is not None
        self.cxn.run(f"mkdir -p {target.parent}")
        transfer = fabric.transfer.Transfer(self.cxn)
        transfer.put(str(source), str(target))
        self.cxn.close()

    def download(self, source: Path, target: Path):
        self._init_connect()

        assert self.cxn is not None

        transfer = fabric.transfer.Transfer(self.cxn)
        transfer.get(str(source), str(target))
        self.cxn.close()

    def can_connect(self) -> bool:
        self._init_connect()
        assert self.cxn is not None

        try:
            self.cxn.open()
        except Exception as e:
            logger.error(e)
            return False
        self.cxn.close()
        return True

    def _init_connect(self):
        if self.cxn is None:
            self.cxn = fabric.Connection(self.name)
