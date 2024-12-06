# AWS-LC ML-DSA readme file

The source code in this folder implements ML-DSA as defined in FIPS 204 Module-Lattice-Based Digital Signature Standard [link](https://csrc.nist.gov/pubs/fips/204/final).

**Source code origin and modifications** 

The source code was imported from a branch of the official repository of the Crystals-Dilithium team: https://github.com/pq-crystals/dilithium. The code was taken at [commit](https://github.com/pq-crystals/dilithium/commit/cbcd8753a43402885c90343cd6335fb54712cda1) as of 10/01/2024. At the moment, only the reference C implementation is imported.

The code was refactored in [this PR](https://github.com/aws/aws-lc/pull/1910) by parameterizing all functions that depend on values that are specific to a parameter set, i.e., that directly or indirectly depend on the value of `DILITHIUM_MODE`. To do this, in `params.h` we defined a structure that holds those ML-DSA parameters and functions
that initialize a given structure with values corresponding to a parameter set. This structure is then passed to every function that requires it as a function argument. In addition, the following changes were made to the source code in `pqcrystals_dilithium_ref_common` directory:

- `randombytes.{h|c}` are deleted because we are using the randomness generation functions provided by AWS-LC.
- `sign.c`: calls to `randombytes` function is replaced with calls to `pq_custom_randombytes` and the appropriate header file is included (`crypto/rand_extra/pq_custom_randombytes.h`).
- `ntt.c`, `poly.c`, `reduce.c`, `reduce.h`: have been modified with a code refactor. The function `fqmul` has been added to bring mode code consistency with Kyber/ML-KEM. See https://github.com/aws/aws-lc/pull/1748 for more details on this change.
- `reduce.c`: a small fix to documentation has been made on the bounds of `reduce32`.
- `poly.c`: a small fix to documentation has been made on the bounds of `poly_reduce`.
- `polyvec.c`: a small fix to documentation has been made on the bounds of `polyveck_reduce`.

**Testing** 

The KATs were obtained from https://github.com/pq-crystals/dilithium/tree/master/ref/nistkat.
To compile the KAT programs on Linux or macOS, go to the `ref/` directory and run `make nistkat`. This will produce executables within `nistkat` which once executed will produce the KATs: `PQCsignKAT_Dilithium2.rsp`, `PQCsignKAT_Dilithium3.rsp`,`PQCsignKAT_Dilithium5.rsp`.
