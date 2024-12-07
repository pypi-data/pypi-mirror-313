import GEOparse
import gseapy as gp
from typing import Union
import pandas as pd
import numpy as np
import os
import logging

from sympy import use
from . import ips
from . import plot 
import matplotlib.pyplot as plt 

def load_geo(
    datasets: Union[list, str] = ["GSE00000", "GSE00001"],
    dir_save: str = "./datasets",
    verbose=False,
) -> dict:
    """
    Check if GEO datasets are already in the directory, and download them if not.

    Parameters:
    datasets (list): List of GEO dataset IDs to download.
    dir_save (str): Directory where datasets will be stored.

    Returns:
    dict: A dictionary containing the GEO objects for each dataset.
    """
    use_str = """
    get_meta(geo: dict, dataset: str = "GSE25097")
    get_expression_data(geo: dict, dataset: str = "GSE25097")
    get_probe(geo: dict, dataset: str = "GSE25097", platform_id: str = "GPL10687")
    get_data(geo: dict, dataset: str = "GSE25097")
    """
    print(f"you could do further: \n{use_str}")
    if not verbose:
        logging.getLogger("GEOparse").setLevel(logging.WARNING)
    else:
        logging.getLogger("GEOparse").setLevel(logging.DEBUG)
    # Create the directory if it doesn't exist
    if not os.path.exists(dir_save):
        os.makedirs(dir_save)
        print(f"Created directory: {dir_save}")
    if isinstance(datasets, str):
        datasets = [datasets]
    geo_data = {}
    for dataset in datasets:
        # Check if the dataset file already exists in the directory
        dataset_file = os.path.join(dir_save, f"{dataset}_family.soft.gz")

        if not os.path.isfile(dataset_file):
            print(f"\n\nDataset {dataset} not found locally. Downloading...")
            geo = GEOparse.get_GEO(geo=dataset, destdir=dir_save)
        else:
            print(f"\n\nDataset {dataset} already exists locally. Loading...")
            geo = GEOparse.get_GEO(filepath=dataset_file)

        geo_data[dataset] = geo

    return geo_data


def get_meta(geo: dict, dataset: str = "GSE25097", verbose=True) -> pd.DataFrame:
    """
    df_meta = get_meta(geo, dataset="GSE25097")
    Extracts metadata from a specific GEO dataset and returns it as a DataFrame.
    The function dynamically extracts all available metadata fields from the given dataset.

    Parameters:
    geo (dict): A dictionary containing the GEO objects for different datasets.
    dataset (str): The name of the dataset to extract metadata from (default is "GSE25097").

    Returns:
    pd.DataFrame: A DataFrame containing structured metadata from the specified GEO dataset.
    """
    # Check if the dataset is available in the provided GEO dictionary
    if dataset not in geo:
        raise ValueError(f"Dataset '{dataset}' not found in the provided GEO data.")

    # List to store metadata dictionaries
    meta_list = []

    # Extract the GEO object for the specified dataset
    geo_obj = geo[dataset]

    # Overall Study Metadata
    study_meta = geo_obj.metadata
    study_metadata = {key: study_meta[key] for key in study_meta.keys()}

    # Platform Metadata
    for platform_id, platform in geo_obj.gpls.items():
        platform_metadata = {
            key: platform.metadata[key] for key in platform.metadata.keys()
        }
        platform_metadata["platform_id"] = platform_id  # Include platform ID

        # Sample Metadata
        for sample_id, sample in geo_obj.gsms.items():
            sample_metadata = {
                key: sample.metadata[key] for key in sample.metadata.keys()
            }
            sample_metadata["sample_id"] = sample_id  # Include sample ID
            # Combine all metadata into a single dictionary
            combined_meta = {
                "dataset": dataset,
                **{
                    k: (
                        v[0]
                        if isinstance(v, list) and len(v) == 1
                        else ", ".join(map(str, v))
                    )
                    for k, v in study_metadata.items()
                },  # Flatten study metadata
                **platform_metadata,  # Unpack platform metadata
                **{
                    k: (
                        v[0]
                        if isinstance(v, list) and len(v) == 1
                        else "".join(map(str, v))
                    )
                    for k, v in sample_metadata.items()
                },  # Flatten sample metadata
            }

            # Append the combined metadata to the list
            meta_list.append(combined_meta)

    # Convert the list of dictionaries to a DataFrame
    meta_df = pd.DataFrame(meta_list)
    col_rm = [
        "channel_count",
        "contact_web_link",
        "contact_address",
        "contact_city",
        "contact_country",
        "contact_department",
        "contact_email",
        "contact_institute",
        "contact_laboratory",
        "contact_name",
        "contact_phone",
        "contact_state",
        "contact_zip/postal_code",
        "contributor",
        "manufacture_protocol",
        "taxid",
        "web_link",
    ]
    # rm unrelavent columns
    meta_df = meta_df.drop(columns=[col for col in col_rm if col in meta_df.columns])
    if verbose:
        print(
            f"Meta info columns for dataset '{dataset}': \n{sorted(meta_df.columns.tolist())}"
        )
        display(meta_df[:1].T)
    return meta_df


def get_probe(
    geo: dict, dataset: str = "GSE25097", platform_id: str = None, verbose=True
):
    """
    df_probe = get_probe(geo, dataset="GSE25097", platform_id: str = "GPL10687")
    """
    # try to find the platform_id from meta
    if platform_id is None:
        df_meta = get_meta(geo=geo, dataset=dataset, verbose=False)
        platform_id = df_meta["platform_id"].unique().tolist()
        print(f"Platform: {platform_id}")
    if len(platform_id) > 1:
        df_probe= geo[dataset].gpls[platform_id[0]].table
        # df_probe=pd.DataFrame()
        # # Iterate over each platform ID and collect the probe tables
        # for platform_id_ in platform_id:
        #     if platform_id_ in geo[dataset].gpls:
        #         df_probe_ = geo[dataset].gpls[platform_id_].table
        #         if not df_probe_.empty:
        #             df_probe=pd.concat([df_probe, df_probe_])
        #         else:
        #             print(f"Warning: Probe table for platform {platform_id_} is empty.")
        #     else:
        #         print(f"Warning: Platform ID {platform_id_} not found in dataset {dataset}.")
    else:
        df_probe= geo[dataset].gpls[platform_id[0]].table
    
    if df_probe.empty:
        print(
            f"Warning: cannot find the probe info. 看一下是不是在单独的文件中包含了probe信息"
        )
        display(f"🔗: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc={platform_id}")
        return get_meta(geo, dataset, verbose=verbose)
    if verbose:
        print(f"columns in the probe table: \n{sorted(df_probe.columns.tolist())}")
    return df_probe


def get_expression_data(geo: dict, dataset: str = "GSE25097") -> pd.DataFrame:
    """
    df_expression = get_expression_data(geo,dataset="GSE25097")
    只包含表达量数据,并没有考虑它的probe和其它的meta

    Extracts expression values from GEO datasets and returns it as a DataFrame.

    Parameters:
    geo (dict): A dictionary containing GEO objects for each dataset.

    Returns:
    pd.DataFrame: A DataFrame containing expression data from the GEO datasets.
    """
    expression_dataframes = []
    try:
        expression_values = geo[dataset].pivot_samples("VALUE")
    except:
        for sample_id, sample in geo[dataset].gsms.items():
            if hasattr(sample, "table"):
                expression_values = (
                    sample.table.T
                )  # Transpose for easier DataFrame creation
                expression_values["dataset"] = dataset
                expression_values["sample_id"] = sample_id
    return expression_values


def get_data(geo: dict, dataset: str = "GSE25097", verbose=False):
    print(f"\n\ndataset: {dataset}\n")
    # get probe info
    df_probe = get_probe(geo, dataset=dataset, verbose=False)
    # get expression values
    df_expression = get_expression_data(geo, dataset=dataset)
    if not df_expression.select_dtypes(include=["number"]).empty:
        # 如果数据全部是counts类型的话, 则使用TMM进行normalize
        if 'counts' in get_data_type(df_expression):
            try:
                df_expression=counts2expression(df_expression.T).T 
                print(f"{dataset}'s type is raw read counts, nomalized(transformed) via 'TMM'")
            except Exception as e: 
                print("raw counts data")
    if any([df_probe.empty, df_expression.empty]):
        print(
            f"got empty values, check the probe info. 看一下是不是在单独的文件中包含了probe信息"
        )
        return get_meta(geo, dataset, verbose=True)
    print(
        f"\n\tdf_expression.shape: {df_expression.shape} \n\tdf_probe.shape: {df_probe.shape}"
    )
    df_exp = pd.merge(
        df_probe,
        df_expression,
        left_on=df_probe.columns.tolist()[0],
        right_index=True,
        how="outer",
    )

    # get meta info
    df_meta = get_meta(geo, dataset=dataset, verbose=False)
    col_rm = [
        "channel_count","contact_web_link","contact_address","contact_city","contact_country","contact_department",
        "contact_email","contact_institute","contact_laboratory","contact_name","contact_phone","contact_state",
        "contact_zip/postal_code","contributor","manufacture_protocol","taxid","web_link",
    ]
    # rm unrelavent columns
    df_meta = df_meta.drop(columns=[col for col in col_rm if col in df_meta.columns])
    # sorte columns
    df_meta = df_meta.reindex(sorted(df_meta.columns), axis=1)
    # find a proper column
    col_sample_id = ips.strcmp("sample_id", df_meta.columns.tolist())[0]
    df_meta.set_index(col_sample_id, inplace=True)  # set gene symbol as index

    col_gene_symbol = ips.strcmp("GeneSymbol", df_exp.columns.tolist())[0]
    # select the 'GSM' columns
    col_gsm = df_exp.columns[df_exp.columns.str.startswith("GSM")].tolist()
    df_exp.set_index(col_gene_symbol, inplace=True)
    df_exp = df_exp[col_gsm].T  # transpose, so that could add meta info

    df_merged = ips.df_merge(df_meta, df_exp,use_index=True)
    
    print(
        f"\ndataset:'{dataset}' n_sample = {df_merged.shape[0]}, n_gene={df_exp.shape[1]}"
    )
    if verbose:
        display(df_merged.sample(5))
    return df_merged

