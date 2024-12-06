
# `pyannote_viewer`
<img alt="Static Badge" src="https://img.shields.io/badge/version%20-%201.0.0%20-%20orange">  

Gradio custom component to visualize pyannote's pipelines outputs

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

## `PyannoteViewer`

### Initialization

<table>
<thead>
<tr>
<th align="left">name</th>
<th align="left" style="width: 25%;">type</th>
<th align="left">default</th>
<th align="left">description</th>
</tr>
</thead>
<tbody>
<tr>
<td align="left"><code>value</code></td>
<td align="left" style="width: 25%;">

```python
str
    | pathlib.Path
    | tuple[int, numpy.ndarray]
    | Callable
    | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">A path, URL, or [sample_rate, numpy array] tuple (sample rate in Hz, audio data as a float or int numpy array) for the default value that SourceViewer component is going to take. If callable, the function will be called whenever the app loads to set the initial value of the component.</td>
</tr>

<tr>
<td align="left"><code>sources</code></td>
<td align="left" style="width: 25%;">

```python
list["upload" | "microphone"] | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">A list of sources permitted for audio. "upload" creates a box where user can drop an audio file, "microphone" creates a microphone input. The first element in the list will be used as the default source. If None, defaults to ["upload", "microphone"], or ["microphone"] if `streaming` is True.</td>
</tr>

<tr>
<td align="left"><code>type</code></td>
<td align="left" style="width: 25%;">

```python
"numpy" | "filepath"
```

</td>
<td align="left"><code>"numpy"</code></td>
<td align="left">The format the audio file is converted to before being passed into the prediction function. "numpy" converts the audio to a tuple consisting of: (int sample rate, numpy.array for the data), "filepath" passes a str path to a temporary file containing the audio.</td>
</tr>

<tr>
<td align="left"><code>label</code></td>
<td align="left" style="width: 25%;">

```python
str | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">The label for this component. Appears above the component and is also used as the header if there are a table of examples for this component. If None and used in a `gr.Interface`, the label will be the name of the parameter this component is assigned to.</td>
</tr>

<tr>
<td align="left"><code>every</code></td>
<td align="left" style="width: 25%;">

```python
float | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">If `value` is a callable, run the function 'every' number of seconds while the client connection is open. Has no effect otherwise. The event can be accessed (e.g. to cancel it) via this component's .load_event attribute.</td>
</tr>

<tr>
<td align="left"><code>show_label</code></td>
<td align="left" style="width: 25%;">

```python
bool | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">if True, will display label.</td>
</tr>

<tr>
<td align="left"><code>container</code></td>
<td align="left" style="width: 25%;">

```python
bool
```

</td>
<td align="left"><code>True</code></td>
<td align="left">If True, will place the component in a container - providing some extra padding around the border.</td>
</tr>

<tr>
<td align="left"><code>scale</code></td>
<td align="left" style="width: 25%;">

```python
int | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">Relative width compared to adjacent Components in a Row. For example, if Component A has scale=2, and Component B has scale=1, A will be twice as wide as B. Should be an integer.</td>
</tr>

<tr>
<td align="left"><code>min_width</code></td>
<td align="left" style="width: 25%;">

```python
int
```

</td>
<td align="left"><code>160</code></td>
<td align="left">Minimum pixel width, will wrap if not sufficient screen space to satisfy this value. If a certain scale value results in this Component being narrower than min_width, the min_width parameter will be respected first.</td>
</tr>

<tr>
<td align="left"><code>interactive</code></td>
<td align="left" style="width: 25%;">

```python
bool | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">If True, will allow users to upload and edit an audio file. If False, can only be used to play audio. If not provided, this is inferred based on whether the component is used as an input or output.</td>
</tr>

<tr>
<td align="left"><code>visible</code></td>
<td align="left" style="width: 25%;">

```python
bool
```

</td>
<td align="left"><code>True</code></td>
<td align="left">If False, component will be hidden.</td>
</tr>

<tr>
<td align="left"><code>streaming</code></td>
<td align="left" style="width: 25%;">

```python
bool
```

</td>
<td align="left"><code>False</code></td>
<td align="left">If set to True when used in a `live` interface as an input, will automatically stream webcam feed. When used set as an output, takes audio chunks yield from the backend and combines them into one streaming audio output.</td>
</tr>

<tr>
<td align="left"><code>elem_id</code></td>
<td align="left" style="width: 25%;">

```python
str | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">An optional string that is assigned as the id of this component in the HTML DOM. Can be used for targeting CSS styles.</td>
</tr>

<tr>
<td align="left"><code>elem_classes</code></td>
<td align="left" style="width: 25%;">

