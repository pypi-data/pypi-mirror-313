<script lang="ts">
	import { Play, Pause, Forward, Backward, Undo, Trim } from "@gradio/icons";
	import { get_skip_rewind_amount } from "../shared/utils";
	import type { I18nFormatter } from "@gradio/utils";
	import WaveSurfer from "wavesurfer.js";
	import RegionsPlugin, {
		type Region
	} from "wavesurfer.js/dist/plugins/regions.js";
	import type { WaveformOptions } from "./types";
	import VolumeLevels from "./VolumeLevels.svelte";
	import VolumeControl from "./VolumeControl.svelte";

	export let waveform: WaveSurfer;
	export let audio_duration: number;
	export let i18n: I18nFormatter;
	export let playing: boolean;
	export let show_redo = false;
	export let interactive = false;
	export let mode = "";
	export let handle_reset_value: () => void;
	export let waveform_options: WaveformOptions = {};
	export let show_volume_slider = false;
	export let editable = true;

	export let trimDuration = 0;

	let playbackSpeeds = [0.5, 1, 1.5, 2];
	let playbackSpeed = playbackSpeeds[1];

	let activeRegion: Region | null = null;

	let currentVolume = 1;

	const adjustRegionHandles = (handle: string, key: string): void => {
		let newStart;
		let newEnd;

		if (!activeRegion) return;
		if (handle === "left") {
			if (key === "ArrowLeft") {
				newStart = activeRegion.start - 0.05;
				newEnd = activeRegion.end;
			} else {
				newStart = activeRegion.start + 0.05;
				newEnd = activeRegion.end;
			}
		} else {
			if (key === "ArrowLeft") {
				newStart = activeRegion.start;
				newEnd = activeRegion.end - 0.05;
			} else {
				newStart = activeRegion.start;
				newEnd = activeRegion.end + 0.05;
			}
		}

		activeRegion.setOptions({
			start: newStart,
			end: newEnd
		});

		trimDuration = activeRegion.end - activeRegion.start;
	};

</script>

<div class="controls" data-testid="waveform-controls">
	<div class="control-wrapper">
		<button
			class="action icon volume"
			style:color={show_volume_slider
				? "var(--color-accent)"
				: "var(--neutral-400)"}
			aria-label="Adjust volume"
			on:click={() => (show_volume_slider = !show_volume_slider)}
		>
			<VolumeLevels {currentVolume} />
		</button>

		{#if show_volume_slider}
			<VolumeControl bind:currentVolume bind:show_volume_slider {waveform} />
		{/if}

		<button
			class:hidden={show_volume_slider}
			class="playback icon"
			aria-label={`Adjust playback speed to ${
				playbackSpeeds[
					(playbackSpeeds.indexOf(playbackSpeed) + 1) % playbackSpeeds.length
				]
			}x`}
			on:click={() => {
				playbackSpeed =
					playbackSpeeds[
						(playbackSpeeds.indexOf(playbackSpeed) + 1) % playbackSpeeds.length
					];

				waveform.setPlaybackRate(playbackSpeed);
			}}
		>
			<span>{playbackSpeed}x</span>
		</button>
	</div>

	<div class="play-pause-wrapper">
		<button
			class="rewind icon"
			aria-label={`Skip backwards by ${get_skip_rewind_amount(
				audio_duration,
				waveform_options.skip_length
			)} seconds`}
			on:click={() =>
				waveform.skip(
					get_skip_rewind_amount(audio_duration, waveform_options.skip_length) *
						-1
				)}
		>
			<Backward />
		</button>
		<button
			class="play-pause-button icon"
			on:click={() => waveform.playPause()}
			aria-label={playing ? i18n("audio.pause") : i18n("audio.play")}
		>
			{#if playing}
				<Pause />
			{:else}
				<Play />
			{/if}
		</button>
		<button
			class="skip icon"
			aria-label="Skip forward by {get_skip_rewind_amount(
				audio_duration,
				waveform_options.skip_length
			)} seconds"
			on:click={() =>
				waveform.skip(
					get_skip_rewind_amount(audio_duration, waveform_options.skip_length)
				)}
		>
			<Forward />
		</button>
	</div>

	<div class="settings-wrapper">
		{#if editable && interactive}
			{#if show_redo && mode === ""}
				<button
					class="action icon"
					aria-label="Reset audio"
					on:click={() => {
						handle_reset_value();
						mode = "";
					}}
				>
					<Undo />
				</button>
			{/if}
		{/if}
	</div>
</div>

<style>
	.settings-wrapper {
		display: flex;
		justify-self: self-end;
		align-items: center;
		grid-area: editing;
	}

	.controls {
		display: grid;
		grid-template-columns: 1fr 1fr 1fr;
		grid-template-areas: "controls playback editing";
		margin-top: 5px;
		align-items: center;
		position: relative;
		flex-wrap: wrap;
		justify-content: space-between;
	}
	.controls div {
		margin: var(--size-1) 0;
	}

	@media (max-width: 600px) {
		.controls {
			grid-template-columns: 1fr 1fr;
			grid-template-rows: auto auto;
			grid-template-areas:
				"playback playback"
				"controls editing";
			overflow: scroll;
		}
	}

	.hidden {
		display: none;
	}

	.control-wrapper {
		display: flex;
		justify-self: self-start;
		align-items: center;
		justify-content: space-between;
		grid-area: controls;
	}

	.action {
		width: var(--size-5);
		color: var(--neutral-400);
		margin-left: var(--spacing-md);
	}
	.icon:hover,
	.icon:focus {
		color: var(--color-accent);
	}
	.play-pause-wrapper {
		display: flex;
		justify-self: center;
		grid-area: playback;
	}

	@media (max-width: 600px) {
		.play-pause-wrapper {
			margin: var(--spacing-md);
		}
	}
	.playback {
		border: 1px solid var(--neutral-400);
		border-radius: var(--radius-sm);
		width: 5.5ch;
		font-weight: 300;
		font-size: var(--size-3);
		text-align: center;
		color: var(--neutral-400);
		height: var(--size-5);
		font-weight: bold;
	}

	.playback:hover,
	.playback:focus {
		color: var(--color-accent);
		border-color: var(--color-accent);
	}

	.rewind,
	.skip {
		margin: 0 10px;
		color: var(--neutral-400);
	}

	.play-pause-button {
		width: var(--size-8);
		display: flex;
		align-items: center;
		justify-content: center;
		color: var(--neutral-400);
		fill: var(--neutral-400);
	}

	.volume {
		position: relative;
		display: flex;
		justify-content: center;
		margin-right: var(--spacing-xl);
		width: var(--size-5);
	}
</style>