def get_data_type(data: pd.DataFrame) -> str:
    """
    Determine the type of data: 'read counts' or 'normalized expression data'.
    usage:
        get_data_type(df_counts)
    """
    numeric_data = data.select_dtypes(include=["number"])
    if numeric_data.empty:
        raise ValueError(f"找不到数字格式的数据, 请先进行转换")
    # Check if the data contains only integers
    if numeric_data.apply(lambda x: x.dtype == "int").all():
        # Check for values typically found in raw read counts (large integers)
        if numeric_data.max().max() > 10000:  # Threshold for raw counts
            return "read counts"
    # Check if all values are floats
    if numeric_data.apply(lambda x: x.dtype == "float").all():
        # If values are small, it's likely normalized data
        if numeric_data.max().max() < 1000:  # Threshold for normalized expression
            return "normalized expression data"
        else:
            print(f"the max value: {numeric_data.max().max()}, it could be a raw read counts data. but needs you to double check it")
            return "read counts"
    # If mixed data types or unexpected values
    return "mixed or unknown"

def split_at_lower_upper(lst):
    """
    将一串list,从全是lowercase,然后就是大写或者nan的地方分隔成两个list
    """
    for i in range(len(lst) - 1):
        if isinstance(lst[i], str) and lst[i].islower():
            next_item = lst[i + 1]
            if isinstance(next_item, str) and next_item.isupper():
                # Found the split point: lowercase followed by uppercase
                return lst[: i + 1], lst[i + 1 :]
            elif pd.isna(next_item):
                # NaN case after a lowercase string
                return lst[: i + 1], lst[i + 1 :]
    return lst, []

def find_condition(data:pd.DataFrame, columns=["characteristics_ch1","title"]):
    if data.shape[1]>=data.shape[0]:
        display(data.iloc[:1,:40].T)
    # 详细看看每个信息的有哪些类, 其中有数字的, 要去除
    for col in columns:
        print(f"{"="*10} {col} {"="*10}")
        display(ips.flatten([ips.ssplit(i, by="numer")[0] for i in data[col]],verbose=False))

def add_condition(
    data: pd.DataFrame,
    column: str = "characteristics_ch1",  # 在哪一行进行分类
    column_new: str = "condition",  # 新col的命名
    by: str = "tissue: tumor liver",  # 通过by来命名
    by_not: str = ": tumor",  # 健康的选择条件
    by_name: str = "non-tumor",  # 健康的命名
    by_not_name: str = "tumor",  # 不健康的命名
    inplace: bool = True,  # replace the data
    verbose: bool = True,
):
    """
    Add a new column to the DataFrame based on the presence of a specific substring in another column.

        Parameters
        ----------
        data : pd.DataFrame
            The input DataFrame containing the data.
        column : str, optional
            The name of the column in which to search for the substring (default is 'characteristics_ch1').
        column_new : str, optional
            The name of the new column to be created (default is 'condition').
        by : str, optional
            The substring to search for in the specified column (default is 'heal').

    """
    # first check the content in column
    content = data[column].unique().tolist()
    if verbose:
        if len(content) > 10:
            display(content[:10])
        else:
            display(content)
    # 优先by
    if by:
        data[column_new] = data[column].apply(
            lambda x: by_name if by in x else by_not_name
        )
    elif by_not:
        data[column_new] = data[column].apply(
            lambda x: by_not_name if not by_not in x else by_name
        )
    if verbose:
        display(data.sample(5))
    if not inplace:
        return data


def add_condition_multi(
    data: pd.DataFrame,
    column: str = "characteristics_ch1",  # Column to classify
    column_new: str = "condition",  # New column name
    conditions: dict = {
        "low": "low",
        "high": "high",
        "intermediate": "intermediate",
    },  # A dictionary where keys are substrings and values are condition names
    default_name: str = "unknown",  # Default name if no condition matches
    inplace: bool = True,  # Whether to replace the data
    verbose: bool = True,
):
    """
    Add a new column to the DataFrame based on the presence of specific substrings in another column.

    Parameters
    ----------
    data : pd.DataFrame
        The input DataFrame containing the data.
    column : str, optional
        The name of the column in which to search for the substrings (default is 'characteristics_ch1').
    column_new : str, optional
        The name of the new column to be created (default is 'condition').
    conditions : dict, optional
        A dictionary where keys are substrings to search for and values are the corresponding labels.
    default_name : str, optional
        The name to assign if no condition matches (default is 'unknown').
    inplace : bool, optional
        Whether to modify the original DataFrame (default is True).
    verbose : bool, optional
        Whether to display the unique values and final DataFrame (default is True).
    """

    # Display the unique values in the column
    content = data[column].unique().tolist()
    if verbose:
        if len(content) > 10:
            display(content[:10])
        else:
            display(content)

    # Check if conditions are provided
    if conditions is None:
        raise ValueError(
            "Conditions must be provided as a dictionary with substrings and corresponding labels."
        )

    # Define a helper function to map the conditions
    def map_condition(value):
        for substring, label in conditions.items():
            if substring in value:
                return label
        return default_name  # If no condition matches, return the default name

    # Apply the mapping function to create the new column
    data[column_new] = data[column].apply(map_condition)

    # Display the updated DataFrame if verbose is True
    if verbose:
        display(data.sample(5))

    if not inplace:
        return data

def clean_dataset(
    data: pd.DataFrame, dataset: str = None, condition: str = "condition",sep="///"
):
    """
    #* it has been involved in bio.batch_effects(), but default: False
    1. clean data set and prepare super_datasets
    2. if "///" in index, then extend it, or others.
    3. drop duplicates and dropna()
    4. add the 'condition' and 'dataset info' to the columns
    5. set genes as index
    """
    usage_str="""clean_dataset(data: pd.DataFrame, dataset: str = None, condition: str = "condition",sep="///")
    """
    if dataset is None:
        try: 
            dataset=data["dataset"][0]
        except:
            print("cannot find 'dataset' name")
            print(f"example\n {usage_str}")
    #! (4.1) clean data set and prepare super_datasets
    # df_data_2, 左边的列是meta,右边的列是gene_symbol
    col_gene = split_at_lower_upper(data.columns.tolist())[1][0]
    idx = ips.strcmp(col_gene, data.columns.tolist())[1]
    df_gene = data.iloc[:, idx:].T  # keep the last 'condition'

    #! if "///" in index, then extend it, or others.
    print(f"before extend shape: {df_gene.shape}")
    df = df_gene.reset_index()
    df_gene = ips.df_extend(df, column="index", sep=sep)
    # reset 'index' column as index
    # df_gene = df_gene.set_index("index")
    print(f"after extended by '{sep}' shape: {df_gene.shape}")

    # *alternative:
    # df_unique = df.reset_index().drop_duplicates(subset="index").set_index("index")
    #! 4.2 drop duplicates and dropna()
    df_gene = df_gene.drop_duplicates(subset=["index"]).dropna()
    print(f"drop duplicates and dropna: shape: {df_gene.shape}")

    #! add the 'condition' and 'dataset info' to the columns
    ds = [data["dataset"][0]] * len(df_gene.columns[1:])
    samp = df_gene.columns.tolist()[1:]
    cond = df_gene[df_gene["index"] == condition].values.tolist()[0][1:]
    df_gene.columns = ["index"] + [
        f"{ds}_{sam}_{cond}" for (ds, sam, cond) in zip(ds, samp, cond)
    ]
    df_gene.drop(df_gene[df_gene["index"] == condition].index, inplace=True)
    #! set genes as index
    df_gene.set_index("index",inplace=True)
    display(df_gene.head())
    return df_gene

def batch_effect(
    data: list = "[df_gene_1, df_gene_2, df_gene_3]", # index (genes),columns(samples)
    datasets: list = ["GSE25097", "GSE62232", "GSE65372"],
    clean_data:bool=False, # default, not do data cleaning
    top_genes:int=10,# only for plotting
    plot_=True,
    dir_save="./res/",
    kws_clean_dataset:dict={},
    **kwargs
):
    """
    usage 1: 
        bio.batch_effect(
                data=[df_gene_1, df_gene_2, df_gene_3],
                datasets=["GSE25097", "GSE62232", "GSE65372"],
                clean_data=False,
                dir_save="./res/")
    
    #! # or conbine clean_dataset and batch_effect together
        # # data = [bio.clean_dataset(data=dt, dataset=ds) for (dt, ds) in zip(data, datasets)]
        data_common = bio.batch_effect(
                    data=[df_data_1, df_data_2, df_data_3],
                    datasets=["GSE25097", "GSE62232", "GSE65372"], clean_data=True
                    )
    """
    # data = [df_gene_1, df_gene_2, df_gene_3]
    # datasets = ["GSE25097", "GSE62232", "GSE65372"]
    # top_genes = 10  # show top 10 genes
    # plot_ = True
    from combat.pycombat import pycombat
    if clean_data:
        data=[clean_dataset(data=dt,dataset=ds,**kws_clean_dataset) for (dt,ds) in zip(data,datasets)]
    #! prepare data
    # the datasets are dataframes where:
    # the indexes correspond to the gene names
    # the column names correspond to the sample names
    #! merge batchs
    # https://epigenelabs.github.io/pyComBat/
    # we merge all the datasets into one, by keeping the common genes only
    df_expression_common_genes = pd.concat(data, join="inner", axis=1)
    #! convert to float
    ips.df_astype(df_expression_common_genes, astype="float", inplace=True)

    #!to visualise results, use Mini datasets, only take the first 10 samples of each batch(dataset)
    if plot_:
        col2plot = []
        for ds in datasets:
            # select the first 10 samples to plot, to see the diff
            dat_tmp = df_expression_common_genes.columns[
                df_expression_common_genes.columns.str.startswith(ds)
            ][:top_genes].tolist()
            col2plot.extend(dat_tmp)
        # visualise results
        _, axs = plt.subplots(2, 1, figsize=(15, 10))
        plot.plotxy(
            ax=axs[0],
            data=df_expression_common_genes.loc[:, col2plot],
            kind="bar",
            figsets=dict(
                title="Samples expression distribution (non-correction)",
                ylabel="Observations",
                xangle=90,
            ),
        )
    # prepare batch list
    batch = [
        ips.ssplit(i, by="_")[0] for i in df_expression_common_genes.columns.tolist()
    ]
    # run pyComBat
    df_corrected = pycombat(df_expression_common_genes, batch, **kwargs)
    print(f"df_corrected.shape: {df_corrected.shape}")
    display(df_corrected.head())
    # visualise results again
    if plot_:

        plot.plotxy(
            ax=axs[1],
            data=df_corrected.loc[:, col2plot],
            kind="bar",
            figsets=dict(
                title="Samples expression distribution (corrected)",
                ylabel="Observations",
                xangle=90,
            ),
        )
        if dir_save is not None:
            ips.figsave(dir_save + "batch_sample_exp_distri.pdf")
    return df_corrected

def get_common_genes(elment1, elment2):
    common_genes=ips.shared(elment1, elment2,verbose=False)
    return common_genes

