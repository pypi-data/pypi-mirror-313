"""
This module contains the repository class for the Artifact model.
"""

from uuid import UUID

from psycopg.rows import class_row

from t1cicd.cicd.db.model.artifact import Artifact, ArtifactCreate
from t1cicd.cicd.db.repository.base import BaseRepository


class ArtifactRepository(BaseRepository[Artifact, ArtifactCreate]):
    """
    Repository class for the Artifact model.

    Provides methods to create, retrieve, update, and delete artifacts in the database.
    """

    async def create(self, item: ArtifactCreate) -> Artifact:
        query = """
        INSERT INTO artifacts (
            job_id, file_path, file_size, expiry_date
        )
        VALUES (%s, %s, %s, %s)
        RETURNING *
        """
        async with self.pool.connection() as conn:
            async with conn.cursor(row_factory=class_row(Artifact)) as cur:
                result = await cur.execute(
                    query,
                    (
                        item.job_id,
                        item.file_path,
                        item.file_size,
                        item.expiry_date,
                    ),
                )
                return await result.fetchone()

    async def get(self, id: UUID) -> Artifact | None:
        query = """
        SELECT * FROM artifacts WHERE id = %s
        """
        async with self.pool.connection() as conn:
            async with conn.cursor(row_factory=class_row(Artifact)) as cur:
                result = await cur.execute(query, (id,))
                return await result.fetchone()

    async def update(self, item: Artifact) -> Artifact | None:
        update_fields = item.model_dump(
            exclude={"id", "created_at", "job_id", "file_path", "file_size"},
            exclude_none=True,
        )
        if not update_fields:
            return await self.get(item.id)
        set_clauses = [f"{field} = %s" for field in update_fields.keys()]
        params = list(update_fields.values())
        params.append(item.id)

        query = f"""
        UPDATE artifacts
        SET {', '.join(set_clauses)}
        WHERE id = %s
        RETURNING *
        """
        async with self.pool.connection() as conn:
            async with conn.cursor(row_factory=class_row(Artifact)) as cur:
                result = await cur.execute(query, params)
                return await result.fetchone()

    async def delete(self, id: UUID) -> bool:
        query = """
        DELETE FROM artifacts WHERE id = %s
        """
        async with self.pool.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute(query, (id,))
                return cur.rowcount > 0
