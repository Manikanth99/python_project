from mstrio.object_management.migration.migration import Migration

def run_undo_migration():
    conn = connect_to_mstr(
        base_url="https://env/MicroStrategyLibrary/api",
        username="admin",
        password="password",
        project_name="MainProject"
    )

    if not conn:
        return

    undo_file_path = load_package_file(r"\\network-drive\undo-package.mmp")

    try:
        Migration.migrate_from_file(
            connection=conn,
            file_path=undo_file_path,
            name="UndoMigration",
            project_id=conn.project_id,
            comments="Undo process"
        )
        refresh_schema(conn)
        notify_user("team@company.com", "UNDO Success", "Undo package applied successfully.")
    except Exception as e:
        notify_user("team@company.com", "UNDO FAILED", str(e))
