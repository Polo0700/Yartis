use pyo3::prelude::*;

/// A Python module implemented in Rust.
#[pymodule]
mod reduce_noise {
    use pyo3::prelude::*;
    #[pyclass]
    struct AudioEngine {
        sample_rate: u32,
        prev_output: f32,
        last_sample: f32,
        initialized: bool,
        rms_value: f32,
    }
    #[pymethods]
    impl AudioEngine {
        #[new]
        fn new(sample_rate: u32) -> Self{
            AudioEngine {
                sample_rate,
                prev_output: 0.0,
                last_sample: 0.0,
                initialized: false,
                rms_value: 0.0,
            }
        }
        fn convert(&self, chunk: Vec<i16>) -> Vec<f32> {
            let chunk_f32: Vec<f32> = chunk.iter().map(|&n| n as f32 / 32768.0).collect();
            chunk_f32
        }
        fn normalize(&mut self, converted: Vec<f32>) -> Vec<f32>{
            let n = converted.len() as f32;
            let normalized: f32 = converted.iter().map(|x| x*x).sum();
            let rms = (normalized / n).sqrt();
            self.rms_value = rms;
            let resultado = converted.iter().map(|m| m / rms).collect();
            resultado
        }
        fn desnormalize(&mut self, analyzed: Vec<f32>) -> Vec<f32>{
            let desnormalize = analyzed.iter().map(|k| k * self.rms_value).collect();
            desnormalize
        }
        fn rnnoise(&self, highpassed: Vec<f32>) -> Vec<f32>{
            use nnnoiseless::DenoiseState;
            let mut lista: Vec<f32> = Vec::new();
            let mut out_buf =[0.0; DenoiseState::FRAME_SIZE as usize];
            let mut neurona = DenoiseState::new();
            let mut first = false;
            for frames in highpassed.chunks_exact(DenoiseState::FRAME_SIZE) {
                neurona.process_frame(&mut out_buf, frames);
                lista.extend_from_slice(&out_buf);
                if !first {
                    first = true;
                }
            }
            lista
        }
        fn highpass(&mut self, normalized: Vec<f32> ) -> Vec<f32>{
            let mut datos: Vec<f32> = Vec::new();
            for sample in normalized.iter() {
                if !self.initialized {
                    self.last_sample = *sample;
                    self.initialized = true;
                }
                let buff = *sample - self.last_sample + (0.8 * self.prev_output);
                self.last_sample = *sample;
                self.prev_output = buff;
                datos.push(buff);
            }
            datos
        }
        fn reduce_noise(&mut self, chunk: Vec<i16>) -> Vec<f32> {
            let converted = self.convert(chunk);
            let normalized = self.normalize(converted);
            let highpassed = self.highpass(normalized);
            let analyzed = self.rnnoise(highpassed);
            let data = self.desnormalize(analyzed);
            data
        }
    }
}
