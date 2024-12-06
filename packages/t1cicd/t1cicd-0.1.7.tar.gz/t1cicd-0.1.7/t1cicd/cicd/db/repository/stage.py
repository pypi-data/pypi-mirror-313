"""
This module contains the repository class for the Stage model.
"""

from uuid import UUID

from psycopg.rows import class_row

from t1cicd.cicd.db.model.stage import Stage, StageCreate
from t1cicd.cicd.db.repository.base import BaseRepository


class StageRepository(BaseRepository[Stage, StageCreate]):
    """
    Repository class for the Stage model.

    Provides methods to create, retrieve, update, and delete stages in the database.
    """

    async def create(self, item: StageCreate) -> Stage:
        query = """
        INSERT INTO stages ( 
            stage_name, pipeline_id, stage_order
        )
        VALUES (%s, %s, %s)
        RETURNING *
        """
        async with self.pool.connection() as conn:
            async with conn.cursor(row_factory=class_row(Stage)) as cur:
                result = await cur.execute(
                    query,
                    (
                        item.stage_name,
                        item.pipeline_id,
                        item.stage_order,
                    ),
                )

                return await result.fetchone()

    async def get(self, id: UUID) -> Stage | None:
        query = """
               SELECT 
                   s.*,
                   COALESCE(
                       (SELECT array_agg(j.id ORDER BY j.job_order)
                        FROM jobs j 
                        WHERE j.stage_id = s.id),
                       ARRAY[]::uuid[]
                   ) as job_ids
               FROM stages s 
               WHERE s.id = %s
               """
        async with self.pool.connection() as conn:
            async with conn.cursor(row_factory=class_row(Stage)) as cur:
                result = await cur.execute(query, (id,))
                return await result.fetchone()

    async def update(self, item: Stage) -> Stage | None:
        update_fields = item.model_dump(
            exclude={"id", "created_at", "job_ids"}, exclude_none=True
        )
        if not update_fields:
            return await self.get(item.id)
        set_clauses = [f"{field} = %s" for field in update_fields.keys()]
        params = list(update_fields.values())
        params.append(item.id)

        query = f"""
        UPDATE stages
        SET {', '.join(set_clauses)}
        WHERE id = %s
        RETURNING *
        """
        async with self.pool.connection() as conn:
            async with conn.cursor(row_factory=class_row(Stage)) as cur:
                result = await cur.execute(query, params)
                return await result.fetchone()

    async def delete(self, id: UUID) -> bool:
        query = """
        DELETE FROM stages WHERE id = %s
        """
        async with self.pool.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute(query, (id,))
                return cur.rowcount > 0
