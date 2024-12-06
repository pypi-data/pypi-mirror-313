import gzip
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from json import load
from pathlib import Path

import polars as pl
from anndata import AnnData
from scipy.sparse import csr_matrix


def find_file(root: Path, base_name: str):
    for ext in ['', '.csv.gz', '.tsv.gz', '.tsv', '.csv', '.gz']:
        if (p := root / f'{base_name}{ext}').exists():
            return p
    return None

@dataclass
class FileHeader:
    comment_lines: list[str]
    header_line: str
    separator: str

    @property
    def headers(self):
        return self.header_line.split(self.separator)


def parse_file_header(file_path: Path):
    if file_path.suffix == '.gz':
        f = gzip.open(file_path, 'rt')
    else:
        f = open(file_path, 'r')

    comment_lines = []
    first_line = None
    for line in f:
        if line.startswith('%'):
            comment_lines.append(line.strip('%'))
        else:
            first_line = line
            break
    if first_line is None:
        raise ValueError(f"No data line found in {file_path}")
    for sep in ['\t', ',', ' ']:
        if sep in first_line:
            break
    else:
        sep = '\t'

    return FileHeader(
        comment_lines = comment_lines,
        header_line   = first_line,
        separator     = sep,
    )

def read_sample_dir(root: Path, verbose=False):
    '''从样本目录中读取'''
    base_names = {
        'matrix'  : ('matrix.mtx', ),
        'barcodes': ('barcodes', ),
        'features': ('features', 'genes'),
    }
    read_config = {
        'matrix': {
            'new_columns': ['gene_index', 'cell_index', 'count'],
        },
        'barcodes': {
            'new_columns': ['cell_barcode'],
        },
        'features': {
            'new_columns': ['gene_name', 'gene_name_2'],
        },
    }

    files = {
        t: [find_file(root, base_name) for base_name in curr_base_names][0]
        for t, curr_base_names in base_names.items()
    }
    if verbose:
        print('Found files:', files)
    for base_name, file_path in files.items():
        if file_path is None:
            raise FileNotFoundError(f"No `{base_name}` file found in `{root}`")

    data = {
        'matrix'  : None,
        'barcodes': None,
        'features': None,
    }
    for base_name, file_path in files.items():
        header = parse_file_header(file_path)
        new_columns = read_config[base_name]['new_columns'][:len(header.headers)]
        if verbose:
            print(f'\t{base_name} file header:', header)

        df = pl.read_csv(
            file_path,
            separator=header.separator,
            comment_prefix='%',
            new_columns=new_columns,
            has_header=False,
        )
        data[base_name] = df

        if verbose:
            print(f'\t{base_name} data shape:', data[base_name].shape)

    m = csr_matrix((
        data['matrix']['count'].cast(pl.Float32).to_numpy(),
        (data['matrix']['cell_index'].to_numpy() - 1, 
            data['matrix']['gene_index'].to_numpy() - 1)
    ))
    if verbose:
        print('Build csr_matrix:', m.shape)

    raw_adata = AnnData(X=m)
    raw_adata.var_names = data['features']['gene_name']
    raw_adata.obs_names = data['barcodes']['cell_barcode']
    if verbose:
        print('Build AnnData:', raw_adata, raw_adata.var_names, raw_adata.obs_names)
    return raw_adata

@dataclass
class SampleMeta:
    species: str
    version: str
    index_files: str
    sample_file_name: str
    files: dict[str, str]
    start_time: str
    end_time: str

    def __repr__(self):
        return f'SampleMeta(species={self.species}, version={self.version}, index_files={self.index_files}, files={len(self.files)}, export_time={self.start_time} ~ {self.end_time})'

