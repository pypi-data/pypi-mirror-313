select entity_type,
       entity_id,
       source_type,
       source_table_full_name,
       target_type,
       target_table_full_name
from system.access.table_lineage
where source_table_full_name is not null
  and target_table_full_name is not null