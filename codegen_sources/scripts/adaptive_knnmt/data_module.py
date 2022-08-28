from pytorch_lightning import LightningDataModule
from torch.utils.data import DataLoader

from codegen_sources.model.translate import Translator
from codegen_sources.scripts.knnmt.knnmt import KNNMT
from codegen_sources.scripts.knnmt.load_functions import load_parallel_functions

from .dataset import Dataset


class DataModule(LightningDataModule):
    def __init__(
        self, 
        batch_size: int, 
        samples: int, 
        dataset_dir: str, 
        datastore_dir: str, 
        model_dir: str,
        cache_dir: str,
        bpe_path: str, 
        language_pair: str,
    ):
        super().__init__()
        self.batch_size = batch_size
        self.samples = samples
        self.dataset_dir = dataset_dir
        self.datastore_dir = datastore_dir
        self.model_dir = model_dir
        self.cache_dir = cache_dir
        self.bpe_path = bpe_path
        self.language_pair = language_pair

    def setup(self, stage: str) -> None:
        knnmt = KNNMT()

        src_language = self.language_pair.split("_")[0]
        tgt_language = self.language_pair.split("_")[1]

        translator_path = f"{self.model_dir}/Online_ST_{src_language.title()}_{tgt_language.title()}.pth"
        translator_path = translator_path.replace("Cpp", "CPP")
        translator = Translator(translator_path, self.bpe_path, global_model=True)

        parallel_functions = load_parallel_functions(self.language_pair)

        self.train_dataset = Dataset(
            batch_size=self.batch_size,
            parallel_functions=parallel_functions, 
            cache_dir=self.cache_dir,
            knnmt=knnmt, 
            translator=translator, 
            language_pair=self.language_pair, 
            phase="train", 
            samples=self.samples
        )

        self.val_dataset = Dataset(
            batch_size=self.batch_size,
            parallel_functions=parallel_functions, 
            cache_dir=self.cache_dir,
            knnmt=knnmt, 
            translator=translator, 
            language_pair=self.language_pair, 
            phase="val", 
            samples=int(0.1 * self.samples)
        )

        self.test_dataset = Dataset(
            batch_size=self.batch_size,
            parallel_functions=parallel_functions,
            cache_dir=self.cache_dir,
            knnmt=knnmt, 
            translator=translator, 
            language_pair=self.language_pair, 
            phase="test", 
            samples=int(0.1 * self.samples)
        )

    def train_dataloader(self) -> DataLoader:
        return DataLoader(self.train_dataset, batch_size=self.batch_size, shuffle=True, num_workers=4)

    def val_dataloader(self) -> DataLoader:
        return DataLoader(self.val_dataset, batch_size=self.batch_size, shuffle=False, num_workers=4)

    def test_dataloader(self) -> DataLoader:
        return DataLoader(self.test_dataset, batch_size=self.batch_size, shuffle=False, num_workers=4)