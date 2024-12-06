
import gradio as gr
from app import demo as app
import os

_docs = {'PyannoteViewer': {'description': "Creates an audio component that can be used to visualize pyannote's pipelines outputs.\nCan only be used as an output component.\n\nSee https://github.com/pyannote/pyannote-audio for more informations about pyannote", 'members': {'__init__': {'value': {'type': 'str\n    | pathlib.Path\n    | tuple[int, numpy.ndarray]\n    | Callable\n    | None', 'default': 'None', 'description': 'A path, URL, or [sample_rate, numpy array] tuple (sample rate in Hz, audio data as a float or int numpy array) for the default value that SourceViewer component is going to take. If callable, the function will be called whenever the app loads to set the initial value of the component.'}, 'sources': {'type': 'list["upload" | "microphone"] | None', 'default': 'None', 'description': 'A list of sources permitted for audio. "upload" creates a box where user can drop an audio file, "microphone" creates a microphone input. The first element in the list will be used as the default source. If None, defaults to ["upload", "microphone"], or ["microphone"] if `streaming` is True.'}, 'type': {'type': '"numpy" | "filepath"', 'default': '"numpy"', 'description': 'The format the audio file is converted to before being passed into the prediction function. "numpy" converts the audio to a tuple consisting of: (int sample rate, numpy.array for the data), "filepath" passes a str path to a temporary file containing the audio.'}, 'label': {'type': 'str | None', 'default': 'None', 'description': 'The label for this component. Appears above the component and is also used as the header if there are a table of examples for this component. If None and used in a `gr.Interface`, the label will be the name of the parameter this component is assigned to.'}, 'every': {'type': 'float | None', 'default': 'None', 'description': "If `value` is a callable, run the function 'every' number of seconds while the client connection is open. Has no effect otherwise. The event can be accessed (e.g. to cancel it) via this component's .load_event attribute."}, 'show_label': {'type': 'bool | None', 'default': 'None', 'description': 'if True, will display label.'}, 'container': {'type': 'bool', 'default': 'True', 'description': 'If True, will place the component in a container - providing some extra padding around the border.'}, 'scale': {'type': 'int | None', 'default': 'None', 'description': 'Relative width compared to adjacent Components in a Row. For example, if Component A has scale=2, and Component B has scale=1, A will be twice as wide as B. Should be an integer.'}, 'min_width': {'type': 'int', 'default': '160', 'description': 'Minimum pixel width, will wrap if not sufficient screen space to satisfy this value. If a certain scale value results in this Component being narrower than min_width, the min_width parameter will be respected first.'}, 'interactive': {'type': 'bool | None', 'default': 'None', 'description': 'If True, will allow users to upload and edit an audio file. If False, can only be used to play audio. If not provided, this is inferred based on whether the component is used as an input or output.'}, 'visible': {'type': 'bool', 'default': 'True', 'description': 'If False, component will be hidden.'}, 'streaming': {'type': 'bool', 'default': 'False', 'description': 'If set to True when used in a `live` interface as an input, will automatically stream webcam feed. When used set as an output, takes audio chunks yield from the backend and combines them into one streaming audio output.'}, 'elem_id': {'type': 'str | None', 'default': 'None', 'description': 'An optional string that is assigned as the id of this component in the HTML DOM. Can be used for targeting CSS styles.'}, 'elem_classes': {'type': 'list[str] | str | None', 'default': 'None', 'description': 'An optional list of strings that are assigned as the classes of this component in the HTML DOM. Can be used for targeting CSS styles.'}, 'render': {'type': 'bool', 'default': 'True', 'description': 'If False, component will not render be rendered in the Blocks context. Should be used if the intention is to assign event listeners now but render the component later.'}, 'format': {'type': '"wav" | "mp3"', 'default': '"wav"', 'description': 'The file format to save audio files. Either \'wav\' or \'mp3\'. wav files are lossless but will tend to be larger files. mp3 files tend to be smaller. Default is wav. Applies both when this component is used as an input (when `type` is "format") and when this component is used as an output.'}, 'autoplay': {'type': 'bool', 'default': 'False', 'description': 'Whether to automatically play the audio when the component is used as an output. Note: browsers will not autoplay audio files if the user has not interacted with the page yet.'}, 'show_download_button': {'type': 'bool | None', 'default': 'None', 'description': 'If True, will show a download button in the corner of the component for saving audio. If False, icon does not appear. By default, it will be True for output components and False for input components.'}, 'show_share_button': {'type': 'bool | None', 'default': 'None', 'description': 'If True, will show a share icon in the corner of the component that allows user to share outputs to Hugging Face Spaces Discussions. If False, icon does not appear. If set to None (default behavior), then the icon appears if this Gradio app is launched on Spaces, but not otherwise.'}, 'editable': {'type': 'bool', 'default': 'True', 'description': 'If True, allows users to manipulate the audio file if the component is interactive. Defaults to True.'}, 'min_length': {'type': 'int | None', 'default': 'None', 'description': 'The minimum length of audio (in seconds) that the user can pass into the prediction function. If None, there is no minimum length.'}, 'max_length': {'type': 'int | None', 'default': 'None', 'description': 'The maximum length of audio (in seconds) that the user can pass into the prediction function. If None, there is no maximum length.'}, 'waveform_options': {'type': 'WaveformOptions | dict | None', 'default': 'None', 'description': 'A dictionary of options for the waveform display. Options include: waveform_color (str), waveform_progress_color (str), show_controls (bool), skip_length (int), trim_region_color (str). Default is None, which uses the default values for these options.'}}, 'postprocess': {'value': {'type': 'tuple[\n        pyannote.core.annotation.Annotation,\n        numpy.ndarray | pathlib.Path | str,\n    ]\n    | None', 'description': 'expects audio data in any of these formats: a `str` or `pathlib.Path` filepath or URL to an audio file, or a `bytes` object (recommended for streaming), or a `tuple` of (sample rate in Hz, audio data as numpy array). Note: if audio is supplied as a numpy array, the audio will be normalized by its peak value to avoid distortion or clipping in the resulting audio.'}}, 'preprocess': {'return': {'type': 'str | tuple[int, numpy.ndarray] | None', 'description': 'passes audio as one of these formats (depending on `type`): a `str` filepath, or `tuple` of (sample rate in Hz, audio data as numpy array). If the latter, the audio data is a 16-bit `int` array whose values range from -32768 to 32767 and shape of the audio data array is (samples,) for mono audio or (samples, channels) for multi-channel audio.'}, 'value': None}}, 'events': {'stream': {'type': None, 'default': None, 'description': 'This listener is triggered when the user streams the PyannoteViewer.'}, 'change': {'type': None, 'default': None, 'description': 'Triggered when the value of the PyannoteViewer changes either because of user input (e.g. a user types in a textbox) OR because of a function update (e.g. an image receives a value from the output of an event trigger). See `.input()` for a listener that is only triggered by user input.'}, 'clear': {'type': None, 'default': None, 'description': 'This listener is triggered when the user clears the PyannoteViewer using the X button for the component.'}, 'play': {'type': None, 'default': None, 'description': 'This listener is triggered when the user plays the media in the PyannoteViewer.'}, 'pause': {'type': None, 'default': None, 'description': 'This listener is triggered when the media in the PyannoteViewer stops for any reason.'}, 'stop': {'type': None, 'default': None, 'description': 'This listener is triggered when the user reaches the end of the media playing in the PyannoteViewer.'}, 'start_recording': {'type': None, 'default': None, 'description': 'This listener is triggered when the user starts recording with the PyannoteViewer.'}, 'pause_recording': {'type': None, 'default': None, 'description': 'This listener is triggered when the user pauses recording with the PyannoteViewer.'}, 'stop_recording': {'type': None, 'default': None, 'description': 'This listener is triggered when the user stops recording with the PyannoteViewer.'}, 'upload': {'type': None, 'default': None, 'description': 'This listener is triggered when the user uploads a file into the PyannoteViewer.'}}}, '__meta__': {'additional_interfaces': {'WaveformOptions': {'source': '@dataclasses.dataclass\nclass WaveformOptions:\n    waveform_color: str | None = None\n    waveform_progress_color: str | None = None\n    trim_region_color: str | None = None\n    show_recording_waveform: bool = True\n    show_controls: bool = False\n    skip_length: int | float = 5\n    sample_rate: int = 44100'}}, 'user_fn_refs': {'PyannoteViewer': []}}}

