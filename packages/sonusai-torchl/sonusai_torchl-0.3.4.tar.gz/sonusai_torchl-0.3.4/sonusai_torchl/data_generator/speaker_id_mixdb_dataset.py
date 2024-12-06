import contextlib
import random
from itertools import cycle

from sonusai.mixture.datatypes import Feature
from sonusai.mixture.datatypes import GeneralizedIDs
from sonusai.mixture.datatypes import TruthDict
from sonusai.mixture.mixdb import MixtureDatabase
from torch.utils.data import Dataset
from torch.utils.data import Sampler

from .dataloader_utils import AawareDataLoader


class MixIDPerSpeaker:
    def __init__(self, random_utterance: bool) -> None:
        self._random_utterance = random_utterance
        self._data: list[cycle] = []

    def append(self, mixids: list[int]) -> None:
        if self._random_utterance:
            self._data.append(cycle(random.sample(mixids, k=len(mixids))))
        else:
            self._data.append(cycle(mixids))

    def next(self, speaker_id: int) -> int:
        return next(self._data[speaker_id])


class MixtureDatabaseDataset(Dataset):
    """Generates a PyTorch dataset ordered by speaker ID and utterances from a SonusAI mixture database"""

    def __init__(
        self,
        mixdb: MixtureDatabase,
        mixids: GeneralizedIDs,
        speakers: int,
        utterances: int,
        cut_len: int,
        random_cut: bool = True,
        random_utterance: bool = False,
    ):
        """Initialization"""
        from copy import deepcopy
        from itertools import cycle

        self.mixdb = mixdb
        self.mixids = self.mixdb.mixids_to_list(mixids)
        self.cut_len = cut_len
        self.random_cut = random_cut
        self.dataset_ids: list[int] = []

        # Get a list of IDs per speaker
        mixid_per_speaker = MixIDPerSpeaker(random_utterance)
        speaker_ids = mixdb.speech_metadata("speaker_id")
        for speaker_id in speaker_ids:
            data = mixdb.mixids_for_speech_metadata("speaker_id", speaker_id)
            mixid_per_speaker.append(data)
        speaker_indices = cycle(range(len(speaker_ids)))

        # Loop over speakers picking utterances per iteration
        # M utterances of Speaker0, M utterances of Speaker1, ...
        # Keep looping until all mixids have been used
        # This results in a new set of dataset indices that map into the original mixdb mixids
        unused_mixids = deepcopy(self.mixids)
        while unused_mixids:
            for _ in range(speakers):
                speaker = next(speaker_indices)
                for _ in range(utterances):
                    mixid = mixid_per_speaker.next(speaker)
                    self.dataset_ids.append(mixid)
                    with contextlib.suppress(ValueError):
                        unused_mixids.remove(mixid)

    def __len__(self):
        return len(self.dataset_ids)

    def __getitem__(self, idx: int) -> tuple[Feature, TruthDict, int]:
        """Get data from one mixture"""
        import random

        import numpy as np

        mixid = self.mixids[self.dataset_ids[idx]]
        feature, truth = self.mixdb.mixture_ft(mixid)

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

        return feature, truth, mixid


def TorchFromSpeakerIDMixtureDatabase(
    mixdb: MixtureDatabase,
    mixids: GeneralizedIDs,
    speakers: int,
    utterances: int,
    num_workers: int = 0,
    cut_len: int = 0,
    drop_last: bool = False,
    shuffle: bool = False,
    random_cut: bool = True,
    random_utterance: bool = False,
    sampler: type[Sampler] | None = None,
    pin_memory: bool = False,
) -> AawareDataLoader:
    """Generates a PyTorch dataloader from a SonusAI mixture database"""
    from .dataloader_utils import collate_fn

    dataset = MixtureDatabaseDataset(
        mixdb=mixdb,
        mixids=mixids,
        speakers=speakers,
        utterances=utterances,
        cut_len=cut_len,
        random_cut=random_cut,
        random_utterance=random_utterance,
    )

    if sampler is not None:
        my_sampler = sampler(dataset)
    else:
        my_sampler = None

    batch_size = speakers * utterances

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
