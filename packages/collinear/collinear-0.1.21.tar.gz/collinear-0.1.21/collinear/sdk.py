from collinear.dataset import Dataset
from collinear.inference import Inference
from collinear.judge import Judge
from collinear.model import Model


class Collinear:
    def __init__(self, access_token: str,space_id:str) -> None:
        self.access_token = access_token
        self.space_id = space_id
        self._judge = None
        self._inference = None
        self._dataset = None
        self._model = None

    @property
    def judge(self):
        """
        Lazy-load Veritas service when accessed for the first time.
        Cache the result for subsequent accesses.
        """
        if self._judge is None:
            self._judge = Judge(self.access_token,self.space_id)
        return self._judge

    @property
    def model(self):
        """
        Lazy-load Inference service when accessed for the first time.
        Cache the result for subsequent accesses.
        """
        if self._model is None:
            self._model = Model(self.access_token,self.space_id)
        return self._model

    @property
    def inference(self):
        """
        Lazy-load Inference service when accessed for the first time.
        Cache the result for subsequent accesses.
        """
        if self._inference is None:
            self._inference = Inference(self.access_token,self.space_id, self.model)
        return self._inference

    @property
    def dataset(self):
        """
        Lazy-load Inference service when accessed for the first time.
        Cache the result for subsequent accesses.
        """
        if self._dataset is None:
            self._dataset = Dataset(self.access_token,self.space_id)
        return self._dataset