def counts2expression(
    counts: pd.DataFrame,# index(samples); columns(genes)
    method: str = "TMM",  # 'CPM', 'FPKM', 'TPM', 'UQ', 'TMM', 'CUF', 'CTF'
    length: list = None,
    uq_factors: pd.Series = None,
    verbose: bool = False,
) -> pd.DataFrame:
    """
    https://www.linkedin.com/pulse/snippet-corner-raw-read-count-normalization-python-mazzalab-gzzyf?trk=public_post
    Convert raw RNA-seq read counts to expression values
    counts: pd.DataFrame
        index: samples
        columns: genes
    usage:
        df_normalized = counts2expression(df_counts, method='TMM', verbose=True)
    recommend cross datasets:
        cross-datasets:
            TMM (Trimmed Mean of M-values); Very suitable for merging datasets, especially
                for cross-sample and cross-dataset comparisons; commonly used in
                differential expression analysis
            CTF (Counts adjusted with TMM factors); Suitable for merging datasets, as
                TMM-based normalization. Typically used as input for downstream analyses
                like differential expression
            TPM (Transcripts Per Million); Good for merging datasets. TPM is often more
                suitable for cross-dataset comparisons because it adjusts for gene length
                and ensures that the expression levels sum to the same total in each sample
            UQ (Upper Quartile);  less commonly used than TPM or TMM
            CUF (Counts adjusted with UQ factors); Can be used, but UQ normalization is
                generally not as standardized as TPM or TMM for merging datasets.
        within-datasets:
            CPM(Counts Per Million); it doesn’t adjust for gene length or other
                variables that could vary across datasets
            FPKM(Fragments Per Kilobase Million); FPKM has been known to be inconsistent
                across different experiments
    Parameters:
    - counts: pd.DataFrame
        Raw read counts with genes as rows and samples as columns.
    - method: str, default='TMM'
        CPM (Counts per Million): Scales counts by total library size.
        FPKM (Fragments per Kilobase Million): Requires gene length; scales by both library size and gene length.
        TPM (Transcripts per Million): Scales by gene length and total transcript abundance.
        UQ (Upper Quartile): Normalizes based on the upper quartile of the counts.
        TMM (Trimmed Mean of M-values): Adjusts for compositional biases.
        CUF (Counts adjusted with Upper Quartile factors): Counts adjusted based on UQ factors.
        CTF (Counts adjusted with TMM factors): Counts adjusted based on TMM factors.
    - gene_lengths: pd.Series, optional
        Gene lengths (e.g., in kilobases) for FPKM/TPM normalization. Required for FPKM/TPM.
    - verbose: bool, default=False
        If True, provides detailed logging information.
    - uq_factors: pd.Series, optional
        Precomputed Upper Quartile factors, required for UQ and CUF normalization.


    Returns:
    - normalized_counts: pd.DataFrame
        Normalized expression values.
    """
    import rnanorm
    print(f"'counts' data shoule be: index(samples); columns(genes)")
    if "length" in method: # 有时候记不住这么多不同的名字
        method="FPKM"
    methods = ["CPM", "FPKM", "TPM", "UQ", "TMM", "CUF", "CTF"]
    method = ips.strcmp(method, methods)[0]
    if verbose:
        print(
            f"Starting normalization using method: {method},supported methods: {methods}"
        )
    columns_org = counts.columns.tolist()
    # Check if gene lengths are provided when necessary
    if method in ["FPKM", "TPM"]:
        if length is None:
            raise ValueError(f"Gene lengths must be provided for {method} normalization.")
        if isinstance(length, list):
            df_genelength = pd.DataFrame({"gene_length": length})
            df_genelength.index = counts.columns # set gene_id as index
            df_genelength.index = df_genelength.index.astype(str).str.strip()
            # length = np.array(df_genelength["gene_length"]).reshape(1,-1)
            length = df_genelength["gene_length"]
            counts.index = counts.index.astype(str).str.strip()
        elif isinstance(length, pd.Series):
            
            length.index=length.index.astype(str).str.strip()
            counts.columns = counts.columns.astype(str).str.strip()
            shared_genes=ips.shared(length.index, counts.columns,verbose=False)
            length=length.loc[shared_genes]
            counts=counts.loc[:,shared_genes]
            columns_org = counts.columns.tolist()
            

    # # Ensure gene lengths are aligned with counts if provided
    # if length is not None:
    #     length = length[counts.index]

    # Start the normalization based on the chosen method
    if method == "CPM":
        normalized_counts = (
            rnanorm.CPM().set_output(transform="pandas").fit_transform(counts)
        )

    elif method == "FPKM":
        if verbose:
            print("Performing FPKM normalization using gene lengths.")
        normalized_counts = (
            rnanorm.CPM().set_output(transform="pandas").fit_transform(counts)
        )
        # convert it to FPKM by, {FPKM= gene length /read counts ×1000} is applied using row-wise division and multiplication.
        normalized_counts=normalized_counts.div(length.values,axis=1)*1e3

    elif method == "TPM":
        if verbose:
            print("Performing TPM normalization using gene lengths.")
        normalized_counts = (
            rnanorm.TPM(gene_lengths=length)
            .set_output(transform="pandas")
            .fit_transform(counts)
        )

    elif method == "UQ":
        if verbose:
            print("Performing Upper Quartile (UQ) normalization.")
        if uq_factors is None:
            uq_factors = rnanorm.upper_quartile_factors(counts)
        normalized_counts = (
            rnanorm.UQ(factors=uq_factors)()
            .set_output(transform="pandas")
            .fit_transform(counts)
        )

    elif method == "TMM":
        if verbose:
            print("Performing TMM normalization (Trimmed Mean of M-values).")
        normalized_counts = (
            rnanorm.TMM().set_output(transform="pandas").fit_transform(counts)
        )

    elif method == "CUF":
        if verbose:
            print("Performing Counts adjusted with UQ factors (CUF).")
        if uq_factors is None:
            uq_factors = rnanorm.upper_quartile_factors(counts)
        normalized_counts = (
            rnanorm.CUF(factors=uq_factors)()
            .set_output(transform="pandas")
            .fit_transform(counts)
        )

    elif method == "CTF":
        if verbose:
            print("Performing Counts adjusted with TMM factors (CTF).")
        normalized_counts = (rnanorm.CTF().set_output(transform="pandas").fit_transform(counts))

    else:
        raise ValueError(f"Unknown normalization method: {method}")
    normalized_counts.columns=columns_org
    if verbose:
        print(f"Normalization complete using method: {method}")

    return normalized_counts

def counts_deseq(counts_sam_gene: pd.DataFrame, 
                 meta_sam_cond: pd.DataFrame,
                 design_factors:list=None,
                 kws_DeseqDataSet:dict={},
                 kws_DeseqStats:dict={}):
    """
    https://pydeseq2.readthedocs.io/en/latest/api/docstrings/pydeseq2.ds.DeseqStats.html
    Note: Using normalized expression data in a DeseqDataSet object is generally not recommended 
            because the DESeq2 framework is designed to work with raw count data. 
    baseMean:
        - This value represents the average normalized count (or expression level) of a 
            gene across all samples in your dataset.
        - For example, a baseMean of 0.287 for 4933401J01Rik indicates that this gene has 
            low expression levels in the samples compared to others with higher baseMean 
            values like Xkr4 (591.015).
    log2FoldChange: the magnitude and direction of change in expression between conditions.
    lfcSE (Log Fold Change Standard Error): standard error of the log2FoldChange. It 
        indicates the uncertainty in the estimate of the fold change.A lower value indicates 
        more confidence in the fold change estimate.
    padj: This value accounts for multiple testing corrections (e.g., Benjamini-Hochberg).
    Log10transforming: The columns -log10(pvalue) and -log10(FDR) are transformations of 
        the p-values and adjusted p-values, respectively
    """
    from pydeseq2.dds import DeseqDataSet
    from pydeseq2.ds import DeseqStats
    from pydeseq2.default_inference import DefaultInference

    # data filtering
    # counts_sam_gene = counts_sam_gene.loc[:, ~(counts_sam_gene.sum(axis=0) < 10)]
    if design_factors is None:
        design_factors=meta_sam_cond.columns.tolist()

    kws_DeseqDataSet.pop("design_factors",{})
    refit_cooks=kws_DeseqDataSet.pop("refit_cooks",True)
    
    #! DeseqDataSet
    inference = DefaultInference(n_cpus=8)
    dds = DeseqDataSet(
        counts=counts_sam_gene,
        metadata=meta_sam_cond,
        design_factors=meta_sam_cond.columns.tolist(),
        refit_cooks=refit_cooks,
        inference=inference,
        **kws_DeseqDataSet
    )
    dds.deseq2()
    #* results
    dds_explain="""
        res[0]:
        # X stores the count data,
        # obs stores design factors,
        # obsm stores sample-level data, such as "design_matrix" and "size_factors",
        # varm stores gene-level data, such as "dispersions" and "LFC"."""
    print(dds_explain)
    #! DeseqStats
    stat_res = DeseqStats(dds,**kws_DeseqStats)
    stat_res.summary()
    diff = stat_res.results_df.assign(padj=lambda x: x.padj.fillna(1))
    
    # handle '0' issue, which will case inf when the later cal (e.g., log10)
    diff["padj"] = diff["padj"].replace(0, 1e-10)
    diff["pvalue"] = diff["pvalue"].replace(0, 1e-10)

    diff["-log10(pvalue)"] = diff["pvalue"].apply(lambda x: -np.log10(x))
    diff["-log10(FDR)"] = diff["padj"].apply(lambda x: -np.log10(x))
    diff=diff.reset_index().rename(columns={"index": "gene"})
    # sig_diff = (
    #     diff.query("log2FoldChange.abs()>0.585 & padj<0.05")
    #     .reset_index()
    #     .rename(columns={"index": "gene"})
    # )
    df_norm=pd.DataFrame(dds.layers['normed_counts'])
    df_norm.index=counts_sam_gene.index
    df_norm.columns=counts_sam_gene.columns
    print("res[0]: dds\nres[1]:diff\nres[2]:stat_res\nres[3]:df_normalized")
    return dds, diff, stat_res,df_norm

def scope_genes(gene_list: list, scopes:str=None, fields: str = "symbol", species="human"):
    """
    usage:
        scope_genes(df_counts.columns.tolist()[:1000], species="mouse")
    """
    import mygene

    if scopes is None:
        # copy from: https://docs.mygene.info/en/latest/doc/query_service.html#scopes
        scopes = ips.fload(
            "/Users/macjianfeng/Dropbox/github/python/py2ls/py2ls/data/mygenes_fields_241022.txt",
            kind="csv",
            verbose=False,
        )
        scopes = ",".join([i.strip() for i in scopes.iloc[:, 0]])
    mg = mygene.MyGeneInfo()
    results = mg.querymany(
        gene_list,
        scopes=scopes,
        fields=fields,
        species=species,
    )
    return pd.DataFrame(results)

