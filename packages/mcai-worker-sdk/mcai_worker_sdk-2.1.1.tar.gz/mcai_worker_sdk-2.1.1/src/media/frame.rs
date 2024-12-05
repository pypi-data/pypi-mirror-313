use std::os::raw::c_uchar;

use mcai_worker_sdk::{MessageError, Result};
use pyo3::{
  prelude::*,
  types::{PyBytes, PyList},
};
use std::convert::TryFrom;

/// Class representing a video frame.
///
/// Note:
///   This class is provided for documentation purpose as frames are given to the :func:`~mcai_worker_sdk.Worker.process_frames` method. It shouldn't be used directly in the worker.
#[pyclass(unsendable)]
#[derive(Debug, Eq, PartialEq)]
pub struct Frame {
  /// Name of the frame. Can be null.
  #[pyo3(get)]
  pub name: Option<String>,
  /// Index of the frame.
  #[pyo3(get)]
  pub index: usize,
  pub data: [*mut c_uchar; 8],
  /// Line size of the frame.
  #[pyo3(get)]
  pub line_size: [i32; 8],
  /// Number of samples of the frame.
  #[pyo3(get)]
  pub nb_samples: i32,
  /// Format of the frame, -1 if unknown or unset Values correspond to enum AVPixelFormat for video frames, enum AVSampleFormat for audio).
  #[pyo3(get)]
  pub format: i32,
  /// 1 -> keyframe, 0-> not.
  #[pyo3(get)]
  pub key_frame: i32,
  /// Presentation timestamp in time_base units (time when frame should be shown to user).
  #[pyo3(get)]
  pub pts: i64,
  /// Picture number in bitstream order.
  #[pyo3(get)]
  pub coded_picture_number: i32,
  /// Picture number in bitstream order.
  #[pyo3(get)]
  pub display_picture_number: i32,
  /// The content of the picture is interlaced.
  #[pyo3(get)]
  pub interlaced_frame: i32,
  /// If the content is interlaced, is top field displayed first.
  #[pyo3(get)]
  pub top_field_first: i32,
  /// Sample rate of the audio data.
  #[pyo3(get)]
  pub sample_rate: i32,
  /// Number of audio channels, only used for audio.
  #[pyo3(get)]
  pub channels: i32,
  /// Size of the corresponding packet containing the compressed frame.
  #[pyo3(get)]
  pub pkt_size: i32,
  /// Width of the frame.
  #[pyo3(get)]
  pub width: i32,
  /// Height of the frame.
  #[pyo3(get)]
  pub height: i32,
}

#[pymethods]
impl Frame {
  /// Sequence of bytes representing the image.
  #[getter]
  fn get_data<'p>(&self, py: Python<'p>) -> PyResult<Bound<'p, PyList>> {
    let data = PyList::empty_bound(py);
    for plane_index in 0..self.data.len() {
      unsafe {
        data.append(PyBytes::bound_from_ptr(
          py,
          self.data[plane_index],
          (self.line_size[plane_index] * self.height) as usize,
        ))?;
      }
    }
    Ok(data)
  }
}

impl TryFrom<&mcai_worker_sdk::prelude::Frame> for Frame {
  type Error = MessageError;

  fn try_from(frame: &mcai_worker_sdk::prelude::Frame) -> Result<Self> {
    if frame.frame.is_null() {
      return Err(MessageError::RuntimeError(
        "Cannot initialize frame struct from null AVFrame".to_string(),
      ));
    }

    let av_frame = unsafe { *frame.frame };

    Ok(Frame {
      name: frame.name.clone(),
      index: frame.index,
      data: av_frame.data,
      line_size: av_frame.linesize,
      nb_samples: av_frame.nb_samples,
      format: av_frame.format,
      key_frame: av_frame.key_frame,
      pts: av_frame.pts,
      coded_picture_number: av_frame.coded_picture_number,
      display_picture_number: av_frame.display_picture_number,
      interlaced_frame: av_frame.interlaced_frame,
      top_field_first: av_frame.top_field_first,
      sample_rate: av_frame.sample_rate,
      channels: av_frame.channels,
      pkt_size: av_frame.pkt_size,
      width: av_frame.width,
      height: av_frame.height,
    })
  }
}

#[test]
pub fn test_frame_from_null_avframe() {
  let sdk_frame = mcai_worker_sdk::prelude::Frame {
    name: None,
    frame: std::ptr::null_mut(),
    index: 0,
  };

  let frame = Frame::try_from(&sdk_frame);
  assert!(frame.is_err());
  assert_eq!(
    MessageError::RuntimeError("Cannot initialize frame struct from null AVFrame".to_string()),
    frame.unwrap_err()
  );
}
