from prefect import Flow
from prefect import Parameter

from berpublicsearch import convert
from berpublicsearch import download


with Flow("Download BERPublicsearch.zip & convert to parquet") as flow:

    path_to_berpublicsearch_zip = Parameter("path_to_berpublicsearch_zip")
    path_to_berpublicsearch_temp = "BERPublicsearch_temp"
    path_to_berpublicsearch_parquet = Parameter("path_to_berpublicsearch_parquet")

    download_berpublicsearch_zip = download.download(
        email_address, path_to_berpublicsearch_zip
    )
    unzip_berpublicsearch_zip = convert.unzip(
        path_to_berpublicsearch_zip, path_to_berpublicsearch_temp
    )
    convert_berpublicsearch_to_parquet = convert.convert(
        path_to_berpublicsearch_temp, path_to_berpublicsearch_parquet
    )
    delete_berpublicsearch_temp = convert.delete_folder(path_to_berpublicsearch_temp)

    unzip_berpublicsearch_zip.set_upstream(download_berpublicsearch_zip)
    convert_berpublicsearch_to_parquet.set_upstream(unzip_berpublicsearch_zip)
    delete_berpublicsearch_temp.set_upstream(convert_berpublicsearch_to_parquet)