```python
list[str] | str | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">An optional list of strings that are assigned as the classes of this component in the HTML DOM. Can be used for targeting CSS styles.</td>
</tr>

<tr>
<td align="left"><code>render</code></td>
<td align="left" style="width: 25%;">

```python
bool
```

</td>
<td align="left"><code>True</code></td>
<td align="left">If False, component will not render be rendered in the Blocks context. Should be used if the intention is to assign event listeners now but render the component later.</td>
</tr>

<tr>
<td align="left"><code>format</code></td>
<td align="left" style="width: 25%;">

```python
"wav" | "mp3"
```

</td>
<td align="left"><code>"wav"</code></td>
<td align="left">The file format to save audio files. Either 'wav' or 'mp3'. wav files are lossless but will tend to be larger files. mp3 files tend to be smaller. Default is wav. Applies both when this component is used as an input (when `type` is "format") and when this component is used as an output.</td>
</tr>

<tr>
<td align="left"><code>autoplay</code></td>
<td align="left" style="width: 25%;">

```python
bool
```

</td>
<td align="left"><code>False</code></td>
<td align="left">Whether to automatically play the audio when the component is used as an output. Note: browsers will not autoplay audio files if the user has not interacted with the page yet.</td>
</tr>

<tr>
<td align="left"><code>show_download_button</code></td>
<td align="left" style="width: 25%;">

```python
bool | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">If True, will show a download button in the corner of the component for saving audio. If False, icon does not appear. By default, it will be True for output components and False for input components.</td>
</tr>

<tr>
<td align="left"><code>show_share_button</code></td>
<td align="left" style="width: 25%;">

```python
bool | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">If True, will show a share icon in the corner of the component that allows user to share outputs to Hugging Face Spaces Discussions. If False, icon does not appear. If set to None (default behavior), then the icon appears if this Gradio app is launched on Spaces, but not otherwise.</td>
</tr>

<tr>
<td align="left"><code>editable</code></td>
<td align="left" style="width: 25%;">

```python
bool
```

</td>
<td align="left"><code>True</code></td>
<td align="left">If True, allows users to manipulate the audio file if the component is interactive. Defaults to True.</td>
</tr>

<tr>
<td align="left"><code>min_length</code></td>
<td align="left" style="width: 25%;">

```python
int | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">The minimum length of audio (in seconds) that the user can pass into the prediction function. If None, there is no minimum length.</td>
</tr>

<tr>
<td align="left"><code>max_length</code></td>
<td align="left" style="width: 25%;">

```python
int | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">The maximum length of audio (in seconds) that the user can pass into the prediction function. If None, there is no maximum length.</td>
</tr>

<tr>
<td align="left"><code>waveform_options</code></td>
<td align="left" style="width: 25%;">

```python
WaveformOptions | dict | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">A dictionary of options for the waveform display. Options include: waveform_color (str), waveform_progress_color (str), show_controls (bool), skip_length (int), trim_region_color (str). Default is None, which uses the default values for these options.</td>
</tr>
</tbody></table>


### Events

| name | description |
|:-----|:------------|
| `stream` | This listener is triggered when the user streams the PyannoteViewer. |
| `change` | Triggered when the value of the PyannoteViewer changes either because of user input (e.g. a user types in a textbox) OR because of a function update (e.g. an image receives a value from the output of an event trigger). See `.input()` for a listener that is only triggered by user input. |
| `clear` | This listener is triggered when the user clears the PyannoteViewer using the X button for the component. |
| `play` | This listener is triggered when the user plays the media in the PyannoteViewer. |
| `pause` | This listener is triggered when the media in the PyannoteViewer stops for any reason. |
| `stop` | This listener is triggered when the user reaches the end of the media playing in the PyannoteViewer. |
| `start_recording` | This listener is triggered when the user starts recording with the PyannoteViewer. |
| `pause_recording` | This listener is triggered when the user pauses recording with the PyannoteViewer. |
| `stop_recording` | This listener is triggered when the user stops recording with the PyannoteViewer. |
| `upload` | This listener is triggered when the user uploads a file into the PyannoteViewer. |



### User function

The impact on the users predict function varies depending on whether the component is used as an input or output for an event (or both).

- When used as an Input, the component only impacts the input signature of the user function.
- When used as an output, the component only impacts the return signature of the user function.

The code snippet below is accurate in cases where the component is used as both an input and an output.

- **As output:** Is passed, passes audio as one of these formats (depending on `type`): a `str` filepath, or `tuple` of (sample rate in Hz, audio data as numpy array). If the latter, the audio data is a 16-bit `int` array whose values range from -32768 to 32767 and shape of the audio data array is (samples,) for mono audio or (samples, channels) for multi-channel audio.
- **As input:** Should return, expects audio data in any of these formats: a `str` or `pathlib.Path` filepath or URL to an audio file, or a `bytes` object (recommended for streaming), or a `tuple` of (sample rate in Hz, audio data as numpy array). Note: if audio is supplied as a numpy array, the audio will be normalized by its peak value to avoid distortion or clipping in the resulting audio.

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
```
