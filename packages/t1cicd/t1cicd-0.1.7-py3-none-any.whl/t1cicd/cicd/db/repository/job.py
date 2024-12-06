"""
This module contains the repository class for the Job model.
"""

from uuid import UUID

from psycopg.rows import class_row

from t1cicd.cicd.db.model.job import Job, JobCreate
from t1cicd.cicd.db.repository.base import BaseRepository


class JobRepository(BaseRepository[Job, JobCreate]):
    """
    Repository class for the Job model.

    Provides methods to create, retrieve, update, and delete jobs in the database.
    """

    async def create(self, item: JobCreate) -> Job:
        """
        Create a new job

        Args:
            item (JobCreate): The job to create

        Returns:
            Job: The created job

        """
        query = """
        INSERT INTO jobs (
            stage_id, job_name, job_order, allow_failure
        )
        VALUES (%s, %s, %s, %s)
        RETURNING *
        """
        async with self.pool.connection() as conn:
            async with conn.cursor(row_factory=class_row(Job)) as cur:
                result = await cur.execute(
                    query,
                    (
                        item.stage_id,
                        item.job_name,
                        item.job_order,
                        item.allow_failure,
                    ),
                )

                return await result.fetchone()

    async def get(self, id: UUID) -> Job | None:
        """

        Get a job from the database

        Args:
            id (UUID): The job id

        Returns:
            Job | None: The job if found, otherwise None

        """
        query = """
        SELECT j.*,
            COALESCE(
                (SELECT array_agg(a.id ORDER BY a.id)
                 FROM artifacts a 
                 WHERE a.job_id = j.id),
                ARRAY[]::uuid[]
            ) as artifact_ids
        FROM jobs j 
        WHERE j.id = %s
        """
        async with self.pool.connection() as conn:
            async with conn.cursor(row_factory=class_row(Job)) as cur:
                result = await cur.execute(query, (id,))
                return await result.fetchone()

    async def update(self, item: Job) -> Job | None:
        """

        Update a job in the database

        Args:
            item (Job): The job to update

        Returns:
            Job | None: The updated job if found, otherwise None


        """
        update_fields = item.model_dump(
            exclude={"id", "created_at", "artifact_ids"}, exclude_none=True
        )
        if not update_fields:
            return await self.get(item.id)
        set_clauses = [f"{field} = %s" for field in update_fields.keys()]
        params = list(update_fields.values())
        params.append(item.id)

        query = f"""
        UPDATE jobs
        SET {', '.join(set_clauses)}
        WHERE id = %s
        RETURNING *, 
            COALESCE(
                (SELECT array_agg(a.id ORDER BY a.id)
                 FROM artifacts a
                 WHERE a.job_id = jobs.id),
                ARRAY[]::uuid[]
            ) as artifact_ids
        """
        async with self.pool.connection() as conn:
            async with conn.cursor(row_factory=class_row(Job)) as cur:
                result = await cur.execute(query, params)
                return await result.fetchone()

    async def delete(self, id: UUID) -> bool:
        """

        Delete a job from the database

        Args:
            id (UUID): The job id

        Returns:
            bool: True if the job was deleted, otherwise False

        """
        query = """
        DELETE FROM jobs WHERE id = %s
        """
        async with self.pool.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute(query, (id,))
                return cur.rowcount > 0