abs_path = os.path.join(os.path.dirname(__file__), "css.css")

with gr.Blocks(
    css=abs_path,
    theme=gr.themes.Default(
        font_mono=[
            gr.themes.GoogleFont("Inconsolata"),
            "monospace",
        ],
    ),
) as demo:
    gr.Markdown(
"""
# `pyannote_viewer`

<div style="display: flex; gap: 7px;">
<img alt="Static Badge" src="https://img.shields.io/badge/version%20-%201.0.0%20-%20orange">  
</div>

Gradio custom component to visualize pyannote's pipelines outputs
""", elem_classes=["md-custom"], header_links=True)
    app.render()
    gr.Markdown(
"""
## Installation

```bash
pip install pyannote_viewer
```

## Usage

```python
import gradio as gr
from pyannote_viewer import PyannoteViewer
from pyannote.audio import Pipeline
import os


def apply_pipeline(audio: str) -> tuple:
    pipeline = Pipeline.from_pretrained(
        "pyannote/speech-separation-ami-1.0", use_auth_token=os.environ["HF_TOKEN"]
    )

    # pipeline = Pipeline.from_pretrained(
    #     "pyannote/speaker-diarization-3.1", use_auth_token=os.environ["HF_TOKEN"]
    # )


    outputs = pipeline(audio)
    if isinstance(outputs, tuple):
        return outputs
    else:
        return (outputs, audio)


with gr.Blocks() as demo:
    audio = gr.Audio(type="filepath")
    btn = gr.Button("Apply separation pipeline")
    pyannote_viewer = PyannoteViewer(interactive=False)

    btn.click(fn=apply_pipeline, inputs=[audio], outputs=[pyannote_viewer])


if __name__ == "__main__":
    demo.launch()

```
""", elem_classes=["md-custom"], header_links=True)


    gr.Markdown("""
## `PyannoteViewer`

### Initialization
""", elem_classes=["md-custom"], header_links=True)

    gr.ParamViewer(value=_docs["PyannoteViewer"]["members"]["__init__"], linkify=['WaveformOptions'])


    gr.Markdown("### Events")
    gr.ParamViewer(value=_docs["PyannoteViewer"]["events"], linkify=['Event'])




    gr.Markdown("""

### User function

The impact on the users predict function varies depending on whether the component is used as an input or output for an event (or both).

- When used as an Input, the component only impacts the input signature of the user function.
- When used as an output, the component only impacts the return signature of the user function.

The code snippet below is accurate in cases where the component is used as both an input and an output.

- **As input:** Is passed, passes audio as one of these formats (depending on `type`): a `str` filepath, or `tuple` of (sample rate in Hz, audio data as numpy array). If the latter, the audio data is a 16-bit `int` array whose values range from -32768 to 32767 and shape of the audio data array is (samples,) for mono audio or (samples, channels) for multi-channel audio.
- **As output:** Should return, expects audio data in any of these formats: a `str` or `pathlib.Path` filepath or URL to an audio file, or a `bytes` object (recommended for streaming), or a `tuple` of (sample rate in Hz, audio data as numpy array). Note: if audio is supplied as a numpy array, the audio will be normalized by its peak value to avoid distortion or clipping in the resulting audio.

 ```python
def predict(
    value: str | tuple[int, numpy.ndarray] | None
) -> tuple[
        pyannote.core.annotation.Annotation,
        numpy.ndarray | pathlib.Path | str,
    ]
    | None:
    return value
```
""", elem_classes=["md-custom", "PyannoteViewer-user-fn"], header_links=True)




    code_WaveformOptions = gr.Markdown("""
## `WaveformOptions`
```python
@dataclasses.dataclass
class WaveformOptions:
    waveform_color: str | None = None
    waveform_progress_color: str | None = None
    trim_region_color: str | None = None
    show_recording_waveform: bool = True
    show_controls: bool = False
    skip_length: int | float = 5
    sample_rate: int = 44100
```""", elem_classes=["md-custom", "WaveformOptions"], header_links=True)

    demo.load(None, js=r"""function() {
    const refs = {
            WaveformOptions: [], };
    const user_fn_refs = {
          PyannoteViewer: [], };
    requestAnimationFrame(() => {

        Object.entries(user_fn_refs).forEach(([key, refs]) => {
            if (refs.length > 0) {
                const el = document.querySelector(`.${key}-user-fn`);
                if (!el) return;
                refs.forEach(ref => {
                    el.innerHTML = el.innerHTML.replace(
                        new RegExp("\\b"+ref+"\\b", "g"),
                        `<a href="#h-${ref.toLowerCase()}">${ref}</a>`
                    );
                })
            }
        })

        Object.entries(refs).forEach(([key, refs]) => {
            if (refs.length > 0) {
                const el = document.querySelector(`.${key}`);
                if (!el) return;
                refs.forEach(ref => {
                    el.innerHTML = el.innerHTML.replace(
                        new RegExp("\\b"+ref+"\\b", "g"),
                        `<a href="#h-${ref.toLowerCase()}">${ref}</a>`
                    );
                })
            }
        })
    })
}

""")

demo.launch()