def get_enrichr(gene_symbol_list, 
                gene_sets:str, 
                download:bool = False,
                species='Human', 
                dir_save="./", 
                plot_=False, 
                n_top=30,
                palette=None,
                check_shared=True,
                figsize=(5,8),
                show_ring=False,
                xticklabels_rot=0,
                title=None,# 'KEGG'
                cutoff=0.05,
                cmap="coolwarm",
                size=5,
                **kwargs):
    """
    Note: Enrichr uses a list of Entrez gene symbols as input.
    
    """
    kws_figsets = {}
    for k_arg, v_arg in kwargs.items():
        if "figset" in k_arg:
            kws_figsets = v_arg
            kwargs.pop(k_arg, None)
            break
    species_org=species
    # organism (str) – Select one from { ‘Human’, ‘Mouse’, ‘Yeast’, ‘Fly’, ‘Fish’, ‘Worm’ }
    organisms=['Human', 'Mouse', 'Yeast', 'Fly', 'Fish', 'Worm']
    species=ips.strcmp(species,organisms)[0]
    if species_org.lower()!= species.lower():
        print(f"species was corrected to {species}, becasue only support {organisms}")
    if os.path.isfile(gene_sets):
        gene_sets_name=os.path.basename(gene_sets)
        gene_sets = ips.fload(gene_sets)
    else:
        lib_support_names = gp.get_library_name()
        # correct input gene_set name
        gene_sets_name=ips.strcmp(gene_sets,lib_support_names)[0]
        
        # download it
        if download:
            gene_sets = gp.get_library(name=gene_sets_name, organism=species)
        else:
            gene_sets = gene_sets_name # 避免重复下载
    print(f"\ngene_sets get ready: {gene_sets_name}")

    # gene symbols are uppercase
    gene_symbol_list=[str(i).upper() for i in gene_symbol_list]

    # # check how shared genes
    if check_shared and isinstance(gene_sets, dict):
        shared_genes=ips.shared(ips.flatten(gene_symbol_list,verbose=False), 
                                ips.flatten(gene_sets,verbose=False),
                                verbose=False)
    
    #! enrichr 
    try:
        enr = gp.enrichr(
            gene_list=gene_symbol_list,
            gene_sets=gene_sets,
            organism=species,
            outdir=None,  # don't write to disk
            **kwargs
        )
    except ValueError as e:
        print(f"\n{'!'*10}  Error  {'!'*10}\n{' '*4}{e}\n{'!'*10}  Error  {'!'*10}")
        return None
    
    results_df = enr.results
    print(f"got enrichr reslutls; shape: {results_df.shape}\n")
    results_df["-log10(Adjusted P-value)"] = -np.log10(results_df["Adjusted P-value"])
    results_df.sort_values("-log10(Adjusted P-value)", inplace=True, ascending=False)

    if plot_:
        if palette is None:
            palette=plot.get_color(n_top, cmap=cmap)[::-1]
        #! barplot
        if n_top<5:
            height_=4
        elif 5<=n_top<10:
            height_=5
        elif 5<=n_top<10:
            height_=6
        elif 10<=n_top<15:
            height_=7
        elif 15<=n_top<20:
            height_=8
        elif 20<=n_top<30:
            height_=9
        else:
            height_=int(n_top/3)
        plt.figure(figsize=[10, height_])

        ax1=plot.plotxy(
            data=results_df.head(n_top),
            kind="barplot",
            x="-log10(Adjusted P-value)",
            y="Term",
            hue="Term",
            palette=palette,
            legend=None,
        )
        plot.figsets(ax=ax1, **kws_figsets)
        if dir_save: 
            ips.figsave(f"{dir_save} enr_barplot.pdf")
        plt.show()

        #! dotplot 
        cutoff_curr = cutoff
        step=0.05
        cutoff_stop = 0.5
        while cutoff_curr <= cutoff_stop:
            try:
                if cutoff_curr!=cutoff:
                    plt.clf()
                ax2 = gp.dotplot(enr.res2d, 
                                column="Adjusted P-value",
                                show_ring=show_ring,
                                xticklabels_rot=xticklabels_rot,
                                title=title,
                                cmap=cmap,
                                cutoff=cutoff_curr,
                                top_term=n_top,
                                size=size,
                                figsize=[10, height_])
                if len(ax2.collections)>=n_top: 
                    print(f"cutoff={cutoff_curr} done! ")
                    break 
                if cutoff_curr==cutoff_stop:
                    break
                cutoff_curr+=step
            except Exception as e:
                cutoff_curr+=step
                print(f"Warning: trying cutoff={cutoff_curr}, cutoff={cutoff_curr-step} failed: {e} ")
            ax = plt.gca()
            plot.figsets(ax=ax,**kws_figsets)
            
        if dir_save:
            ips.figsave(f"{dir_save}enr_dotplot.pdf")

    return results_df

def plot_enrichr(results_df,
                 kind="bar",# 'barplot', 'dotplot'
                 cutoff=0.05,
                 show_ring=False,
                 xticklabels_rot=0,
                 title=None,# 'KEGG'
                 cmap="coolwarm",
                 n_top=10,
                 size=5,
                 ax=None,
                 **kwargs):
    kws_figsets = {}
    for k_arg, v_arg in kwargs.items():
        if "figset" in k_arg:
            kws_figsets = v_arg
            kwargs.pop(k_arg, None)
            break
    if isinstance(cmap,str):
        palette = plot.get_color(n_top, cmap=cmap)[::-1]
    elif isinstance(cmap,list):
        palette=cmap
    if n_top < 5:
        height_ = 3
    elif 5 <= n_top < 10:
        height_ = 3 
    elif 10 <= n_top < 15:
        height_ = 3
    elif 15 <= n_top < 20:
        height_ =4
    elif 20 <= n_top < 30:
        height_ = 5
    elif 30 <= n_top < 40:
        height_ = int(n_top / 6)
    else:
        height_ = int(n_top / 8) 

    #! barplot
    if 'bar' in kind.lower():
        if ax is None:
            _,ax=plt.subplots(1,1,figsize=[10, height_])
        ax=plot.plotxy(
            data=results_df.head(n_top),
            kind="barplot",
            x="-log10(Adjusted P-value)",
            y="Term",
            hue="Term",
            palette=palette,
            legend=None,
        )
        plot.figsets(ax=ax, **kws_figsets)
        return ax,results_df

    #! dotplot
    elif 'dot' in kind.lower():
        #! dotplot 
        cutoff_curr = cutoff
        step=0.05
        cutoff_stop = 0.5
        while cutoff_curr <= cutoff_stop:
            try:
                if cutoff_curr!=cutoff:
                    plt.clf()
                ax = gp.dotplot(results_df, 
                                column="Adjusted P-value",
                                show_ring=show_ring,
                                xticklabels_rot=xticklabels_rot,
                                title=title,
                                cmap=cmap,
                                cutoff=cutoff_curr,
                                top_term=n_top,
                                size=size,
                                figsize=[10, height_])
                if len(ax.collections)>=n_top: 
                    print(f"cutoff={cutoff_curr} done! ")
                    break 
                if cutoff_curr==cutoff_stop:
                    break
                cutoff_curr+=step
            except Exception as e:
                cutoff_curr+=step
                print(f"Warning: trying cutoff={cutoff_curr}, cutoff={cutoff_curr-step} failed: {e} ")
        plot.figsets(ax=ax, **kws_figsets)
        return ax,results_df

    #! barplot with counts
    elif 'count' in kind.lower():
        if ax is None:
            _,ax=plt.subplots(1,1,figsize=[10, height_])
        # 从overlap中提取出个数
        results_df["Count"] = results_df["Overlap"].apply(
        lambda x: int(x.split("/")[0]) if isinstance(x, str) else x)
        df_=results_df.sort_values(by="Count", ascending=False)

        ax=plot.plotxy(
            data=df_.head(n_top),
            kind="barplot",
            x="Count",
            y="Term",
            hue="Term",
            palette=palette,
            legend=None,
            ax=ax
        )
        
        plot.figsets(ax=ax, **kws_figsets)
        return ax,df_

def plot_bp_cc_mf(
    deg_gene_list,
    gene_sets=[
        "GO_Biological_Process_2023",
        "GO_Cellular_Component_2023",
        "GO_Molecular_Function_2023",
    ],
    species="human",
    download=False,
    n_top=10,
    plot_=True,
    ax=None,
    palette=plot.get_color(3),
    **kwargs,
):

    def res_enrichr_2_count(res_enrichr, n_top=10):
        """把enrich resulst 提取出count,并排序"""
        res_enrichr["Count"] = res_enrichr["Overlap"].apply(
            lambda x: int(x.split("/")[0]) if isinstance(x, str) else x
        )
        res_enrichr.sort_values(by="Count", ascending=False, inplace=True)

        return res_enrichr.head(n_top)#[["Term", "Count"]]

    res_enrichr_BP = get_enrichr(
        deg_gene_list, gene_sets[0], species=species, plot_=False,download=download
    )
    res_enrichr_CC = get_enrichr(
        deg_gene_list, gene_sets[1], species=species, plot_=False,download=download
    )
    res_enrichr_MF = get_enrichr(
        deg_gene_list, gene_sets[2], species=species, plot_=False,download=download
    )

    df_BP = res_enrichr_2_count(res_enrichr_BP, n_top=n_top)
    df_BP["Ontology"] = ["BP"] * n_top

    df_CC = res_enrichr_2_count(res_enrichr_CC, n_top=n_top)
    df_CC["Ontology"] = ["CC"] * n_top

    df_MF = res_enrichr_2_count(res_enrichr_MF, n_top=n_top)
    df_MF["Ontology"] = ["MF"] * n_top
    
    # 合并
    df2plot = pd.concat([df_BP, df_CC, df_MF])
    n_top=n_top*3
    if n_top < 5:
        height_ = 4
    elif 5 <= n_top < 10:
        height_ = 5 
    elif 10 <= n_top < 15:
        height_ = 6
    elif 15 <= n_top < 20:
        height_ = 7
    elif 20 <= n_top < 30:
        height_ = 8
    elif 30 <= n_top < 40:
        height_ = int(n_top / 4)
    else:
        height_ = int(n_top / 5)
    if ax is None:
        _,ax=plt.subplots(1,1,figsize=[10, height_])
    # 作图
    display(df2plot)
    if df2plot["Term"].tolist()[0].endswith(")"):
        df2plot["Term"] = df2plot["Term"].apply(lambda x: x.split("(")[0][:-1])
    if plot_:
        ax = plot.plotxy(
            data=df2plot,
            x="Count",
            y="Term",
            hue="Ontology",
            kind="bar",
            palette=palette,
            ax=ax,
            **kwargs
        )
    return ax, df2plot

