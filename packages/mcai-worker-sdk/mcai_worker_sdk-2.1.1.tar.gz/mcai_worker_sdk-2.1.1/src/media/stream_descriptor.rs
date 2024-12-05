use super::filter::extract_generic_filters;
use mcai_worker_sdk::prelude::*;
use pyo3::{
  prelude::*,
  types::{PyList, PySequence},
};

#[pyclass]
#[derive(Debug)]
pub struct StreamDescriptorHandler {}

#[derive(Debug, Clone, Eq, PartialEq)]
pub enum StreamType {
  Audio,
  Data,
  Video,
}

#[pyclass(subclass)]
#[derive(Debug, Clone)]
pub struct GenericStreamDescriptor {
  pub(crate) index: u32,
  pub(crate) filters: Vec<GenericFilter>,
  pub(crate) stream_type: StreamType,
}

impl GenericStreamDescriptor {
  fn new(
    stream_type: StreamType,
    index: u32,
    filters: Option<&Bound<'_, PySequence>>,
  ) -> PyResult<GenericStreamDescriptor> {
    let filters = if let Some(filters) = filters {
      extract_generic_filters(filters)?
    } else {
      vec![]
    };

    Ok(GenericStreamDescriptor {
      index,
      filters,
      stream_type,
    })
  }
}

/// Class defining an audio stream descriptor.
///
/// Arguments:
///   index (int): Index of the stream.
///   filters (collections.abc.Sequence(:class:`~mcai_worker_sdk.Filter`)): a list of FFmpeg filters to apply to the stream.
///
/// Examples:
///   >>> audio_filter = mcai.Filter(name="aformat")
///   >>> audio_filter.add_parameters(sample_rates=16000, channel_layouts="mono")
///   >>> audio_stream = mcai.AudioStreamDescriptor(1, (audio_filter,))
#[pyclass(extends=GenericStreamDescriptor)]
pub struct AudioStreamDescriptor {}

#[pymethods]
impl AudioStreamDescriptor {
  #[new]
  pub fn new(
    index: u32,
    filters: &Bound<'_, PySequence>,
  ) -> PyResult<(Self, GenericStreamDescriptor)> {
    Ok((
      AudioStreamDescriptor {},
      GenericStreamDescriptor::new(StreamType::Audio, index, Some(filters))?,
    ))
  }
}

/// Class defining an video stream descriptor.
///
/// Arguments:
///   index (int): Index of the stream.
///   filters (collections.abc.Sequence(:class:`~mcai_worker_sdk.Filter`)): a list of FFmpeg filters to apply to the stream.
///
/// Examples:
///   >>> crop_filter = mcai.Filter(name="crop", label="crop_filter")
///   >>> crop_filter.add_parameters(out_w=10, out_h=20)
///   >>> video_stream = mcai.VideoStreamDescriptor(1, (crop_filter,))
#[pyclass(extends=GenericStreamDescriptor)]
pub struct VideoStreamDescriptor {}

#[pymethods]
impl VideoStreamDescriptor {
  #[new]
  pub fn new(
    index: u32,
    filters: &Bound<'_, PySequence>,
  ) -> PyResult<(Self, GenericStreamDescriptor)> {
    Ok((
      VideoStreamDescriptor {},
      GenericStreamDescriptor::new(StreamType::Video, index, Some(filters))?,
    ))
  }
}

/// Class defining a data stream descriptor.
///
/// Arguments:
///   index (int): Index of the stream.
///
/// Examples:
///   >>> data_stream = mcai.DataStreamDescriptor(1)
#[pyclass(extends=GenericStreamDescriptor)]
pub struct DataStreamDescriptor {}

#[pymethods]
impl DataStreamDescriptor {
  #[new]
  pub fn new(index: u32) -> PyResult<(Self, GenericStreamDescriptor)> {
    Ok((
      DataStreamDescriptor {},
      GenericStreamDescriptor::new(StreamType::Data, index, None)?,
    ))
  }
}

pub fn get_stream_descriptors(
  stream_descriptors: &Bound<'_, PyList>,
) -> PyResult<Vec<StreamDescriptor>> {
  Ok(
    stream_descriptors
      .into_iter()
      .map(|value| value.extract::<GenericStreamDescriptor>())
      .filter(|extracted| extracted.is_ok())
      .map(|extracted| get_stream_descriptor(extracted.unwrap()))
      .collect(),
  )
}

fn get_stream_descriptor(generic_stream_descriptor: GenericStreamDescriptor) -> StreamDescriptor {
  match generic_stream_descriptor.stream_type {
    StreamType::Audio => {
      let filters = generic_stream_descriptor
        .filters
        .iter()
        .cloned()
        .map(AudioFilter::Generic)
        .collect();
      StreamDescriptor::new_audio(generic_stream_descriptor.index as usize, filters)
    }
    StreamType::Data => StreamDescriptor::new_data(generic_stream_descriptor.index as usize),
    StreamType::Video => {
      let filters = generic_stream_descriptor
        .filters
        .iter()
        .cloned()
        .map(VideoFilter::Generic)
        .collect();
      StreamDescriptor::new_video(generic_stream_descriptor.index as usize, filters)
    }
  }
}

#[cfg(test)]
mod test {
  use super::*;
  use crate::media::PyGenericFilter;
  use mcai_worker_sdk::prelude::GenericFilter;
  use pyo3::Python;

  #[test]
  fn test_create_data_stream_descriptor() {
    let data_descr = DataStreamDescriptor::new(0).unwrap().1;
    assert_eq!(data_descr.index, 0);
    assert_eq!(data_descr.stream_type, StreamType::Data);
    assert_eq!(data_descr.filters, vec![]);
  }

  #[test]
  fn test_create_audio_stream_descriptor() {
    pyo3::prepare_freethreaded_python();

    Python::with_gil(|py| {
      let audio_filter = Bound::new(
        py,
        PyGenericFilter {
          name: "my_filter".to_string(),
          label: None,
          parameters: Default::default(),
        },
      )
      .unwrap();

      let binding = PyList::new_bound(py, [audio_filter]);
      let filter_list = binding.as_sequence();

      let data_descr = AudioStreamDescriptor::new(1, filter_list).unwrap().1;
      assert_eq!(data_descr.index, 1);
      assert_eq!(data_descr.stream_type, StreamType::Audio);

      assert_eq!(
        data_descr.filters,
        Vec::from([GenericFilter {
          name: "my_filter".to_string(),
          label: None,
          parameters: Default::default(),
        }])
      );
    });
  }

  #[test]
  fn test_create_video_stream_descriptor() {
    pyo3::prepare_freethreaded_python();

    Python::with_gil(|py| {
      let video_filter = Bound::new(
        py,
        PyGenericFilter {
          name: "my_filter".to_string(),
          label: None,
          parameters: Default::default(),
        },
      )
      .unwrap();

      let binding = PyList::new_bound(py, [video_filter]);
      let filter_list = binding.as_sequence();

      let data_descr = VideoStreamDescriptor::new(2, filter_list).unwrap().1;
      assert_eq!(data_descr.index, 2);
      assert_eq!(data_descr.stream_type, StreamType::Video);

      assert_eq!(
        data_descr.filters,
        Vec::from([GenericFilter {
          name: "my_filter".to_string(),
          label: None,
          parameters: Default::default(),
        }])
      );
    });
  }
}
