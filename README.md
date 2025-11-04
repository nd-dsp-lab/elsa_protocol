# ELSA

## Select-Then-Compute: Encrypted Label Selection and Analytics over Distributed Datasets using FHE

This repository contains reference implementations for the ELSA protocol and supporting modules (VAF, wDEP, hashing, logistic regression). You can build and run either natively or via Docker (recommended).

# Dependencies

### Core library
Install OpenFHE v1.2.3 via [Link](https://github.com/openfheorg/openfhe-development)

### System (for native builds)

- OS: Ubuntu 22.04 (or similar)

- Build tools: ```cmake, make, g++, build-essential```

- Libraries: ```libomp-dev, openssl, libssl-dev```

- Optional: ```parallel, time, git, curl```

Note: Docker users do not need to install the above on the host.

### Build the Project

You can build the project using the following commands:

```
make clean
rm -r build
mkdir build && cd build
cmake -S .. -B .
make -j"$(nproc)"
```

### Executables

Depending on build flags/components, the project produces:

- ```main``` – end-to-end pipeline (slotwise windowing options).

- ```main_vaf``` – VAF + wDEP evaluation.

- ```main_psmt``` – protocol test on tabular datasets (e.g., VLDP).

- ```main_pepsi``` – PEPSI's implementation in OpenFHE.

- ```main_logreg``` – logistic-regression demo (breast cancer dataset).

- ```main_hash``` – hashing module checks.

CMake will place binaries under ```build/```. In Docker, runtime outputs will be placed under ```/opt```.


# Docker (Recommended)

If Docker is not installed, please refer to [Docker Installation](https://docs.docker.com/engine/install/) to install Docker for Ubuntu 22.04. 

The repository includes a Dockerfile that pins OpenFHE v1.2.3 and builds it inside the container. It also copies the repository to ```/opt/src``` and builds the project out-of-source into ```/opt/build```.

To test using Docker, first clone the repository:

```
git clone https://github.com/nd-dsp-lab/elsa_protocol.git
cd elsa_protocol
```

### Build the image

From the repo root run the following:

```
docker build -t ndss-elsa .
```

Note: If your Docker daemon requires elevated privileges, prepend sudo to docker commands.

### Run the full-test

Once docker is built, you can run the full test suite for the above executables. We provide a script that runs the executables and prints pass/fail summaries. Run the  ```run_all_tests.sh``` in the repo root for the full test:

```
chmod +x run_all_tests.sh
IMAGE=ndss-elsa ./run_all_tests.sh
```


### Optional 

You can also run each binary directly from ```/opt``` inside the container. Examples:

```
docker run --rm -it ndss-elsa /opt/main_psmt -DBPath /data/VLDP/ -DBName VLDP -isSim 1 -isCompact 1 -numChunks 4 -itemLen 1 -scalingModSize 44

docker run --rm -it ndss-elsa /opt/main_pepsi -bitlen 89 -HW 32 -isEncrypted 0
```


# Data

```/data``` folder contains the preprocessed datasets for testing ELSA's various components in the experimental evaluation. Read the ```README.md``` inside ```/data``` to learn how to generate and pre-process new datasets.

The end-to-end functionality ELSA is tested on VLDP (Vehicle Loan Default Prediction) dataset only due to repository size constraints in GitHub. If you’d like to test ELSA on additional datasets, please use Amazon’s collection here: [Link](https://github.com/amazon-science/fraud-dataset-benchmark).  

# VAF Parameters

The proposed VAF takes several parameters for each domain size.

#### WeakDEP Parameters ($f(x) = \frac{3\sqrt{3}}{2k\sqrt{k}}x(k - x^{2})$)
- `k`: weakDEP Parameter
- `L`: Domain extension rate ($\sqrt{k/3} < L < \sqrt{k}$)
- `R`: Base domain size
- `n_dep`: Number of DEP extensions

#### VAF Parameters
- `isNewVAF`: Naive Squaring vs. New Transformation
- `n_vaf`: Number of transformations ($f(x) \mapsto $f(x)^{2}$ or $f(x) \mapsto (\frac{3}{2}f(x) - \frac{1}{2})^{2}$).


#### Optional Parameter
- `n_cleanse`: Number of cleanse function $f(x) = -2x^{3} + 3x^{2}$.
- `depth`: Required depth for running the protocol. (TODO: automatically calculate the required depth)

# Presets for Each Domain Size

|       | $2^{1}$ | $2^{2}$ | $2^{4}$ | $2^{5}$ | $2^{6}$  | $2^{8}$  | $2^{10}$ | $2^{12}$  | $2^{14}$ | $2^{16}$ | $2^{18}$ | $2^{20}$ |
|-------|----|----|----|----|----|----|--------|-------|--------|---------|-------|-------|
| $k$   | NA | NA | NA | 17 | 17 | 17 | 6.75   | 6.75  | 6.75   | 17      | 17    | 6.75  |
| $L$   | NA | NA | NA | 4  | 4  | 4  | 2.59   | 2.59  | 2.59   | 4       | 4     | 2.59  |
| $R$   | 2  | 4  | 16 | 4  | 11 | 4  | 158.54 | 91.09 | 148.45 | 5112.73 | 73139 | 12583 |
| n_dep | 0  | 0  | 0  | 2  | 1  | 3  | 2      | 4     | 5      | 2       | 1     | 5     |
| n_vaf | 4  | 7  | 4  | 3  | 4  | 4  | 8      | 7     | 8      | 16      | 20    | 16    |
| newVAF| F  | F  | T  | T  | T  | T  | T      | T     | T      | T       | T     | T     |
| depth | 7  | 10 | 13 | 16 | 15 | 19 | 22     | 25    | 28     | 32      | 35    | 38    |
