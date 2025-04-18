class SQLQuery:
    CREATE_ASSETS_TABLE_QUERY = """
            CREATE TABLE IF NOT EXISTS assets (
                asset_name TEXT,
                asset_version INTEGER,
                asset_description TEXT,
                asset_type TEXT,
                asset_binary BLOB,
                is_deployed BOOLEAN DEFAULT 0,
                deployment_time TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (asset_name, asset_version)
            )
        """

    CREATE_EXPERIMENTS_TABLE_QUERY = """
                    CREATE TABLE IF NOT EXISTS experiments (
                        experiment_id TEXT PRIMARY KEY,
                        model BLOB,
                        asset BLOB,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """

    INSERT_EXPERIMENT_QUERY = """
                            INSERT INTO experiments (
                                    experiment_id,
                                    model,
                                    asset,
                                    created_at
                            ) VALUES (?, ?, ?, ?)"""

    CREATE_EXPERIMENT_RESULT_TABLE_QUERY = """
                    CREATE TABLE IF NOT EXISTS experiment_result (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        experiment_id TEXT,
                        dataset_record_id TEXT,
                        inference TEXT,
                        prompt_tokens INTEGER,
                        completion_tokens INTEGER,
                        latency_ms REAL,
                        evaluation BLOB,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY(experiment_id) REFERENCES experiments(experiment_id)
                    )
                """

    INSERT_BATCH_EXPERIMENT_RESULT_QUERY = """
                                INSERT INTO experiment_result (
                                        experiment_id,
                                        dataset_record_id,
                                        inference,
                                        prompt_tokens,
                                        completion_tokens,
                                        latency_ms,
                                        evaluation,
                                        created_at
                                ) VALUES (
                                        :experiment_id,
                                        :dataset_record_id,
                                        :inference,
                                        :prompt_tokens,
                                        :completion_tokens,
                                        :latency_ms,
                                        :evaluation,
                                        :created_at)
            """

    INSERT_ASSETS_QUERY = """INSERT INTO assets(
                                    asset_name, 
                                    asset_version, 
                                    asset_description, 
                                    asset_type, 
                                    asset_binary,
                                    created_at
                                ) VALUES(?, ?, ?, ?, ?, ?)"""

    SELECT_ASSET_QUERY = """SELECT  asset_name, 
                                    asset_description, 
                                    asset_version, 
                                    asset_type, 
                                    asset_binary,
                                    created_at
                            FROM assets
                            WHERE asset_name = ? AND asset_version = ?"""

    SELECT_ASSET_BY_NAME_QUERY = """SELECT  asset_name, 
                                    asset_description, 
                                    asset_version, 
                                    asset_type, 
                                    asset_binary,
                                    created_at
                            FROM assets
                            WHERE asset_name = ? AND asset_version = (SELECT MAX(asset_version) FROM assets WHERE asset_name = ?)"""

    SELECT_ASSET_BY_TYPE_QUERY = """SELECT  
                                    asset_name, 
                                    asset_description, 
                                    asset_version, 
                                    asset_type, 
                                    asset_binary,
                                    is_deployed,
                                    deployment_time,
                                    created_at
                            FROM assets WHERE asset_type = ?"""

    SELECT_DATASET_FILE_PATH_QUERY = """SELECT 
                                            json_extract(asset_binary, '$.file_path') AS file_path 
                                        FROM assets 
                                        WHERE asset_name =  ? AND asset_version = ?"""

    SELECT_EXPERIMENTS_QUERY = """
                                SELECT
                                    e.experiment_id,
                                    concat(json_extract(model, '$.inference_model_type'), ' - ' ,json_extract(model, '$.inference_model_name')) AS inference_model,
                                    concat(json_extract(model, '$.embedding_model_type'), ' - ' ,json_extract(model, '$.embedding_model_name')) AS embedding_model,
                                    json_extract(asset, '$.prompt_template_name') AS prompt_template_name,
                                    json_extract(asset, '$.prompt_template_version') AS prompt_template_version,
                                    json_extract(asset, '$.dataset_name') AS dataset_name,
                                    json_extract(asset, '$.dataset_version') AS dataset_version,
                                    er.dataset_record_id as dataset_record_id,
                                    er.inference as inference,
                                    er.prompt_tokens as prompt_tokens,
                                    er.completion_tokens as completion_tokens,
                                    er.latency_ms as latency_ms,
                                    er.evaluation as evaluation,
                                    a.asset_binary
                                FROM experiments e
                                JOIN experiment_result er on 
                                    e.experiment_id = er.experiment_id 
                                JOIN assets a ON
                                    a.asset_name = prompt_template_name AND a.asset_version = prompt_template_version
                                """

    DEPLOY_ASSET_QUERY = """UPDATE assets SET is_deployed = 1, deployment_time = CURRENT_TIMESTAMP WHERE asset_name = ? and asset_version = ?"""