def get_library_name(by=None, verbose=False):
    lib_names=gp.get_library_name()
    if by is None:
        if verbose:
            [print(i) for i in lib_names]
        return lib_names
    else:
        return ips.flatten(ips.strcmp(by, lib_names, get_rank=True,verbose=verbose),verbose=verbose)
    

def get_gsva(
    data_gene_samples: pd.DataFrame,  # index(gene),columns(samples)
    gene_sets: str,
    species:str="Human",
    dir_save:str="./",
    plot_:bool=False,
    n_top:int=30,
    check_shared:bool=True,
    cmap="coolwarm",
    min_size=1,
    max_size=1000,
    kcdf="Gaussian",# 'Gaussian' for continuous data
    method='gsva',
    seed=1,
    **kwargs,
):
    kws_figsets = {}
    for k_arg, v_arg in kwargs.items():
        if "figset" in k_arg:
            kws_figsets = v_arg
            kwargs.pop(k_arg, None)
            break
    species_org = species
    # organism (str) – Select one from { ‘Human’, ‘Mouse’, ‘Yeast’, ‘Fly’, ‘Fish’, ‘Worm’ }
    organisms = ["Human", "Mouse", "Yeast", "Fly", "Fish", "Worm"]
    species = ips.strcmp(species, organisms)[0]
    if species_org.lower() != species.lower():
        print(f"species was corrected to {species}, becasue only support {organisms}")
    if os.path.isfile(gene_sets):
        gene_sets_name = os.path.basename(gene_sets)
        gene_sets = ips.fload(gene_sets)
    else:
        lib_support_names = gp.get_library_name()
        # correct input gene_set name
        gene_sets_name = ips.strcmp(gene_sets, lib_support_names)[0]
        # download it
        gene_sets = gp.get_library(name=gene_sets_name, organism=species)
    print(f"gene_sets get ready: {gene_sets_name}")

    # gene symbols are uppercase
    gene_symbol_list = [str(i).upper() for i in data_gene_samples.index]
    data_gene_samples.index=gene_symbol_list
    # display(data_gene_samples.head(3))
    # # check how shared genes
    if check_shared:
        ips.shared(
            ips.flatten(gene_symbol_list, verbose=False),
            ips.flatten(gene_sets, verbose=False),
            verbose=False
        )
    gsva_results = gp.gsva(
        data=data_gene_samples,  #  matrix should have genes as rows and samples as columns
        gene_sets=gene_sets,
        outdir=None,
        kcdf=kcdf,  # 'Gaussian' for continuous data
        min_size=min_size,
        method=method,
        max_size=max_size,
        verbose=True,
        seed=seed,
        # no_plot=False,
    )
    gsva_res = gsva_results.res2d.copy()
    gsva_res["ES_abs"] = gsva_res["ES"].apply(np.abs)
    gsva_res = gsva_res.sort_values(by="ES_abs", ascending=False)
    gsva_res = (
        gsva_res.drop_duplicates(subset="Term").drop(columns="ES_abs")
        # .iloc[:80, :]
        .reset_index(drop=True)
    )
    gsva_res = gsva_res.sort_values(by="ES", ascending=False)
    if plot_:
        if gsva_res.shape[0]>=2*n_top:
            gsva_res_plot=pd.concat([gsva_res.head(n_top),gsva_res.tail(n_top)])
        else:
            gsva_res_plot = gsva_res
        if isinstance(cmap,str):
            palette = plot.get_color(n_top*2, cmap=cmap)[::-1]
        elif isinstance(cmap,list):
            if len(cmap)==2:
                palette = [cmap[0]]*n_top+[cmap[1]]*n_top
            else:
                palette=cmap
        # ! barplot
        if n_top < 5:
            height_ = 3
        elif 5 <= n_top < 10:
            height_ = 4 
        elif 10 <= n_top < 15:
            height_ = 5
        elif 15 <= n_top < 20:
            height_ = 6
        elif 20 <= n_top < 30:
            height_ = 7
        elif 30 <= n_top < 40:
            height_ = int(n_top / 3.5)
        else:
            height_ = int(n_top / 3)
        plt.figure(figsize=[10, height_])
        ax2 = plot.plotxy(
            data=gsva_res_plot,
            x="ES",
            y="Term",
            hue="Term",
            palette=palette,
            kind=["bar"],
            figsets=dict(yticklabel=[], ticksloc="b", boxloc="b", ylabel=None),
        )
        # 改变labels的位置
        for i, bar in enumerate(ax2.patches):
            term = gsva_res_plot.iloc[i]["Term"]
            es_value = gsva_res_plot.iloc[i]["ES"]

            # Positive ES values: Align y-labels to the left
            if es_value > 0:
                ax2.annotate(
                    term,
                    xy=(0, bar.get_y() + bar.get_height() / 2),
                    xytext=(-5, 0),  # Move to the left
                    textcoords="offset points",
                    ha="right",
                    va="center",  # Align labels to the right
                    fontsize=10,
                    color="black",
                )
            # Negative ES values: Align y-labels to the right
            else:
                ax2.annotate(
                    term,
                    xy=(0, bar.get_y() + bar.get_height() / 2),
                    xytext=(5, 0),  # Move to the right
                    textcoords="offset points",
                    ha="left",
                    va="center",  # Align labels to the left
                    fontsize=10,
                    color="black",
                )
        plot.figsets(ax=ax2, **kws_figsets)
        if dir_save:
            ips.figsave(dir_save + f"GSVA_{gene_sets_name}.pdf")
        plt.show()
    return gsva_res.reset_index(drop=True)

def plot_gsva(gsva_res, # output from bio.get_gsva()
              n_top=10,
              ax=None,            
              x="ES",
              y="Term",
              hue="Term",
              cmap="coolwarm",
              **kwargs
              ):
    kws_figsets = {}
    for k_arg, v_arg in kwargs.items():
        if "figset" in k_arg:
            kws_figsets = v_arg
            kwargs.pop(k_arg, None)
            break
    # ! barplot
    if n_top < 5:
        height_ = 4
    elif 5 <= n_top < 10:
        height_ = 5 
    elif 10 <= n_top < 15:
        height_ = 6
    elif 15 <= n_top < 20:
        height_ = 7
    elif 20 <= n_top < 30:
        height_ = 8
    elif 30 <= n_top < 40:
        height_ = int(n_top / 3.5)
    else:
        height_ = int(n_top / 3)
    if ax is None:
        _,ax=plt.subplots(1,1,figsize=[10, height_])
    gsva_res = gsva_res.sort_values(by=x, ascending=False)

    if gsva_res.shape[0]>=2*n_top:
        gsva_res_plot=pd.concat([gsva_res.head(n_top),gsva_res.tail(n_top)])
    else:
        gsva_res_plot = gsva_res
    if isinstance(cmap,str):
        palette = plot.get_color(n_top*2, cmap=cmap)[::-1]
    elif isinstance(cmap,list):
        if len(cmap)==2:
            palette = [cmap[0]]*n_top+[cmap[1]]*n_top
        else:
            palette=cmap

    ax = plot.plotxy(
        ax=ax,
        data=gsva_res_plot,
        x=x,
        y=y,
        hue=hue,
        palette=palette,
        kind=["bar"],
        figsets=dict(yticklabel=[], ticksloc="b", boxloc="b", ylabel=None),
    )
    # 改变labels的位置
    for i, bar in enumerate(ax.patches):
        term = gsva_res_plot.iloc[i]["Term"]
        es_value = gsva_res_plot.iloc[i]["ES"]

        # Positive ES values: Align y-labels to the left
        if es_value > 0:
            ax.annotate(
                term,
                xy=(0, bar.get_y() + bar.get_height() / 2),
                xytext=(-5, 0),  # Move to the left
                textcoords="offset points",
                ha="right",
                va="center",  # Align labels to the right
                fontsize=10,
                color="black",
            )
        # Negative ES values: Align y-labels to the right
        else:
            ax.annotate(
                term,
                xy=(0, bar.get_y() + bar.get_height() / 2),
                xytext=(5, 0),  # Move to the right
                textcoords="offset points",
                ha="left",
                va="center",  # Align labels to the left
                fontsize=10,
                color="black",
            )
    plot.figsets(ax=ax, **kws_figsets)
    return ax

