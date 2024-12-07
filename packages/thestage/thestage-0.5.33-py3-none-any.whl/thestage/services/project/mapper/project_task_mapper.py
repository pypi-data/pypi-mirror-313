from typing import Optional

from thestage.entities.project_task import ProjectTaskEntity
from thestage.services.abstract_mapper import AbstractMapper
from thestage.services.task.dto.task_dto import TaskDto


class ProjectTaskMapper(AbstractMapper):

    def build_entity(self, item: TaskDto) -> Optional[ProjectTaskEntity]:
        if not item:
            return None

        return ProjectTaskEntity(
            id=item.id or '',
            title=item.title or '',
            status=item.frontend_status.status_translation or '',
            docker_container_id=item.docker_container_id or '',
            docker_container_slug=(str(item.docker_container.slug) or '') if item.docker_container else '',
            started_at=item.started_at or '',
            finished_at=item.finished_at or '',
        )
