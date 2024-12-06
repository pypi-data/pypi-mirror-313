<script lang="ts">
	import { onMount } from "svelte";
	import { Music } from "@gradio/icons";
	import { format_time, type I18nFormatter } from "@gradio/utils";
	import WaveSurfer from "wavesurfer.js";
	import RegionsPlugin from "wavesurfer.js/dist/plugins/regions";
	import { skip_audio } from "../shared/utils";
	import WaveformControls from "../shared/WaveformControls.svelte";
	import { Empty } from "@gradio/atoms";
	import type { WaveformOptions, PipelineOutput } from "../shared/types";
	import { createEventDispatcher } from "svelte";
    import Color from "@gradio/icons/src/Color.svelte";

	export let value: PipelineOutput | null = null;
	export let label: string;
	export let root: string;
	export let i18n: I18nFormatter;
	export let interactive = false;
	export let editable = true;
	export let waveform_settings: Record<string, any>;
	export let waveform_options: WaveformOptions;
	export let mode = "";
	export let handle_reset_value: () => void = () => {};

	let container: HTMLDivElement;
	let waveform: WaveSurfer | undefined;
	let wsRegion: RegionsPlugin | undefined;
	let playing = false;

	let timeRef: HTMLTimeElement;
	let durationRef: HTMLTimeElement;
	let audio_duration: number;

	let colors: string[] = ["#f005", "#0f05", "#00f5", "#ff05", "#f0f5", "#0ff5"];

	let audioDecoded: boolean = false;
	let audioContext: AudioContext | undefined;
	let mediaNode: MediaElementAudioSourceNode | undefined;
	let splitter: ChannelSplitterNode | undefined;
	let trimDuration = 0;

	let show_volume_slider = false;

	const dispatch = createEventDispatcher<{
		stop: undefined;
		play: undefined;
		pause: undefined;
		edit: undefined;
		end: undefined;
	}>();

	const create_waveform = (): void => {
		const audio = new Audio(root + `/file=${value.audio_file.path}`)
		audio.crossOrigin = "anonymous"

		audioContext = new AudioContext();

		waveform = WaveSurfer.create({
			container: container,
			media: audio,
			splitChannels: value.multichannel,
			...waveform_settings
		});
	};

	$: if (container !== undefined) {
		if (waveform !== undefined) waveform.destroy();
		container.innerHTML = "";
		create_waveform();
		playing = false;
	}

	$: waveform?.on("decode", (duration: any) => {
		audioDecoded = true;
		const numChannels = waveform.getDecodedData().numberOfChannels;
		console.log(numChannels);
		audio_duration = duration;
		durationRef && (durationRef.textContent = format_time(duration));
	
		mediaNode = audioContext.createMediaElementSource(waveform.getMediaElement() );

		splitter = audioContext.createChannelSplitter(numChannels);
		mediaNode.connect(splitter);

		if(!value.multichannel){
			splitter.connect(audioContext.destination, 0);
		}

		// add diarization annotation on each source:
		if(!wsRegion){
			wsRegion = waveform.registerPlugin(RegionsPlugin.create())
			value.segments.forEach(segment => {
				const region = wsRegion.addRegion({
					start: segment.start,
					end: segment.end,
					channelIdx: value.multichannel ? segment.channel : 0,
					drag: false,
					resize: false,
					color: colors[segment.channel % colors.length],
				});

				const regionHeight = 100 / (value.multichannel ? numChannels : 1);
				region.element.style.cssText += `height: ${regionHeight}% !important;`;
				// TODO: Can we do better than force region color ?
				region.element.style.cssText += `background-color: ${region.color} !important;`;
			});
		}
	});

	$: waveform?.on(
		"timeupdate",
		(currentTime: any) =>
			timeRef && (timeRef.textContent = format_time(currentTime))
	);

	$: waveform?.on("ready", () => {
		if (!waveform_settings.autoplay) {
			waveform?.stop();
		} else {
			waveform?.play();
		}
	});

	$: waveform?.on("finish", () => {
		playing = false;
		dispatch("stop");
	});
	$: waveform?.on("pause", () => {
		playing = false;
		dispatch("pause");
	});
	$: waveform?.on("play", () => {
		playing = true;
		dispatch("play");
	});

	onMount(() => {
		window.addEventListener("keydown", (e) => {
			if (!waveform || show_volume_slider) return;
			if (e.key === "ArrowRight" && mode !== "edit") {
				skip_audio(waveform, 0.1);
			} else if (e.key === "ArrowLeft" && mode !== "edit") {
				skip_audio(waveform, -0.1);
			}
		});
	});
