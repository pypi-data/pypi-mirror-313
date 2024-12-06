import os
import subprocess
import platform

from kabaret import flow
from kabaret.flow.object import _Manager
from libreflow.baseflow.file import GenericRunAction,TrackedFile,TrackedFolder,FileRevisionNameChoiceValue,MarkImageSequence
from libreflow.baseflow.task import Task
from libreflow.utils.os import remove_folder_content

class RenderQualityChoiceValue(flow.values.ChoiceValue):
    CHOICES = ['Preview','Final']


class RenderTvPaintPlayblast(flow.Action):

    ICON = ('icons.libreflow', 'tvpaint')

    _file = flow.Parent()
    _files = flow.Parent(2)
    _task = flow.Parent(3)
    _shot = flow.Parent(5)
    _sequence = flow.Parent(7)

    revision = flow.Param(None, FileRevisionNameChoiceValue)
    render_quality  = flow.Param("Preview",RenderQualityChoiceValue)

    with flow.group('Advanced settings'):
        start_frame = flow.IntParam()
        end_frame = flow.IntParam()
        show_reference = flow.BoolParam(False)
        keep_existing_frames = flow.BoolParam(True)

    
    def allow_context(self, context):
        return (
            context
            and self._file.format.get() == 'tvpp'
            )

    def get_buttons(self):
        self.revision.revert_to_default()
        self.start_frame.revert_to_default()
        self.end_frame.revert_to_default()
        return ['Render', 'Cancel']

    def ensure_render_folder(self):
        folder_name = self._file.display_name.get().split('.')[0]
        folder_name += '_render'
        if self.render_quality.get() == 'Preview':
            folder_name += '_preview'

        if not self._files.has_folder(folder_name):
            self._files.create_folder_action.folder_name.set(folder_name)
            self._files.create_folder_action.category.set('Outputs')
            self._files.create_folder_action.tracked.set(True)
            self._files.create_folder_action.run(None)
        
        return self._files[folder_name]
    
    def ensure_render_folder_revision(self):
        folder = self.ensure_render_folder()
        revision_name = self.revision.get()
        revisions = folder.get_revisions()
        source_revision = self._file.get_revision(self.revision.get())
        
        if not folder.has_revision(revision_name):
            revision = folder.add_revision(revision_name)
            folder.set_current_user_on_revision(revision_name)
        else:
            revision = folder.get_revision(revision_name)
        
        revision.comment.set(source_revision.comment.get())
        
        folder.ensure_last_revision_oid()
        
        self._files.touch()
        
        return revision
    
    def start_tvpaint(self, path):
        start_action = self._task.start_tvpaint
        start_action.file_path.set(path)
        ret = start_action.run(None)
        self.tvpaint_runner = self.root().session().cmds.SubprocessManager.get_runner_info(ret['runner_id'])

    def execute_render_script(self, path, start_frame, end_frame, render_quality):
        exec_script = self._file.execute_render_playblast_script
        exec_script.output_path.set(path)
        exec_script.start_frame.set(start_frame)
        exec_script.end_frame.set(end_frame)
        exec_script.render_quality.set(render_quality)
        exec_script.show_ref.set(show_reference)
        exec_script.run(None)
    
    def _export_audio(self):
        export_audio = self._file.export_ae_audio
        ret = export_audio.run('Export')
        return ret
    
    def _mark_image_sequence(self, folder_name, revision_name, render_pid):
        mark_sequence_wait = self._file.mark_image_sequence_wait
        mark_sequence_wait.folder_name.set(folder_name)
        mark_sequence_wait.revision_name.set(revision_name)
        mark_sequence_wait.wait_pid(render_pid)
        mark_sequence_wait.run(None)
    
    def run(self, button):
        if button == 'Cancel':
            return

        rev = self._file.get_revision(self.revision.get())
        self.start_tvpaint(rev.get_path())
        
        output_name =  f"{self._sequence.name()}_{self._shot.name()}.#.png"
        output_path = os.path.join(self.ensure_render_folder_revision().get_path(),output_name)

        if (os.path.exists(os.path.split(output_path)[0]) 
            and self.keep_existing_frames.get() is False):
            remove_folder_content(os.path.split(output_path)[0])

        self.execute_render_script(output_path,self.start_frame.get(),self.end_frame.get(),self.render_quality.get())
        self._export_audio()

        # Configure image sequence marking
        folder_name = self._file.name()[:-len(self._file.format.get())]
        folder_name += 'render'
        if self.render_quality.get() == 'Preview':
            folder_name += '_preview'
        revision_name = self.revision.get()
        self._mark_image_sequence(
            folder_name,
            revision_name,
            render_pid=self.tvpaint_runner['pid']
        )

