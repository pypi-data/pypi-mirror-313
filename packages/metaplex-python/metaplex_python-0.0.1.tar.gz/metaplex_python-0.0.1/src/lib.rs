use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;
use pyo3::types::PyBytes;
use solana_program::pubkey::Pubkey;
use std::str::FromStr;

#[pymodule()]
mod metaplex_python {
    use super::*;

    use mpl_token_metadata::accounts::Metadata;

    #[pyclass(name = "Metadata", eq)]
    #[derive(Eq, PartialEq)]
    struct PyMetadata {
        metadata: Metadata,
    }

    fn bytes_from_py(bytes: &Bound<'_, PyAny>) -> PyResult<Vec<u8>> {
        Ok(bytes.downcast::<PyBytes>()?.as_bytes().to_vec())
    }

    #[pymethods]
    impl PyMetadata {
        #[staticmethod]
        fn find_pda(mint_pubkey_str: &str) -> PyResult<(String, u8)> {
            let mint_pubkey = Pubkey::from_str(mint_pubkey_str)
                .map_err(|e| PyValueError::new_err(format!("{e}")))?;

            let (pubkey, bump) = Metadata::find_pda(&mint_pubkey);

            Ok((pubkey.to_string(), bump))
        }

        #[new]
        fn new(#[pyo3(from_py_with = "bytes_from_py")] bytes: Vec<u8>) -> PyResult<Self> {
            let metadata = Metadata::from_bytes(&bytes)?;

            Ok(Self { metadata })
        }

        fn mint(&self) -> String {
            self.metadata.mint.to_string()
        }

        fn symbol(&self) -> &str {
            // Strings are fixed-length and right-padded
            &self.metadata.symbol.trim_end_matches('\0')
        }
    }

    #[pymodule_init]
    fn init(module: &Bound<'_, PyModule>) -> PyResult<()> {
        module.add_class::<PyMetadata>()
    }
}
