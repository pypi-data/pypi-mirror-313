# FindingEmo-Light — Dataset Only

<div align="center">
<hr>
🚨⚠️🚨 NOT FOR COMMERCIAL PURPOSES 🚨⚠️🚨
<hr>
</div>

This repository contains only the annotations and URL list of the FindingEmo dataset, reported in the paper
["FindingEmo: A Picture Dataset for Emotion Recognition in the Wild"](https://arxiv.org/abs/2402.01355) by Laurent Mertens et al.,
accepted at the [NeurIPS 2024 Datasets and Benchmarks Track](https://nips.cc/virtual/2024/poster/97871).

If you also require the code, please visit [https://gitlab.com/EAVISE/lme/findingemo](https://gitlab.com/EAVISE/lme/findingemo) instead.

## <a name="obtaining_images"></a>Obtaining the annotated images
### Solution 1: Using the PyPi package
Install the FindingEmo-Light package:
```
pip install findingemo-light
```
Then, in a Python script, do
```python
from findingemo_light.paper.download_multi import download_data

download_data(target_dir='./Path/To/Where/You/Want/To/Download/The/Images')
```
To get the annotations, use
```python
from findingemo_light.data.read_annotations import read_annotations

ann_data = read_annotations()
print(ann_data)
```

### Solution 2: Using the codebase
Clone the repository locally, execute ```paper/download_multi.py``` and save images to ```Config.DIR_IMAGES```
(which is the default save location).

The annotations are located under ```data/annotations_single.ann```.

## Logo
The ```./data/Logo``` folder contains image files with the dataset logo in various formats. If you find this data useful,
feel free to use the logo on your poster.

<div align="center">
<img src="https://www.laurentmertens.com/FindingEmo/FindingEmo_Color_Logo.png">
</div>

## Dataset
The <u><b>annotations</b></u> are stored in the [```data/annotations_single.ann```](findingemo_light/data/annotations_single.ann) file, which is a simple text file in CSV format.
The [```data/dataset_urls_exploded.json```](findingemo_light/data/dataset_urls_exploded.json) file contains the <u><b>URLs for the annotated images</b></u>, with multiple URLs provided
for a large number of images. We intend to update this file as we obtain backup URLs for more images.

A <u><b>Croissant metadata</b></u> file is also included ([```./croissant-findingemo.json```](./croissant-findingemo.json) to allow loading the dataset through the [Croissant](https://github.com/mlcommons/croissant) framework.

Dataset <u><b>documentation</b></u> can be found at [```datasheet/datasheet.md```](findingemo_light/datasheet/datasheet.md).

## Legal Compliance and Privacy
This dataset contains URLs to potentially copyrighted material. If you are a member of a research institution located
within the European Union, you are allowed to use this material for **non-commercial research purposes** by virtue of Title
II, Article 3 of the [InfSoc directive](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32019L0790)). If you
are not located within the European Union, it is your responsibility to verify with local legislation whether you are
allowed to use this material or not.

<font color='red'>In case you are the legal copyright holder of any of the images we provide a link to, or are depicted in any of these
images, and you do not wish that your material and/or likeness be used for Machine Learning purposes, you can contact
either [laurent.mertens@kuleuven.be](laurent.mertens@kuleuven.be) or
[joost.vennekens@kuleuven.be](joost.vennekens@kuleuven.be) with the details of the image, and we will immediately remove
it from the dataset.

**IN NO CASE SHALL THIS DATASET BE USED FOR ANY COMMERCIAL PURPOSE.**</font>

## Licensing
All data (annotations + list of URLs) is shared  under a
[Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License][cc-by-nc-sa] (see [LICENSE_data.md](./LICENSE_data.md)).

[cc-by-nc-sa]: http://creativecommons.org/licenses/by-nc-sa/4.0/
[cc-by-nc-sa-shield]: https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg

## Data overview
The ```data``` folder contains the CSV/TXT files containing the results per experiment used to generate the results
reported in the paper.

The ```data/Logo``` folder contains image files with the dataset logo.

The ```annotations_single.ann``` file, which is a simple text file in CSV format, contains the image annotations.

The ```dataset_urls_exploded.json``` file is the extended version of ```dataset_urls.txt```, which list multiple URLs for a
number of images, and is used by the ```paper/download_multi.py``` script.

## Acknowledgment
This work was funded by KU Leuven grant IDN/21/010.


Author: Laurent Mertens\
Mail: [laurent.mertens@kuleuven.be](laurent.mertens@kuleuven.be)