def get_prerank(
    rnk: pd.DataFrame,
    gene_sets: str,
    download: bool = False,
    species="Human",
    threads=8,  # Number of CPU cores to use
    permutation_num=1000,  # Number of permutations for significance 
    min_size=1,  # Minimum gene set size
    max_size=2000,  # Maximum gene set size
    seed=1,  # Seed for reproducibility
    verbose=True,  # Verbosity
    dir_save="./",
    plot_=False,
    size=5,
    cutoff=0.25,
    show_ring=False,
    cmap="coolwarm",
    check_shared=True,
    **kwargs,
):
    """
    Note: Enrichr uses a list of Entrez gene symbols as input.

    """
    kws_figsets = {}
    for k_arg, v_arg in kwargs.items():
        if "figset" in k_arg:
            kws_figsets = v_arg
            kwargs.pop(k_arg, None)
            break
    species_org = species
    # organism (str) – Select one from { ‘Human’, ‘Mouse’, ‘Yeast’, ‘Fly’, ‘Fish’, ‘Worm’ }
    organisms = ["Human", "Mouse", "Yeast", "Fly", "Fish", "Worm"]
    species = ips.strcmp(species, organisms)[0]
    if species_org.lower() != species.lower():
        print(f"species was corrected to {species}, becasue only support {organisms}")
    if os.path.isfile(gene_sets):
        gene_sets_name = os.path.basename(gene_sets)
        gene_sets = ips.fload(gene_sets)
    else:
        lib_support_names = gp.get_library_name()
        # correct input gene_set name
        gene_sets_name = ips.strcmp(gene_sets, lib_support_names)[0]

        # download it
        if download:
            gene_sets = gp.get_library(name=gene_sets_name, organism=species)
        else:
            gene_sets = gene_sets_name  # 避免重复下载
    print(f"\ngene_sets get ready: {gene_sets_name}")

    #! prerank
    try:
        pre_res = gp.prerank(
            rnk=rnk,
            gene_sets=gene_sets,
            threads=threads,  # Number of CPU cores to use
            permutation_num=permutation_num,  # Number of permutations for significance
            min_size=min_size,  # Minimum gene set size
            max_size=max_size,  # Maximum gene set size
            seed=seed,  # Seed for reproducibility
            verbose=verbose,  # Verbosity
        )
    except ValueError as e:
        print(f"\n{'!'*10}  Error  {'!'*10}\n{' '*4}{e}\n{'!'*10}  Error  {'!'*10}")
        return None
    df_prerank = pre_res.res2d
    if plot_:
        #! gseaplot
        # # (1) easy way
        # terms = df_prerank.Term
        # axs = pre_res.plot(terms=terms[0])
        # (2) # to make more control on the plot, use
        terms = df_prerank.Term
        axs = pre_res.plot(
            terms=terms[:7],
            # legend_kws={"loc": (1.2, 0)},  # set the legend loc
            # show_ranking=True,  # whether to show the second yaxis
            figsize=(3, 4),
        )
        ips.figsave(dir_save + f"prerank_gseaplot_{gene_sets}.pdf")
        #!dotplot
        from gseapy import dotplot

        # to save your figure, make sure that ``ofname`` is not None
        ax = dotplot(
            df_prerank,
            column="NOM p-val",  # FDR q-val",
            cmap=cmap,
            size=size,
            figsize=(10, 5),
            cutoff=cutoff,
            show_ring=show_ring,
        )
        ips.figsave(dir_save + f"prerank_dotplot_{gene_sets}.pdf")

        #! network plot
        from gseapy import enrichment_map
        import networkx as nx

        for top_term in range(5, 50):
            try:
                # return two dataframe
                nodes, edges = enrichment_map(
                    df=df_prerank,
                    columns="FDR q-val",
                    cutoff=0.25,  # 0.25 when "FDR q-val"; 0.05 when "Nom p-value"
                    top_term=top_term,
                )
                # build graph
                G = nx.from_pandas_edgelist(
                    edges,
                    source="src_idx",
                    target="targ_idx",
                    edge_attr=["jaccard_coef", "overlap_coef", "overlap_genes"],
                )
                # to check if nodes.Hits_ratio or nodes.NES doesn’t match the number of nodes
                if len(list(nodes.Hits_ratio)) == len(G.nodes):
                    node_sizes = list(nodes.Hits_ratio * 1000)
                else:
                    raise ValueError(
                        "The size of node_size list does not match the number of nodes in the graph."
                    )

                layout = "circular"
                fig, ax = plt.subplots(figsize=(8, 8))
                if layout == "spring":
                    pos = nx.layout.spring_layout(G)
                elif layout == "circular":
                    pos = nx.layout.circular_layout(G)
                elif layout == "shell":
                    pos = nx.layout.shell_layout(G)
                elif layout == "spectral":
                    pos = nx.layout.spectral_layout(G)

                # node_size = nx.get_node_attributes()
                # draw node
                nx.draw_networkx_nodes(
                    G,
                    pos=pos,
                    cmap=plt.cm.RdYlBu,
                    node_color=list(nodes.NES),
                    node_size=list(nodes.Hits_ratio * 1000),
                )
                # draw node label
                nx.draw_networkx_labels(
                    G,
                    pos=pos,
                    labels=nodes.Term.to_dict(),
                    font_size=8,
                    verticalalignment="bottom",
                )
                # draw edge
                edge_weight = nx.get_edge_attributes(G, "jaccard_coef").values()
                nx.draw_networkx_edges(
                    G,
                    pos=pos,
                    width=list(map(lambda x: x * 10, edge_weight)),
                    edge_color="#CDDBD4",
                )
                ax.set_axis_off()
                print(f"{gene_sets}(top_term={top_term})")
                plot.figsets(title=f"{gene_sets}(top_term={top_term})")
                ips.figsave(dir_save + f"prerank_network_{gene_sets}.pdf")
                break
            except:
                print(f"not work {top_term}")
    return df_prerank
def plot_prerank(
    results_df,
    kind="bar",  # 'barplot', 'dotplot'
    cutoff=0.25,
    show_ring=False,
    xticklabels_rot=0,
    title=None,  # 'KEGG'
    cmap="coolwarm",
    n_top=10,
    size=5, # when size is None in network, by "NES"
    facecolor=None,# default by "NES"
    linewidth=None,# default by "NES"
    linecolor=None,# default by "NES"
    linealpha=None, # default by "NES"
    alpha=None,# default by "NES"
    ax=None,
    **kwargs,
):
    kws_figsets = {}
    for k_arg, v_arg in kwargs.items():
        if "figset" in k_arg:
            kws_figsets = v_arg
            kwargs.pop(k_arg, None)
            break
    if isinstance(cmap, str):
        palette = plot.get_color(n_top, cmap=cmap)[::-1]
    elif isinstance(cmap, list):
        palette = cmap
    if n_top < 5:
        height_ = 4
    elif 5 <= n_top < 10:
        height_ = 5
    elif 10 <= n_top < 15:
        height_ = 6
    elif 15 <= n_top < 20:
        height_ = 7
    elif 20 <= n_top < 30:
        height_ = 8
    elif 30 <= n_top < 40:
        height_ = int(n_top / 5)
    else:
        height_ = int(n_top / 6)
    results_df["-log10(Adjusted P-value)"]=results_df["FDR q-val"].apply(lambda x : -np.log10(x))
    results_df["Count"] = results_df["Lead_genes"].apply(lambda x: len(x.split(";")))
    #! barplot
    if "bar" in kind.lower():
        df_=results_df.sort_values(by="-log10(Adjusted P-value)",ascending=False)
        if ax is None:
            _, ax = plt.subplots(1, 1, figsize=[10, height_])
        ax = plot.plotxy(
            data=df_.head(n_top),
            kind="barplot",
            x="-log10(Adjusted P-value)",
            y="Term",
            hue="Term",
            palette=palette,
            legend=None,
        )
        plot.figsets(ax=ax, **kws_figsets)
        return ax, df_

    #! dotplot
    elif "dot" in kind.lower():
        #! dotplot
        cutoff_curr = cutoff
        step = 0.05
        cutoff_stop = 0.5
        while cutoff_curr <= cutoff_stop:
            try:
                if cutoff_curr != cutoff:
                    plt.clf()
                ax = gp.dotplot(
                    results_df,
                    column="NOM p-val",
                    show_ring=show_ring,
                    xticklabels_rot=xticklabels_rot,
                    title=title,
                    cmap=cmap,
                    cutoff=cutoff_curr,
                    top_term=n_top,
                    size=size,
                    figsize=[10, height_],
                )
                if len(ax.collections) >= n_top:
                    print(f"cutoff={cutoff_curr} done! ")
                    break
                if cutoff_curr == cutoff_stop:
                    break
                cutoff_curr += step
            except Exception as e:
                cutoff_curr += step
                print(
                    f"Warning: trying cutoff={cutoff_curr}, cutoff={cutoff_curr-step} failed: {e} "
                )
        plot.figsets(ax=ax, **kws_figsets)
        return ax, results_df

    #! barplot with counts
    elif "co" in kind.lower():
        if ax is None:
            _, ax = plt.subplots(1, 1, figsize=[10, height_])
        # 从overlap中提取出个数
        df_ = results_df.sort_values(by="Count", ascending=False)
        ax = plot.plotxy(
            data=df_.head(n_top),
            kind="barplot",
            x="Count",
            y="Term",
            hue="Term",
            palette=palette,
            legend=None,
            ax=ax,
            **kwargs,
        )

        plot.figsets(ax=ax, **kws_figsets)
        return ax, df_
    #! scatter with counts
    elif "sca" in kind.lower():
        if isinstance(cmap, str):
            palette = plot.get_color(n_top, cmap=cmap)
        elif isinstance(cmap, list):
            palette = cmap
        if ax is None:
            _, ax = plt.subplots(1, 1, figsize=[10, height_])
        # 从overlap中提取出个数
        df_ = results_df.sort_values(by="Count", ascending=False)
        ax = plot.plotxy(
            data=df_.head(n_top),
            kind="scatter",
            x="Count",
            y="Term",
            hue="Count",
            size="Count",
            sizes=[10,50],
            palette=palette,
            legend=None,
            ax=ax,
            **kwargs,
        )

        plot.figsets(ax=ax, **kws_figsets)
        return ax, df_
    elif "net" in kind.lower():
        #! network plot
        from gseapy import enrichment_map
        import networkx as nx
        from matplotlib import cm
        # try:
        if cutoff>=1 or cutoff is None:
            print(f"cutoff is {cutoff} => Without applying filter")
            nodes, edges = enrichment_map(
                df=results_df,
                columns="NOM p-val",
                cutoff=1.1,  # 0.25 when "FDR q-val"; 0.05 when "Nom p-value"
                top_term=n_top,
            )
        else:
            cutoff_curr = cutoff
            step = 0.05
            cutoff_stop = 1.0
            while cutoff_curr <= cutoff_stop:
                try:
                    # return two dataframe
                    nodes, edges = enrichment_map(
                        df=results_df,
                        columns="NOM p-val",
                        cutoff=cutoff_curr,  # 0.25 when "FDR q-val"; 0.05 when "Nom p-value"
                        top_term=n_top,
                    )

                    if nodes.shape[0] >= n_top:
                        print(f"cutoff={cutoff_curr} done! ")
                        break
                    if cutoff_curr == cutoff_stop:
                        break
                    cutoff_curr += step
                except Exception as e:
                    cutoff_curr += step
                    print(
                        f"{e}: trying cutoff={cutoff_curr}"
                    )

        print("size: by 'NES'") if size is None else print("")
        print("linewidth: by 'NES'") if linewidth is None else print("")
        print("linecolor: by 'NES'") if linecolor is None else print("")
        print("linealpha: by 'NES'") if linealpha is None else print("")
        print("facecolor: by 'NES'")  if facecolor is None else print("")
        print("alpha: by '-log10(Adjusted P-value)'")  if alpha is None else print("")
        edges.sort_values(by="jaccard_coef", ascending=False,inplace=True)
        colormap = cm.get_cmap(cmap)  # Get the 'coolwarm' colormap
        G,ax=plot_ppi(
            interactions=edges,
            player1="src_name",
            player2="targ_name",
            weight="jaccard_coef",
            size=[
                    node["NES"] * 300 for _, node in nodes.iterrows()
                ] if size is None else size,  #  size nodes by NES
            facecolor=[colormap(node["NES"]) for _, node in nodes.iterrows()] if facecolor is None else facecolor,  # Color by FDR q-val
            linewidth=[node["NES"] * 300 for _, node in nodes.iterrows()] if linewidth is None else linewidth,
            linecolor=[node["NES"] * 300 for _, node in nodes.iterrows()] if linecolor is None else linecolor,
            linealpha=[node["NES"] * 300 for _, node in nodes.iterrows()] if linealpha is None else linealpha,
            alpha=[node["NES"] * 300 for _, node in nodes.iterrows()] if alpha is None else alpha,
            **kwargs
            )
        # except Exception as e:
        #     print(f"not work {n_top},{e}")
        return ax, G, nodes, edges

    