class BatchSampleReader:
    '''批量读取样本
    
    >>> reader = BatchSampleReader(Path('/mnt/112-rawdata-112/output/macaque-20241203/'))
    >>> print(reader)
    BatchSampleReader(root=/mnt/112-rawdata-112/output/macaque-20241203, meta=SampleMeta(species=macaque, version=20241203, index_files=/mnt/112-rawdata-112/macaque/snRNA/all-files-20240826.txt, files=39, export_time=2024-12-03 16:16:28 ~ 2024-12-03 16:16:35))
    >>> adatas = reader.read(verbose=False)
    100%|███████████████████████████████████████████████████████████████████████████████████████████| 39/39 [00:15<00:00,  2.44it/s, 80T73-2-210420]
    >>> print(adatas)
    [AnnData object with n_obs × n_vars = 2048 × 19140
    uns: 'sample_name', '105T85-1-210422', AnnData object with n_obs × n_vars = 2123 × 19194
    uns: 'sample_name', '105T85-2-210422', AnnData object with n_obs × n_vars = 1588 × 18800
    uns: 'sample_name', '54T37-1-210415', AnnData object with n_obs × n_vars = 1353 × 18659
    uns: 'sample_name', '54T37-2-210415', AnnData object with n_obs × n_vars = 1539 × 18957
    uns: 'sample_name', '65T49-1-210416', AnnData object with n_obs × n_vars = 1299 × 18740
    uns: 'sample_name', '65T49-2-210416', AnnData object with n_obs × n_vars = 1351 × 18573
    uns: 'sample_name', '68T49-1-210416', AnnData object with n_obs × n_vars = 1368 × 18607
    uns: 'sample_name', '68T49-2-210416', AnnData object with n_obs × n_vars = 1493 × 19086
    uns: 'sample_name', '71T61-1-210420', AnnData object with n_obs × n_vars = 1650 × 18900
    uns: 'sample_name', '71T61-2-210420', AnnData object with n_obs × n_vars = 2461 × 19405
    uns: 'sample_name', '72T61-1-210420', AnnData object with n_obs × n_vars = 1695 × 19172
    uns: 'sample_name', '72T61-2-210420', AnnData object with n_obs × n_vars = 4517 × 19847
    uns: 'sample_name', '79T73-1-210420', AnnData object with n_obs × n_vars = 1075 × 18712
    uns: 'sample_name', '79T73-2-210420', AnnData object with n_obs × n_vars = 2814 × 19466
    uns: 'sample_name', '7T35-1-210426', AnnData object with n_obs × n_vars = 4162 × 19796
    uns: 'sample_name', '7T35-2-210426', AnnData object with n_obs × n_vars = 1671 × 18730
    uns: 'sample_name', '90T85-1-210421', AnnData object with n_obs × n_vars = 1807 × 18889
    uns: 'sample_name', '90T85-2-210421', AnnData object with n_obs × n_vars = 3958 × 20198
    uns: 'sample_name', 'MQC286R-159.SZM20230403', AnnData object with n_obs × n_vars = 3872 × 20283
    uns: 'sample_name', 'MQC286R-160.SZM20230403', AnnData object with n_obs × n_vars = 3800 × 20361
    uns: 'sample_name', 'MQC286R-196.SZM20230403', AnnData object with n_obs × n_vars = 3993 × 20386
    uns: 'sample_name', 'MQC286R-197.SZM20230403', AnnData object with n_obs × n_vars = 4536 × 19918
    uns: 'sample_name', 'MQC286R-268.SZM20230403', AnnData object with n_obs × n_vars = 8103 × 20637
    uns: 'sample_name', 'SZM20230529_MQ277L-249', AnnData object with n_obs × n_vars = 11243 × 21018
    uns: 'sample_name', 'SZM20230529_MQ277L-250', AnnData object with n_obs × n_vars = 17731 × 21697
    uns: 'sample_name', 'SZM20230529_MQ277L-510', AnnData object with n_obs × n_vars = 16316 × 21160
    uns: 'sample_name', 'SZM20230529_MQ277L-513', AnnData object with n_obs × n_vars = 9166 × 20970
    uns: 'sample_name', 'ssDNA_97_LC0613', AnnData object with n_obs × n_vars = 4347 × 20160
    uns: 'sample_name', 'ssDNA_98_LC0613', AnnData object with n_obs × n_vars = 14475 × 21107
    uns: 'sample_name', 'ssDNA_107_LC0613', AnnData object with n_obs × n_vars = 17834 × 21468
    uns: 'sample_name', 'ssDNA_94_LC0613', AnnData object with n_obs × n_vars = 19106 × 21348
    uns: 'sample_name', 'ssDNA_95_LC0613', AnnData object with n_obs × n_vars = 13515 × 20308
    uns: 'sample_name', 'ssDNA_33_LZY20230427', AnnData object with n_obs × n_vars = 7596 × 20958
    uns: 'sample_name', 'ssDNA_24_LZY20230427', AnnData object with n_obs × n_vars = 3743 × 20463
    uns: 'sample_name', 'MQC286R-42.SZM20230403', AnnData object with n_obs × n_vars = 12647 × 21107
    uns: 'sample_name', 'SZM20230529_MQ277L-174', AnnData object with n_obs × n_vars = 17455 × 21205
    uns: 'sample_name', 'SZM20230529_MQ277L-219', AnnData object with n_obs × n_vars = 3896 × 19377
    uns: 'sample_name', '80T73-1-210420', AnnData object with n_obs × n_vars = 3544 × 19517
    uns: 'sample_name', '80T73-2-210420']

    '''
    def __init__(self, root: Path | str):
        self.root = Path(root)
        self.sample_meta_p = self.root.joinpath('samples.xlsx')
        self.meta_p = self.root.joinpath('meta.json')
        assert self.sample_meta_p.exists(), f'No `samples.xlsx` file found in `{self.root}`'
        assert self.meta_p.exists(), f'No `meta.json` file found in `{self.root}`'

        self.meta = SampleMeta(**load(open(self.meta_p)))

    @classmethod
    def from_dir(cls, root: Path | str):
        self = cls(root)
        return self

    def __repr__(self):
        return f'BatchSampleReader(root={self.root}, meta={self.meta})'

    def read(self, verbose=False, with_tqdm=True, n_jobs=8):
        if with_tqdm:
            from tqdm import tqdm
        else:
            tqdm = lambda x, *args, **kwargs: x

        sample_meta_df = pl.read_excel(self.sample_meta_p)

        adatas = []
        with ThreadPoolExecutor(n_jobs) as executor:
            tasks_samples = []
            for sample_name in (sample_meta_df['文库编号']):
                sample_p = self.root.joinpath(sample_name)
                if (p := sample_p.joinpath('02.count/filter_matrix')).exists():
                    sample_p = p
                if verbose:
                    print(f'Read {sample_name} from {sample_p}')
                tasks_samples.append((
                    executor.submit(read_sample_dir, sample_p, verbose=verbose),
                    sample_name,
                ))

            for task, sample_name in (pbar := tqdm(tasks_samples, total=len(tasks_samples))):
                adatas.append(task.result())
                # 设置样本名
                adatas[-1].uns['sample_name'] = sample_name
                adatas[-1].uns[sample_name] = sample_name
                if hasattr(pbar, 'set_postfix_str'):
                    pbar.set_postfix_str(f'{sample_name}')

        return adatas

if __name__ == '__main__':
    reader = BatchSampleReader.from_dir('/mnt/112-rawdata-112/output/macaque-20241203/')
    print(reader)
    adatas = reader.read(verbose=False)
    print(adatas)
