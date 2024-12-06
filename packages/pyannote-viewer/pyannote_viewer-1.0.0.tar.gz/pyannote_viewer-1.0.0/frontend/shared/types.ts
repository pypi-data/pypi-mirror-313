import type { FileData } from "@gradio/client";

export type WaveformOptions = {
	waveform_color?: string;
	waveform_progress_color?: string;
	show_controls?: boolean;
	skip_length?: number;
	trim_region_color?: string;
	show_recording_waveform?: boolean;
	sample_rate?: number;
};

export type Segment = {
	start: number;
	end: number;
	channel: number;
}

export type PipelineOutput = {
	segments: Segment[];
	labels: string[];
	multichannel: boolean;
	audio_file: FileData;
}