</script>

{#if value === null}
	<Empty size="small">
		<Music />
	</Empty>
{:else if value.audio_file.is_stream}
	<audio
		class="standard-player"
		src={value.audio_file.url}
		controls
		autoplay={waveform_settings.autoplay}
	/>
{:else}
	<div
		class="component-wrapper"
		data-testid={label ? "waveform-" + label : "unlabelled-audio"}
	>
	<div class="viewer">
		<div class="source-selection">
			{#if audioDecoded}
				{#if value.multichannel}
					<!-- Separation pipeline case -->
					{#each [...Array(waveform.getDecodedData().numberOfChannels).keys()] as channelIdx}
						<label style={`height: ${waveform_settings.height}px; background-color: ${colors[channelIdx % colors.length]}`}>
							<input 
								type="radio" 
								name="channels" 
								value={`${channelIdx}`}
								on:change={(ev) => {
									splitter.disconnect()
									splitter.connect(audioContext.destination, Number(ev.target.value), 0);
								}}
							/>
							{value.labels[channelIdx]}
						</label>
					{/each}
				{:else}
						{#each [...Array(value.labels.length)].keys() as labelIdx}
							<label style={`background-color: ${colors[labelIdx % colors.length]};`}>
								<input type="hidden">
								{value.labels[labelIdx]}
							</label>
						{/each}
				{/if}
			{/if}
		</div>
		<div class="waveform-container">
			<div id="waveform" bind:this={container} />
			<div class="timestamps">
				<time bind:this={timeRef} id="time">0:00</time>
				<div>
					{#if mode === "edit" && trimDuration > 0}
						<time id="trim-duration">{format_time(trimDuration)}</time>
					{/if}
					<time bind:this={durationRef} id="duration">0:00</time>
				</div>
			</div>
		</div>
	</div>

		{#if waveform}
			<WaveformControls
				{waveform}
				{playing}
				{audio_duration}
				{i18n}
				{interactive}
				bind:mode
				bind:trimDuration
				bind:show_volume_slider
				show_redo={interactive}
				{handle_reset_value}
				{waveform_options}
				{editable}
			/>
		{/if}
	</div>
{/if}

<style>
	input[type="radio"] {
		appearance: none;
		background-color: #fff;
		margin-right: 0.5em;
		font: inherit;
		color: var(--neutral-400);
		width: 1.15em;
		height: 1.15em;
		border: 0.15em solid var(--neutral-400);
		border-radius: 50%;
	}

	input[type="radio"]:checked {
		background-color: var(--color-accent);
	}

	label {
		display: flex;
		align-items: center;
		margin-bottom: 0.25em;
		padding-left: 0.5em;
		padding-right: 0.5em;
	}


	.component-wrapper {
		padding: var(--size-3);
		width: 100%;
	}

	.viewer {
		display: flex;
	}

	.source-selection {
		display: flex;
		flex-direction: column;
		margin-right: 1em;
	}

	:global(::part(wrapper)) {
		margin-bottom: var(--size-2);
	}

	.timestamps {
		display: flex;
		justify-content: space-between;
		align-items: center;
		width: 100%;
		padding: var(--size-1) 0;
	}

	#time {
		color: var(--neutral-400);
	}

	#duration {
		color: var(--neutral-400);
	}

	#trim-duration {
		color: var(--color-accent);
		margin-right: var(--spacing-sm);
	}
	.waveform-container {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		width: var(--size-full);
	}

	#waveform {
		width: 100%;
		height: 100%;
		position: relative;
	}

	.standard-player {
		width: 100%;
		padding: var(--size-2);
	}
</style>
