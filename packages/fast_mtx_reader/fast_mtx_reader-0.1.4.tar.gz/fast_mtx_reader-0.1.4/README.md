此 [工具](http://10.20.34.150:8503/) 导出的结果可以在 Python 里并行批量导入，要自动批量导入得先安装包

## 安装

```bash
pip install -U fast_mtx_reader --index https://pypi.org/simple
```
或
```bash
uv add -U fast_mtx_reader --index https://pypi.org/simple
```

## 使用
```python
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

```