class ExportAudio(flow.Action):

    _file = flow.Parent()
    _files = flow.Parent(2)
    _shot = flow.Parent(5)

    audio_path = flow.Param(None)

    def allow_context(self, context):
        return context
    
    def get_audio_path(self):
        return self.audio_path.get()
    
    def get_animatic_path(self):
        if not self._shot.tasks.has_mapped_name('animatic'):
            return None
        task = self._shot.tasks['animatic']
        if not task.files.has_file('animatic', 'mov'):
            return None
        rev = task.files['animatic_mov'].get_head_revision()
        if (rev is None) \
            or (rev.get_sync_status() != 'Available'):
            return None
        path = rev.get_path()
        return path if os.path.isfile(path) else None

    def run(self, button):
        if button == 'Cancel':
            return
        
        audio_source_path = self.get_animatic_path()
        if audio_source_path is not None and os.path.exists(audio_source_path) :
            _audio_path = audio_source_path.replace('.mov','.wav')
            print(audio_source_path)
            print(_audio_path)
            print(f'ffmpeg -i {audio_source_path} -map 0:a {_audio_path} -y')
            subprocess.call(f'ffmpeg -i {audio_source_path} -map 0:a {_audio_path} -y', shell=True)
            self.audio_path.set(_audio_path)
        else : 
            self.root().session().log_warning("No audio found")

class MarkImageSeqTvPaint(MarkImageSequence):
    
    def _get_audio_path(self):
        scene_name = re.search(r"(.+?(?=_render))", self._folder.name()).group()
        scene_name += '_tvpp'
        
        print('scene_name', scene_name)
            
        if not self._files.has_mapped_name(scene_name):
            print('[GET_AUDIO_PATH] Scene not found')
            return None
        
        print('get_audio_path', self._files[scene_name].export_ae_audio.get_audio_path())
            
        return self._files[scene_name].export_ae_audio.get_audio_path()
        

class StartTvPaint(GenericRunAction):

    file_path = flow.Param()

    def allow_context(self, context):
        return context

    def runner_name_and_tags(self):
        return 'TvPaint', []

    def target_file_extension(self):
        return 'tvpp'

    def extra_argv(self):
        return [self.file_path.get()]


class ExecuteRenderPlayblastScript(GenericRunAction):

    output_path = flow.Param()
    start_frame = flow.IntParam()
    end_frame = flow.IntParam()
    render_quality = flow.Param()
    show_ref = flow.Param()

    def allow_context(self, context):
        return False
    
    def runner_name_and_tags(self):
        return 'PythonRunner', []

    def get_version(self, button):
        return None

    def get_run_label(self):
        return "Render TvPaint Playblast"

    def extra_argv(self):
        current_dir = os.path.split(__file__)[0]
        script_path = os.path.normpath(os.path.join(current_dir,"scripts/render.py"))
        return [script_path, '--output-path', self.output_path.get(), '--start-frame',self.start_frame.get() ,'--end-frame',self.end_frame.get(),'--render-quality',self.render_quality.get(),'--show-ref',self.show_ref.get()]



def start_tvpaint(parent):
    if isinstance(parent, Task):
        r = flow.Child(StartTvPaint)
        r.name = 'start_tvpaint'
        r.index = None
        r.ui(hidden=True)
        return r

def export_audio(parent):
    if isinstance(parent, TrackedFile) \
        and (parent.name().endswith('_tvpp')):
        r = flow.Child(ExportAudio)
        r.name = 'export_ae_audio'
        r.index = None
        r.ui(hidden=True)
        return r

def render_tvpaint_playblast(parent):
    if isinstance(parent, TrackedFile) \
        and (parent.name().endswith('_tvpp')):
        r = flow.Child(RenderTvPaintPlayblast)
        r.name = 'render_tvpaint_playblast'
        r.index = None
        return r

def execute_render_playblast_script(parent):
    if isinstance(parent, TrackedFile) \
        and (parent.name().endswith('_tvpp')):
        r = flow.Child(ExecuteRenderPlayblastScript)
        r.name = 'execute_render_playblast_script'
        r.index = None
        r.ui(hidden=True)
        return r

def mark_sequence_tvpaint(parent):
    if isinstance(parent, TrackedFolder):
        r = flow.Child(MarkImageSeqTvPaint)
        r.name = 'mark_image_sequence'
        r.index = None
        return r


def install_extensions(session):
    return {
        "tvpaint_playblast": [
            start_tvpaint,
            render_tvpaint_playblast,
            execute_render_playblast_script,
            export_audio,
            mark_sequence_tvpaint
        ]
    }


from . import _version
__version__ = _version.get_versions()['version']
