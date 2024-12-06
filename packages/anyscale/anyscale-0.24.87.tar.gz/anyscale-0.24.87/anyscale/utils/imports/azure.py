import click


# TODO: type the return value
def try_import_azure_storage_blob_BlobServiceClient():
    try:
        from azure.storage.blob import BlobServiceClient

        return BlobServiceClient
    except ImportError:
        raise click.ClickException(
            "pip package `azure-storage-blob` is not installed locally on this machine but required "
            "for the command. Please install with `pip install 'anyscale[azure]'`."
        )
