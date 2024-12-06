from typing import Dict, List, Optional

import tabulate

from anyscale.cli_logger import LogsLogger
from anyscale.client.openapi_client.models.create_resource_quota import (
    CreateResourceQuota,
)
from anyscale.client.openapi_client.models.list_resource_quotas_query import (
    ListResourceQuotasQuery,
)
from anyscale.client.openapi_client.models.quota import Quota
from anyscale.client.openapi_client.models.resource_quota import ResourceQuota
from anyscale.client.openapi_client.models.resource_quota_status import (
    ResourceQuotaStatus,
)
from anyscale.cloud import get_cloud_id_and_name
from anyscale.controllers.base_controller import BaseController
from anyscale.project import get_project_id_for_cloud_from_name
from anyscale.sdk.anyscale_client.models.page_query import PageQuery
from anyscale.sdk.anyscale_client.models.text_query import TextQuery
from anyscale.utils.user_utils import get_user_id_by_email


class ResourceQuotaController(BaseController):
    def __init__(self):
        super().__init__()
        self.log = LogsLogger()

    def create(  # noqa: PLR0913
        self,
        name: str,
        cloud: str,
        project: Optional[str] = None,
        user_email: Optional[str] = None,
        num_cpus: Optional[int] = None,
        num_instances: Optional[int] = None,
        num_gpus: Optional[int] = None,
        num_accelerators: Optional[Dict[str, int]] = None,
    ) -> str:

        cloud_id, _ = get_cloud_id_and_name(self.api_client, cloud_name=cloud)
        project_id = (
            get_project_id_for_cloud_from_name(
                project, cloud_id, self.api_client, self.anyscale_api_client
            )
            if project
            else None
        )
        user_id = (
            get_user_id_by_email(self.api_client, user_email) if user_email else None
        )

        create_resource_quota = CreateResourceQuota(
            name=name,
            cloud_id=cloud_id,
            project_id=project_id,
            user_id=user_id,
            quota=Quota(
                num_cpus=num_cpus,
                num_instances=num_instances,
                num_gpus=num_gpus,
                num_accelerators=num_accelerators,
            ),
        )

        with self.log.spinner("Creating resource quota..."):
            resource_quota_id = self.api_client.create_resource_quota_api_v2_resource_quotas_post(
                create_resource_quota
            ).result.id

        create_resource_quota_message = [f"Name: {name}\nCloud name: {cloud}"]
        if project:
            create_resource_quota_message.append(f"Project name: {project}")
        if user_email:
            create_resource_quota_message.append(f"User email: {user_email}")
        if num_cpus:
            create_resource_quota_message.append(f"Number of CPUs: {num_cpus}")
        if num_instances:
            create_resource_quota_message.append(
                f"Number of instances: {num_instances}"
            )
        if num_gpus:
            create_resource_quota_message.append(f"Number of GPUs: {num_gpus}")
        if num_accelerators:
            create_resource_quota_message.append(
                f"Number of accelerators: {dict(num_accelerators)}"
            )

        self.log.info("\n".join(create_resource_quota_message))
        self.log.info(f"Resource quota created successfully ID: {resource_quota_id}")

        return resource_quota_id

    def _format_resource_quotas(self, resource_quotas: List[ResourceQuota]) -> str:
        table_rows = []
        for resource_quota in resource_quotas:
            table_rows.append(
                [
                    resource_quota.id,
                    resource_quota.name,
                    resource_quota.cloud_id,
                    resource_quota.project_id,
                    resource_quota.user_id,
                    resource_quota.is_enabled,
                    resource_quota.created_at.strftime("%m/%d/%Y"),
                    resource_quota.deleted_at.strftime("%m/%d/%Y")
                    if resource_quota.deleted_at
                    else None,
                    resource_quota.quota,
                ]
            )
        table = tabulate.tabulate(
            table_rows,
            headers=[
                "ID",
                "NAME",
                "CLOUD ID",
                "PROJECT ID",
                "USER ID",
                "IS ENABLED",
                "CREATED AT",
                "DELETED AT",
                "QUOTA",
            ],
            tablefmt="plain",
        )

        return f"Resource quotas:\n{table}"

    def list_resource_quotas(
        self,
        *,
        name: Optional[str] = None,
        cloud: Optional[str] = None,
        creator_id: Optional[str] = None,
        is_enabled: Optional[bool] = None,
        max_items: int = 20,
    ) -> List[ResourceQuota]:
        cloud_id, _ = (
            get_cloud_id_and_name(self.api_client, cloud_name=cloud)
            if cloud
            else (None, None)
        )

        resource_quotas = self.api_client.search_resource_quotas_api_v2_resource_quotas_search_post(
            ListResourceQuotasQuery(
                name=TextQuery(equals=name) if name else None,
                cloud_id=cloud_id,
                creator_id=creator_id,
                is_enabled=is_enabled,
                paging=PageQuery(count=max_items),
            )
        ).results

        print(self._format_resource_quotas(resource_quotas))
        return resource_quotas

    def delete(self, resource_quota_id: str,) -> None:
        """
        Delete a resource quota.
        """
        with self.log.spinner("Deleting resource quota..."):
            self.api_client.delete_resource_quota_api_v2_resource_quotas_resource_quota_id_delete(
                resource_quota_id
            )

        self.log.info(
            f"Resource quota with ID {resource_quota_id} deleted successfully."
        )

    def set_status(self, resource_quota_id: str, *, is_enabled: bool,) -> None:
        """
        Set the status of a resource quota.
        """
        with self.log.spinner("Setting resource quota status..."):
            self.api_client.set_resource_quota_status_api_v2_resource_quotas_resource_quota_id_status_patch(
                resource_quota_id, ResourceQuotaStatus(is_enabled=is_enabled)
            )

        self.log.info(
            f"{'Enabled' if is_enabled else 'Disabled'} resource quota with ID {resource_quota_id} successfully."
        )
