from mstrio.connection import Connection
from mstrio.object_management.migration.migration import Migration
import smtplib

# --------------------------------------------------------------------------
# Step 1: Connect to MicroStrategy
# --------------------------------------------------------------------------
def connect_to_mstr(base_url, username, password, project_name):
    try:
        conn = Connection(base_url, username, password, project_name=project_name)
        print("Connected to MicroStrategy.")
        return conn
    except Exception as e:
        print(f"Connection failed: {e}")
        return None

# --------------------------------------------------------------------------
# Step 2: Load Package from File (.mmp)
# --------------------------------------------------------------------------
def load_package_file(file_path):
    print(f"Loaded package from: {file_path}")
    return file_path

# --------------------------------------------------------------------------
# Step 3: Apply Package & Create Undo
# --------------------------------------------------------------------------
def apply_package_with_undo(connection, file_path, project_id):
    try:
        migration = Migration.migrate_from_file(
            connection=connection,
            file_path=file_path,
            name="Migration_Job",
            project_id=project_id,
            comments="Automated migration",
            generate_undo=True
        )
        print("Package applied successfully.")
        return True
    except Exception as e:
        print(f"Package apply failed: {e}")
        return False

# --------------------------------------------------------------------------
# Step 4: Refresh Schema
# --------------------------------------------------------------------------
def refresh_schema(connection):
    try:
        connection.post('/api/model/schema/refresh')
        print("Schema refresh executed.")
    except Exception as e:
        print("Schema refresh failed:", e)

# --------------------------------------------------------------------------
# Step 5: Notify via Email
# --------------------------------------------------------------------------
def notify_user(email, subject, body):
    # Fill your SMTP config
    pass

# --------------------------------------------------------------------------
# MAIN WORKFLOW
# --------------------------------------------------------------------------
def run_package_migration():
    conn = connect_to_mstr(
        base_url="https://env/MicroStrategyLibrary/api",
        username="admin",
        password="password",
        project_name="MainProject"
    )

    if not conn:
        return

    file_path = load_package_file(r"\\network-drive\migration.mmp")
    success = apply_package_with_undo(conn, file_path, conn.project_id)

    if success:
        refresh_schema(conn)
        notify_user("team@company.com", "Migration Success", "Package migration succeeded.")
    else:
        notify_user("team@company.com", "Migration FAILED", "Package migration failed.")
