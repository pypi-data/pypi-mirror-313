import base64
import getpass
import os
import re
import shutil
import subprocess  # nosec
from datetime import datetime, timezone
from distutils.dir_util import copy_tree
from pathlib import Path
from typing import List, Optional

import yaml
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from django.conf import settings
from django.core.management import CommandError

from restore.common_commands import CommonCommand


class Command(CommonCommand):
    help = (
        "Restore files or/and database backup from an environment (backup server) "
        "with encrypted secret file after decrypting it (secret file is defined in "
        "settings.BACKUP_CONF_FILE)"
    )

    def handle(self, *args, **options):
        # postgres_db, dump_name and files_path can be used as a django parameter
        # or as a command line parameter.
        # The command line has priority.
        if options["postgres_db"] is None:
            try:
                options["postgres_db"] = settings.USE_POSTGRES_DB
            except AttributeError:
                options["postgres_db"] = False

        if options["dump_name"] is None:
            try:
                options["dump_name"] = settings.DB_BACKUP_DUMP_NAME
            except AttributeError:
                options["dump_name"] = False

        if options["files_path"] is None:
            try:
                options["files_path"] = settings.FILES_BACKUP_PATH
            except AttributeError:
                options["files_path"] = False

        if options["encrypt"] is True and options["decrypt"] is True:
            return self.error(
                "You can not use both encrypt and decrypt options at the same time"
            )

        if options["era_only"] is True and options["deal"] is not None:
            return self.error(
                "You can not use both era_only and deal options at the same time"
            )
        if options["era_only"] is True and options["db_only"] is True:
            return self.error(
                "You can not use both era_only and db_only options at the same time"
            )

        if options["db_only"] is True and options["files_only"] is True:
            return self.error(
                "You can not use both db_only and files_only options at the same time"
            )

        if options["db_only"] is False and options["files_only"] is False:
            # it should manage both database and files if these options are not defined
            should_manage_app_and_db = True
        else:
            should_manage_app_and_db = False

        try:
            self.management(options, should_manage_app_and_db)
        except InvalidToken:
            return self.error("Invalid password")

    def management(self, options, should_manage_app_and_db):
        conf = self.get_backup_conf()
        key = self.create_key(confirm_password=options["encrypt"])

        if options["encrypt"] is True:
            # Just encrypt the conf file
            if should_manage_app_and_db is True or options["db_only"] is True:
                # Encrypt restic database backup configuration
                self.encrypt(conf, options["name_env"], "DB", key)
                self.success(
                    "Encryption of the configuration file of the Database backup "
                    "is completed."
                )

            if should_manage_app_and_db is True or options["files_only"] is True:
                # Encrypt restic documents backup configuration
                self.encrypt(conf, options["name_env"], "APP", key)
                self.success(
                    "Encryption of the configuration file of the Documents backup "
                    "is completed."
                )
        elif options["decrypt"] is True:
            # Just decrypt the conf file
            if should_manage_app_and_db is True or options["db_only"] is True:
                # Decrypt restic database backup configuration
                self.decrypt_and_save(conf, options["name_env"], "DB", key)
            if should_manage_app_and_db is True or options["files_only"] is True:
                # Decrypt restic documents backup configuration
                self.decrypt_and_save(conf, options["name_env"], "APP", key)
        elif options["show_secret"] is True:
            # Just show secrets
            if should_manage_app_and_db is True or options["db_only"] is True:
                # Show secrets of database backup configuration
                self.display_secret(conf, options["name_env"], "DB", key)
            if should_manage_app_and_db is True or options["files_only"] is True:
                # Show secrets of documents backup configuration
                self.display_secret(conf, options["name_env"], "APP", key)
        else:
            # decrypt conf file and restore backup
            db_conf = self.get_db_conf()
            if should_manage_app_and_db is True or options["db_only"] is True:
                # Restore or unlock database
                db_access = self.decrypt(conf, options["name_env"], "DB", key)
                self.set_restic_access(db_access)

                if options["unlock"] is True:
                    self.unlock_backups("db")
                elif options["list_snapshots"] is True:
                    self.list_snapshots()
                elif self.host_is_allowed() is True:
                    self.get_backup_db(
                        db_conf=db_conf,
                        backup_id=options["db_id"],
                        dump_name=options["dump_name"],
                        postgres_db=options["postgres_db"],
                    )

            if should_manage_app_and_db is True or options["files_only"] is True:
                # Restore or unlock app documents
                app_access = self.decrypt(conf, options["name_env"], "APP", key)
                self.set_restic_access(app_access)

                if options["unlock"] is True:
                    self.unlock_backups("app")
                elif options["list_snapshots"] is True:
                    self.list_snapshots()
                elif self.host_is_allowed() is True:
                    self.get_backup_documents(
                        options["files_id"],
                        options["deal"],
                        options["era_only"],
                        options["files_path"],
                    )

    def add_arguments(self, parser):
        parser.add_argument(
            "name_env",
            type=str,
            help="Name of env to back up "
            '(like primary for "digital ocean" and secondary for "aws")',
        ),
        parser.add_argument(
            "--encrypt",
            default=False,
            required=False,
            action="store_true",
            help="Just encrypt the file that contains "
            "secrets (tokens, password, etc.) of backup server "
            "(incompatible with --decrypt option)",
        )
        parser.add_argument(
            "--decrypt",
            default=False,
            required=False,
            action="store_true",
            help="Just decrypt the file that contains "
            "secrets (tokens, password, etc.) of backup server "
            "(incompatible with --encrypt option)",
        )
        parser.add_argument(
            "--db-only",
            default=False,
            required=False,
            action="store_true",
            help="Restore the backup of the database only "
            "(if --encrypt or --decrypt option is defined, "
            "just encrypt or decrypt the file that contains "
            "secrets (tokens, password, etc.) "
            "of DATABASE backup server "
            "(incompatible with --files-only option)",
        )
        parser.add_argument(
            "--files-only",
            default=False,
            required=False,
            action="store_true",
            help="Restore the backup of the database only "
            "(if --encrypt or --decrypt option is defined, "
            "just encrypt or decrypt the file that contains "
            "secrets (tokens, password, etc.) "
            "of FILES backup server "
            "(incompatible with --db-only option)",
        )
        parser.add_argument(
            "--db-id",
            default="latest",
            required=False,
            help="Parameter to specify the ID of the Database snapshot to restore.",
        )
        parser.add_argument(
            "--files-id",
            default="latest",
            required=False,
            help="Parameter to specify the ID of the Documents (MEDIA_ROOT) snapshot to restore.",
        )
        parser.add_argument(
            "--unlock",
            default=False,
            required=False,
            action="store_true",
            help="Unlock backup if there are locked",
        )
        parser.add_argument(
            "-ls",
            "--list-snapshots",
            default=False,
            required=False,
            action="store_true",
            help="List every backup available",
        )
        parser.add_argument(
            "--show-secret",
            default=False,
            required=False,
            action="store_true",
            help="show the secret decrypted configured for the environment selected",
        )
        parser.add_argument(
            "--deal",
            type=str,
            help="Deal folder that should be retrive",
        )
        parser.add_argument(
            "--postgres_db",
            default=None,
            required=False,
            action="store_true",
            help="Use postgres database, default: mysql",
        )
        parser.add_argument(
            "--dump_name",
            type=str,
            default=None,
            required=False,
            help="Name of dump",
        )
        parser.add_argument(
            "--files_path",
            type=str,
            default=None,
            required=False,
            help="Name of path of documents",
        )
        parser.add_argument(
            "--era-only",
            action="store_true",
            default=None,
            required=False,
            help="Restore only era-reconciliation "
            "of FILES backup server "
            "(incompatible with --db-only and --deal options)",
        )

    def get_db_conf(self):
        _db_instance = "default"

        db_configuration = {
            "USER": settings.DATABASES[_db_instance]["USER"],
            "PASSWORD": settings.DATABASES[_db_instance]["PASSWORD"],
            "NAME": settings.DATABASES[_db_instance]["NAME"],
            "HOST": settings.DATABASES[_db_instance]["HOST"],
            "PORT": settings.DATABASES[_db_instance]["PORT"],
        }

        return db_configuration

    def get_backup_conf(self):
        with open(settings.BACKUP_CONF_FILE) as file:
            conf = yaml.load(file, Loader=yaml.SafeLoader)
            return conf

    def encrypt(self, conf, env, type, key):
        f = Fernet(key)
        with open(conf[env][type], "rb") as file:
            file_data = file.read()
        encrypted_data = f.encrypt(file_data)
        with open(conf[env][type], "wb") as file:
            file.write(encrypted_data)

    def decrypt_and_save(self, conf, env, type, key):
        decrypted_data = self.decrypt(conf, env, type, key)
        backup = "Database" if type == "DB" else "Documents"
        with open(conf[env][type], "wb") as file:
            file.write(decrypted_data)
        self.success(
            f"Decryption of the configuration file of the {backup} backup "
            "is completed. Be careful !"
        )

    def decrypt(self, conf, env, type, key):
        f = Fernet(key)
        with open(conf[env][type], "rb") as file:
            encrypted_data = file.read()
        decrypted_data = f.decrypt(encrypted_data)
        return decrypted_data

    def display_secret(self, conf, env, type, key):
        decrypted_data = self.decrypt(conf, env, type, key)
        backup = "Database" if type == "DB" else "Documents"
        self.success(f"{backup} secrets:")
        print(decrypted_data.decode("utf-8"))

    def create_key(self, confirm_password=False):
        matching_passwords: bool = False
        pw: str

        if confirm_password is True:
            while matching_passwords is False:
                pw = getpass.getpass("Password:")
                confirm_pw = getpass.getpass("Confirm password:")

                if pw == confirm_pw:
                    matching_passwords = True
                else:
                    self.error("Passwords do not match. Please retry.")
        else:
            pw = getpass.getpass("Password:")

        password = pw.encode("utf-8")
        salt = os.urandom(0)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password))
        return key

    def set_restic_access(self, access):
        access_str = access.decode("utf-8")
        os.environ["AWS_ACCESS_KEY_ID"] = re.search(
            'AWS_ACCESS_KEY_ID="(.+)"', access_str
        ).group(1)
        os.environ["AWS_SECRET_ACCESS_KEY"] = re.search(
            'AWS_SECRET_ACCESS_KEY="(.+)"', access_str
        ).group(1)
        os.environ["RESTIC_REPOSITORY"] = re.search(
            'RESTIC_REPOSITORY="(.+)"', access_str
        ).group(1)
        os.environ["RESTIC_PASSWORD"] = re.search(
            'RESTIC_PASSWORD="(.+)"', access_str
        ).group(1)

        # self.success(os.environ)

    def get_backup_db(
        self,
        db_conf,
        backup_id,
        dump_name: str,
        postgres_db: bool,
    ):
        self.info(f"Requested: {os.environ['RESTIC_REPOSITORY']}\n")

        self.info(
            "The configuration of the database to which you will restore the data:"
        )
        self.info(f"\tDatabase: {db_conf['NAME']}")
        self.info(f"\tUser: {db_conf['USER']}")
        self.info(f"\tHost: {db_conf['HOST']}")
        self.info(f"\tPort: {db_conf['PORT']}")

        self.warning(
            "The database must be empty before continuing with the restore command. "
            "Drop and recreate a database manually before proceeding if this is not the case."
        )

        pw = input("Do you want to continue ? (type y for yes)\n")
        if pw != "y":
            self.error("Restoration canceled")
            return

        if postgres_db:
            dump_file_path = f"dump_{backup_id}.sql"

            self.warning(
                f"WARNING. You should remove database dump file ("
                + dump_file_path
                + ") on this system after the restoration."
            )

            remove_dump_file_after_restore = False
            if backup_id == "latest":
                # to avoid different latest dump
                remove_dump_file_after_restore = True
            else:
                pw = input(
                    "Do you want to remove it after database restoration ? (tape n for no)\n"
                )
                if pw != "n":
                    remove_dump_file_after_restore = True

            self.info(
                "Database restoration in progress... Started at "
                + self.get_datetime_now()
            )

            errors = ""

            if os.path.isfile(dump_file_path):
                self.info(
                    "Download skipped. The dump file already exists locally. "
                    "It is it that will be used for the restoration."
                )
            else:
                self.info("Downloading dump...")
                dump_file = open(dump_file_path, "wb")

                p1 = subprocess.Popen(  # nosec
                    ["restic", "dump", backup_id, dump_name],
                    stdout=dump_file,
                    stderr=subprocess.PIPE,
                )
                (output1, err1) = p1.communicate()
                errors += err1.decode("utf-8")

                dump_file.flush()
                dump_file.close()

            if len(errors) == 0:
                os.environ["PGPASSWORD"] = db_conf["PASSWORD"]
                p2 = subprocess.Popen(  # nosec
                    [
                        "pg_restore",
                        "-Fc",
                        "-d",
                        db_conf["NAME"],
                        "-U",
                        db_conf["USER"],
                        "-h",
                        db_conf["HOST"],
                    ]
                    + (["-p", db_conf["PORT"]] if "PORT" in db_conf else [])
                    + (["-1", dump_file_path]),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )

                self.info("Dump loading...")
                (output2, err2) = p2.communicate()
                errors = err2.decode("utf-8") + errors

                if remove_dump_file_after_restore:
                    os.remove(dump_file_path)
                    self.info("Dump file (" + dump_file_path + ") removed.")
        else:
            self.info(
                "Database restoration in progress... Started at "
                + self.get_datetime_now()
            )
            p1 = subprocess.Popen(  # nosec
                ["restic", "dump", backup_id, dump_name],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            p2 = subprocess.Popen(  # nosec
                ["pigz", "-d"],
                stdin=p1.stdout,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            p3 = subprocess.Popen(  # nosec
                [
                    "mysql",
                    "-u",
                    db_conf["USER"],
                    db_conf["NAME"],
                    f"-p{db_conf['PASSWORD']}",
                ]
                + (["-h", db_conf["HOST"]] if "HOST" in db_conf else []),
                stdin=p2.stdout,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            (output3, err3) = p3.communicate()
            (output2, err2) = p2.communicate()
            (output1, err1) = p1.communicate()
            errors = err3.decode("utf-8") + err2.decode("utf-8") + err1.decode("utf-8")
        if len(errors) != 0:
            self.error(
                "Restoration of database not completed:\n"
                f"-----------------\n {errors} -----------------\n"
            )
            self.unlock_backups("DB")
        else:
            self.success(
                "Restoration of database completed. " + self.get_datetime_now()
            )

    def unlock_backups(self, repo_name):
        p1 = subprocess.Popen(  # nosec
            [
                "restic",
                "unlock",
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        (output, err) = p1.communicate()
        if len(err.decode("utf-8")) == 0:
            self.success(f"Backups are unlocked for {repo_name}.")
        else:
            self.error(
                f"Backups have not been unlocked for {repo_name}:\n"
                + err.decode("utf-8")
            )

    def list_snapshots(self):
        p1 = subprocess.Popen(  # nosec
            [
                "restic",
                "snapshots",
            ],
        )
        p1.communicate()

        self.info("Time is UTC.")

    def get_backup_documents(
        self,
        backup_id,
        deal,
        era,
        files_path: str,
    ):
        self.info(f"Requested: {os.environ['RESTIC_REPOSITORY']}")
        self.warning(
            "Warning: When restoring from backup, only folders that exist in both MEDIA_ROOT and the backup will be "
            "overwritten. Any existing folder in MEDIA_ROOT that isn't in the backup will be preserved. To ensure "
            "MEDIA_ROOT exactly matches the backup state, please clear your MEDIA_ROOT folder before restoration."
        )
        self.info("Files restoration in progress... " + self.get_datetime_now())

        restore_arg = [
            "restic",
            "restore",
            backup_id,
            "--target",
            "/tmp/restic/",
        ]

        if deal is not None:
            restore_arg.extend(["--include", deal])
        elif era is True:
            restore_arg.extend(["--include", "era-reconciliation"])

        restic_tmp_directory = "/tmp/restic"

        # remove restic tmp directory to avoid environment conflict:
        # we cannot determine the environment directory if there are several
        if os.path.exists(restic_tmp_directory):
            shutil.rmtree(restic_tmp_directory)
        os.mkdir(restic_tmp_directory, 0o755)

        # Download MEDIA_ROOT documents from backup in temporary directory
        p = subprocess.Popen(restore_arg)  # nosec
        (output, err) = p.communicate()
        p.wait()
        location = Path(restic_tmp_directory)

        try:
            # Gets the path of the temporary backup folder if it is not empty
            documents_path = next(iter(location.rglob(f"**/{files_path}/")))
        except StopIteration:
            self.warning("Error while browsing the backup folder: The backup folder for the files appears to be empty.")
            return

        copy_tree(
            str(documents_path),
            files_path + "/",
        )

        # clean tmp directory after restoration
        shutil.rmtree(location)
        os.mkdir(restic_tmp_directory, 0o755)
        self.success("Restoration of documents completed. " + self.get_datetime_now())

    @staticmethod
    def get_datetime_now() -> str:
        return datetime.now(timezone.utc).strftime("%Y-%d-%m %H:%M:%S") + " (UTC)"

    @staticmethod
    def get_allowed_hosts() -> Optional[List[str]]:
        try:
            allowed_hosts = settings.ALLOWED_RESTIC_HOSTS
        except AttributeError:
            raise CommandError(
                "Allowed hosts must be provided. "
                "You should set up hosts in ALLOWED_RESTIC_HOSTS setting."
            )
        else:
            return allowed_hosts

    def host_is_allowed(self) -> bool:
        is_allowed = False

        if settings.DEBUG is True:
            is_allowed = True

        elif os.environ["RESTIC_REPOSITORY"] in self.get_allowed_hosts():
            is_allowed = True

        elif self.get_allowed_hosts() in [None, []]:
            self.error(
                "Operation denied. You should set up hosts in ALLOWED_RESTIC_HOSTS setting"
            )
            is_allowed = False

        elif os.environ["RESTIC_REPOSITORY"] not in self.get_allowed_hosts():
            self.error(
                "Operation denied. "
                f"{ os.environ['RESTIC_REPOSITORY'] } is not in the list "
                f"of allowed hosts ({ self.get_allowed_hosts() })."
            )
            is_allowed = False

        return is_allowed
