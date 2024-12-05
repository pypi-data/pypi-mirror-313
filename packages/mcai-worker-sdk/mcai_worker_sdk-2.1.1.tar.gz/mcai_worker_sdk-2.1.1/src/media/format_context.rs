use pyo3::prelude::*;
use serde::{Deserialize, Serialize};
use stainless_ffmpeg::stream::Stream;
use std::{
  collections::{BTreeMap, HashMap},
  sync::{Arc, Mutex},
};

#[pyclass]
#[derive(Debug, Deserialize, PartialEq, Serialize)]
pub struct FormatContext {
  /// Name of the format.
  #[pyo3(get)]
  pub format_name: String,
  /// Long name of the format.
  #[pyo3(get)]
  pub format_long_name: String,
  /// Number of programs.
  #[pyo3(get)]
  pub program_count: u32,
  /// Start time.
  #[pyo3(get)]
  pub start_time: Option<f32>,
  /// Duration
  #[pyo3(get)]
  pub duration: Option<f64>,
  /// Bit rate.
  #[pyo3(get)]
  pub bit_rate: Option<i64>,
  /// Packet size.
  #[pyo3(get)]
  pub packet_size: u32,
  /// Number of streams.
  #[pyo3(get)]
  pub nb_streams: u32,
  /// Dictionnary containing the metadata.
  #[pyo3(get)]
  pub metadata: BTreeMap<String, String>,
  /// List of :class:`~mcai_worker_sdk.StreamDescriptor`.
  #[pyo3(get)]
  pub streams: Vec<StreamDescriptor>,
}

impl From<Arc<Mutex<mcai_worker_sdk::prelude::FormatContext>>> for FormatContext {
  fn from(format_context: Arc<Mutex<mcai_worker_sdk::prelude::FormatContext>>) -> Self {
    let context = format_context.lock().unwrap();

    let format_name = context.get_format_name();
    let format_long_name = context.get_format_long_name();

    let program_count = context.get_program_count();
    let start_time = context.get_start_time();
    let duration = context.get_duration();

    let bit_rate = context.get_bit_rate();
    let packet_size = context.get_packet_size();
    let nb_streams = context.get_nb_streams();

    let metadata = context.get_metadata();
    let mut streams = vec![];

    for stream_index in 0..context.get_nb_streams() {
      let stream = Stream::new(context.get_stream(stream_index as isize)).unwrap();

      let stream_descriptor = unsafe {
        StreamDescriptor {
          index: stream_index,
          start_time,
          duration: stream.get_duration(),
          stream_metadata: stream.get_stream_metadata(),
          nb_frames: stream.get_nb_frames().unwrap_or_default() as u64,
          avg_frame_rate: (*stream.stream).avg_frame_rate.num as f32
            / (*stream.stream).avg_frame_rate.den as f32,
          r_frame_rate: (*stream.stream).r_frame_rate.num as f32
            / (*stream.stream).r_frame_rate.den as f32,
          kind: format!("{:?}", context.get_stream_type(stream_index as isize)),
          width: stream.get_width() as u32,
          height: stream.get_height() as u32,
          channels: stream.get_channels() as u32,
          sample_rate: stream.get_sample_rate() as u32,
        }
      };
      streams.push(stream_descriptor);
    }

    FormatContext {
      format_name,
      format_long_name,
      program_count,
      start_time,
      duration,
      bit_rate,
      packet_size,
      nb_streams,
      metadata,
      streams,
    }
  }
}

/// Class representing a stream.
///
/// Note:
///   This class is provided for documentation purpose. It shouldn't be used directly in the worker.
#[pyclass]
#[derive(Debug, Deserialize, PartialEq, Serialize, Clone)]
pub struct StreamDescriptor {
  /// Index of the stream
  #[pyo3(get)]
  pub(crate) index: u32,
  /// Number of frames of the stream.
  #[pyo3(get)]
  pub(crate) nb_frames: u64,
  /// Average frame rate of the stream.
  #[pyo3(get)]
  pub(crate) avg_frame_rate: f32,
  /// Real base framerate of the stream.
  #[pyo3(get)]
  pub(crate) r_frame_rate: f32,
  /// Kind of the stream.
  #[pyo3(get)]
  pub(crate) kind: String,
  /// Width of the stream.
  #[pyo3(get)]
  pub(crate) width: u32,
  /// Height of the stream.
  #[pyo3(get)]
  pub(crate) height: u32,
  /// Channels of the stream.
  #[pyo3(get)]
  pub(crate) channels: u32,
  /// Sample rate of the stream.
  #[pyo3(get)]
  pub(crate) sample_rate: u32,
  /// Start time of the stream.
  #[pyo3(get)]
  pub(crate) start_time: Option<f32>,
  /// Duration of the stream.
  #[pyo3(get)]
  pub(crate) duration: Option<f32>,
  /// Dictionnary containing the metadata of the stream.
  #[pyo3(get)]
  pub(crate) stream_metadata: HashMap<String, String>,
}