#! https://string-db.org/help/api/

import pandas as pd
import requests
import networkx as nx
import matplotlib.pyplot as plt
from io import StringIO
from py2ls import ips


def get_ppi(
    target_genes:list,
    species:int=9606, # "human"
    ci:float=0.1, # int 1~1000
    max_nodes:int=50,
    base_url:str="https://string-db.org",
    gene_mapping_api:str="/api/json/get_string_ids?",
    interaction_api:str="/api/tsv/network?",
):
    """
    Generate a Protein-Protein Interaction (PPI) network using STRINGdb data.

    return:
    the STRING protein-protein interaction (PPI) data, which contains information about 
    predicted and experimentally validated associations between proteins.
    
    stringId_A and stringId_B: Unique identifiers for the interacting proteins based on the 
    STRING database.
    preferredName_A and preferredName_B: Standard gene names for the interacting proteins.
    ncbiTaxonId: The taxon ID (9606 for humans).
    score: A combined score reflecting the overall confidence of the interaction, which aggregates different sources of evidence.

    nscore, fscore, pscore, ascore, escore, dscore, tscore: These are sub-scores representing the confidence in the interaction based on various evidence types:
    - nscore: Neighborhood score, based on genes located near each other in the genome.
    - fscore: Fusion score, based on gene fusions in other genomes.
    - pscore: Phylogenetic profile score, based on co-occurrence across different species.
    - ascore: Coexpression score, reflecting the likelihood of coexpression.
    - escore: Experimental score, based on experimental evidence.
    - dscore: Database score, from curated databases.
    - tscore: Text-mining score, from literature co-occurrence.

    Higher score values (closer to 1) indicate stronger evidence for an interaction.
    - Combined score: Useful for ranking interactions based on overall confidence. A score >0.7 is typically considered high-confidence.
    - Sub-scores: Interpret the types of evidence supporting the interaction. For instance:
    - High ascore indicates strong evidence of coexpression.
    - High escore suggests experimental validation.

    """
    print("check api: https://string-db.org/help/api/")
    
    # 将species转化为taxon_id
    if isinstance(species,str):
        print(species)
        species=list(get_taxon_id(species).values())[0]
        print(species)
        
    
    string_api_url = base_url + gene_mapping_api
    interaction_api_url = base_url + interaction_api
    # Map gene symbols to STRING IDs
    mapped_genes = {}
    for gene in target_genes:
        params = {"identifiers": gene, "species": species, "limit": 1}
        response = requests.get(string_api_url, params=params)
        if response.status_code == 200:
            try:
                json_data = response.json()
                if json_data:
                    mapped_genes[gene] = json_data[0]["stringId"]
            except ValueError:
                print(
                    f"Failed to decode JSON for gene {gene}. Response: {response.text}"
                )
        else:
            print(
                f"Failed to fetch data for gene {gene}. Status code: {response.status_code}"
            )
    if not mapped_genes:
        print("No mapped genes found in STRING database.")
        return None

    # Retrieve PPI data from STRING API
    string_ids = "%0d".join(mapped_genes.values())
    params = {
        "identifiers": string_ids,
        "species": species,
        "required_score": int(ci * 1000),
        "limit": max_nodes,
    }
    response = requests.get(interaction_api_url, params=params)

    if response.status_code == 200:
        try:
            interactions = pd.read_csv(StringIO(response.text), sep="\t")
        except Exception as e:
            print("Error reading the interaction data:", e)
            print("Response content:", response.text)
            return None
    else:
        print(
            f"Failed to retrieve interaction data. Status code: {response.status_code}"
        )
        print("Response content:", response.text)
        return None
    display(interactions.head())
    # Filter interactions by ci score
    if "score" in interactions.columns:
        interactions = interactions[interactions["score"] >= ci]
        if interactions.empty:
            print("No interactions found with the specified confidence.")
            return None
    else:
        print("The 'score' column is missing from the retrieved data. Unable to filter by confidence interval.")
    if "fdr" in interactions.columns:
        interactions=interactions.sort_values(by="fdr",ascending=False)
    return interactions
# * usage
# interactions = get_ppi(target_genes, ci=0.0001)

def plot_ppi(
    interactions,
    player1="preferredName_A",
    player2="preferredName_B",
    weight="score",
    n_layers=None,  # Number of concentric layers
    n_rank=[5, 10],  # Nodes in each rank for the concentric layout
    dist_node = 10,  # Distance between each rank of circles
    layout="degree", 
    size=None,#700,
    sizes=(50,500),# min and max of size
    facecolor="skyblue",
    cmap='coolwarm',
    edgecolor="k",
    edgelinewidth=1.5,
    alpha=.5,
    alphas=(0.1, 1.0),# min and max of alpha
    marker="o",
    node_hideticks=True,
    linecolor="gray",
    line_cmap='coolwarm',
    linewidth=1.5,
    linewidths=(0.5,5),# min and max of linewidth
    linealpha=1.0,
    linealphas=(0.1,1.0),# min and max of linealpha
    linestyle="-",
    line_arrowstyle='-',
    fontsize=10,
    fontcolor="k",
    ha:str="center",
    va:str="center",
    figsize=(12, 10),
    k_value=0.3,    
    bgcolor="w",
    dir_save="./ppi_network.html",
    physics=True,
    notebook=False,
    scale=1,
    ax=None,
    **kwargs
):
    """
    Plot a Protein-Protein Interaction (PPI) network with adjustable appearance.
    """
    from pyvis.network import Network
    import networkx as nx 
    from IPython.display import IFrame
    from matplotlib.colors import Normalize
    from matplotlib import cm
    # Check for required columns in the DataFrame
    for col in [player1, player2, weight]:
        if col not in interactions.columns:
            raise ValueError(f"Column '{col}' is missing from the interactions DataFrame.")
    interactions.sort_values(by=[weight], inplace=True)
    # Initialize Pyvis network
    net = Network(height="750px", width="100%", bgcolor=bgcolor, font_color=fontcolor)
    net.force_atlas_2based(
        gravity=-50, central_gravity=0.01, spring_length=100, spring_strength=0.1
    ) 
    net.toggle_physics(physics)

    kws_figsets = {}
    for k_arg, v_arg in kwargs.items():
        if "figset" in k_arg:
            kws_figsets = v_arg
            kwargs.pop(k_arg, None)
            break

    # Create a NetworkX graph from the interaction data
    G = nx.Graph()
    for _, row in interactions.iterrows():
        G.add_edge(row[player1], row[player2], weight=row[weight])
    # G = nx.from_pandas_edgelist(interactions, source=player1, target=player2, edge_attr=weight)


    # Calculate node degrees
    degrees = dict(G.degree())
    norm = Normalize(vmin=min(degrees.values()), vmax=max(degrees.values()))
    colormap = cm.get_cmap(cmap)  # Get the 'coolwarm' colormap

    if not ips.isa(facecolor, 'color'):
        print("facecolor: based on degrees")
        facecolor = [colormap(norm(deg)) for deg in degrees.values()]  # Use colormap
    num_nodes = G.number_of_nodes()
    #* size
    # Set properties based on degrees
    if not isinstance(size, (int,float,list)):
        print("size: based on degrees")
        size = [deg * 50 for deg in degrees.values()]  # Scale sizes
    size = (size[:num_nodes] if len(size) > num_nodes else size) if isinstance(size, list) else [size] * num_nodes
    if isinstance(size, list) and len(ips.flatten(size,verbose=False))!=1:
        # Normalize sizes
        min_size, max_size = sizes  # Use sizes tuple for min and max values
        min_degree, max_degree = min(size), max(size)
        if max_degree > min_degree:  # Avoid division by zero
            size = [
                min_size + (max_size - min_size) * (sz - min_degree) / (max_degree - min_degree)
                for sz in size
            ]
        else:
            # If all values are the same, set them to a default of the midpoint
            size = [(min_size + max_size) / 2] * len(size)

    #* facecolor
    facecolor = (facecolor[:num_nodes] if len(facecolor) > num_nodes else facecolor) if isinstance(facecolor, list) else [facecolor] * num_nodes
    # * facealpha
    if isinstance(alpha, list):
        alpha = (alpha[:num_nodes] if len(alpha) > num_nodes else alpha + [alpha[-1]] * (num_nodes - len(alpha)))
        min_alphas, max_alphas = alphas  # Use alphas tuple for min and max values
        if len(alpha) > 0:
            # Normalize alpha based on the specified min and max
            min_alpha, max_alpha = min(alpha), max(alpha)
            if max_alpha > min_alpha:  # Avoid division by zero
                alpha = [
                    min_alphas + (max_alphas - min_alphas) * (ea - min_alpha) / (max_alpha - min_alpha)
                    for ea in alpha
                ]
            else:
                # If all alpha values are the same, set them to the average of min and max
                alpha = [(min_alphas + max_alphas) / 2] * len(alpha)
        else:
            # Default to a full opacity if no edges are provided
            alpha = [1.0] * num_nodes  
    else:
        # If alpha is a single value, convert it to a list and normalize it
        alpha = [alpha] * num_nodes  # Adjust based on alphas

    for i, node in enumerate(G.nodes()):
        net.add_node(
            node,
            label=node,
            size=size[i],
            color=facecolor[i],
            alpha=alpha[i],
            font={"size": fontsize, "color": fontcolor},
        )
    print(f'nodes number: {i+1}')

    for edge in G.edges(data=True):
        net.add_edge(
            edge[0],
            edge[1],
            weight=edge[2]["weight"],
            color=edgecolor,
            width=edgelinewidth * edge[2]["weight"],
        )

    layouts = [
        "spring",
        "circular",
        "kamada_kawai",
        "random",
        "shell",
        "planar",
        "spiral",
        "degree"
    ]
    layout = ips.strcmp(layout, layouts)[0]
    print(f"layout:{layout}, or select one in {layouts}")
    
    # Choose layout
    if layout == "spring":
        pos = nx.spring_layout(G, k=k_value)
    elif layout == "circular":
        pos = nx.circular_layout(G)
    elif layout == "kamada_kawai":
        pos = nx.kamada_kawai_layout(G)
    elif layout == "spectral":
        pos = nx.spectral_layout(G)
    elif layout == "random":
        pos = nx.random_layout(G)
    elif layout == "shell":
        pos = nx.shell_layout(G)
    elif layout == "planar":
        if nx.check_planarity(G)[0]:
            pos = nx.planar_layout(G)
        else:
            print("Graph is not planar; switching to spring layout.")
            pos = nx.spring_layout(G, k=k_value)
    elif layout == "spiral":
        pos = nx.spiral_layout(G)
    elif layout=='degree':
        # Calculate node degrees and sort nodes by degree
        degrees = dict(G.degree())
        sorted_nodes = sorted(degrees.items(), key=lambda x: x[1], reverse=True)
        norm = Normalize(vmin=min(degrees.values()), vmax=max(degrees.values()))
        colormap = cm.get_cmap(cmap)
        
        # Create positions for concentric circles based on n_layers and n_rank
        pos = {}
        n_layers=len(n_rank)+1 if n_layers is None else n_layers
        for rank_index in range(n_layers):
            if rank_index < len(n_rank):
                nodes_per_rank = n_rank[rank_index]
                rank_nodes = sorted_nodes[sum(n_rank[:rank_index]): sum(n_rank[:rank_index + 1])]
            else:
                # 随机打乱剩余节点的顺序
                remaining_nodes = sorted_nodes[sum(n_rank[:rank_index]):]
                random_indices = np.random.permutation(len(remaining_nodes)) 
                rank_nodes = [remaining_nodes[i] for i in random_indices]

            radius = (rank_index + 1) * dist_node  # Radius for this rank

            # Arrange nodes in a circle for the current rank
            for i, (node, degree) in enumerate(rank_nodes):
                angle = (i / len(rank_nodes)) * 2 * np.pi  # Distribute around circle
                pos[node] = (radius * np.cos(angle), radius * np.sin(angle))

    else:
        print(f"Unknown layout '{layout}', defaulting to 'spring',or可以用这些: {layouts}")
        pos = nx.spring_layout(G, k=k_value)

    for node, (x, y) in pos.items():
        net.get_node(node)["x"] = x * scale
        net.get_node(node)["y"] = y * scale

    # If ax is None, use plt.gca()
    if ax is None:
        fig, ax = plt.subplots(1,1,figsize=figsize) 
    
    # Draw nodes, edges, and labels with customization options
    nx.draw_networkx_nodes(
        G,
        pos,
        ax=ax,
        node_size=size,
        node_color=facecolor,
        linewidths=edgelinewidth,
        edgecolors=edgecolor,
        alpha=alpha,
        hide_ticks=node_hideticks,
        node_shape=marker
    )

    #* linewidth
    if not isinstance(linewidth, list):
        linewidth = [linewidth] * G.number_of_edges()
    else:
        linewidth = (linewidth[:G.number_of_edges()] if len(linewidth) > G.number_of_edges() else linewidth + [linewidth[-1]] * (G.number_of_edges() - len(linewidth)))
        # Normalize linewidth if it is a list
        if isinstance(linewidth, list):
            min_linewidth, max_linewidth = min(linewidth), max(linewidth)
            vmin, vmax = linewidths  # Use linewidths tuple for min and max values
            if max_linewidth > min_linewidth:  # Avoid division by zero
                # Scale between vmin and vmax
                linewidth = [
                    vmin + (vmax - vmin) * (lw - min_linewidth) / (max_linewidth - min_linewidth)
                    for lw in linewidth
                ]
            else:
                # If all values are the same, set them to a default of the midpoint
                linewidth = [(vmin + vmax) / 2] * len(linewidth)
        else:
            # If linewidth is a single value, convert it to a list of that value
            linewidth = [linewidth] * G.number_of_edges()
    #* linecolor 
    if not isinstance(linecolor, str):  
        weights = [G[u][v]["weight"] for u, v in G.edges()]
        norm = Normalize(vmin=min(weights), vmax=max(weights))
        colormap = cm.get_cmap(line_cmap)
        linecolor = [colormap(norm(weight)) for weight in weights]
    else:
        linecolor = [linecolor] * G.number_of_edges()

    # * linealpha
    if isinstance(linealpha, list):
        linealpha = (linealpha[:G.number_of_edges()] if len(linealpha) > G.number_of_edges() else linealpha + [linealpha[-1]] * (G.number_of_edges() - len(linealpha)))
        min_alpha, max_alpha = linealphas  # Use linealphas tuple for min and max values
        if len(linealpha) > 0:
            min_linealpha, max_linealpha = min(linealpha), max(linealpha)
            if max_linealpha > min_linealpha:  # Avoid division by zero
                linealpha = [
                    min_alpha + (max_alpha - min_alpha) * (ea - min_linealpha) / (max_linealpha - min_linealpha)
                    for ea in linealpha
                ]
            else:
                linealpha = [(min_alpha + max_alpha) / 2] * len(linealpha)
        else:
            linealpha = [1.0] * G.number_of_edges() # 如果设置有误,则将它设置成1.0
    else:
        linealpha = [linealpha] * G.number_of_edges()  # Convert to list if single value
    nx.draw_networkx_edges(
        G, 
        pos, 
        ax=ax, 
        edge_color=linecolor, 
        width=linewidth,
        style=linestyle,
        arrowstyle=line_arrowstyle, 
        alpha=linealpha
    )
 
    nx.draw_networkx_labels(
        G, pos, ax=ax, font_size=fontsize, font_color=fontcolor,horizontalalignment=ha,verticalalignment=va
    )
    plot.figsets(ax=ax,**kws_figsets)
    ax.axis("off")
    if dir_save:
        if not os.path.basename(dir_save):
            dir_save="_.html"
        net.write_html(dir_save)
        nx.write_graphml(G, dir_save.replace(".html",".graphml"))  # Export to GraphML
        print(f"could be edited in Cytoscape \n{dir_save.replace(".html",".graphml")}")
        ips.figsave(dir_save.replace(".html",".pdf"))
    return G,ax


