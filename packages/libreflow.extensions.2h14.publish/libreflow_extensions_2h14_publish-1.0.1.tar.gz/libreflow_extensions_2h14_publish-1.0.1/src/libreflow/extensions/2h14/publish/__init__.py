import time
import os
import shutil
from kabaret import flow
from kabaret.flow.object import _Manager
from kabaret.flow_entities.entities import EntityCollection, Entity, Property
from libreflow.baseflow.file import TrackedFile
from libreflow.baseflow.task_manager import DefaultTaskFile


class DefaultTaskChoiceValue(flow.values.ChoiceValue):

    def choices(self):
        return [
            dft_task.display_name.get()
            for dft_task in self.root().project().get_default_tasks().mapped_items()
        ]


class DefaultFileChoiceValue(flow.values.ChoiceValue):

    _action = flow.Parent()

    def choices(self):
        if not self._action.task_name.get():
            return []

        _mgr = self.root().project().get_task_manager()

        return [
            file_name
            for n, (file_name, _, _, _, _, _, _, _, _, _, _, _) in _mgr.get_task_files(self._action.task_name.get().lower()).items()
        ]
    
    def revert_to_default(self):
        names = self.choices()
        self.set(names[0] if names else None)


class AddPublishRelation(flow.Action):

    task_name = flow.Param([], DefaultTaskChoiceValue).watched()
    file_name = flow.Param([], DefaultFileChoiceValue)

    _map = flow.Parent()

    def needs_dialog(self):
        return True

    def allow_context(self, context):
        return context

    def get_buttons(self):
        self.task_name.set('Animatic')
        return ['Create', 'Cancel']

    def child_value_changed(self, child_value):
        if child_value is self.task_name:
            self.file_name.revert_to_default()
    
    def run(self, button):
        if button == 'Cancel':
            return
        
        self._map.add_publish_relation(dict(
            name=f'relation_{str(int(time.time()))}',
            task_name=self.task_name.get(),
            file_name=self.file_name.get()
        ))


class RemovePublishRelation(flow.Action):

    ICON = ('icons.gui', 'remove-symbol')

    _relation = flow.Parent()
    _map = flow.Parent(2)

    def needs_dialog(self):
        return False

    def allow_context(self, context):
        return context

    def run(self, button):
        self._map.delete_publish_relation(self._relation.name())


class PublishRelation(Entity):

    task_name = Property()
    file_name = Property()

    remove = flow.Child(RemovePublishRelation)


class PublishRelations(EntityCollection):

    add_relation = flow.Child(AddPublishRelation)

    @classmethod
    def mapped_type(cls):
        return PublishRelation

    def add_publish_relation(self, data):
        c = self.get_entity_store().get_collection(
            self.collection_name())
        c.insert_one(data)
        self._document_cache = None
        self.touch()

    def delete_publish_relation(self, name):
        c = self.get_entity_store().get_collection(
            self.collection_name())
        c.delete_one(
            {'name': name}
        )
        self._document_cache = None
        self.touch()
    
    def get_publish_relation(self, task_name):
        match = [relation for relation in self.mapped_items() if relation.task_name.get() == task_name]
        return match[0] if match else None

    def columns(self):
        return ["Task", "File"]

    def _fill_row_cells(self, row, item):
        row["Task"] = item.task_name.get()
        row["File"] = item.file_name.get()


class PublishTaskChoiceValue(flow.values.ChoiceValue):

    _file = flow.Parent(2)
    _task = flow.Parent(4)

    def choices(self):
        _mgr = self.root().project().get_task_manager()
        _dft_file = _mgr.default_tasks[self._task.name()].files[self._file.name()]

        return [
            relation.task_name.get()
            for relation in _dft_file.publish_relations.mapped_items()
        ]


class PublishNextTask(flow.Action):
    _MANAGER_TYPE = _Manager

    ICON = ("icons.libreflow", "publish")

    _file = flow.Parent()
    _task = flow.Parent(3)
    _tasks = flow.Parent(4)

    target_task = flow.Param([], PublishTaskChoiceValue)

    def get_buttons(self):
        self.message.set("<h2>Publish To Next Task</h2>")

        return ['Publish', 'Cancel']

    def allow_context(self, context):
        return (
            context
            and self._file.get_revision_names(sync_status='Available', published_only=True)
            and self.target_task.choices() != []
        )

    def _create_file(self, target_task, default_file):
        session = self.root().session()

        file_name = default_file.file_name.get()
        name, ext = os.path.splitext(file_name)
        target_file = None

        # Create default file
        if ext:
            if target_task.files.has_file(name, ext[1:]) is False:
                session.log_info(f'[Publish Next Task] Creating File {file_name}')
                target_file = target_task.files.add_file(
                    name, ext[1:],
                    display_name=file_name,
                    tracked=True,
                    default_path_format=default_file.path_format.get()
                )
                target_file.file_type.set(default_file.file_type.get())
                target_file.is_primary_file.set(default_file.is_primary_file.get())
            else:
                session.log_info(f'[Publish Next Task] File {file_name} exists')
                target_file = target_task.files[default_file.name()]
        else:
            if target_task.files.has_folder(name) is False:
                session.log_info(f'[Publish Next Task] Creating Folder {file_name}')
                target_file = target_task.files.add_folder(
                    name,
                    display_name=file_name,
                    tracked=True,
                    default_path_format=default_file.path_format.get()
                )
            else:
                session.log_info(f'[Publish Next Task] Folder {file_name} exists')
                target_file = target_task.files[default_file.name()]

        return target_file

    def publish_file(self, target_file):
        session = self.root().session()
        file_name = target_file.display_name.get()
        name, ext = os.path.splitext(file_name)

        source_revision = self._file.get_head_revision(sync_status='Available')

        if source_revision is not None and os.path.exists(source_revision.get_path()):
            r = target_file.add_revision(comment=f'from {self._file.display_name.get()} {source_revision.name()}')
            session.log_info(f'[Publish Next Task] Creating Revision {target_file.display_name.get()} {r.name()}')

            target_path = r.get_path()
            os.makedirs(os.path.dirname(target_path), exist_ok=True)
            
            session.log_info(f'[Publish Next Task] Copying Source Revision')

            if ext:
                shutil.copy2(source_revision.get_path(), target_path)
            else:
                shutil.copytree(source_revision.get_path(), target_path)

    def run(self, button):
        if button == "Cancel":
            return

        # Get publish relation file name
        _mgr = self.root().project().get_task_manager()
        current_dft_file = _mgr.default_tasks[self._task.name()].files[self._file.name()]

        relation = current_dft_file.publish_relations.get_publish_relation(self.target_task.get())

        # Get default file data
        target_dft_file = _mgr.default_tasks[relation.task_name.get().lower()].files[relation.file_name.get().replace('.', '_')]
        
        # Get target task shot
        if self._tasks.has_mapped_name(relation.task_name.get().lower()):
            target_task_object = self._tasks[relation.task_name.get().lower()]

            # Create file
            target_file = self._create_file(target_task_object, target_dft_file)
            
            # Create revision
            self.publish_file(target_file)


def publish_action(parent):
    if isinstance(parent, TrackedFile):
        r = flow.Child(PublishNextTask).ui(label='Publish to next task')
        r.name = 'publish_next_task'
        r.index = 28
        return r
    if isinstance(parent, DefaultTaskFile):
        r = flow.Child(PublishRelations)
        r.name = 'publish_relations'
        r.index = 13
        return r


def install_extensions(session):
    return {
        "2h14_publish": [
            publish_action,
        ]
    }


from . import _version
__version__ = _version.get_versions()['version']
