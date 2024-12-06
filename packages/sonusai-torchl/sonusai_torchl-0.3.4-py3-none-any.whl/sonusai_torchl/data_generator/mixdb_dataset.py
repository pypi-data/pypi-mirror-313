from sonusai.mixture.datatypes import Feature
from sonusai.mixture.datatypes import GeneralizedIDs
from sonusai.mixture.datatypes import TruthDict
from sonusai.mixture.mixdb import MixtureDatabase
from torch.utils.data import Dataset
from torch.utils.data import Sampler

from .dataloader_utils import AawareDataLoader


class MixtureDatabaseDataset(Dataset):
    """Generates a PyTorch dataset from a SonusAI mixture database"""

    def __init__(self, mixdb: MixtureDatabase, mixids: GeneralizedIDs, cut_len: int, random_cut: bool = True):
        """Initialization"""
        self.mixdb = mixdb
        self.mixids = self.mixdb.mixids_to_list(mixids)
        self.cut_len = cut_len
        self.random_cut = random_cut

    def __len__(self):
        return len(self.mixids)

    def __getitem__(self, idx: int) -> tuple[Feature, TruthDict, int]:
        """Get data from one mixture"""
        import random

        import numpy as np

        feature, truth = self.mixdb.mixture_ft(self.mixids[idx])

        length = feature.shape[0]

        if self.cut_len > 0:
            if length < self.cut_len:
                reps = int(np.ceil(self.cut_len / length))

                feature = np.tile(feature, (reps, 1, 1))
                feature = feature[: self.cut_len]
                for key in truth:
                    truth[key] = np.tile(truth[key], (reps, 1, 1))
                    truth[key] = truth[key][: self.cut_len]
            else:
                if self.random_cut:
                    start = random.randint(0, length - self.cut_len)  # noqa: S311
                else:
                    start = 0

                feature = feature[start : start + self.cut_len]
                for key in truth:
                    truth[key] = truth[key][start : start + self.cut_len]

        return feature, truth, idx


def TorchFromMixtureDatabase(
    mixdb: MixtureDatabase,
    mixids: GeneralizedIDs,
    batch_size: int,
    num_workers: int = 0,
    cut_len: int = 0,
    drop_last: bool = False,
    shuffle: bool = False,
    random_cut: bool = True,
    sampler: type[Sampler] | None = None,
    pin_memory: bool = False,
) -> AawareDataLoader:
    """Generates a PyTorch dataloader from a SonusAI mixture database"""
    from .dataloader_utils import collate_fn

    dataset = MixtureDatabaseDataset(
        mixdb=mixdb,
        mixids=mixids,
        cut_len=cut_len,
        random_cut=random_cut,
    )

    if sampler is not None:
        my_sampler = sampler(dataset)
    else:
        my_sampler = None

    if cut_len == 0 and batch_size > 1:
        result = AawareDataLoader(
            dataset=dataset,
            batch_size=batch_size,
            pin_memory=pin_memory,
            shuffle=shuffle,
            sampler=my_sampler,
            drop_last=drop_last,
            num_workers=num_workers,
            collate_fn=collate_fn,
        )
    else:
        result = AawareDataLoader(
            dataset=dataset,
            batch_size=batch_size,
            pin_memory=pin_memory,
            shuffle=shuffle,
            sampler=my_sampler,
            drop_last=drop_last,
            num_workers=num_workers,
        )

    result.cut_len = cut_len

    return result
