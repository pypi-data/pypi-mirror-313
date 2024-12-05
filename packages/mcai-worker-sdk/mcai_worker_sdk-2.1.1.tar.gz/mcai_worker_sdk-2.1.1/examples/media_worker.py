import logging

import mcai_worker_sdk as mcai


class McaiWorkerParameters(mcai.WorkerParameters):
    action: str
    number: int
    array_of_strings: list[str]
    array_of_integers: list[int]
    source_path: str
    destination_path: str


class McaiWorkerTest(mcai.Worker):
    def __init__(self, params, desc):
        super().__init__(params, desc)
        # You should avoid doing stuff here as error handling won't be done properly...

    def setup(self) -> None:
        """
        Optional worker setup function. May be used to load models, do some checks...
        """
        self.model = "Loading the statistic model to use it during process"

    def init_process(self, context, parameters: McaiWorkerParameters) -> list:
        """
        Function called before the media process (the "media" feature must be activated).
        """

        logging.info("Initialise the media process...")
        logging.debug("Number of streams: %d", context.nb_streams)
        logging.debug("Message parameters: %s", parameters)

        assert parameters.source_path is not None

        if parameters.destination_path is not None:
            logging.info("Destination path: %s", parameters.destination_path)

        for stream in context.streams:
            if stream.kind == "AVMEDIA_TYPE_VIDEO":
                logging.debug(
                    "Stream #%d: Video Resolution: %dx%d, %s frames, %sfps",
                    stream.index,
                    stream.width,
                    stream.height,
                    stream.nb_frames,
                    stream.r_frame_rate,
                )
            if stream.kind == "AVMEDIA_TYPE_AUDIO":
                logging.debug(
                    "Stream #%d: Audio %s channels, %s Hz, %s samples",
                    stream.index,
                    stream.channels,
                    stream.sample_rate,
                    stream.nb_frames,
                )
            if stream.kind == "AVMEDIA_TYPE_DATA":
                logging.debug("Stream #%d: Data", stream.index)

        # Here audio/video filters can be set to be applied on the worker input frames, using a simple python dict as follow.
        # Check the FFmpeg documentation to have more details on filters usage: https://ffmpeg.org/ffmpeg-filters.html
        stream_descriptors = []
        for stream in context.streams:
            if stream.kind == "AVMEDIA_TYPE_VIDEO":

                crop_filter = mcai.Filter(name="crop", label="crop_filter")
                crop_filter.add_parameters(out_w=10, out_h=20)

                video_stream = mcai.VideoStreamDescriptor(stream.index, [crop_filter])

                logging.info(
                    f"Add video stream {stream.index} to process: {video_stream}"
                )
                stream_descriptors.append(video_stream)

            if stream.kind == "AVMEDIA_TYPE_AUDIO":

                audio_filter = mcai.Filter(name="aformat")
                audio_filter.add_parameters(
                    sample_rates=16000, channel_layouts="mono", sample_fmts="s16"
                )

                audio_stream = mcai.AudioStreamDescriptor(stream.index, [audio_filter])
                logging.info(f"Add audio stream to process: {audio_stream}")

                stream_descriptors.append(audio_stream)

            if stream.kind in ["AVMEDIA_TYPE_SUBTITLES", "AVMEDIA_TYPE_DATA"]:
                data_stream = mcai.DataStreamDescriptor(stream.index)
                logging.info(f"Add data stream to process: {data_stream}")
                stream_descriptors.append(data_stream)

        # returns a list of description of the streams to be processed
        return stream_descriptors

    def process_frames(self, job_id, stream_index, frames) -> dict:
        """
        Process media frames (the "media" feature must be activated).
        """
        for frame in frames:
            data_length = 0
            for plane in range(0, len(frame.data)):
                data_length = data_length + len(frame.data[plane])

            if frame.width != 0 and frame.height != 0:
                logging.info(
                    f"Job: {job_id} - Process video stream {stream_index} frame - PTS: {frame.pts}, image size: {frame.width}x{frame.height}, data length: {data_length}"
                )
            else:
                logging.info(
                    f"Job: {job_id} - Process audio stream {stream_index} frame - PTS: {frame.pts}, sample_rate: {frame.sample_rate}Hz, channels: {frame.channels}, nb_samples: {frame.nb_samples}, data length: {data_length}"
                )

        # returns the process result as a JSON object (this is fully customisable)
        return {"status": "success"}

    def ending_process(self):
        """
        Function called at the end of the media process (the "media" feature must be activated).
        """
        logging.info("Ending Python worker process...")


if __name__ == "__main__":
    desc = mcai.WorkerDescription(__package__) # This allows retrieving information from the worker, such as name, version, license...
    worker = McaiWorkerTest(McaiWorkerParameters, desc)
    worker.start()