# * usage: 
# G, ax = bio.plot_ppi(
#     interactions,
#     player1="preferredName_A",
#     player2="preferredName_B",
#     weight="score",
#     # size="auto",
#     # size=interactions["score"].tolist(),
#     # layout="circ",
#     n_rank=[5, 10, 15],
#     dist_node=100,
#     alpha=0.6,
#     linecolor="0.8",
#     linewidth=1,
#     figsize=(8, 8.5),
#     cmap="jet",
#     edgelinewidth=0.5,
#     # facecolor="#FF5F57",
#     fontsize=10,
#     # fontcolor="b",
#     # edgecolor="r",
#     # scale=100,
#     # physics=False,
#     figsets=dict(title="ppi networks"),
# )
# figsave("./ppi_network.pdf")
  
def top_ppi(interactions, n_top=10):
    """
    Analyzes protein-protein interactions (PPIs) to identify key proteins based on
    degree and betweenness centrality.

    Parameters:
        interactions (pd.DataFrame): DataFrame containing PPI data with columns
                                      ['preferredName_A', 'preferredName_B', 'score'].

    Returns:
        dict: A dictionary containing the top key proteins by degree and betweenness centrality.
    """

    # Create a NetworkX graph from the interaction data
    G = nx.Graph()
    for _, row in interactions.iterrows():
        G.add_edge(row["preferredName_A"], row["preferredName_B"], weight=row["score"])

    # Calculate Degree Centrality
    degree_centrality = G.degree()
    key_proteins_degree = sorted(degree_centrality, key=lambda x: x[1], reverse=True)

    # Calculate Betweenness Centrality
    betweenness_centrality = nx.betweenness_centrality(G)
    key_proteins_betweenness = sorted(
        betweenness_centrality.items(), key=lambda x: x[1], reverse=True
    )
    print(
        {
            "Top 10 Key Proteins by Degree Centrality": key_proteins_degree[:10],
            "Top 10 Key Proteins by Betweenness Centrality": key_proteins_betweenness[
                :10
            ],
        }
    )
    # Return the top n_top key proteins
    if n_top == "all":
        return key_proteins_degree, key_proteins_betweenness
    else:
        return key_proteins_degree[:n_top], key_proteins_betweenness[:n_top]


# * usage: top_ppi(interactions)
# top_ppi(interactions, n_top="all")
# top_ppi(interactions, n_top=10)



species_dict = {
    "Human": "Homo sapiens",
    "House mouse": "Mus musculus",
    "Zebrafish": "Danio rerio",
    "Norway rat": "Rattus norvegicus",
    "Fruit fly": "Drosophila melanogaster",
    "Baker's yeast": "Saccharomyces cerevisiae",
    "Nematode": "Caenorhabditis elegans",
    "Chicken": "Gallus gallus",
    "Cattle": "Bos taurus",
    "Rice": "Oryza sativa",
    "Thale cress": "Arabidopsis thaliana",
    "Guinea pig": "Cavia porcellus",
    "Domestic dog": "Canis lupus familiaris",
    "Domestic cat": "Felis catus",
    "Horse": "Equus caballus",
    "Domestic pig": "Sus scrofa",
    "African clawed frog": "Xenopus laevis",
    "Great white shark": "Carcharodon carcharias",
    "Common chimpanzee": "Pan troglodytes",
    "Rhesus macaque": "Macaca mulatta",
    "Water buffalo": "Bubalus bubalis",
    "Lettuce": "Lactuca sativa",
    "Tomato": "Solanum lycopersicum",
    "Maize": "Zea mays",
    "Cucumber": "Cucumis sativus",
    "Common grape vine": "Vitis vinifera",
    "Scots pine": "Pinus sylvestris",
}


def get_taxon_id(species_list):
    """
    Convert species names to their corresponding taxon ID codes.

    Parameters:
    - species_list: List of species names (strings).

    Returns:
    - dict: A dictionary with species names as keys and their taxon IDs as values.
    """
    from Bio import Entrez

    if not isinstance(species_list, list):
        species_list = [species_list]
    species_list = [
        species_dict[ips.strcmp(i, ips.flatten(list(species_dict.keys())))[0]]
        for i in species_list
    ]
    taxon_dict = {}

    for species in species_list:
        try:
            search_handle = Entrez.esearch(db="taxonomy", term=species)
            search_results = Entrez.read(search_handle)
            search_handle.close()

            # Get the taxon ID
            if search_results["IdList"]:
                taxon_id = search_results["IdList"][0]
                taxon_dict[species] = int(taxon_id)
            else:
                taxon_dict[species] = None  # Not found
        except Exception as e:
            print(f"Error occurred for species '{species}': {e}")
            taxon_dict[species] = None  # Error in processing
    return taxon_dict


# # * usage: get_taxon_id("human")
# species_names = ["human", "nouse", "rat"]
# taxon_ids = get_taxon_id(species_names)
# print(taxon_ids)