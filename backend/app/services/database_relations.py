
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.models import Database, DatabaseRecord, RollupCache
from app.schemas.database import RelationConfig

class DatabaseRelationManager:
    def __init__(self, db: Session):
        self.db = db

    async def handle_relation_update(self,
                                   record_id: int,
                                   property_name: str,
                                   related_ids: List[int],
                                   relation_config: RelationConfig) -> None:
        """관계형 프로퍼티 업데이트 처리"""
        # 기존 관계 삭제
        self.db.execute(
            """DELETE FROM database_relations 
               WHERE source_record_id = :record_id 
               AND relation_type = :property_name""",
            {"record_id": record_id, "property_name": property_name}
        )

        # 새로운 관계 추가
        for related_id in related_ids:
            self.db.execute(
                """INSERT INTO database_relations 
                   (source_record_id, target_record_id, relation_type)
                   VALUES (:source_id, :target_id, :relation_type)""",
                {
                    "source_id": record_id,
                    "target_id": related_id,
                    "relation_type": property_name
                }
            )

        # 양방향 관계 처리
        if relation_config.reverse_property:
            await self._handle_reverse_relation(
                record_id, related_ids,
                relation_config.reverse_property
            )

        # 관련 롤업 값 업데이트
        await self._update_related_rollups(record_id, property_name)

    async def get_related_records(self,
                                  record_id: int,
                                  property_name: str) -> List[Dict[str, Any]]:
        """관계된 레코드 조회"""
        records = self.db.execute(
            """SELECT r.* FROM database_records r
               JOIN database_relations rel 
               ON r.id = rel.target_record_id
               WHERE rel.source_record_id = :record_id
               AND rel.relation_type = :property_name""",
            {"record_id": record_id, "property_name": property_name}
        ).fetchall()

        return [dict(record) for record in records]

    async def _handle_reverse_relation(self,
                                       source_id: int,
                                       target_ids: List[int],
                                       reverse_property: str) -> None:
        """양방향 관계 처리"""
        # 기존 역방향 관계 삭제
        self.db.execute(
            """DELETE FROM database_relations 
               WHERE target_record_id = :source_id 
               AND relation_type = :reverse_property""",
            {"source_id": source_id, "reverse_property": reverse_property}
        )

        # 새로운 역방향 관계 추가
        for target_id in target_ids:
            self.db.execute(
                """INSERT INTO database_relations 
                   (source_record_id, target_record_id, relation_type)
                   VALUES (:target_id, :source_id, :reverse_property)""",
                {
                    "target_id": target_id,
                    "source_id": source_id,
                    "reverse_property": reverse_property
                }
            )

    async def _update_related_rollups(self,
                                      record_id: int,
                                      relation_property: str) -> None:
        """관련된 롤업 값들 업데이트"""
        # 해당 레코드와 관련된 모든 롤업 프로퍼티 찾기
        rollups = self.db.execute(
            """SELECT rc.* FROM rollup_cache rc
               JOIN database_relations rel 
               ON rc.record_id = rel.source_record_id
               WHERE rel.target_record_id = :record_id
               AND rel.relation_type = :relation_property""",
            {"record_id": record_id, "relation_property": relation_property}
        ).fetchall()

        # 각 롤업 값 재계산
        from app.services.database_compute import DatabaseCompute
        compute_service = DatabaseCompute()

        for rollup in rollups:
            record = self.db.query(DatabaseRecord).get(rollup.record_id)
            if not record:
                continue

            # 관련 레코드들 가져오기
            related_records = await self.get_related_records(
                record.id,
                rollup.property_name
            )

            # 롤업 값 재계산
            new_value = await compute_service.compute_rollup(
                record.rollup_cache.get(rollup.property_name, {}),
                related_records,
                rollup.property_name
            )

            # 캐시 업데이트
            self.db.query(RollupCache).filter_by(
                id=rollup.id
            ).update({
                "value": new_value,
                "updated_at": datetime.utcnow()
            })

    async def get_bidirectional_relations(self,
                                          record_id: int) -> Dict[str, List[int]]:
        """양방향 관계 정보 조회"""
        forward_relations = self.db.execute(
            """SELECT relation_type, target_record_id 
               FROM database_relations
               WHERE source_record_id = :record_id""",
            {"record_id": record_id}
        ).fetchall()

        backward_relations = self.db.execute(
            """SELECT relation_type, source_record_id 
               FROM database_relations
               WHERE target_record_id = :record_id""",
            {"record_id": record_id}
        ).fetchall()

        relations = {}

        # 정방향 관계 처리
        for rel_type, target_id in forward_relations:
            if rel_type not in relations:
                relations[rel_type] = []
            relations[rel_type].append(target_id)

        # 역방향 관계 처리
        for rel_type, source_id in backward_relations:
            reverse_key = f"reverse_{rel_type}"
            if reverse_key not in relations:
                relations[reverse_key] = []
            relations[reverse_key].append(source_id)

        return relations

    async def validate_relation(self,
                                source_database_id: int,
                                target_database_id: int,
                                relation_config: RelationConfig) -> bool:
        """관계 유효성 검증"""
        source_db = self.db.query(Database).get(source_database_id)
        target_db = self.db.query(Database).get(target_database_id)

        if not source_db or not target_db:
            return False

        # 순환 참조 검사
        if source_database_id == target_database_id:
            # 자기 참조는 허용하되, 순환 참조는 금지
            if relation_config.reverse_property:
                existing_relations = self._check_circular_reference(
                    source_database_id,
                    target_database_id
                )
                if existing_relations:
                    return False

        return True

    def _check_circular_reference(self,
                                  source_db_id: int,
                                  target_db_id: int,
                                  visited: set = None) -> bool:
        """순환 참조 검사"""
        if visited is None:
            visited = set()

        if source_db_id in visited:
            return True

        visited.add(source_db_id)

        relations = self.db.execute(
            """SELECT DISTINCT target_database_id 
               FROM database_relations dr
               JOIN database_records r ON dr.target_record_id = r.id
               WHERE r.database_id = :db_id""",
            {"db_id": source_db_id}
        ).fetchall()

        for relation in relations:
            related_db_id = relation[0]
            if self._check_circular_reference(related_db_id, target_db_id, visited):
                return True

        visited.remove(source_db_id)
        return False